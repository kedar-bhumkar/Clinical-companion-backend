from pydantic import BaseModel, Field
from faker import Faker
import random
from datetime import date, datetime, timedelta
from typing import List, Dict, Any, Optional
from langchain.agents import tool
from shared import shared_data_instance
import json

fake = Faker()


def getAllPatientSummary(patient_ids: List[str]) -> Dict[str, Any]:
    
    summaries = []  
    for patient_id in patient_ids:
        summaries.append(getPatientSummary(patient_id))
    
    return {'summaries': summaries}

    
def generate_patient_id() -> str:
    return f"P{fake.random_number(digits=6, fix_len=True)}"

def getPatientSummary(patient_id: str) -> Dict[str, Any]:
    return {"Summary": {
        "patient_id": patient_id,
        "basic_info": {
            "name": 'John Doe',
            "age": random.randint(18, 90),
            "gender": random.choice(["Male", "Female", "Other"]),
            "blood_type": random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
            "height": round(random.uniform(150, 200), 1),
            "weight": round(random.uniform(45, 120), 1),
            "is_member_self_responsible": random.choice([True, False])    
        },
        "vitals": getPatientVitals(patient_id),
        "allergies": getPatientAllergies(patient_id),
        "conditions": getPatientConditions(patient_id),
        "immunizations": getPatientImmunizations(patient_id),
        "lab_results": getPatientLabResults(patient_id),
        "procedures": getPatientProcedures(patient_id),
        "medications": getPatientMedications(patient_id),
        "appointments": getPatientAppointments(patient_id),
        "messages": getPatientMessages(patient_id),
        "soap_note": getSoapNoteData()
    }}

def getPatientVitals(patient_id: str) -> Dict[str, Any]:
    return  {"Vitals": {
        "patient_id": patient_id,
        "temperature": round(random.uniform(36.1, 37.5), 1),
        "heart_rate": random.randint(60, 100),
        "blood_pressure": f"{random.randint(90, 140)}/{random.randint(60, 90)}",
        "respiratory_rate": random.randint(12, 20),
        "oxygen_saturation": random.randint(95, 100),
    }}

def getPatientAllergies(patient_id: str) -> List[str]:
    allergies = ["Penicillin", "Peanuts", "Latex", "Aspirin", "Shellfish", "Eggs", "Soy", "Wheat", "Milk", "Tree nuts"]
    return random.sample(allergies, random.randint(0, 3))

def getPatientConditions(patient_id: str) -> List[str]:
    conditions = ["Hypertension", "Type 2 Diabetes", "Asthma", "Osteoarthritis", "Depression", "Anxiety", "GERD", "Hypothyroidism", "Hyperlipidemia", "Chronic kidney disease"]
    return random.sample(conditions, random.randint(0, 4))

def getPatientImmunizations(patient_id: str) -> List[Dict[str, Any]]:
    immunizations = ["Influenza", "Tetanus", "Hepatitis B", "MMR", "Pneumococcal", "HPV", "Varicella", "Shingles"]
    return [
        {
            "name": imm,
            "date": fake.date_between(start_date="-5y", end_date="today").strftime("%Y-%m-%d"),
        }
        for imm in random.sample(immunizations, random.randint(2, 5))
    ] 

def getPatientLabResults(patient_id: str) -> List[Dict[str, Any]]:
    lab_tests = ["Complete Blood Count", "Lipid Panel", "Comprehensive Metabolic Panel", "Hemoglobin A1C", "Thyroid Function Tests", "Urinalysis"]
    return [
        {
            "test_name": test,
            "date": fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d"),
            "result": f"{random.uniform(0.5, 2.0):.2f}",
            "unit": random.choice(["mg/dL", "mmol/L", "%", "U/L"]),
            "reference_range": f"{random.uniform(0.1, 0.9):.1f} - {random.uniform(1.1, 3.0):.1f}",
        }
        for test in random.sample(lab_tests, random.randint(2, 4))
    ]

