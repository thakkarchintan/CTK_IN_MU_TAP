from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.build_log import BuildLogEntry
from app.services.build_log_service import list_build_logs
from app.api.deps import get_current_user
from app.models.models import User

router = APIRouter(prefix="/api/build-log", tags=["build-log"])


@router.get("", response_model=list[BuildLogEntry])
def get_build_log(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_build_logs(db)
