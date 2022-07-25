

from datetime import datetime
from pydantic import BaseModel


class Strategy(BaseModel):
    user_id : str
    strategy_id : str
    created_at : str
    updated_at : str
    budget : str = None
    volume : str = None
    locked_volume : str = None
    weight : int = None