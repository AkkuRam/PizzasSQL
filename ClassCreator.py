from audioop import add
import datetime
from inspect import CO_ASYNC_GENERATOR
from sqlalchemy import TIMESTAMP, PrimaryKeyConstraint, create_engine
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, Float, DateTime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

engine = create_engine("mysql://root:123@localhost/pizzaSQL")
base = declarative_base()
connection = engine.connect()

pizza_ingredients = Table(
    'pizza_ingredients', base.metadata,
    Column('pizza_id', Integer, ForeignKey('pizzas.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
)

# order_pizzas = Table(
#     'order_pizzas', base.metadata,
#     Column('order_id', Integer, ForeignKey('orders.id')),
#     Column('pizza_id', Integer, ForeignKey('pizzas.id'))
# )

# order_drinks = Table(
#     'order_drinks', base.metadata,
#     Column('order_id', Integer, ForeignKey('orders.id')),
#     Column('drink_id', Integer, ForeignKey('drinks.id'))
# )

# order_deserts = Table(
#     'order_deserts', base.metadata,
#     Column('order_id', Integer, ForeignKey('orders.id')),
#     Column('desert_id', Integer, ForeignKey('deserts.id'))
# )


class Pizza(base):

    __tablename__ = 'pizzas'

    id = Column(Integer, primary_key = True)
    pizza_name = Column(String(255))
    ingredients = relationship('Ingredient', secondary = pizza_ingredients)

    def __init__(self, pizza_name):
        self.pizza_name = pizza_name

class Drink(base):
    __tablename__ = 'drinks'
    id = Column(Integer, primary_key = True)
    drink_name = Column(String(255))
    drink_amount = Column(Float)
    drink_price = Column(Float)

    def __init__(self, drink_name, drink_amount, drink_price):
        self.drink_name = drink_name
        self.drink_amount = drink_amount
        self.drink_price = drink_price

class Desert(base):
    __tablename__ = 'deserts'
    id = Column(Integer, primary_key = True)
    desert_name = Column(String(255))
    desert_price = Column(Float)

    def __init__(self, desert_name, desert_price):
        self.desert_name = desert_name
        self.desert_price = desert_price
  
 
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
    # pizzas = relationship('Pizza', secondary = order_pizzas)
    # drinks = relationship('Drink', secondary = order_drinks)
    # deserts = relationship('Desert', secondary = order_deserts)
    pizzaAmounts = relationship('OrderPizzaAmount', cascade = "all, delete")
    desertAmounts = relationship('OrderDesertAmount', cascade = "all, delete")
    drinkAmounts = relationship('OrderDrinkAmount', cascade = "all, delete")
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

class OrderPizzaAmount(base):
    __tablename__ = 'orderpizzaamount'
    id = Column(Integer, primary_key = True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    pizza_id = Column(Integer)
    pizza_amount = Column(Integer)
    

    def __init__(self, order_id, pizza_id, pizza_amount):
        self.order_id = order_id
        self.pizza_id = pizza_id
        self.pizza_amount = pizza_amount

class OrderDesertAmount(base):
    __tablename__ = 'orderdesertamount'
    id = Column(Integer, primary_key = True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    desert_id = Column(Integer)
    desert_amount = Column(Integer)
    

    def __init__(self, order_id, desert_id, desert_amount):
        self.order_id = order_id
        self.desert_id = desert_id
        self.desert_amount = desert_amount


class OrderDrinkAmount(base):
    __tablename__ = 'orderdrinkamount'
    id = Column(Integer, primary_key = True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    drink_id = Column(Integer)
    drink_amount = Column(Integer)
    

    def __init__(self, order_id, drink_id, drink_amount):
        self.order_id = order_id
        self.drink_id = drink_id
        self.drink_amount = drink_amount

    
# base.metadata.create_all(engine)