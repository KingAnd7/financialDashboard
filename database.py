from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.date.today)
    type = Column(String)  # 'Income' or 'Expense'
    category = Column(String)
    amount = Column(Float)
    notes = Column(String)

    def __repr__(self):
        return f"<Transaction(date={self.date}, type={self.type}, amount={self.amount}, category={self.category})>"

class AssetValue(Base):
    __tablename__ = 'asset_values'

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.date.today)
    type = Column(String) # 'Cash', 'Credit Card Debt', 'Investment', 'Property'
    name = Column(String) # e.g. "Chase Checking", "Amex", "Vanguard", "Main St House"
    amount = Column(Float)

class RecurringTransaction(Base):
    __tablename__ = 'recurring_transactions'

    id = Column(Integer, primary_key=True)
    name = Column(String) # e.g., "Rent", "Netflix"
    amount = Column(Float)
    category = Column(String)
    type = Column(String) # 'Income' or 'Expense'
    frequency = Column(String) # 'Daily', 'Weekly', 'Monthly', 'Yearly'
    start_date = Column(Date)
    next_run_date = Column(Date)
    is_active = Column(Integer, default=1) # 1=Active, 0=Paused

# Database setup
DATABASE_URL = "sqlite:///financial_data.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
