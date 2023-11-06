from fastapi import FastAPI
from app.api.endpoints import company, person, advertisement 
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI() 

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(company.router, prefix="/api", tags=["Company"])
app.include_router(person.router, prefix="/api", tags=["People"])
app.include_router(advertisement.router, prefix="/api", tags=["Advertisements"])

