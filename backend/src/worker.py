from pathlib import Path
import redis,traceback
from sqlalchemy import select
from src.config.settings import REDIS_URL
from src.config.database import Session
from src.models import SpectralRun,SpectralStudy,SamplingWindow,SignalDataset
from src.services.windows import points_for
from src.services.analysis import analyze
client=redis.Redis.from_url(REDIS_URL);heartbeat=Path("/artifacts/worker-heartbeat")
def execute(id):
 with Session() as db:
  run=db.get(SpectralRun,id)
  if not run or run.status not in ("queued","running"):return
  run.status="running";db.commit()
  try:
   study=db.get(SpectralStudy,run.study_id);window=db.get(SamplingWindow,study.window_id);dataset=db.get(SignalDataset,window.dataset_id)
   run.result=analyze(run.input_points or points_for(dataset,window),study);run.status="completed"
  except Exception as e:run.error=str(e);run.status="failed";traceback.print_exc()
  db.commit()
def main():
 with Session() as db:
  for id in db.scalars(select(SpectralRun.id).where(SpectralRun.status.in_(["queued","running"]))):client.lpush("jitter-spectrum:jobs",id)
 while True:
  heartbeat.touch();job=client.brpop("jitter-spectrum:jobs",timeout=1)
  if job:execute(job[1].decode())
if __name__=="__main__":main()
