from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Column,
    Float,
)

from sqlalchemy.orm import relationship, backref
from .db import db


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Agent(BaseModel):
    """

    """

    __tablename__ = "agents"

    hostname = Column(String(length=250), default="")
    ip = Column(String(length=150))
    mac = Column(String(length=25), default="")


class Disk(BaseModel):
    """

    """

    __tablename__ = "disks"

    agent_id = Column(Integer, ForeignKey(Agent.id), nullable=False)
    agent = relationship(Agent, backref=backref("disks"))

    mountpoint = Column(String(length=300))


class DiskStatistic(BaseModel):
    """

    """

    __tablename__ = "statistics"

    disk_id = Column(Integer, ForeignKey(Disk.id), nullable=False)
    disk = relationship(Disk, backref=backref("statistics"))

    total = Column(Float)
    used = Column(Float)
    free = Column(Float)
    percent = Column(Float)

class Tasks(BaseModel):
    """

    """

    __tablename__ = "tasks"

    agent_id = Column(Integer, ForeignKey(Agent.id), nullable=False)
    agent = relationship(Agent, backref=backref("tasks"))

    code = Column(Integer)
    output = Column(String(length=300))
    errors = Column(String(length=300))
    executed_at = Column(DateTime, default=datetime.utcnow)