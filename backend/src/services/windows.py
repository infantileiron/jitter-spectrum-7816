import uuid
from fastapi import HTTPException
from sqlalchemy import select
from src.models import SamplingWindow
from src.services.datasets import require
from src.utils.time import now
from src.utils.serialization import serialize
def points_for(dataset,window):return [p for p in dataset.points if p["link_id"]==window.link_id and window.start_minutes<=p["time_minutes"]<=window.end_minutes]
def create(db,payload):
 dataset=require(db,payload.dataset_id);link=[p for p in dataset.points if p["link_id"]==payload.link_id]
 if not link:raise HTTPException(422,"链路不存在")
 if payload.start_minutes<min(p["time_minutes"] for p in link) or payload.end_minutes>max(p["time_minutes"] for p in link):raise HTTPException(422,"窗口不能超出该链路实际观测覆盖，不做补零或外推")
 points=points_for(dataset,payload)
 if len(points)<16:raise HTTPException(422,"窗口内不足16点，不计算周期")
 if db.scalar(select(SamplingWindow).where(SamplingWindow.name==payload.name)):raise HTTPException(409,"窗口名称已存在")
 item=SamplingWindow(id=str(uuid.uuid4()),point_count=len(points),created_at=now(),**payload.model_dump());db.add(item);db.commit();return serialize(item)
