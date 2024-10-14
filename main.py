# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import engine, get_db, Base
from typing import List
from utils.schema import (PatientSignup, PatientUpdate, DoctorSignup, DoctorUpdate,
                          AppointmentCreate, AppointmentUpdate, DiagnosisCreate, DiagnosisUpdate,
                          TreatmentCreate, TreatmentUpdate, FollowUpCreate, FollowUpUpdate, Login, HerbResponse,
                          HerbCreate, RemedyResponse, RemedyCreate)
from utils.models import Doctor, Patient, Appointment, Diagnosis, Treatment, FollowUp, Herb, Remedy
from utils.jwt import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AyuVibe - Ayurvedic Doctors Directory")


@app.get("/", tags=["Home"])
def home():
    return {"message": "This is AyuVibe home"}

# Routes
# Patients CRUD Endpoints
@app.post("/signup/patient", tags=["Auth"])
def patient_signup(patient: PatientSignup, db: Session = Depends(get_db)):
    existing_patient = db.query(Patient).filter(Patient.email == patient.email).first()
    if existing_patient:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(patient.password)
    new_patient = Patient(
        first_name=patient.first_name,
        last_name=patient.last_name,
        date_of_birth=patient.date_of_birth,
        gender=patient.gender,
        phone_number=patient.phone_number,
        email=patient.email,
        password=hashed_password,
        address=patient.address,
        city=patient.city,
        state=patient.state,
        postal_code=patient.postal_code
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return {"message": "Patient registered successfully"}


@app.post("/auth", tags=["Auth"])
def authenticate(login: Login, db: Session = Depends(get_db)):
    user = db.query(Patient).filter(Patient.email == login.email).first() or \
           db.query(Doctor).filter(Doctor.email == login.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(login.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Generate JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": login.email, "user_id": user.patient_id if isinstance(user, Patient) else user.doctor_id},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# New Login Route: Returns user data
@app.post("/login", tags=["Auth"])
def login_user(login: Login, db: Session = Depends(get_db)):
    user = db.query(Patient).filter(Patient.email == login.email).first() or \
           db.query(Doctor).filter(Doctor.email == login.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(login.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")


    print("====================================")
    print(user)
    print("====================================")

    # Returning user data (excluding password)
    user_data = {
        # "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "user_type": "patient" if isinstance(user, Patient) else "doctor",
        "registration_date": user.registration_date
    }

    return user_data


@app.get("/patients/", tags=["Patient"])
def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()


# Update Patient
@app.put("/patients/{patient_id}", tags=["Patient"])
def update_patient(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    for key, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient


# Delete Patient
@app.delete("/patients/{patient_id}", tags=["Patient"])
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}


@app.get("/patients/{patient_id}", tags=["Patient"])
def get_patient_by_id(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# Doctors CRUD Endpoints
@app.post("/signup/doctor", tags=["Auth"])
def doctor_signup(doctor: DoctorSignup, db: Session = Depends(get_db)):
    existing_doctor = db.query(Doctor).filter(Doctor.email == doctor.email).first()
    if existing_doctor:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(doctor.password)
    new_doctor = Doctor(
        first_name=doctor.first_name,
        last_name=doctor.last_name,
        specialization=doctor.specialization,
        phone_number=doctor.phone_number,
        email=doctor.email,
        password=hashed_password,
        address=doctor.address,
        city=doctor.city,
        state=doctor.state,
        postal_code=doctor.postal_code
    )
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return {"message": "Doctor registered successfully"}

@app.get("/doctors/", tags=["Doctor"])
def get_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()


# Update Doctor
@app.put("/doctors/{doctor_id}", tags=["Doctor"])
def update_doctor(doctor_id: int, doctor: DoctorUpdate, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    for key, value in doctor.dict(exclude_unset=True).items():
        setattr(db_doctor, key, value)

    db.commit()
    db.refresh(db_doctor)
    return db_doctor


# Delete Doctor
@app.delete("/doctors/{doctor_id}", tags=["Doctor"])
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db.delete(db_doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}


@app.get("/doctors/{doctor_id}", tags=["Doctor"])
def get_doctor_by_id(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# Appointments CRUD Endpoints
@app.post("/appointments/", response_model=AppointmentCreate, tags=["Appointments"])
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@app.get("/appointments/", tags=["Appointments"])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()


# Update Appointment
@app.put("/appointments/{appointment_id}", tags=["Appointments"])
def update_appointment(appointment_id: int, appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    for key, value in appointment.dict(exclude_unset=True).items():
        setattr(db_appointment, key, value)

    db.commit()
    db.refresh(db_appointment)
    return db_appointment


# Delete Appointment
@app.delete("/appointments/{appointment_id}", tags=["Appointments"])
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(db_appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}


@app.get("/appointments/{appointment_id}", tags=["Appointments"])
def get_appointment_by_id(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@app.get("/appointments/{appointment_id}/diagnoses_treatments", tags=["Appointments"])
def get_diagnoses_and_treatments_by_appointment(appointment_id: int, db: Session = Depends(get_db)):
    diagnoses = db.query(Diagnosis).filter(Diagnosis.appointment_id == appointment_id).all()

    if not diagnoses:
        raise HTTPException(status_code=404, detail="No diagnoses found for this appointment")

    result = []
    for diagnosis in diagnoses:
        treatments = db.query(Treatment).filter(Treatment.diagnosis_id == diagnosis.diagnosis_id).all()
        result.append({
            "diagnosis": diagnosis,
            "treatments": treatments
        })

    return result

# Diagnoses CRUD Endpoints
@app.post("/diagnoses/", response_model=DiagnosisCreate, tags=["Diagnoses"])
def create_diagnosis(diagnosis: DiagnosisCreate, db: Session = Depends(get_db)):
    db_diagnosis = Diagnosis(**diagnosis.dict())
    db.add(db_diagnosis)
    db.commit()
    db.refresh(db_diagnosis)
    return db_diagnosis

@app.get("/diagnoses/", tags=["Diagnoses"])
def get_diagnoses(db: Session = Depends(get_db)):
    return db.query(Diagnosis).all()


# Update Diagnosis
@app.put("/diagnoses/{diagnosis_id}", tags=["Diagnoses"])
def update_diagnosis(diagnosis_id: int, diagnosis: DiagnosisUpdate, db: Session = Depends(get_db)):
    db_diagnosis = db.query(Diagnosis).filter(Diagnosis.diagnosis_id == diagnosis_id).first()
    if not db_diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")

    for key, value in diagnosis.dict(exclude_unset=True).items():
        setattr(db_diagnosis, key, value)

    db.commit()
    db.refresh(db_diagnosis)
    return db_diagnosis


# Delete Diagnosis
@app.delete("/diagnoses/{diagnosis_id}", tags=["Diagnoses"])
def delete_diagnosis(diagnosis_id: int, db: Session = Depends(get_db)):
    db_diagnosis = db.query(Diagnosis).filter(Diagnosis.diagnosis_id == diagnosis_id).first()
    if not db_diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")

    db.delete(db_diagnosis)
    db.commit()
    return {"message": "Diagnosis deleted successfully"}


@app.get("/diagnoses/{diagnosis_id}", tags=["Diagnoses"])
def get_diagnosis_by_id(diagnosis_id: int, db: Session = Depends(get_db)):
    diagnosis = db.query(Diagnosis).filter(Diagnosis.diagnosis_id == diagnosis_id).first()
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return diagnosis


# Treatments CRUD Endpoints
@app.post("/treatments/", response_model=TreatmentCreate, tags=["Treatment"])
def create_treatment(treatment: TreatmentCreate, db: Session = Depends(get_db)):
    db_treatment = Treatment(**treatment.dict())
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)
    return db_treatment

@app.get("/treatments/", tags=["Treatment"])
def get_treatments(db: Session = Depends(get_db)):
    return db.query(Treatment).all()


# Update Treatment
@app.put("/treatments/{treatment_id}", tags=["Treatment"])
def update_treatment(treatment_id: int, treatment: TreatmentUpdate, db: Session = Depends(get_db)):
    db_treatment = db.query(Treatment).filter(Treatment.treatment_id == treatment_id).first()
    if not db_treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    for key, value in treatment.dict(exclude_unset=True).items():
        setattr(db_treatment, key, value)

    db.commit()
    db.refresh(db_treatment)
    return db_treatment


# Delete Treatment
@app.delete("/treatments/{treatment_id}", tags=["Treatment"])
def delete_treatment(treatment_id: int, db: Session = Depends(get_db)):
    db_treatment = db.query(Treatment).filter(Treatment.treatment_id == treatment_id).first()
    if not db_treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    db.delete(db_treatment)
    db.commit()
    return {"message": "Treatment deleted successfully"}


@app.get("/treatments/{treatment_id}", tags=["Treatment"])
def get_treatment_by_id(treatment_id: int, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.treatment_id == treatment_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return treatment


# Follow-Ups CRUD Endpoints
@app.post("/follow_ups/", response_model=FollowUpCreate, tags=["Follow Ups"])
def create_follow_up(follow_up: FollowUpCreate, db: Session = Depends(get_db)):
    db_follow_up = FollowUp(**follow_up.dict())
    db.add(db_follow_up)
    db.commit()
    db.refresh(db_follow_up)
    return db_follow_up

@app.get("/follow_ups/", tags=["Follow Ups"])
def get_follow_ups(db: Session = Depends(get_db)):
    return db.query(FollowUp).all()


# Update Follow-Up
@app.put("/follow_ups/{follow_up_id}", tags=["Follow Ups"])
def update_follow_up(follow_up_id: int, follow_up: FollowUpUpdate, db: Session = Depends(get_db)):
    db_follow_up = db.query(FollowUp).filter(FollowUp.follow_up_id == follow_up_id).first()
    if not db_follow_up:
        raise HTTPException(status_code=404, detail="Follow-Up not found")

    for key, value in follow_up.dict(exclude_unset=True).items():
        setattr(db_follow_up, key, value)

    db.commit()
    db.refresh(db_follow_up)
    return db_follow_up


# Delete Follow-Up
@app.delete("/follow_ups/{follow_up_id}", tags=["Follow Ups"])
def delete_follow_up(follow_up_id: int, db: Session = Depends(get_db)):
    db_follow_up = db.query(FollowUp).filter(FollowUp.follow_up_id == follow_up_id).first()
    if not db_follow_up:
        raise HTTPException(status_code=404, detail="Follow-Up not found")

    db.delete(db_follow_up)
    db.commit()
    return {"message": "Follow-Up deleted successfully"}



# CRUD operations for Herbs
@app.post("/herbs/", tags=["Herbs"])
def create_herb(herb: HerbCreate, db: Session = Depends(get_db)):
    db_herb = Herb(**herb.dict())
    db.add(db_herb)
    db.commit()
    db.refresh(db_herb)
    return db_herb

@app.get("/herbs/", tags=["Herbs"])
def read_herbs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    herbs = db.query(Herb).offset(skip).limit(limit).all()
    return herbs

@app.get("/herbs/{herb_id}", tags=["Herbs"])
def read_herb(herb_id: int, db: Session = Depends(get_db)):
    herb = db.query(Herb).filter(Herb.herb_id == herb_id).first()
    if herb is None:
        raise HTTPException(status_code=404, detail="Herb not found")
    return herb

@app.put("/herbs/{herb_id}", tags=["Herbs"])
def update_herb(herb_id: int, herb: HerbCreate, db: Session = Depends(get_db)):
    db_herb = db.query(Herb).filter(Herb.herb_id == herb_id).first()
    if db_herb is None:
        raise HTTPException(status_code=404, detail="Herb not found")
    for key, value in herb.dict().items():
        setattr(db_herb, key, value)
    db.commit()
    return db_herb

@app.delete("/herbs/{herb_id}", tags=["Herbs"])
def delete_herb(herb_id: int, db: Session = Depends(get_db)):
    db_herb = db.query(Herb).filter(Herb.herb_id == herb_id).first()
    if db_herb is None:
        raise HTTPException(status_code=404, detail="Herb not found")
    db.delete(db_herb)
    db.commit()
    return {"detail": "Herb deleted"}

# CRUD operations for Remedies
@app.post("/remedies/", tags=["Remedies"])
def create_remedy(remedy: RemedyCreate, db: Session = Depends(get_db)):
    db_remedy = Remedy(**remedy.dict())
    db.add(db_remedy)
    db.commit()
    db.refresh(db_remedy)
    return db_remedy

@app.get("/remedies/", tags=["Remedies"])
def read_remedies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    remedies = db.query(Remedy).offset(skip).limit(limit).all()
    return remedies

@app.get("/remedies/{remedy_id}", tags=["Remedies"])
def read_remedy(remedy_id: int, db: Session = Depends(get_db)):
    remedy = db.query(Remedy).filter(Remedy.remedy_id == remedy_id).first()
    if remedy is None:
        raise HTTPException(status_code=404, detail="Remedy not found")
    return remedy

@app.put("/remedies/{remedy_id}", tags=["Remedies"])
def update_remedy(remedy_id: int, remedy: RemedyCreate, db: Session = Depends(get_db)):
    db_remedy = db.query(Remedy).filter(Remedy.remedy_id == remedy_id).first()
    if db_remedy is None:
        raise HTTPException(status_code=404, detail="Remedy not found")
    for key, value in remedy.dict().items():
        setattr(db_remedy, key, value)
    db.commit()
    return db_remedy

@app.delete("/remedies/{remedy_id}", tags=["Remedies"])
def delete_remedy(remedy_id: int, db: Session = Depends(get_db)):
    db_remedy = db.query(Remedy).filter(Remedy.remedy_id == remedy_id).first()
    if db_remedy is None:
        raise HTTPException(status_code=404, detail="Remedy not found")
    db.delete(db_remedy)
    db.commit()
    return {"detail": "Remedy deleted"}