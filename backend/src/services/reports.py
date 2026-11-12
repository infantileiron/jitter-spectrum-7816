import uuid,csv,io
from sqlalchemy import select
from fastapi import HTTPException
from src.models import Report,PeriodReview
from src.services.runs import require_completed
from src.utils.time import now
from src.utils.serialization import serialize
def create(db,payload,user):
 require_completed(db,payload.run_id)
 review=db.scalar(select(PeriodReview).where(PeriodReview.run_id==payload.run_id).order_by(PeriodReview.created_at.desc()))
 if not review or review.decision!="accepted":raise HTTPException(409,"最新周期复核须接受后才能归档")
 if db.scalar(select(Report).where(Report.run_id==payload.run_id)):raise HTTPException(409,"本次运行已归档")
 item=Report(id=str(uuid.uuid4()),published_by=user["email"],created_at=now(),**payload.model_dump());db.add(item);db.commit();return serialize(item)
def export(db,id):
 report=db.get(Report,id)
 if not report:raise HTTPException(404,"报告不存在")
 run=require_completed(db,report.run_id);result=run.result;buf=io.StringIO();writer=csv.DictWriter(buf,["method","frequency_per_minute","period_minutes","power","units","dataset_version"]);writer.writeheader()
 for method in ("fft","ls"):
  for peak in result[method]["peaks"]:writer.writerow({"method":method,**peak,"units":result[method]["units"],"dataset_version":run.dataset_version})
 return "\ufeff"+buf.getvalue()
