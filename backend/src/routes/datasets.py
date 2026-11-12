from fastapi import APIRouter,Depends
from sqlalchemy import select
from src.config.database import db_session
from src.controllers.auth import current_user,writer,admin
from src.models import SignalDataset
from src.schemas.dataset import DatasetInput,BackfillInput
from src.services import datasets as service
from src.utils.serialization import rows
router=APIRouter(prefix="/datasets")
@router.get("")
def listing(db=Depends(db_session),user=Depends(current_user)):return rows(db.scalars(select(SignalDataset).order_by(SignalDataset.created_at.desc())))
@router.post("")
def create(payload:DatasetInput,db=Depends(db_session),user=Depends(writer)):return service.create(db,payload)
@router.get("/backfills")
def backfills(db=Depends(db_session),user=Depends(current_user)):return service.backfills(db)
@router.post("/{id}/backfill")
def backfill(id:str,payload:BackfillInput,db=Depends(db_session),user=Depends(writer)):return service.backfill(db,id,payload,user)
