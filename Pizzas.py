from cmath import pi
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://root:123@localhost:3306/pizza_service")
base = declarative_base()

class Pizzas(base):

    __tablename__ = 'Pizzas'

    pizza_id = Column(Integer, primary_key=True)
    pizza_name = Column(String)
    price = Column(Integer)

    def __init__(self, pizza_id, pizza_name, price):                 
        self.pizza_id = pizza_id
        self.pizza_name = pizza_name
        self.price = price

base.metadata.create_all(engine)