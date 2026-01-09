from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database
import crud
import schemas
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

database.init_db()

# --- SCHEDULER SETUP ---
def run_scheduler_job():
    """Function to run periodically"""
    db = database.SessionLocal()
    try:
        count = crud.process_recurring_transactions(db)
        if count > 0:
            print(f"Scheduler: Processed {count} recurring transactions.")
    except Exception as e:
        print(f"Scheduler Error: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start Scheduler
    scheduler = BackgroundScheduler()
    # Check every hour
    scheduler.add_job(run_scheduler_job, 'interval', minutes=60)
    # Also run once immediately on startup to catch up missed ones
    run_scheduler_job()
    scheduler.start()
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Transactions ---
@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)

@app.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    return crud.get_transactions(db, skip=skip, limit=limit)

# --- Assets ---
@app.post("/assets/", response_model=schemas.Asset)
def create_asset_entry(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    return crud.create_asset_value(db=db, asset=asset)

@app.get("/assets/", response_model=List[schemas.Asset])
def read_assets(db: Session = Depends(get_db)):
    return crud.get_latest_asset_values(db)

# --- Recurring ---
@app.post("/recurring/", response_model=schemas.Recurring)
def create_recurring(recurring: schemas.RecurringCreate, db: Session = Depends(get_db)):
    return crud.create_recurring(db=db, recurring=recurring)

@app.get("/recurring/", response_model=List[schemas.Recurring])
def read_recurring(db: Session = Depends(get_db)):
    return crud.get_recurring(db)

@app.put("/recurring/{recurring_id}", response_model=schemas.Recurring)
def update_recurring(recurring_id: int, recurring_update: schemas.RecurringUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_recurring(db, recurring_id, recurring_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recurring transaction not found")
    return db_item

@app.delete("/recurring/{recurring_id}", response_model=schemas.Recurring)
def delete_recurring(recurring_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_recurring(db, recurring_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recurring transaction not found")
    return db_item


# Manual Trigger endpoint (for testing)
@app.post("/recurring/process")
def trigger_recurring_process(db: Session = Depends(get_db)):
    count = crud.process_recurring_transactions(db)
    return {"processed": count}