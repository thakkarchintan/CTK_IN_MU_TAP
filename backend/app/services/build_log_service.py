from sqlalchemy.orm import Session

from app.models.models import BuildLog


def list_build_logs(db: Session) -> list[BuildLog]:
    return db.query(BuildLog).order_by(BuildLog.timestamp.desc()).all()


def record_build_log(db: Session, step: str, title: str, description: str) -> BuildLog:
    """Called at the end of each development step to add a visible entry to the in-app Build Log screen."""
    entry = BuildLog(step=step, title=title, description=description)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