def getPatientProcedures(patient_id: str) -> List[Dict[str, Any]]:
    procedures = ["Appendectomy", "Colonoscopy", "Knee Arthroscopy", "Cataract Surgery", "Tonsillectomy", "Wisdom Teeth Extraction"]
    return [
        {
            "name": proc,
            "date": fake.date_between(start_date="-3y", end_date="today").strftime("%Y-%m-%d"),
            "provider": fake.name(),
        }
        for proc in random.sample(procedures, random.randint(0, 2))
    ]

def getPatientMedications(patient_id: str) -> List[Dict[str, Any]]:
    medications = ["Lisinopril", "Metformin", "Levothyroxine", "Amlodipine", "Metoprolol", "Omeprazole", "Gabapentin", "Sertraline"]
    return [
        {
            "name": med,
            "dosage": f"{random.choice([5, 10, 20, 25, 50, 100])} mg",
            "frequency": random.choice(["Once daily", "Twice daily", "Three times daily", "As needed"]),
            "prescribed_date": fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d"),
        }
        for med in random.sample(medications, random.randint(1, 4))
    ]

def getPatientAppointments(patient_id: str) -> List[Dict[str, Any]]:
    appointment_types = ["Annual Physical", "Follow-up", "Specialist Consultation", "Vaccination", "Lab Work"]
    return [
        {
            "type": random.choice(appointment_types),
            "date": fake.date_between(start_date="today", end_date="+6m").strftime("%Y-%m-%d"),
            "time": fake.time(),
            "provider": fake.name(),
        }
        for _ in range(random.randint(1, 3))
    ]

def getPatientMessages(patient_id: str) -> List[Dict[str, Any]]:
    message_templates = [
        {
            "subject": "Appointment Confirmation",
            "content": "Your appointment with Dr. {doctor} is confirmed for {date} at {time}. Please arrive 15 minutes early to complete any necessary paperwork. If you need to reschedule, please call our office at least 24 hours in advance."
        },
        {
            "subject": "Prescription Refill Request",
            "content": "This is to confirm that we've received your request to refill your prescription for {medication}. We'll process this and send it to your pharmacy within 48 hours. If you have any questions, please don't hesitate to contact us."
        },
        {
            "subject": "Lab Results Available",
            "content": "Your recent lab results for {test} are now available. Please log in to your patient portal to view them. If you have any questions about your results, please schedule a follow-up appointment with Dr. {doctor}."
        },
        {
            "subject": "Appointment Reminder",
            "content": "This is a reminder that you have an appointment scheduled with Dr. {doctor} on {date} at {time} for your {appointment_type}. Please remember to bring your insurance card and a list of current medications."
        },
        {
            "subject": "Health Question",
            "content": "I've been experiencing {symptom} for the past {duration}. It seems to worsen when {trigger}. Is this something I should be concerned about or schedule an appointment for?"
        }
    ]

    return [
        {
            "subject": template["subject"],
            "date": fake.date_between(start_date="-3m", end_date="today").strftime("%Y-%m-%d"),
            "time": fake.time(),
            "sender": random.choice(["Patient", "Provider"]),
            "content": template["content"].format(
                doctor=fake.name(),
                date=fake.date_between(start_date="today", end_date="+30d").strftime("%Y-%m-%d"),
                time=fake.time(),
                medication=fake.word(),
                test=random.choice(["Complete Blood Count", "Lipid Panel", "Thyroid Function"]),
                appointment_type=random.choice(["annual check-up", "follow-up visit", "consultation"]),
                symptom=random.choice(["headache", "back pain", "nausea", "fatigue"]),
                duration=random.choice(["two days", "a week", "three days"]),
                trigger=random.choice(["I stand for long periods", "I eat certain foods", "I exercise"])
            )
        }
        for template in random.sample(message_templates, random.randint(2, 5))
    ]

