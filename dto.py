from typing import List, Dict, Any
import duckduckgo_search
from langchain.agents import tool

from mock_data import (
    getPatientVitals,
    getPatientAllergies,
    getPatientConditions,
    getPatientImmunizations,
    getPatientLabResults,
    getPatientProcedures,
    getPatientMedications,
    getPatientAppointments,
    getPatientMessages,
    getSoapNoteData,
    getPatientSummary,
    getAllPatientSummary    
)  

def get_All_patient_summary(patient_ids: List[str]) -> Dict[str, Any]:
    return getAllPatientSummary(patient_ids)

def get_Patient_Summary(patient_id: str) -> Dict[str, Any]:
    return getPatientSummary(patient_id)

def get_patient_vitals(patient_id: str) -> Dict[str, Any]:
    return getPatientVitals(patient_id)

def get_patient_allergies(patient_id: str) -> List[str]:
    return getPatientAllergies(patient_id)

def get_patient_conditions(patient_id: str) -> List[str]:
    return getPatientConditions(patient_id)

def get_patient_immunizations(patient_id: str) -> List[Dict[str, Any]]:
    return getPatientImmunizations(patient_id)

def get_patient_lab_results(patient_id: str) -> List[Dict[str, Any]]:
    return getPatientLabResults(patient_id)

def get_patient_procedures(patient_id: str) -> List[Dict[str, Any]]:
    return getPatientProcedures(patient_id)

def get_patient_medications(patient_id: str) -> List[Dict[str, Any]]:
    return getPatientMedications(patient_id)

def get_patient_appointments(patient_id: str) -> List[Dict[str, Any]]:
    return getPatientAppointments(patient_id)

def get_patient_messages(patient_id: str) -> List[Dict[str, Any]]:
    return getPatientMessages(patient_id)

def get_soap_note_data() -> Dict[str, Any]:
    return getSoapNoteData()

@tool
def web_search(query: str) -> List[Dict[str, Any]]:
    """
    Perform a web search using DuckDuckGo based on the user's query.

    Args:
        query (str): The search query provided by the user.

    Returns:
        List[Dict[str, Any]]: A list of search results, where each result is a dictionary
        containing information about the search result.
    """
    ddg = duckduckgo_search.DDGS()
    results = list(ddg.text(query, max_results=5))
    return results

