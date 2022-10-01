from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("mysql://root:****l@localhost/pizzaSQL", echo = True)
base = declarative_base()
connection = engine.connect()


class Pizza(base):

    __tablename__ = 'pizza'

    id = Column(Integer, primary_key = True)
    pizza_name = Column(String(255))
    price = Column(Integer)
  

"""  
class Ingredients(base):

    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key = True)
    ingredient_name = Column(String(255))
    price = Column(Integer)

class Order(base):

    __tablename__ = 'order'

    order_id = Column(Integer, primary_key = True)
    pizza_id = Column(Integer, ForeignKey('pizza.id'))
    pizza = relationship("Pizza")

class Customer(base):

    __tablename__ = 'customer'

    name = Column(String(255))
    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship("Address")


class Address(base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key = True)
    city_name = Column(String(255))
    street_name = Column(String(255))
    zip_code = Column(String(255))
"""
    
base.metadata.create_all(engine)