from sqlalchemy import String,Double,Integer,Boolean,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class SpectralRun(Base):
 __tablename__="spectral_runs"
 id:Mapped[str]=mapped_column(String,primary_key=True)
 study_id:Mapped[str]=mapped_column(ForeignKey("spectral_studies.id"))
 status:Mapped[str]=mapped_column(String)
 result:Mapped[dict]=mapped_column(JSON,default=dict)
 error:Mapped[str]=mapped_column(Text,default="")
 dataset_version:Mapped[int]=mapped_column(Integer,default=1)
 input_points:Mapped[list]=mapped_column(JSON,default=list)
 stale:Mapped[bool]=mapped_column(Boolean,default=False)
 created_at:Mapped[str]=mapped_column(String)
