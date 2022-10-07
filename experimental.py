from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ClassCreator import Pizza, Ingredient

engine = create_engine("mysql://root:123sql@localhost/PizzaSQL", echo = False)
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

pizzas = session.query(Pizza).all()

print('\nAll Pizzas: ')
for pizza in pizzas:
    print(f'Pizza is called {pizza.pizza_name}. The ingredients are: ')
    ingredients = pizza.ingredients
    for ingredient in ingredients:
        print(ingredient.ingredient_name)
print('')

session.close()