from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta
from db.models import Advertisement, AdvertisementCreate, TokenData
import mysql.connector
from db.session import get_db_connection
from core.security import hash_password, verify_password
from services.auth import get_user, get_current_token, get_current_user, create_access_token

router = APIRouter()

@router.post("/advertisements")
async def create_advertisement(advertisement: AdvertisementCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "Recruteur":
        raise HTTPException(status_code=403, detail="Seuls les recruteurs peuvent poster une annonce.")
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT company_id FROM companies WHERE recruiter_id=%s",
                (current_user["person_id"],)
            )
            company = cursor.fetchone()
            if not company:
                raise HTTPException(status_code=404, detail="Aucune entreprise trouvée pour ce recruteur.")
            company_id = company["company_id"]
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO advertisements (company_id, job_title, localisation, study_level, salary, contract_type, job_description, date_posted) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    company_id, 
                    advertisement.job_title,
                    advertisement.localisation,
                    advertisement.study_level,
                    advertisement.salary,
                    advertisement.contract_type,
                    advertisement.job_description,
                    advertisement.date_posted
                )
            )
            conn.commit()
        return {"status": "L'annonce a été créée avec succès !"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.get("/advertisements/last")
async def get_last_user_advertisement(current_user: dict = Depends(get_current_user)):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT company_id FROM companies WHERE recruiter_id=%s",
                (current_user["person_id"],)
            )
            company = cursor.fetchone()
            if not company:
                raise HTTPException(status_code=404, detail="Aucune entreprise trouvée pour ce recruteur.")
            company_id = company["company_id"]

            cursor.execute(
                "SELECT * FROM advertisements WHERE company_id=%s ORDER BY date_posted DESC LIMIT 1",
                (company_id,)
            )
            advertisement = cursor.fetchone()
        return advertisement
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.put("/advertisements")
async def update_advertisement(advertisement: AdvertisementCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "Recruteur":
        raise HTTPException(status_code=403, detail="Seuls les recruteurs peuvent modifier une annonce.")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT company_id FROM companies WHERE recruiter_id=%s",
                (current_user["person_id"],)
            )
            company = cursor.fetchone()
            if not company:
                raise HTTPException(status_code=404, detail="Aucune entreprise trouvée pour ce recruteur.")
            company_id = company["company_id"]

            cursor.execute(
                """
                UPDATE advertisements SET job_title=%s, localisation=%s, study_level=%s, salary=%s, contract_type=%s, job_description=%s, date_posted=%s 
                WHERE company_id=%s ORDER BY date_posted DESC LIMIT 1""",
                (
                    advertisement.job_title,
                    advertisement.localisation,
                    advertisement.study_level,
                    advertisement.salary,
                    advertisement.contract_type,
                    advertisement.job_description,
                    advertisement.date_posted,
                    company_id
                )
            )
            conn.commit()
        return {"status": "L'annonce a été modifiée avec succès !"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.delete("/advertisements")
async def delete_advertisement(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "Recruteur":
        raise HTTPException(status_code=403, detail="Seuls les recruteurs peuvent supprimer une annonce.")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT company_id FROM companies WHERE recruiter_id=%s",
                (current_user["person_id"],)
            )
            company = cursor.fetchone()
            if not company:
                raise HTTPException(status_code=404, detail="Aucune entreprise trouvée pour ce recruteur.")
            company_id = company["company_id"]

            cursor.execute(
                "DELETE FROM advertisements WHERE company_id=%s ORDER BY date_posted DESC LIMIT 1",
                (company_id,)
            )
            conn.commit()
        return {"status": "L'annonce a été supprimée avec succès !"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.get("/advertisements/all")
async def get_all_advertisements():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM advertisements")
            advertisements = cursor.fetchall()
        return advertisements
    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))

