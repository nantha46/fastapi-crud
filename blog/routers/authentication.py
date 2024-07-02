from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database, token
from sqlalchemy.orm import Session
from .. hashing import Hash

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
    if not Hash.verify_password(request.password, user.password):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid password")

    access_token = token.create_access_token(data={"sub": user.mail})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/logout')
def logout(access_token: str):
    return {"message": "Logged out successfully."}
