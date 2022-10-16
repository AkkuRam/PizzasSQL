from audioop import add
import datetime
from inspect import CO_ASYNC_GENERATOR
from sqlalchemy import TIMESTAMP, create_engine
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, Float, DateTime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

engine = create_engine("mysql://root:123sql@localhost/pizzaSQL")
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
    price = Column(Float)
    vegetarian = Column(Boolean)

    def __init__(self, ingredient_name, price, vegetarian):
        self.ingredient_name = ingredient_name
        self.price = price
        self.vegetarian = vegetarian


class Order(base):

    __tablename__ = 'orders'

    id = Column(Integer, primary_key = True)
    order_time = Column(DateTime, default = sqlalchemy.func.now())
    price = Column(Float)
    pizzas = relationship('Pizza', secondary = order_pizzas)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee", backref=backref("order", uselist = False))
    
    def __init__(self, customer_id, employee):
        self.customer_id = customer_id
        self.employee = employee

class Customer(base):

    __tablename__ = 'customers'
    id = Column(Integer, primary_key = True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship('Address')
    discountCode = Column(String(255))
    discountCodeUsed = Column(Boolean)
    pizzaCounter = Column(Integer)
    orders = relationship("Order")

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.discountCode = None
        self.discountCodeUsed = False
        self.pizzaCounter = 0

class Address(base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key = True)
    street = Column(String(255))
    housenumber = Column(String(255))
    zipcode = Column(String(255))
    city = Column(String(255))

    def __init__(self, street, housenumber, zipcode, city):
        self.street = street
        self.housenumber = housenumber
        self.zipcode = zipcode
        self.city = city

class Employee(base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key = True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    zipcode = Column(String(255))

    def __init__(self, first_name, last_name, zipcode):
        self.first_name = first_name
        self.last_name = last_name
        self.zipcode = zipcode

    
# base.metadata.create_all(engine)