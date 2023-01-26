from .database import Base
from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.sql.schema import ForeignKey

class User(Base):
    __tablename__="users"
    user_id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String)

class Ride(Base):
     __tablename__= "rides"
     ride_id=Column(Integer,primary_key=True,nullable=False)
     user_id=Column(Integer,ForeignKey('users.user_id'),nullable=False,)
     from_address=Column(String,nullable=False)
     to_address=Column(String,nullable=False)
     date_and_time=Column(DateTime)
     travel_medium=Column(String,nullable=False)
     asset_qunatity=Column(Integer,nullable=False)
     

class Request(Base):
     __tablename__= "requests"
     request_id=Column(Integer,primary_key=True,nullable=False)
     user_id=Column(Integer,ForeignKey('users.user_id'),nullable=False,)
     from_address=Column(String,nullable=False)
     to_address=Column(String,nullable=False)
     date_and_time=Column(DateTime)
     no_of_assest=Column(Integer,nullable=False)
     asset_type=Column(String,nullable=False)
     asset_sensitivity=Column(String,nullable=False)
     whom_to_deliver=Column(String,nullable=False)
     status=Column(String,default='pending')
     ride_id=Column(Integer,default=-1)
     

