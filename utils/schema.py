# schemas.py
from typing import Optional

from pydantic import BaseModel, EmailStr

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    phone_number: str
    email: str
    address: str
    city: str
    state: str
    postal_code: str


class PatientUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[str]
    gender: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    password: str
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]


# Pydantic Schemas
class PatientSignup(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    phone_number: str
    email: EmailStr
    password: str
    address: str
    city: str
    state: str
    postal_code: str


class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    phone_number: str
    email: str
    address: str
    city: str
    state: str
    postal_code: str


class DoctorUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    specialization: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    password: str
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]


class DoctorSignup(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    phone_number: str
    email: EmailStr
    password: str
    address: str
    city: str
    state: str
    postal_code: str


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str
    reason: str


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[str]
    reason: Optional[str]
    appointment_status: Optional[str]


class DiagnosisCreate(BaseModel):
    appointment_id: int
    diagnosis_description: str


class DiagnosisUpdate(BaseModel):
    diagnosis_description: Optional[str]


class TreatmentCreate(BaseModel):
    diagnosis_id: int
    treatment_description: str
    dosage: str
    duration: str


class TreatmentUpdate(BaseModel):
    treatment_description: Optional[str]
    dosage: Optional[str]
    duration: Optional[str]


class FollowUpCreate(BaseModel):
    appointment_id: int
    follow_up_date: str
    follow_up_notes: str


class FollowUpUpdate(BaseModel):
    follow_up_date: Optional[str]
    follow_up_notes: Optional[str]


class Login(BaseModel):
    email: EmailStr
    password: str


class HerbCreate(BaseModel):
    herb_name: str
    botanical_name: str = None
    common_names: str = None
    benefits: str = None
    primary_uses: str = None
    dosage: str = None
    form: str = None

class HerbResponse(HerbCreate):
    herb_id: int

class RemedyCreate(BaseModel):
    remedy_name: str
    ingredients: str
    benefits: str
    preparation_method: str = None
    dosage_instructions: str = None
    precautions: str = None

class RemedyResponse(RemedyCreate):
    remedy_id: int

