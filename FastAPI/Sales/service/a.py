from fastapi import FastAPI
from typing import List, Dict
from pathlib import Path
import json

app = FastAPI()

base_path = Path(__file__).resolve().parent
path = base_path/"data"/"dummy.json"
print(path)
products = {}
if path.exists() : 
    with open(path,'r')as f :
        products = json.load(f)
print(products)