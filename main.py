from fastapi import FastAPI,Path,HTTPException,Query
import json 

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

@app.get('/')
def welcome():
    return {"Message ": "Hello krish"}

@app.get('/view')
def patients():
    data = load_data()
    return data

@app.get("/view/patients/{patient_id}")
def show_patient(patient_id: str = Path(...,description = "ID of the patient",example = "PT-1005")):
    patients = load_data()

    for patient in patients:
        if patient["patient_id"] == patient_id:
            return patient

    raise HTTPException(status_code= 404,detail = "patient not found")


@app.get("/sort")
def sort(
    sort_by: str = Query(..., description="Sort by age or patient_id"),
    order: str = Query("asc", description="asc or desc")
):

    valid_fields = ["age", "patient_id"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Choose from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order"
        )

    data = load_data()

    sorted_data = sorted(
        data,
        key=lambda x: x.get(sort_by),
        reverse=(order == "desc")
    )

    return sorted_data
    
