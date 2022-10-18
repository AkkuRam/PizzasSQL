# Setting up Schema in Workbench
1. Make a new schema in workbench and name your database

2. Then the next step, would be to specify these changes in the engine, where you define your localhost

3. For the following changes below mentioned with the engine, you will have to do this in the (ClassCreator.py)

4. Below the two things to modify would be the password and schema used, which is shown in **'*'**

`engine = create_engine("mysql://root:***@localhost********"`

5. This is how it would look for our example:

`engine = create_engine("mysql://root:123@localhost/pizzaSQL")`

---

# Creating tables into your workbench Schema (ClassCreator.py)

1. As you can see in (ClassCreator.py), all the following tables are made and ready for execution

2. At the bottom of the class in (ClassCreator.py), you will have to uncomment the following statement and execute it:

`base.metadata.create_all(engine)`

3. After this execution, you can refresh your schema in workbench and you should see the all the tables created

---

# Inserting in data into your tables in workbench (PizzaPopulator.py)

1. All the following data to be inserted is defined in the class (PizzaPopulator.py) for drinks, deserts, pizzas, ingredients and employees

2. To insert this data into workbench, you must uncomment the these statements found at the bottom of the class (PizzaPopulator.py) and execute them:

`session.add_all([salami, tuna, onion, olive, ham, prawns, fish, champignon, peperoni, pineapple, anchovy, pizzaSalami, pizzaTonno, pizzaMargherita, pizzaHawaii, pizzaFunghi, pizzaDiavolo, pizzaFruttiDiMare, pizzaNapoletana, pizzaTaormina, pizzaArmageddon,tiramisu, panacotta, water, sparklingWater, cokeSmall, cokeLarge, spriteSmall, spriteLarge, tom, ella, marc, lisa])`  
`session.commit()`

3. Now, refresh your schema in workbench you should be able to view the contents of the database with some querying commands

4. Example:

`SELECT * FROM Pizzas`  
`SELECT * FROM Employees`

---
# Running the Pizza Service (TerminalApp.py)

1. Now, after all these following steps, you can run the executable file: TerminalApp.py. Enjoy testing out our ordering service for Pizzas!
