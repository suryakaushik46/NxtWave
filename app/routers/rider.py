from fastapi import status,HTTPException,Depends,APIRouter,Response,Query,Request
from sqlalchemy.orm import Session
from app.database import get_db
from app import models,schemas
router=APIRouter(
    prefix='/rider',
    tags=['rider api']
)

@router.get("/")
def fun():
    return "hello"
#adding ride to database with in data validation
@router.post("/add_ride")
def addRide(ride:schemas.Ride,db:Session=Depends(get_db)):
    new_ride=models.Ride(**ride.dict())
    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)
    return new_ride
    