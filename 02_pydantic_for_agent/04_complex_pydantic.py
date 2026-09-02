from pydantic import BaseModel, ValidationError, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
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

    # Custom validator for name field to transform the name to uppercase before validation
    @field_validator("name")
    @classmethod
    def transform_name(cls, value):
        return value.upper()  # Transform the name to uppercase before validation 

    # Custom validator for the entire model to check if the age and blood type are compatible
    @model_validator(mode="before")  # model_validator is a decorator provided by Pydantic to define custom validation logic for the entire model. In this case, we are defining a custom validator that will be executed before the model is validated.
    @classmethod
    def check_age_and_blood_type(cls, values):
        age = values.get("age")
        blood_type = values.get("blood_type")
        if age is not None and blood_type is not None:
            if age < 18 and blood_type in ["AB+", "AB-"]:
                raise ValueError("Patients under 18 cannot have AB blood type")
        return values

    # Computed field to calculate the Body Mass Index (BMI) of the patient
    @computed_field  # computed_field is a decorator provided by Pydantic to define computed fields in the model. Computed fields are fields that are not explicitly defined in the model but are derived from other fields in the model.
    @property   # property is a built-in Python decorator that allows you to define a method as a property, which can be accessed like an attribute. In this case, we are defining a computed field for the BMI of the patient.
    def bmi(self) -> float:
        """Calculate the Body Mass Index (BMI) of the patient."""
        return round(self.weight / (self.height / 100) ** 2, 2)  # BMI formula: weight (kg) / (height (m))^2, rounded to 2 decimal places

# Function to add patient data (simulated database operation)
def add_patient_data(patient_data: PatientData):
    print(f"Adding patient data: {patient_data.model_dump()}") 

# Main function to demonstrate the usage of the PatientData model
def main():
    # Example patient data
    patient_data = {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
        "age": 15,
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