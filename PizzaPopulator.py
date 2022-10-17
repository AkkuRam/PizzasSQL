from ClassCreator import  Employee, Ingredient, Pizza, Desert, Drink

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ClassCreator import engine, connection

Session = sessionmaker(bind=engine)
session = Session()

# create ingredients
salami = Ingredient('Salami', 1, False)
tuna = Ingredient('Tuna', 1, False)
ham = Ingredient('Ham', 1, False)
prawns = Ingredient('Prawns', 2, False)
fish = Ingredient('Fish', 2, False)
onion = Ingredient('Onion', 0.5, True)
olive = Ingredient('Olive', 1, True)
champignon = Ingredient('Champignon', 0.5, True)
peperoni = Ingredient('Peperoni', 0.5, True)
pineapple = Ingredient('Pineapple', 0.5, True)
anchovy = Ingredient('Anchovy', 1.5, False)



#create pizzas
pizzaSalami = Pizza('Pizza Salami')
pizzaTonno = Pizza('Pizza Tonno')
pizzaMargherita = Pizza('Pizza Margherita')
pizzaHawaii = Pizza('Pizza Hawaii')
pizzaFunghi = Pizza('Pizza Funghi')
pizzaDiavolo = Pizza('Pizza Diavolo')
pizzaFruttiDiMare = Pizza('Pizza Frutti Di Mare')
pizzaNapoletana = Pizza('Pizza Napoletana')
pizzaTaormina = Pizza('Pizza Taormina')
pizzaArmageddon = Pizza('Pizza Armageddon')



pizzaSalami.ingredients = [salami]
pizzaTonno.ingredients = [tuna, onion]
pizzaHawaii.ingredients = [ham, pineapple]
pizzaFunghi.ingredients = [champignon]
pizzaDiavolo.ingredients = [salami, peperoni]
pizzaFruttiDiMare.ingredients = [fish, prawns]
pizzaNapoletana.ingredients = [anchovy, olive]
pizzaTaormina.ingredients = [ham, champignon]
pizzaArmageddon.ingredients = [salami, tuna, ham, prawns, fish, onion]


# create Deserts
tiramisu = Desert('Tiramisu', 4.5)
panacotta = Desert('Panacotta', 4)


# create drinks

water = Drink('Water', 0.5, 1)
sparklingWater = Drink('Sparkling Water', 0.5, 1.5)
spriteSmall = Drink('Spriter', 0.2, 2)
spriteLarge = Drink('Sprite', 0.5, 4)
cokeSmall = Drink('Coke', 0.2, 2)
cokeLarge = Drink('Coke', 0.5, 4)

# create Employees
marc = Employee('Marc', 'Tuscolo', '6228LD')
lisa = Employee('Lisa', 'Smith', '6228LC')
tom = Employee('Tom', 'Mueller', '6228LC')
ella = Employee('Ella', 'Van Gracht', '6228LD')

# session.add_all([salami, tuna, onion, olive, ham, prawns, fish, champignon, peperoni, pineapple, anchovy, pizzaSalami, pizzaTonno, pizzaMargherita, pizzaHawaii, pizzaFunghi, pizzaDiavolo, pizzaFruttiDiMare, pizzaNapoletana, pizzaTaormina, pizzaArmageddon,tiramisu, panacotta, water, sparklingWater, cokeSmall, cokeLarge, spriteSmall, spriteLarge, tom, ella, marc, lisa])
# session.commit()
session.close()
