# PizzasSQL
1. Make a new schema in workbench and name your database

2. Then the next step, would be to specify these changes in the engine, where you define your localhost

3. Below the two things to modify would be the password and schema used, which is shown in **'*'**

`engine = create_engine("mysql://root:\*\*\*@\localhost/\*\*\*\*\*\*\*\*"`

4. This is how it would look for our example:

engine = create_engine("mysql://root:123@localhost/pizzaSQL")

5. Then you can run the executable file: TerminalApp.py

---
