from pydantic import BaseModel, ValidationError

# Define a Pydantic model for address information
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

# Define a Pydantic model for patient data with nested address information
class PatientData(BaseModel):
    name: str
    email: str
    age: int
    blood_type: str
    address: Address  # Nested model for address information

def add_patient_data(patient_data: PatientData):
    print(f"Adding patient data: {patient_data.model_dump()}")
    print(f"Patient City: {patient_data.address.city}")  # Accessing nested model attribute

def main():
    # Example patient data with nested address information
    patient_data = {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
        "age": 30,
        "blood_type": "O+",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip_code": "12345"
        }
    }

    try:
        valid_patient_data = PatientData(**patient_data)
        add_patient_data(valid_patient_data)

    except ValidationError as e:
        print(f"Validation Error: {e}")

if __name__ == "__main__":
    main()