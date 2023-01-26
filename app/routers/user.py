from fastapi import status,HTTPException,Depends,APIRouter,Response,Query,Request
from sqlalchemy.orm import Session
from app.database import get_db
from app import models,schemas
router=APIRouter(
    prefix='/user',
    tags=['rider api']
)

@router.get("/")
def fun():
    return "hello"
#adding user to database with in data validation
@router.post("/add_user",status_code=status.HTTP_200_OK)
def addUser(user:schemas.User,db:Session=Depends(get_db)):
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user