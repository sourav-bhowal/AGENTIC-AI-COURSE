# Pydantic is a data validation and settings management library for Python, based on Python type annotations. 
# It allows you to define data models with type hints and automatically validates the data against those models.

# Currently, this code does not use Pydantic for data validation. Instead, it simply prints the patient data passed to the add_patient_data function.

def add_patient_data(patient_data):
    # Here, you would typically validate the patient_data using Pydantic models.
    # For demonstration purposes, we'll just print the data.
    print(f"Adding patient data: {patient_data}")


def main():
    # Example patient data
    patient_data = {
        "name": "John Doe",
        "age": 30,
        "blood_type": "O+"
    }

    add_patient_data(patient_data)

if __name__ == "__main__":
    main()