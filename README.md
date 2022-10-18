# PizzasSQL

1. Run the app using the TerminalApp.py

2. Make a new schema in workbench and name your database

3. Then the next step, would be to specify these changes in the engine, where you define your localhost

Below the two things to modify would be the password and schema used, which is shown in '*'

engine = create_engine("mysql://root:\*\*\*@\localhost/\*\*\*\*\*\*\*\*")

4. This is how it would look for our example:

engine = create_engine("mysql://root:123@localhost/pizzaSQL")
