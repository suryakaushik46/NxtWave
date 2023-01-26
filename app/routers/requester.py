from fastapi import status,HTTPException,Depends,APIRouter,Response,Query,Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional,Union
from app.database import get_db
from fastapi_pagination import paginate, LimitOffsetPage,Page
from app import models,schemas
import pytz
import datetime
router=APIRouter(
    prefix='/requester',
    tags=['rider api']
)

@router.get("/")
def fun():
    return "hello from request page "

#adding request to database with in data validation
@router.post("/add_request")
def addRequest(request:schemas.Request,db:Session=Depends(get_db)):
    new_request=models.Request(**request.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


#shows all requesting of the user with out data validation
@router.get("/my_requests/{user_id}",status_code=status.HTTP_200_OK,response_model=Page[schemas.RequestOut])
async def get_all_request_by_user_id(user_id:int, asset_type:Optional[str] = None, status:Optional[str] = None, db : Session = Depends(get_db)):
    filters=[models.Request.user_id==user_id]
    #adding to filter with asset_type
    if(asset_type and asset_type.lower() in ["laptop","package","travel_bag"]):
        filters.append(models.Request.asset_type == asset_type.upper())
    #adding to filter with status
    if(status and status.lower() in ["pending","active","expired"]):
        filters.append(models.Request.status == status.lower())

    #filters to set requsets as expired or not 
    #to igone data which is already expired
    filter_expired=[models.Request.status != 'expired']
    #check the condtition of expire
    filter_expired.append(models.Request.date_and_time<datetime.datetime.now())
    #upadte the database table
    db.query(models.Request).filter(*filter_expired).update({'status':'expired'},synchronize_session=False)

    #get all reuests to show to user based on given filters
    requests = db.query(models.Request).filter(*filters).order_by(desc(models.Request.date_and_time)).all()
    if not requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no avalible requests")
    db.commit()
    # to implement pagination
    return paginate(requests)

#get all matching rides with the request
@router.get("/match_request/{request_id}",status_code=status.HTTP_200_OK,response_model=Page[schemas.RideOut])
def get_all_matching_rides(request_id:int,db:Session=Depends(get_db)):
    #adding request filters
    request_filters=[models.Request.request_id == request_id]
    #get data requeried such that we can query from the ride table using the conditions
    request_data_from_db = db.query(models.Request).filter(*request_filters).first()

    #if no request with the request id
    if not request_data_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"requests are not available")
    # adding filters to query from the ride table like from,to,date time,no of assets
    filters=[models.Ride.from_address==request_data_from_db.from_address,
             models.Ride.to_address==request_data_from_db.to_address,
             models.Ride.date_and_time>=datetime.datetime.now()-datetime.timedelta(1),
             models.Ride.asset_qunatity>=request_data_from_db.no_of_assest]

    #query to order by the time 
    rides_from_db=db.query(models.Ride).filter(*filters).order_by(desc(models.Ride.date_and_time)).all()

    #if no matching rides
    if not rides_from_db:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"no matching rides")
    return paginate(rides_from_db)


#to approve the ride
@router.patch("/match_request/{request_id}/apply/{ride_id}",status_code=status.HTTP_200_OK)
def apply_ride(request_id:int,ride_id:int,db:Session=Depends(get_db)):
    #adding filters
    request_filters=[models.Request.request_id == request_id]
    #getting the ni_of assest requested by the requester
    request_data=db.query(models.Request).filter(*request_filters).first()
    no_of_assests=request_data.no_of_assest
    #adding filter if the ride_id has capcity to carry all assets
    ride_data=db.query(models.Ride).filter(models.Ride.ride_id==ride_id,models.Ride.asset_qunatity>=no_of_assests).first()
    
    #if not able to carry
    if not ride_data:
        return {'message':"the rider is not allowed exceeded maximum qunatity"}

    #if the rider can carry keeing status as active
    db.query(models.Request).filter(*request_filters).update({'status':'active'},synchronize_session=False)

    #if the rider can carry keeing ride_id to ride
    db.query(models.Request).filter(*request_filters).update({'ride_id':ride_id},synchronize_session=False)
    
    #here we update the asset qunatity of the ride as some case he can take to requests
    db.query(models.Ride).filter(models.Ride.ride_id==ride_id).update({'asset_qunatity':ride_data.asset_qunatity-no_of_assests},synchronize_session=False)

    #getting name of rider from users table
    user_data=db.query(models.User).filter(models.User.user_id==ride_data.user_id).first()
    db.commit()
    return {"message":f'your rider is {user_data.name}'}