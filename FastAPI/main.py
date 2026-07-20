from fastapi import FastAPI,Query, HTTPException
from typing import Annotated, Dict,List
import json

from pydantic import Field

app = FastAPI()

@app.get('/')
def login_page():
    data = load_data()
    return data


def load_data():
    path = r'FastAPI\patients.json'
    data = {}
    with open('path','r') as f:
        data = json.load(f)
    return data
