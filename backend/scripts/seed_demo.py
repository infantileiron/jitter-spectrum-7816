import random,math,json
from sqlalchemy import select,func
from src.config.database import Base,engine,Session
from src.models import User,SignalDataset,SamplingWindow,SpectralStudy,SpectralRun,PeriodReview,Report
from src.services.analysis import analyze
from src.utils.security import hash_password
from src.utils.time import now
def seed():
 Base.metadata.create_all(engine)
 with Session() as db:
  for role in ("admin","analyst","viewer"):
   if not db.get(User,role):db.add(User(id=role,email=role+"@beiyu.demo",password=hash_password("Signal2026!"),role=role))
  rng=random.Random(2307);points=[]
  for link in range(1,7):
   for i in range(480):
    t=float(i)
    if link==3:t+=int(i>=120)+int(i>=240)+int(i>=360)
    if link==4 and i>0:t+=rng.uniform(-.2,.2)
    value=12+math.sin(2*math.pi*t/30)+.5*math.cos(2*math.pi*t/80)+rng.gauss(0,.025)
    if link==2:value+=.009*t
    if link==5:value=10+1.2*math.sin(2*math.pi*t/45)+.4*math.cos(2*math.pi*t/120)
    if link==6:value=14
    points.append({"link_id":f"BY-{link:02}","time_minutes":round(t,6),"jitter_ms":round(value,8)})
  if not db.get(SignalDataset,"demo-data"):db.add(SignalDataset(id="demo-data",name="北屿离线观测·6链路各480点",source="beiyu_jitter_202611.json",points=points,version=1,created_at=now()));db.flush()
  for link in (1,2,3,4,5,6):
   samples=[p for p in points if p["link_id"]==f"BY-{link:02}"]
   if not db.get(SamplingWindow,f"demo-window-{link}"):db.add(SamplingWindow(id=f"demo-window-{link}",name=f"BY-{link:02}·完整观测窗口",dataset_id="demo-data",link_id=f"BY-{link:02}",start_minutes=min(p["time_minutes"] for p in samples),end_minutes=max(p["time_minutes"] for p in samples),point_count=480,created_at=now()))
  db.flush()
  if not db.get(SpectralStudy,"demo-study"):db.add(SpectralStudy(id="demo-study",name="BY-01·去均值与Hann双谱复核",window_id="demo-window-1",detrend="mean",fft_window="hann",min_frequency=.005,max_frequency=.1,frequency_points=1400,created_at=now()));db.flush()
  if not db.get(SpectralRun,"demo-run"):
   samples=[p for p in points if p["link_id"]=="BY-01"]
   db.add(SpectralRun(id="demo-run",study_id="demo-study",status="completed",result=analyze(samples,db.get(SpectralStudy,"demo-study")),error="",dataset_version=1,input_points=samples,stale=False,created_at=now()));db.flush()
  if not db.get(PeriodReview,"demo-review"):db.add(PeriodReview(id="demo-review",run_id="demo-run",note="规则采样两谱候选接近30与80分钟。FFT PSD和LS解释比例单位不同，幅相以首观测为原点；峰值不构成链路故障因果证据。",decision="accepted",author="analyst@beiyu.demo",created_at=now()));db.flush()
  if not db.get(Report,"demo-report"):db.add(Report(id="demo-report",run_id="demo-run",title="北屿BY-01·周期候选人工复核",published_by="admin@beiyu.demo",created_at=now()))
  db.commit();return {m.__tablename__:db.scalar(select(func.count()).select_from(m)) for m in (User,SignalDataset,SamplingWindow,SpectralStudy,SpectralRun,PeriodReview,Report)}
if __name__=="__main__":print(json.dumps(seed(),ensure_ascii=False))