def getSoapNoteData() -> Dict[str, Any]:
    chief_complaints = {
        "Chest pain": ["sharp", "dull", "crushing", "radiating", "intermittent", "constant"],
        "Shortness of breath": ["at rest", "on exertion", "when lying flat", "sudden onset"],
        "Abdominal pain": ["cramping", "sharp", "dull", "localized", "diffuse", "intermittent"],
        "Headache": ["throbbing", "pressure-like", "unilateral", "bilateral", "with aura"],
        "Back pain": ["lower", "upper", "mid", "radiating", "constant", "intermittent"],
        "Fever": ["high-grade", "low-grade", "intermittent", "with chills", "persistent"],
        "Cough": ["dry", "productive", "persistent", "with blood-tinged sputum", "nocturnal"],
        "Fatigue": ["generalized", "sudden onset", "progressive", "with weakness"],
        "Nausea": ["with vomiting", "without vomiting", "intermittent", "persistent"],
        "Dizziness": ["vertigo", "lightheadedness", "with fainting", "positional"]
    }
    
    hpi_elements = {
        "onset": ["sudden", "gradual", "acute", "chronic", "intermittent"],
        "location": ["localized", "diffuse", "radiating", "migrating"],
        "duration": ["for the past day", "for several days", "for a week", "for several weeks", "for months"],
        "characterization": ["sharp", "dull", "aching", "burning", "throbbing", "stabbing"],
        "alleviating factors": ["rest", "medication", "position change", "ice", "heat"],
        "aggravating factors": ["movement", "eating", "stress", "certain positions", "time of day"],
        "associated symptoms": ["nausea", "vomiting", "fever", "chills", "sweating", "fatigue"]
    }
    
    ros_systems = {
        "Constitutional": ["fever", "chills", "fatigue", "weight loss", "weight gain"],
        "Eyes": ["vision changes", "eye pain", "redness", "discharge"],
        "Ears, Nose, Mouth, Throat": ["hearing loss", "tinnitus", "sore throat", "nasal congestion"],
        "Cardiovascular": ["chest pain", "palpitations", "edema", "orthopnea"],
        "Respiratory": ["cough", "shortness of breath", "wheezing", "hemoptysis"],
        "Gastrointestinal": ["nausea", "vomiting", "diarrhea", "constipation", "abdominal pain"],
        "Genitourinary": ["dysuria", "frequency", "urgency", "hematuria"],
        "Musculoskeletal": ["joint pain", "muscle pain", "stiffness", "swelling"],
        "Integumentary": ["rash", "itching", "skin lesions", "changes in moles"],
        "Neurological": ["headache", "dizziness", "numbness", "tingling", "weakness"],
        "Psychiatric": ["depression", "anxiety", "sleep disturbances", "mood changes"],
        "Endocrine": ["heat/cold intolerance", "excessive thirst", "excessive urination"],
        "Hematologic/Lymphatic": ["easy bruising", "bleeding", "swollen lymph nodes"],
        "Allergic/Immunologic": ["seasonal allergies", "food allergies", "frequent infections"]
    }
    
    pe_sections = {
        "General": ["Well-appearing", "Ill-appearing", "Comfortable", "Distressed"],
        "HEENT": ["PERRL", "EOMI", "TMs clear", "Oropharynx clear", "Mild erythema"],
        "Neck": ["Supple", "No lymphadenopathy", "Thyromegaly", "JVD present"],
        "Chest": ["Clear to auscultation", "Wheezes", "Crackles", "Rhonchi"],
        "Cardiovascular": ["RRR", "Murmur present", "S3 gallop", "S4 gallop"],
        "Abdomen": ["Soft", "Non-tender", "Distended", "Rebound tenderness", "Guarding"],
        "Musculoskeletal": ["Full ROM", "Tenderness", "Swelling", "Deformity"],
        "Neurological": ["Alert and oriented", "CN II-XII intact", "Sensory intact", "Motor strength 5/5"],
        "Skin": ["No rashes", "Erythema", "Petechiae", "Ecchymosis"]
    }

    def generate_chief_complaint() -> str:
        complaint, details = random.choice(list(chief_complaints.items()))
        return f"{complaint}: {', '.join(random.sample(details, random.randint(1, min(3, len(details)))))}"

    def generate_hpi() -> str:
        return " ".join([
            f"{element.capitalize()}: {random.choice(details)}."
            for element, details in random.sample(list(hpi_elements.items()), random.randint(3, 6))
        ])

    def generate_ros() -> Dict[str, str]:
        return {
            system: ", ".join(random.sample(findings, random.randint(0, min(3, len(findings)))))
            if random.choice([True, False]) else "No abnormalities noted."
            for system, findings in ros_systems.items()
        }

    def generate_pe() -> Dict[str, str]:
        return {
            section: ", ".join(random.sample(findings, random.randint(1, min(3, len(findings)))))
            for section, findings in pe_sections.items()
        }

    return {
        "chief_complaint": generate_chief_complaint(),
        "history_of_present_illness": generate_hpi(),
        "review_of_systems": generate_ros(),
        "physical_exam": generate_pe()
    }

