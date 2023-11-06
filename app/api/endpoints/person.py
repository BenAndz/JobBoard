from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta
from db.models import PersonCreate, PersonInDB, PersonResponse, PersonPut, TokenData
import mysql.connector
from db.session import get_db_connection
from core.security import hash_password, verify_password
from services.auth import get_user, get_current_token, get_current_user, create_access_token

router = APIRouter()

@router.post("/register") 
async def register_user(user: PersonCreate): 
    hashed_password = hash_password(user.password)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO people (first_name, last_name, email, hashed_password, phone, role)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (user.first_name,
                 user.last_name,
                 user.email,
                 hashed_password,
                 user.phone,
                 user.role
                 )
            )

            conn.commit()

            new_person_id = cursor.lastrowid 

        return {"person_id": new_person_id, **user.dict(), "hashed_password": hashed_password} 


    except mysql.connector.Error as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()): 
    user = get_user(email=form_data.username) 
    if not user or not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user['email']}, expires_delta=access_token_expires)

    user_company = None
    if user["role"] == "Recruteur":
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM companies WHERE recruiter_id=%s",
                (user["person_id"],)
            )
            user_company = cursor.fetchone()

    return {"access_token": access_token, "token_type": "bearer", "company": user_company}


@router.get("/profile", response_model=PersonResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.put("/profile")
async def update_user_profile(update_data: PersonPut, current_user: dict = Depends(get_current_user)):
    user = get_user(email=current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE people
            SET first_name = %s, last_name = %s, phone = %s
            WHERE email = %s
            """,
            (
                update_data.first_name or user["first_name"],
                update_data.last_name or user["last_name"],
                update_data.phone or user["phone"],
                current_user["email"]
            )
        )
        conn.commit()
        
    updated_user = get_user(email=current_user["email"])
    return updated_user

@router.delete("/profile")
async def delete_user_profile(current_user: dict = Depends(get_current_user)):
    user = get_user(email=current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM people 
            WHERE email = %s
            """,
            (current_user["email"],)
        )
        conn.commit()
        
    return {"detail": "User profile deleted successfully"}