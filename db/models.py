from pydantic import BaseModel 
from typing import Optional 
from enum import Enum 

class StudyLevel(str, Enum):
    CAP = 'CAP'
    BEP = 'BEP'
    Bac = 'Bac'
    Bac2 = 'Bac+2'
    Bac3 = 'Bac+3'
    Bac5 = 'Bac+5'
    Bac8 = 'Bac+8'

class ContractType(str, Enum):
    CDI = 'CDI'
    CDD = 'CDD'
    Stage = 'Stage'
    Alternance = 'Alternance'

class Role(str, Enum):
    Candidat = "Candidat"
    Recruteur = "Recruteur"

class ApplicationStatus(str, Enum):
    EnAttente = 'En attente'
    Acceptee = 'Acceptée'
    Refusee = 'Refusée'

class CompanyCreate(BaseModel):
    company_name: str
    company_website: Optional[str] = None
    company_address: Optional[str] = None

class CompanyCreateDB(BaseModel):
    company_name: str
    company_website: Optional[str] = None
    company_address: Optional[str] = None
    recruiter_id : Optional[int] = None

class Company(CompanyCreate):
    company_id: int
    recruiter_id: int

class Advertisement(BaseModel):
    ad_id: int
    company_id: int
    job_title: str
    localisation: str
    study_level: StudyLevel
    salary: str
    contract_type: ContractType
    job_description: str
    date_posted: str

class AdvertisementCreate(BaseModel):
    job_title: str
    localisation: str
    study_level: StudyLevel
    salary: str
    contract_type: ContractType
    job_description: str
    date_posted: str

class PersonCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone: Optional[str] = None
    role: Role

class PersonInDB(BaseModel):
    first_name: str
    last_name: str
    email: str
    hashed_password: str
    phone: Optional[str] = None
    role: Role

class PersonResponse(BaseModel):
    person_id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    role: Role

class PersonPut(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None

class Application(BaseModel):
    application_id: int
    ad_id: int
    applicant_id: int
    date_applied: str
    email_content: str
    status: ApplicationStatus

class TokenData(BaseModel):
    email: str
    role: str
