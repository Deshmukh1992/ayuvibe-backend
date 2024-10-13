# models.py

from sqlalchemy import Column, Integer, String, func, ForeignKey, Date, DateTime, Text
from sqlalchemy.orm import relationship
from database.db import Base

# Models for SQLAlchemy
class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10))
    phone_number = Column(String(15))
    email = Column(String(100))
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    postal_code = Column(String(10))
    registration_date = Column(DateTime, server_default=func.now())
    password = Column(String(255), nullable=False)

class Doctor(Base):
    __tablename__ = "doctors"
    doctor_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    specialization = Column(String(100))
    phone_number = Column(String(15))
    email = Column(String(100))
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    postal_code = Column(String(10))
    registration_date = Column(DateTime, server_default=func.now())
    password = Column(String(255), nullable=False)

class Appointment(Base):
    __tablename__ = "appointments"
    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"))
    appointment_date = Column(DateTime, nullable=False)
    reason = Column(Text)
    appointment_status = Column(String(50), default='Scheduled')
    created_at = Column(DateTime, server_default=func.now())

    patient = relationship("Patient")
    doctor = relationship("Doctor")

class Diagnosis(Base):
    __tablename__ = "diagnoses"
    diagnosis_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.appointment_id"))
    diagnosis_date = Column(DateTime, server_default=func.now())
    diagnosis_description = Column(Text, nullable=False)

    appointment = relationship("Appointment")

class Treatment(Base):
    __tablename__ = "treatments"
    treatment_id = Column(Integer, primary_key=True, index=True)
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.diagnosis_id"))
    treatment_description = Column(Text, nullable=False)
    dosage = Column(String(100))
    duration = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

    diagnosis = relationship("Diagnosis")

class FollowUp(Base):
    __tablename__ = "follow_ups"
    follow_up_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.appointment_id"))
    follow_up_date = Column(DateTime)
    follow_up_notes = Column(Text)

    appointment = relationship("Appointment")
