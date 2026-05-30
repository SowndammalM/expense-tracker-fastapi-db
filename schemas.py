from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    category: str
    amount: float