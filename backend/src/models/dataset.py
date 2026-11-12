from sqlalchemy import String,Double,Integer,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class SignalDataset(Base):
 __tablename__="signal_datasets"
 id:Mapped[str]=mapped_column(String,primary_key=True)
 name:Mapped[str]=mapped_column(String,unique=True)
 source:Mapped[str]=mapped_column(String)
 points:Mapped[list]=mapped_column(JSON)
 created_at:Mapped[str]=mapped_column(String)
