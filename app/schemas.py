from pydantic import BaseModel,EmailStr,ValidationError, validator
from datetime import datetime

class User(BaseModel):
    name:str

class Request(BaseModel):
    user_id:int
    from_address:str
    to_address:str
    date_and_time:datetime
    no_of_assest:int
    asset_type:str
    asset_sensitivity:str
    whom_to_deliver:str
    
    @validator('asset_type')
    def asset_type_validator(cls,asset_type):
        if asset_type.lower() not in ['laptop','travel_bag','package']:
            return ValueError('Must Be Any one of laptop , travel_bag , package')
        return asset_type.upper()
    
    @validator('asset_sensitivity')
    def tasset_sensitivity_validator(cls,asset_sensitivity):
        if asset_sensitivity.lower() not in ['highly_sensitive','sensitive','normal']:
            return ValueError('Must Be Any one of highly_sensitive , sensitive , normal')
        return asset_sensitivity.upper()


class Ride(BaseModel):
    user_id:int
    from_address:str
    to_address:str
    date_and_time:datetime
    travel_medium:str
    asset_qunatity:int

    @validator('travel_medium')
    def travel_medium_validator(cls,travel_medium):
        if travel_medium.lower() not in ['bus','car','train']:
            print("----")
            return ValueError('Must Be Any one of Bus , Car , Train')
        return travel_medium.upper()

class RequestOut(BaseModel):
    request_id:int
    from_address:str
    to_address:str
    date_and_time:datetime
    asset_type:str
    asset_sensitivity:str
    no_of_assest:int
    whom_to_deliver:str
    status:str
    ride_id:int
    class Config:
        orm_mode = True
        
class RideOut(BaseModel):
    ride_id:int
    user_id:int
    from_address:str
    to_address:str
    date_and_time:datetime
    travel_medium:str
    asset_qunatity:int
    class Config:
        orm_mode = True