from sqlalchemy import String,Double,Integer,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class SpectralStudy(Base):
 __tablename__="spectral_studies"
 id:Mapped[str]=mapped_column(String,primary_key=True)
 name:Mapped[str]=mapped_column(String,unique=True)
 window_id:Mapped[str]=mapped_column(ForeignKey("sampling_windows.id"))
 detrend:Mapped[str]=mapped_column(String)
 fft_window:Mapped[str]=mapped_column(String)
 min_frequency:Mapped[float]=mapped_column(Double)
 max_frequency:Mapped[float]=mapped_column(Double)
 frequency_points:Mapped[int]=mapped_column(Integer)
 created_at:Mapped[str]=mapped_column(String)
