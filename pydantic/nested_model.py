from pydantic import BaseModel, Field, field_validator, model_validator,AnyUrl
from typing import Dict, List, Optional

class Patient(BaseModel):
    name : 