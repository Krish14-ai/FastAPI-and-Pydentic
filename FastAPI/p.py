import json
from main import Update_Patient
with open(r'C:\Users\Krish\Downloads\FastApi\FastAPI\patients.json', 'r') as f:
    data = json.load(f)

first = data[7]

updated_patient = Update_Patient
updated_patient = first
updated_patient["first_name"]= "Krish" 
print(updated_patient)

id = "PT-1008"
updates = []

for patient in data:

    if patient["patient_id"] == id:

        updates = updated_patient.model_dump(
            exclude_unset=True,
            mode="json"
        )
print(updates)