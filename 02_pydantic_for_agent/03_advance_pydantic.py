from pydantic import BaseModel, ValidationError, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

# Pydantic is a data validation and settings management library for Python, based on Python type annotations. 
# It allows you to define data models with type hints and automatically validates the data against those models.

# In this example, we will demonstrate how to use Pydantic to validate patient data before adding it to a system.
# We have List and Dict types in the patient data model to represent allergies and contact information, respectively. This allows for more complex data structures to be validated easily.

# Define a Pydantic model for patient data (BaseModel is the base class for creating Pydantic models)
class PatientData(BaseModel):
    name: Annotated[str, Field(max_length=50, description="The name of the patient", title="Name", examples=["John Doe"])]    # Use Field to specify additional validation constraints, such as maximum length for the name field, Annotated is used to provide additional metadata for the field, such as description, title, and examples
    email: EmailStr  # EmailStr is a special type provided by Pydantic to validate email addresses
    age: Annotated[int, Field(gt=0, lt=100, description="The age of the patient")]  # Use Field to specify that age must be greater than 0 and less than 100
    blood_type: str
    height: float = Field(gt=0, strict=True, description="The height of the patient")  # Use Field to specify that height must be greater than 0
    weight: float = Field(gt=0, description="The weight of the patient")  # Use Field to specify that weight must be greater than 0
    married: bool
    allergies: List[str]  # List of strings to represent allergies
    contact_info: Annotated[Dict[str, str], Field(description="The contact information of the patient", examples=[{"phone": "123-456-7890", "email": "demo@gmail.com"}])]  # Dictionary to represent contact information with string keys and values
    note: Optional[List[str]] = Field(default=None, max_length=5)  # Optional field for additional notes, with a maximum length of 5 notes and default value of None if not provided
    report_url: AnyUrl  # AnyUrl is a special type provided by Pydantic to validate URLs

def add_patient_data(patient_data: PatientData):
    print(f"Adding patient data: {patient_data.model_dump()}")  # Use model_dump() to get a dictionary representation of the validated data

def main():
    # Example patient data
    patient_data = {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
        "age": 50,
        "blood_type": "O+",
        "height": 175.5,
        "weight": 70.5,
        "married": True,
        "allergies": ["Peanuts", "Shellfish"],
        "contact_info": {
            "phone": "123-456-7890",
            "email": "demo@gmail.com"
        },
        "report_url": "https://example.com/report",
        "note": ["Patient is allergic to peanuts", "Patient is married"]    # This is an optional field that can be None if not provided
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