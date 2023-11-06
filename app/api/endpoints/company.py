from fastapi import APIRouter, HTTPException, status, Depends, Request
from db.models import CompanyCreate, Company, CompanyCreateDB
import mysql.connector 
from db.session import get_db_connection
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from typing import Optional, List
from datetime import datetime, timedelta
from db.session import get_db_connection
from core.security import hash_password, verify_password
from services.auth import get_user, get_current_token, get_current_user, create_access_token
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/companies")
async def create_company(company: CompanyCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "Recruteur":
        raise HTTPException(status_code=403, detail="T'es pas un recruteur.")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO companies (company_name, company_website, company_address, recruiter_id) 
                VALUES (%s, %s, %s, %s)""",
                (
                    company.company_name, 
                    company.company_website,
                    company.company_address,
                    current_user["person_id"]
                )
            )
            conn.commit()
        return {"status": "Le profil de l'entreprise a été créé avec succès !"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))
    
@router.get("/companies", response_model=CompanyCreate)
async def get_my_company(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "Recruteur":
        raise HTTPException(status_code=403, detail="T'es pas recruteur.")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM companies WHERE recruiter_id=%s",
                (current_user["person_id"],)
            )
            company = cursor.fetchone()
            if not company:
                raise HTTPException(status_code=404, detail="Aucune entreprise trouvée pour ce recruteur.")
            return company
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.put("/companies")
async def update_company(company: CompanyCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "Recruteur":
        raise HTTPException(status_code=403, detail="T'es pas un recruteur.")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE companies 
                SET company_name=%s, company_website=%s, company_address=%s 
                WHERE recruiter_id=%s""",
                (
                    company.company_name, 
                    company.company_website,
                    company.company_address,
                    current_user["person_id"]
                )
            )
            conn.commit()
        return {"status": "Le profil de l'entreprise a été mis à jour avec succès !"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))
    
@router.delete("/companies")
async def delete_company(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "Recruteur":
        raise HTTPException(status_code=403, detail="T'es pas un recruteur.")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM companies WHERE recruiter_id=%s",
                (current_user["person_id"],)
            )
            conn.commit()
        return {"status": "Le profil de l'entreprise a été supprimé avec succès !"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))

# Monitoring data-base

@router.get("/companiesAll")
async def get_all_companies():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM companies")
            results = cursor.fetchall()
            companies = [Company(**result) for result in results]
            return companies
    except mysql.connector.Error as error:
       raise HTTPException(status_code=400, detail=str(error))
    
@router.post("/companiesDB")
async def post_db_company(company : CompanyCreateDB):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
            """
            INSERT INTO companies (company_name, company_website, company_address, recruiter_id)
            VALUES (%s, %s, %s, %s)
            """,
            (
                company.company_name,
                company.company_website,
                company.company_address,
                company.recruiter_id
            )
            )
            conn.commit()
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))
    
@router.put("/companiesChange/{company_id}")
async def update_db_company(company_id: int, company: CompanyCreateDB):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE companies 
                SET company_name = %s, company_website = %s, company_address = %s, recruiter_id = %s
                WHERE company_id = %s
                """,
                (
                    company.company_name,
                    company.company_website,
                    company.company_address,
                    company.recruiter_id,
                    company_id
                )
            )
            conn.commit()
            return {"detail": "Successfully updated company"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))
    
@router.delete("/deleteCompany/{company_id}")
async def delete_company(company_id: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM advertisements WHERE company_id = %s", (company_id,))
            cursor.execute("DELETE FROM companies WHERE company_id = %s", (company_id,))
            conn.commit()
            return {"detail": "Successfully deleted company and related records"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))