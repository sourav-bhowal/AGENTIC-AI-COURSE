from pydantic import BaseModel, ValidationError
from typing import List, Dict

# Pydantic is a data validation and settings management library for Python, based on Python type annotations. 
# It allows you to define data models with type hints and automatically validates the data against those models.

# In this example, we will demonstrate how to use Pydantic to validate patient data before adding it to a system.
# We have List and Dict types in the patient data model to represent allergies and contact information, respectively. This allows for more complex data structures to be validated easily.

# Define a Pydantic model for patient data (BaseModel is the base class for creating Pydantic models)
class PatientData(BaseModel):
    name: str
    age: int
    blood_type: str
    weight: float
    married: bool
    allergies: List[str]  # List of strings to represent allergies
    contact_info: Dict[str, str]  # Dictionary to represent contact information with string keys and values

def add_patient_data(patient_data: PatientData):
    print(f"Adding patient data: {patient_data.model_dump()}")  # Use model_dump() to get a dictionary representation of the validated data

def main():
    # Example patient data
    patient_data = {
        "name": "John Doe",
        "age": 50,
        "blood_type": "O+",
        "weight": 70.5,
        "married": True,
        "allergies": ["Peanuts", "Shellfish"],
        "contact_info": {
            "phone": "123-456-7890",
            "email": "demo@gmail.com"
        }
    }

    try:
        # Validate the patient data using the Pydantic model
        # ** means unpacking the dictionary so that the keys of the dictionary are passed as keyword arguments to the PatientData constructor
        valid_patient_data = PatientData(**patient_data)
        
        # Pass the validated data to the add_patient_data function
        add_patient_data(valid_patient_data)  
    except ValidationError as e:
        print("Validation error:", e)

if __name__ == "__main__":
    main()