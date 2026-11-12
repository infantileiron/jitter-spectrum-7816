from sqlalchemy import String,Double,Integer,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class BackfillBatch(Base):
 __tablename__="backfill_batches"
 id:Mapped[str]=mapped_column(String,primary_key=True)
 dataset_id:Mapped[str]=mapped_column(ForeignKey("signal_datasets.id"))
 actor:Mapped[str]=mapped_column(String)
 added:Mapped[int]=mapped_column(Integer)
 duplicates:Mapped[int]=mapped_column(Integer)
 corrections:Mapped[list]=mapped_column(JSON,default=list)
 dataset_version:Mapped[int]=mapped_column(Integer)
 created_at:Mapped[str]=mapped_column(String)
