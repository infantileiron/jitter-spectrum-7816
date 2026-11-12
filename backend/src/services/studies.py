import uuid
from fastapi import HTTPException
from sqlalchemy import select
from src.models import SamplingWindow,SignalDataset,SpectralStudy
from src.services.windows import points_for
from src.services.preprocessing import sampling_meta
from src.utils.time import now
from src.utils.serialization import serialize
def create(db,payload):
 window=db.get(SamplingWindow,payload.window_id)
 if not window:raise HTTPException(404,"采样窗口不存在")
 dataset=db.get(SignalDataset,window.dataset_id);meta=sampling_meta(points_for(dataset,window))
 if payload.min_frequency<1/meta["span"]*(1-1e-9):raise HTTPException(422,"最大搜索周期不能超过观测跨度")
 if meta["regular"] and payload.max_frequency>meta["nyquist"]*(1+1e-9):raise HTTPException(422,"规则数据搜索上限超过FFT Nyquist")
 if db.scalar(select(SpectralStudy).where(SpectralStudy.name==payload.name)):raise HTTPException(409,"频谱研究名称已存在")
 item=SpectralStudy(id=str(uuid.uuid4()),created_at=now(),**payload.model_dump());db.add(item);db.commit();return serialize(item)
