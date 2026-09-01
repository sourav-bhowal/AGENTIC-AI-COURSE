from pydantic import BaseModel, ValidationError

# Pydantic is a data validation and settings management library for Python, based on Python type annotations. 
# It allows you to define data models with type hints and automatically validates the data against those models.

# In this example, we will demonstrate how to use Pydantic to validate patient data before adding it to a system.

# Define a Pydantic model for patient data (BaseModel is the base class for creating Pydantic models)
class PatientData(BaseModel):
    name: str
    age: int
    blood_type: str

def add_patient_data(patient_data: PatientData):
    print(f"Adding patient data: {patient_data.model_dump()}")  # Use model_dump() to get a dictionary representation of the validated data

def main():
    # Example patient data
    patient_data = {
        "name": "John Doe",
        "age": 50,
        "blood_type": "O+"
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