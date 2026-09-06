from fastapi import FastAPI
import data
from typing import List, Dict

app = FastAPI()


def load_products() -> List[Dict]:
    products = data.items
    if not products : 
        return []

    
    