from sqlalchemy import String,Double,Integer,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class SamplingWindow(Base):
 __tablename__="sampling_windows"
 id:Mapped[str]=mapped_column(String,primary_key=True)
 name:Mapped[str]=mapped_column(String,unique=True)
 dataset_id:Mapped[str]=mapped_column(ForeignKey("signal_datasets.id"))
 link_id:Mapped[str]=mapped_column(String)
 start_minutes:Mapped[float]=mapped_column(Double)
 end_minutes:Mapped[float]=mapped_column(Double)
 point_count:Mapped[int]=mapped_column(Integer)
 created_at:Mapped[str]=mapped_column(String)
