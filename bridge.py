from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, relationship, Session
import pymysql
import cryptography 


username = "admin"
password = "Admin@2025"
host = "127.0.0.1"   
port = 3306             
database = "NBA"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}", connect_args={"connect_timeout": 60})
metadata = MetaData()
Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    id = Column(String, primary_key= True)
    name = Column(String(64), unique= True)
    weight = Column(Integer)
    height = Column(Integer)
    exp = Column(Integer)
    age = Column(Integer)
    
    seasons = relationship("Season", back_populates="player")
    positions = relationship("Position", back_populates="player")
    
class Season(Base):
    __tablename__ = "seasons"
    id = Column(String ,primary_key= True)
    season = Column(Integer)
    player_id = Column(String(64), ForeignKey("players.id"))
    Rank = Column(Integer)
    which_group_id = Column(String, ForeignKey("which_group.id"))
    
    player = relationship("Player", back_populates="seasons")
    group = relationship("Group", back_populates="seasons")

    
class Position(Base):
    __tablename__ = "positions"
    id = Column(String, primary_key= True)
    position = Column(String(64))
    player_id = Column(String(64),ForeignKey("players.id"))
    
    player = relationship("Player", back_populates="positions")

    
class Group(Base):
    __tablename__ = "which_group"
    id = Column(String, primary_key= True)
    group_name = Column(String(32))
    
    seasons = relationship("Season", back_populates="group")
    
    
Base.metadata.create_all(engine)

# with Session(engine) as session:
#     for _, row in df_players.iterrows():
#         player = Player(
#             name=row["name"],
#             weight=row["weight"],
#             height=row["height"],
#             exp=row["exp"],
#             age=row["age"]
#         )
#         session.add(player)
    
#     session.commit()
