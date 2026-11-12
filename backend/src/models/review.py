from sqlalchemy import String,Double,Integer,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class PeriodReview(Base):
 __tablename__="period_reviews"
 id:Mapped[str]=mapped_column(String,primary_key=True)
 run_id:Mapped[str]=mapped_column(ForeignKey("spectral_runs.id"))
 note:Mapped[str]=mapped_column(Text)
 decision:Mapped[str]=mapped_column(String)
 author:Mapped[str]=mapped_column(String)
 created_at:Mapped[str]=mapped_column(String)
