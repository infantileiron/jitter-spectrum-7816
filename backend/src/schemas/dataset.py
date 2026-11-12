from pydantic import BaseModel,Field,model_validator
class Point(BaseModel):
 link_id:str=Field(min_length=1,max_length=60)
 time_minutes:float=Field(ge=0,le=10000000,allow_inf_nan=False)
 jitter_ms:float=Field(ge=-1000000,le=1000000,allow_inf_nan=False)
class DatasetInput(BaseModel):
 name:str=Field(min_length=2,max_length=120)
 source:str=Field(default="jitter_observations.json",max_length=120)
 points:list[Point]=Field(min_length=2,max_length=6000)
 @model_validator(mode="after")
 def valid(self):
  keys=[(p.link_id,p.time_minutes) for p in self.points]
  if len(set(keys))!=len(keys):raise ValueError("同一链路重复时间戳必须先复核，不允许静默去重")
  if len({p.link_id for p in self.points})>12:raise ValueError("一批最多12条模拟链路")
  return self
class BackfillInput(BaseModel):
 points:list[Point]=Field(min_length=1,max_length=6000)
 confirm_corrections:bool=False
 @model_validator(mode="after")
 def valid(self):
  keys=[(p.link_id,p.time_minutes) for p in self.points]
  if len(set(keys))!=len(keys):raise ValueError("同一批次内重复时间戳必须先复核，不允许静默去重")
  return self
