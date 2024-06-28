from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.mail == request.mail).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Credential doesn't match")
    if not Hash.verify_password(request.password, user.password): # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid password")
    return user
