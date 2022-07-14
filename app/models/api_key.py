import datetime
from pydantic import BaseModel


class ApiKey(BaseModel):
    user_id : str
    exchange : str
    access : str
    secret : str
    created_at : str
    updated_at : str