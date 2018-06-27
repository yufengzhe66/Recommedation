from flask import escape,flash,request,abort


from math import ceil


from sqlalchemy.orm import sessionmaker,Query,relationship,backref 
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import create_engine  

from sqlalchemy import Column, String ,Integer,Float,ForeignKey,Date,DateTime,Table

# 创建对象的基类:  
Base = declarative_base()  

"""
relation1 = Table('relation1', Base.metadata,
      Column('u_id',Integer,ForeignKey('user.u_id')),
      Column('o_id',Integer,ForeignKey('OrderForm.id'))
      )

relation2 = Table('relation2', Base.metadata,
      Column('o_id',Integer,ForeignKey('OrderForm.id')),
      Column('b_id',Integer,ForeignKey('book.b_id'))
      )
"""





class OrderForm(Base):
    __tablename__ = 'OrderForm'
    id = Column(Integer,primary_key=True,autoincrement = True)
    u_id = Column(Integer,ForeignKey('user.u_id'))
    b_id = Column(Integer,ForeignKey('book.b_id'))
    amount = Column(Integer)
    time = Column(Date)
    type = Column(Integer)
    rate = Column(Float)
    comment = Column(String)
 #   user = relationship('User',secondary=relation1,backref=backref('orderforms', lazy='dynamic'))   
 #   book = relationship('Book',secondary=relation2,backref=backref('orderforms', lazy='dynamic'))
    
    def __init__(self,u_id,b_id, amount,time,type):
#        self.id = id
        self.u_id = u_id
        self.b_id = b_id
        self.amount = amount
        self.time = time
        self.type = type
      
       


"""
OrderForm = Table('OrderForm', Base.metadata,
#      Column('id',Integer,primary_key=True,autoincrement = True),
      Column('u_id',Integer,ForeignKey('user.u_id')),
      Column('b_id',Integer,ForeignKey('book.b_id'))
#      Column('amount',Integer),
#      Column('time',Date),
#      Column('type',Integer),
#      Column('rate',Float)
#    user = relationship('User',backref='orderforms'),   
#    book = relationship('Book',backref='orderforms')
   ) 
"""



class User(Base):  
    __tablename__ = 'user'  
    u_id = Column(Integer, primary_key=True)  
    u_name = Column(String(20))
    u_password = Column(String(20))
    u_sex = Column(String(10))
    u_age = Column(Integer)
    u_address = Column(String(50))
    realname = Column(String(20))
    tel = Column(Integer)
 #   orderforms = relationship('OrderForm',backref=backref('user'))
    
    def __init__(self,u_id,u_name,u_password,u_sex,u_age,u_address):
        self.u_id = u_id
        self.u_name = u_name
        self.u_password = u_password
        self.u_sex = u_sex
        self.u_age = u_age
        self.u_address = u_address
       
    
    
    
class admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)  
    name = Column(String(20))
    password = Column(String(20))
    
    
    def __init__(self,id,name,password):
        self.id = id
        self.name = name
        self.password = password
        
        
        
class Book(Base):
    __tablename__ = 'book'
    b_id = Column(Integer, primary_key=True)  
    b_name = Column(String(20))
    b_author = Column(String(20))
    b_publish = Column(String(40))
    b_type = Column(String(20))
    b_price = Column(Float)
    b_stock = Column(Integer)
    b_totalSold = Column(Integer)
    b_date = Column(Date)
#    orderforms = relationship('OrderForm',backref=backref('book'))
    
    
    def __init__(self,b_id,b_name,b_author,b_publish,b_type,b_price,b_stock,b_totalSold,b_date):
        self.b_id = b_id
        self.b_name = b_name
        self.b_author=b_author
        self.b_publish = b_publish
        self.b_type = b_type
        self.b_price = b_price
        self.b_stock = b_stock
        self.b_totalSold = b_totalSold
        self.b_date = b_date
 


class Recommendation(Base):
    __tablename__ = 'recommendation'
    u_id = Column(Integer, primary_key=True)
    
    recommendation1 = Column(Integer)
    recommendation2 = Column(Integer)  
    recommendation3 = Column(Integer)
    recommendation4 = Column(Integer)
    recommendation5 = Column(Integer)
    
    def __init__(self,u_id,sumOperation):
        self.u_id = u_id
       
 

# 初始化数据库连接:  
engine = create_engine('mysql+pymysql://root:@localhost:3306/bookshop?charset=utf8') #现在是用pymysql做sql驱动了  
# 创建DBSession类型:  
DBSession = sessionmaker(bind=engine)

    
     