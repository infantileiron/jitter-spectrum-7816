import uuid
from fastapi import HTTPException
from sqlalchemy import select
from src.models import SignalDataset,SamplingWindow,SpectralStudy,SpectralRun,BackfillBatch
from src.utils.time import now
from src.utils.serialization import serialize,rows
MAX_POINTS=6000
def create(db,payload):
 if db.scalar(select(SignalDataset).where(SignalDataset.name==payload.name)):raise HTTPException(409,"观测集名称已存在")
 item=SignalDataset(id=str(uuid.uuid4()),name=payload.name,source=payload.source,points=[p.model_dump() for p in payload.points],version=1,created_at=now());db.add(item);db.commit();return serialize(item)
def require(db,id):
 item=db.get(SignalDataset,id)
 if not item:raise HTTPException(404,"观测集不存在")
 return item
def backfill(db,id,payload,user):
 dataset=require(db,id)
 existing={(p["link_id"],p["time_minutes"]):p["jitter_ms"] for p in dataset.points}
 added,duplicates,corrections=[],0,[]
 for p in payload.points:
  key=(p.link_id,p.time_minutes)
  if key not in existing:added.append(p.model_dump())
  elif existing[key]==p.jitter_ms:duplicates+=1
  else:corrections.append({"link_id":p.link_id,"time_minutes":p.time_minutes,"old_jitter_ms":existing[key],"new_jitter_ms":p.jitter_ms})
 summary={"added":len(added),"duplicates":duplicates,"corrections":corrections}
 if corrections and not payload.confirm_corrections:return {"status":"needs_confirmation",**summary}
 if not added and not corrections:return {"status":"noop",**summary}
 if len(dataset.points)+len(added)>MAX_POINTS:raise HTTPException(422,f"观测集总点数超过{MAX_POINTS}上限，请分批核对后再补采")
 points=[dict(p) for p in dataset.points]
 if corrections:
  fix={(c["link_id"],c["time_minutes"]):c["new_jitter_ms"] for c in corrections}
  points=[{**p,"jitter_ms":fix.get((p["link_id"],p["time_minutes"]),p["jitter_ms"])} for p in points]
 dataset.points=points+added;dataset.version+=1
 touched={(p["link_id"],p["time_minutes"]) for p in added}|{(c["link_id"],c["time_minutes"]) for c in corrections}
 windows=[w for w in db.scalars(select(SamplingWindow).where(SamplingWindow.dataset_id==dataset.id)) if any(l==w.link_id and w.start_minutes<=t<=w.end_minutes for l,t in touched)]
 stale_runs=0
 for w in windows:
  w.point_count=len([p for p in dataset.points if p["link_id"]==w.link_id and w.start_minutes<=p["time_minutes"]<=w.end_minutes])
  for study in db.scalars(select(SpectralStudy).where(SpectralStudy.window_id==w.id)):
   for run in db.scalars(select(SpectralRun).where(SpectralRun.study_id==study.id,SpectralRun.status.in_(["queued","running","completed"]),SpectralRun.stale.is_(False))):
    run.stale=True;stale_runs+=1
 db.add(BackfillBatch(id=str(uuid.uuid4()),dataset_id=dataset.id,actor=user["email"],added=len(added),duplicates=duplicates,corrections=corrections,dataset_version=dataset.version,created_at=now()))
 db.commit()
 return {"status":"applied",**summary,"dataset_version":dataset.version,"affected_windows":[w.name for w in windows],"stale_runs":stale_runs}
def backfills(db):return rows(db.scalars(select(BackfillBatch).order_by(BackfillBatch.created_at.desc())))
