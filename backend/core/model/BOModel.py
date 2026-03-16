from flask import session
from flask import request,Blueprint, jsonify
from sqlalchemy import create_engine, select, MetaData, Table,text
from sqlalchemy.sql import and_, or_
from core import app

engine= create_engine(app.config['DB_URL'],pool_size=5000,pool_recycle=3600)

class BOModel():

    def __init__(self):
        self.meta=MetaData()
        


    def GetAllUser(self):
        with engine.connect() as conn:
            stmt=text("select * from users;")
            result=conn.execute(stmt).all()
            conn.close()
            
            # return result._mapping if result else None
            return [dict(r._mapping) for r in result ] if result else None