from ClassCreator import Ingredient, Pizza

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ClassCreator import engine, connection

Session = sessionmaker(bind=engine)
session = Session()

# create ingredients
salami = Ingredient('Salami', 1)
tuna = Ingredient('Tuna', 1)
onion = Ingredient('Onion', 0.5)
olive = Ingredient('Olive', 1)

#create pizzas
pizzaSalami = Pizza('Pizza Salami')
pizzaTonno = Pizza('Pizza Tonno')
pizzaMargherita = Pizza('Pizza Margherita')

pizzaSalami.ingredients = [salami]
pizzaTonno.ingredients = [tuna, onion]

session.add_all([salami, tuna, onion, olive, pizzaSalami, pizzaTonno, pizzaMargherita])
session.commit()
session.close()
