from pydantic import BaseModel
from datetime import date
from typing import Optional

# --- Transaction Schemas ---
class TransactionBase(BaseModel):
    date: date
    type: str  # 'Income' or 'Expense'
    category: str
    amount: float
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True

# --- Asset Schemas ---
class AssetBase(BaseModel):
    date: date
    type: str # 'Cash', 'Credit Card Debt', 'Investment', 'Property'
    name: str
    amount: float

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int

    class Config:
        from_attributes = True

# --- Recurring Schemas ---
class RecurringBase(BaseModel):
    name: str
    amount: float
    category: str
    type: str
    frequency: str
    start_date: date
    is_active: bool = True

class RecurringCreate(RecurringBase):
    pass

class RecurringUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    type: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[date] = None
    is_active: Optional[bool] = None

class Recurring(RecurringBase):
    id: int
    next_run_date: date

    class Config:
        from_attributes = True