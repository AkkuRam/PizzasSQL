from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://root:123@localhost:3306/pizza_service", echo = True)
base = declarative_base()
connection = engine.connect()


class Pizzas(base):

    __tablename__ = 'Pizzas'

    pizza_id = Column(Integer, primary_key=True)
    pizza_name = Column(String(255))
    price = Column(Integer)

    
class Ingredients(base):

    __tablename__ = 'Ingredients'

    ingredient_id = Column(Integer, primary_key=True)
    ingredient_name = Column(String(255))
    price = Column(Integer)



base.metadata.create_all(engine)