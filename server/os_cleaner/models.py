from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Column,
    Float,
)

from sqlalchemy.orm import relationship
from .db import db


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Agent(BaseModel):
    """

    """

    __tablename__ = "agents"

    hostname = Column(String(length=250), default="")
    ip = Column(String(length=150))

    disks = relationship("Disks", back_populates="agent")
    tasks = relationship("Tasks", back_populates="agent")


class Disks(BaseModel):
    """

    """

    __tablename__ = "disks"

    agent_id = Column(Integer, ForeignKey(Agent.id), nullable=False)
    agent = relationship(Agent, back_populates="disks")

    mountpoint = Column(String(length=300))

    total = Column(Float)
    used = Column(Float)
    free = Column(Float)
    percent = Column(Float)


class Tasks(BaseModel):
    """

    """

    __tablename__ = "tasks"

    agent_id = Column(Integer, ForeignKey(Agent.id), nullable=False)
    agent = relationship(Agent, back_populates="tasks")

    code = Column(Integer)
    output = Column(String(length=300))
    errors = Column(String(length=300))
    command = Column(String(length=700))
