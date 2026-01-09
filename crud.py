from sqlalchemy.orm import Session
from sqlalchemy import func
import database
from database import Transaction, AssetValue, RecurringTransaction
import schemas
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# --- Transactions ---
def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Transaction).offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# --- Assets ---
def create_asset_value(db: Session, asset: schemas.AssetCreate):
    db_asset = AssetValue(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def get_latest_asset_values(db: Session):
    return db.query(AssetValue).all()

# --- Recurring ---
def create_recurring(db: Session, recurring: schemas.RecurringCreate):
    # Initial next_run_date is start_date
    db_obj = RecurringTransaction(**recurring.dict(), next_run_date=recurring.start_date)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_recurring(db: Session):
    return db.query(RecurringTransaction).all()

def get_recurring_item(db: Session, recurring_id: int):
    return db.query(RecurringTransaction).filter(RecurringTransaction.id == recurring_id).first()

def update_recurring(db: Session, recurring_id: int, recurring_update: schemas.RecurringUpdate):
    db_item = db.query(RecurringTransaction).filter(RecurringTransaction.id == recurring_id).first()
    if db_item:
        update_data = recurring_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        
        # Recalculate next_run_date if start_date or frequency changed? 
        # For simplicity, if user changes start_date, we might need to reset logic, 
        # but let's assume user knows what they are doing or just updates next_run_date manually if needed.
        # Ideally, we should check if frequency/start_date changed and re-compute.
        # For MVP: simple field update.
        
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_recurring(db: Session, recurring_id: int):
    db_item = db.query(RecurringTransaction).filter(RecurringTransaction.id == recurring_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

def process_recurring_transactions(db: Session):
    """
    Checks all active recurring transactions. 
    If next_run_date <= today, create a transaction and update next_run_date.
    """
    today = date.today()
    due_items = db.query(RecurringTransaction).filter(
        RecurringTransaction.is_active == 1,
        RecurringTransaction.next_run_date <= today
    ).all()
    
    processed_count = 0
    
    for item in due_items:
        # 1. Create the Transaction
        new_txn = Transaction(
            date=item.next_run_date, # Use the scheduled date, not necessarily today
            type=item.type,
            category=item.category,
            amount=item.amount,
            notes=f"Auto-generated: {item.name}"
        )
        db.add(new_txn)
        
        # 2. Calculate Next Run Date
        next_date = item.next_run_date
        if item.frequency == 'Daily':
            next_date += timedelta(days=1)
        elif item.frequency == 'Weekly':
            next_date += timedelta(weeks=1)
        elif item.frequency == 'Monthly':
            next_date += relativedelta(months=1)
        elif item.frequency == 'Yearly':
            next_date += relativedelta(years=1)
            
        item.next_run_date = next_date
        processed_count += 1
    
    if processed_count > 0:
        db.commit()
        
    return processed_count