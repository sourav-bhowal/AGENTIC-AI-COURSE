from pydantic import BaseModel, ValidationError, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

# Define a Pydantic model for patient data (BaseModel is the base class for creating Pydantic models)
class PatientData(BaseModel):
    name: Annotated[str, Field(max_length=50, description="The name of the patient", title="Name")]  
    email: EmailStr
    age: Annotated[int, Field(gt=0, lt=100, description="The age of the patient")] 
    blood_type: str
    height: float = Field(gt=0, strict=True, description="The height of the patient")  
    weight: float = Field(gt=0, description="The weight of the patient")  
    married: bool
    allergies: List[str]
    contact_info: Annotated[Dict[str, str], Field(description="The contact information of the patient")]  
    note: Optional[List[str]] = Field(default=None, max_length=5)
    report_url: AnyUrl

    # Custom validator for email field to ensure it belongs to a specific domain
    @field_validator("email")   # field_validator is a decorator provided by Pydantic to define custom validation logic for specific fields in the model. In this case, we are defining a custom validator for the "email" field.
    @classmethod    # classmethod is a decorator that allows the method to be called on the class itself, rather than on an instance of the class. This is useful for validation methods that don't need access to instance-specific data.
    def validate_email(cls, value):
        valid_domains = ["gmail.com", "yahoo.com", "outlook.com"]
        domain = value.split("@")[-1]
        if domain not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        return value

    # Custom validator for blood_type field to ensure it is one of the valid blood types
    @field_validator("blood_type")
    @classmethod
    def validate_blood_type(cls, value):
        valid_blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        if value not in valid_blood_types:
            raise ValueError(f"Blood type must be one of {valid_blood_types}")
        return value


def add_patient_data(patient_data: PatientData):
    print(f"Adding patient data: {patient_data.model_dump()}") 

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
        "note": ["Patient is allergic to peanuts", "Patient is married"]
    }

    try:
        valid_patient_data = PatientData(**patient_data)
        
        add_patient_data(valid_patient_data)  
    except ValidationError as e:
        print("Validation error:", e)

if __name__ == "__main__":
    main()