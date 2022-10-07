from tracemalloc import start
from ClassCreator import Customer, Pizza, Ingredient
from PizzaPopulator import session
class TerminalApp:

    def __init__(self):
        self.pizzaMenu = session.query(Pizza).all()
    
    def start(self):
        print('Welcome to our pizza service! Have you ordered with us before?')
        choice = 999
        while choice < 1 or choice > 2:
            print('1 - Yes\n2 - No')
            choice = int(input())
        if choice == 1:
            print('Hello again, please enter your customer ID:')
            customerID = int(input())
            self.currentCustomer = session.query(Customer).get(customerID)
        elif choice == 2:
            print("Please register as a customer")
            print('First name:')
            firstName = input()
            print('Last name:')
            lastName = input()
            print('Address: ')
            address = input()
            self.currentCustomer = Customer(firstName, lastName, address)
            session.add(self.currentCustomer)
        
        self.orderMenu()
        
                        
    
    def orderMenu(self):
        print('How would you like to proceed?')
        choice = 999
        while choice < 1 or choice > 2:
            print('1 - Make a new Order\n2 - View your current Order')
            choice = int(input())
        if(choice == 1):
            self.makeOrder()
        
            

            
    def makeOrder(self):
        self.printMenu()
        print("Please enter the number of pizzas you would like to order")
        pizzaN = int(input())
        for i in range(pizzaN):
            print('Enter the number of the pizza you want to add to your Order')
            pizza = int(input())
       

    def printMenu(self):
        for pizza in self.pizzaMenu:
            print(f'{pizza.id}: {pizza.pizza_name}')
            print('Ingredients:')
            for ingredient in pizza.ingredients:
                print(f'{ingredient.ingredient_name}')
            print()
                

app = TerminalApp()   
app.start()