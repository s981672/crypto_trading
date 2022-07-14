

from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    user_id : str
    email : str = None
    phone : str = None
    budget : str = None
    created_at : str
    updated_at : str