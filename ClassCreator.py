from inspect import CO_ASYNC_GENERATOR
from time import time
from pymysql import Date
from sqlalchemy import TIMESTAMP, create_engine
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

engine = create_engine("mysql://root:123sql@localhost/pizzaSQL", echo = True)
base = declarative_base()
connection = engine.connect()

pizza_ingredients = Table(
    'pizza_ingredients', base.metadata,
    Column('pizza_id', Integer, ForeignKey('pizzas.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
)

order_pizzas = Table(
    'order_pizzas', base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('pizza_id', Integer, ForeignKey('pizzas.id'))
)


class Pizza(base):

    __tablename__ = 'pizzas'

    id = Column(Integer, primary_key = True)
    pizza_name = Column(String(255))
    ingredients = relationship('Ingredient', secondary = pizza_ingredients)

    def __init__(self, pizza_name):
        self.pizza_name = pizza_name
  
 
class Ingredient(base):

    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key = True)
    ingredient_name = Column(String(255))
    price = Column(Integer)

    def __init__(self, ingredient_name, price):
        self.ingredient_name = ingredient_name
        self.price = price


class Order(base):

    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key = True)
    order_time = Column(TIMESTAMP)
    pizzas = relationship('Pizza', secondary = order_pizzas)
    customer_id = Column(Integer, ForeignKey('customers.id'))

class Customer(base):

    __tablename__ = 'customers'

    name = Column(String(255))
    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship('Address')

    
base.metadata.create_all(engine)