def getACPData() -> Dict[str, Any]:
    return {
        "ACP": {
            "is_member_self_responsible": random.choice([True, False]),
            "is_member_self_responsible_reason": fake.sentence(nb_words=3) if not random.choice([True, False]) else None,
            "is_member_self_responsible_date": fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d") if not random.choice([True, False]) else None
        }
    }

def getMemContactsData() -> Dict[str, Any]:
    return {
        "MemContacts": {
            "contacts": [
                {
                    "name": fake.name(),
                    "relationship": random.choice(["Spouse", "Parent", "Child", "Sibling", "Friend", "Other"]),
                    "phone_number": fake.phone_number(),
                    "email": fake.email()
                }
                for _ in range(random.randint(1, 3))
            ]
        }
    }


##########################################################################################
# Non random data
##########################################################################################

class Patient(BaseModel):
    name: str
    phone_number: str = Field(pattern=r'^\+?1?\d{9,15}$')
    address: str
    age: int = Field(ge=0, le=120)
    gender: str
    weight: float = Field(ge=0)
    height: float = Field(ge=0)

class Allergy(BaseModel):
    allergy_name: str
    loinc_code: str = Field(pattern=r'^[0-9]{1,5}-[0-9]$')
    start_date: date
    status: str
    end_date: Optional[date] = None

class PatientWithAllergies(BaseModel):
    patient: Patient
    allergies: List[Allergy]

