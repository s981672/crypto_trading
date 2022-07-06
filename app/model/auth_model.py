
from pydantic import BaseModel


class ApiAuth(BaseModel):
    api_key: str
    secret_key : str
    
