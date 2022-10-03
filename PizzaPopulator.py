from ClassCreator import Pizza

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://root:****l@localhost/PizzaSQL", echo = True)
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()


pizza1 = Pizza(pizza_name="Margherita", price = 6)
pizza2 = Pizza(pizza_name="Salami", price = 8)
pizza3 = Pizza(pizza_name="Tonno", price = 8)
pizza4 = Pizza(pizza_name="Vegetaria", price = 6)

session.add_all([pizza1, pizza2, pizza3, pizza4])
session.commit()