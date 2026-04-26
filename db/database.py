import datetime
import os

from sqlalchemy import create_engine, Column, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR}/signals.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Signal(Base):
    __tablename__ = "signals"

    ticker = Column(String, primary_key=True)
    current_price = Column(Float)
    signal = Column(String)
    reason = Column(Text)
    ema_status = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.now)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_signal(ticker: str, price: float, signal: str, reason: str, ema_status: str):
    db = SessionLocal()
    try:
        existing = db.query(Signal).filter(Signal.ticker == ticker).first()
        if existing:
            existing.current_price = price
            existing.signal = signal
            existing.reason = reason
            existing.ema_status = ema_status
            existing.updated_at = datetime.datetime.now()
        else:
            new_signal = Signal(
                ticker=ticker,
                current_price=price,
                signal=signal,
                reason=reason,
                ema_status=ema_status,
                updated_at=datetime.datetime.now()
            )
            db.add(new_signal)
        db.commit()
    finally:
        db.close()


def get_all_signals():
    db = SessionLocal()
    try:
        return db.query(Signal).all()
    finally:
        db.close()