def date_to_str(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def get_patient(patient_id: str) -> Dict[str, Any]:
    """
    Returns a dictionary containing patient data, data types, and field descriptions.
    
    The returned dictionary has the following structure:
    {
        "data": { ... },
        "types": { ... },
        "descriptions": {
            "patient": {
                "name": str,
                "phone_number": str,
                "address": str,
                "age": str,
                "gender": str,
                "weight": str,
                "height": str
            },
            "allergies": {
                "allergy_name": str,
                "loinc_code": str,
                "start_date": str,
                "status": str,
                "end_date": str
            }
        }
    }
    """
    mock_patient = Patient(
        name="Jaani Khan",
        phone_number="+1234567890",
        address="123 Main St, Anytown, USA",
        age=35,
        gender="Male",
        weight=75.5,
        height=180.0
    )

    mock_allergies = [
        Allergy(
            allergy_name="Peanut Allergy",
            loinc_code="12345-6",
            start_date=date(2020, 1, 15),
            status="Active"
        ),
        Allergy(
            allergy_name="Penicillin Allergy",
            loinc_code="78901-2",
            start_date=date(2018, 5, 20),
            status="Inactive",
            end_date=date(2022, 3, 10)
        )
    ]

    mock_patient_with_allergies = PatientWithAllergies(
        patient=mock_patient,
        allergies=mock_allergies
    )

    patient_data = json.loads(json.dumps(mock_patient_with_allergies.model_dump(), default=date_to_str))
    
    return {
        "data": patient_data,
        "types": {
            "patient": {
                "name": "str",
                "phone_number": "str",
                "address": "str",
                "age": "int",
                "gender": "str",
                "weight": "float",
                "height": "float"
            },
            "allergies": {
                "allergy_name": "str",
                "loinc_code": "str",
                "start_date": "date",
                "status": "str",
                "end_date": "Optional[date]"
            }
        },
        "descriptions": {
            "patient": {
                "name": "Full name of the patient",
                "phone_number": "Contact phone number with country code",
                "address": "Current residential address",
                "age": "Age in years",
                "gender": "Self-identified gender",
                "weight": "Weight in kilograms",
                "height": "Height in centimeters"
            },
            "allergies": {
                "allergy_name": "Common name of the allergy",
                "loinc_code": "LOINC code for standardized allergy identification",
                "start_date": "Date when the allergy was first diagnosed or reported",
                "status": "Current status of the allergy (e.g., Active, Inactive)",
                "end_date": "Date when the allergy was resolved or became inactive, if applicable"
            }
        }
    }
@tool
def get_advanced_care_plan(patient_id: str) -> Dict[str, Any]:
    """
    A tool that returns a dictionary containing the Advanced_care_plan data, data types, and field descriptions.
    
    The returned dictionary has the following structure:
    {
        "data": { ... },
        "types": { ... },
        "descriptions": { ... }
    }
    """
    print("inside get_advanced_care_plan")
    shared_data_instance.set_data('auto_populate', [])
    today = date.today()

    acp_data = {
        "is_member_self_responsible": True,
        "status": "Completed",
        "created_date": today.isoformat()
    }

    return {"Advanced care plan (ACP)": {
        "data": acp_data,
        "types": {
            "is_member_self_responsible": "bool",
            "status": "str",
            "created_date": "date"
        },
        "descriptions": {
            "is_member_self_responsible": "Indicates if the member is responsible for their own decisions",
            "status": "Current status of the ACP document (options: Draft, Completed, Entered in error)",
            "created_date": "Date when the ACP document was created"
        }
    }}
@tool
def get_Responsible_party(patient_id: str) -> Dict[str, Any]:
    """
    
    A tool that returns a dictionary containing Responsible_party details or MemberContacts data, data types, and field descriptions.
    
    The returned dictionary has the following structure:
    {
        "data": { ... },
        "types": { ... },
        "descriptions": { ... }
    }
    """
    
    print("inside get_Responsible_party")
    shared_data_instance.set_data('auto_populate', 'auto_populate')
    today = date.today()
    

    member_contacts_data = {
        "responsible_party_name": "Ron H",
        "responsible_party_role": "POA",
        "created_date": today.isoformat(),
        "status": "active"
    }

    return {"Member contacts (MemContacts)": {
        "data": member_contacts_data,
        "types": {
            "responsible_party_name": "str",
            "responsible_party_role": "str",
            "created_date": "date",
            "status": "str"
        },
        "descriptions": {
            "responsible_party_name": "Represents the responsible party's name",
            "responsible_party_role": "Represents the  role of the responsible party (options: Legal Guardian, POA, Health surrogate)",
            "created_date": "Date when the contact was created",
            "status": "Current status of the contact (options: active, inactive)"
        }
    }}

# Example usage
#if __name__ == "__main__":
#    patient_info = get_patient()
#    print("Patient Data:")
#    print(patient_info["data"])
#    print("\nData Types:")
#    print(patient_info["types"])
#    print("\nField Descriptions:")
#    print(patient_info["descriptions"])
#
#    acp_info = get_Advanced_care_Plan()
#    print("ACP Data:")
#    print(acp_info["data"])
#    print("\nData Types:")
#    print(acp_info["types"])
#    print("\nField Descriptions:")
#    print(acp_info["descriptions"])





