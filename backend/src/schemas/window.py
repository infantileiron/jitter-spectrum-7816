from pydantic import BaseModel,Field,model_validator
class WindowInput(BaseModel):
 name:str=Field(min_length=2,max_length=120)
 dataset_id:str
 link_id:str=Field(min_length=1,max_length=60)
 start_minutes:float=Field(ge=0,allow_inf_nan=False)
 end_minutes:float=Field(gt=0,allow_inf_nan=False)
 @model_validator(mode="after")
 def ordered(self):
  if self.end_minutes<=self.start_minutes:raise ValueError("采样窗口结束须晚于开始")
  return self
