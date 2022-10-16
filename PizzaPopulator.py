from ClassCreator import Employee, Ingredient, Pizza

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ClassCreator import engine, connection

Session = sessionmaker(bind=engine)
session = Session()

# create ingredients
salami = Ingredient('Salami', 1, False)
tuna = Ingredient('Tuna', 1, False)
onion = Ingredient('Onion', 0.5, True)
olive = Ingredient('Olive', 1, True)

#create pizzas
pizzaSalami = Pizza('Pizza Salami')
pizzaTonno = Pizza('Pizza Tonno')
pizzaMargherita = Pizza('Pizza Margherita')

pizzaSalami.ingredients = [salami]
pizzaTonno.ingredients = [tuna, onion]


# create Employees

marc = Employee('Marc', 'Tuscolo', '6228LD')
lisa = Employee('Lisa', 'Smith', '6228LC')


# session.add_all([salami, tuna, onion, olive, pizzaSalami, pizzaTonno, pizzaMargherita, marc, lisa])
# session.commit()
session.close()
