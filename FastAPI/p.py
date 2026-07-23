import json
from main import Update_Patient
with open(r'C:\Users\Krish\Downloads\FastApi\FastAPI\patients.json', 'r') as f:
    data = json.load(f)

first = data[7]

print(data[7],"\n")
updated_patient = Update_Patient
updated_patient = first
updated_patient["first_name"]= "Krish" 


id = "PT-1008"
updates = []

first.update(updated_patient)

data[7] = first
print(data[7])