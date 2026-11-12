import uuid
from fastapi import HTTPException
from sqlalchemy import select
from src.models import SignalDataset
from src.utils.time import now
from src.utils.serialization import serialize
def create(db,payload):
 if db.scalar(select(SignalDataset).where(SignalDataset.name==payload.name)):raise HTTPException(409,"观测集名称已存在")
 item=SignalDataset(id=str(uuid.uuid4()),name=payload.name,source=payload.source,points=[p.model_dump() for p in payload.points],created_at=now());db.add(item);db.commit();return serialize(item)
def require(db,id):
 item=db.get(SignalDataset,id)
 if not item:raise HTTPException(404,"观测集不存在")
 return item
