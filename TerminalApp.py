import sqlalchemy
from datetime import timedelta, datetime
from sqlalchemy import delete
import random, string
from tracemalloc import start
from ClassCreator import Address, Customer, Employee, Pizza, Ingredient, Order
from PizzaPopulator import session
class TerminalApp:
    
    def __init__(self):
        self.pizzaMenu = session.query(Pizza).all()
    
    def start(self):
        self.currentCustomer = None
        while self.currentCustomer is None:
            print('Welcome to our pizza service! Have you ordered with us before?')
            choice = 0
            while choice < 1 or choice > 2:
                print('1 - Yes\n2 - No')
                choice = int(input())
            if choice == 1:
                customerID = -1
                customer = None
                while customer is None:
                    print('Hello again, please enter your customer ID:')
                    customerID = int(input())
                    customer = session.query(Customer).get(customerID)
                self.currentCustomer = customer
            elif choice == 2:
                self.newCustomer()
        
        self.orderMenu()


    def orderMenu(self):
        print('How would you like to proceed?')
        choice = 0
        while choice < 1 or choice > 2:
            print('1 - Make a new Order')
            print('2 - View current Order')
            choice = int(input())
        if choice == 1:
            self.makeOrder()
        else:
            self.viewOrder()


    # Register a new customer and add him to the databasae
    def newCustomer(self):
        print("Please register as a customer")
        print('First name:')
        firstName = input()
        print('Last name:')
        lastName = input()
        print('Street:')
        street = input()
        print('Housenumber:')
        housenumber = input()
        print('Zipcode:')
        zipcode = input()
        print('City:')
        city = input()
        if(session.query(Employee).filter(Employee.zipcode == zipcode).count() == 0):
            print('We currently do not deliver to your Area, sorry!')
            return
        
        address =  session.query(Address).filter(Address.street == street, Address.housenumber == housenumber, Address.zipcode == zipcode, Address.city == city).first()
        if address is None:
            print('address not previously stored')
            address = Address(street, housenumber, zipcode, city)
        

        self.currentCustomer = Customer(firstName, lastName)
        self.currentCustomer.address = address
        session.add_all([self.currentCustomer, address])
        session.commit()


    # Make a new Order and add it to the database
    def makeOrder(self):
        deliveryGuy = self.driversAvailable()
        if deliveryGuy is None:
            print('There are currently no employees availabe to deliver to your are. Sorry!')
            return
        pizzaList = []
        self.printMenu()
        pizzaN = 0
        print("Please enter the amount of pizzas you would like to order. Please order at least one pizza.")
        while pizzaN < 1:
            pizzaN = int(input())
        for i in range(pizzaN):
            pizzaId = -1
            pizza = None
            print('Enter the number of the pizza you want to add to your Order')
            while pizza is None:
                pizzaID = int(input())
                pizza = self.getPizza(pizzaID)
            pizzaList.append(pizza)
        order = Order(self.currentCustomer.id, deliveryGuy)
        order.pizzas = pizzaList
        order.price = self.orderPrice(order)
        print(f'The Price of your order will be {order.price}€')
        self.currentCustomer.pizzaCounter += len(pizzaList)
        if self.currentCustomer.discountCode is None and self.currentCustomer.pizzaCounter > 10:
            self.currentCustomer.discountCode = self.generateDiscountCode
            print('Congratulations! You have ordered more than 10 Pizzas with us! To celebrate you have been gifted a Discount Code.')
            print(f'Your Discount Code: {self.currentCustomer.discountCode}')
        if(self.currentCustomer.discountCode is not None and self.currentCustomer.discountCodeUsed is False):
            print('Do you want to enter your dicount code for 10 percent off?')
            print('1 - Yes')
            print('2 - No')
            choice = 0
            while choice > 2 or choice < 1:
                choice = int(input())
            if(choice == 1):
                validCode = False
                while not validCode:
                    print('Please enter your discount code')
                    discountCode = input()
                    if(discountCode == self.currentCustomer.discountCode):
                        validCode = True
                        order.price *= 0.9
                        self.currentCustomer.discountCodeUsed = True
                    else:
                        print('You have entered the wrong code. Try again!')
                
        session.add_all([order, self.currentCustomer, deliveryGuy])
        session.commit()
        print('Your order is now completed!')
        self.printOrder(order)


    # Check whether there currently is a driver available in the area of the customer
    def driversAvailable(self):
        drivers = session.query(Employee).all()
        for driver in drivers:
            if driver.zipcode == self.currentCustomer.address.zipcode:
                if driver.order is None:
                    return driver
                td = datetime.now() - driver.order.order_time
                if td.seconds > 2400:
                    return driver
        return None


    # Giving the customer options to view his order and cancel if it's still early enough
    def viewOrder(self):
        orderId = -1
        order = None
        while order is None:
            print('Please enter your order Id')
            orderId = int(input())
            order = self.getOrder(orderId)
        self.printOrder(order)
        td = datetime.now() - order.order_time
        if td.seconds < 300:
            print('Your order is younger than 5 minutes. Do you wish to cancel your order?')
            choice = 0
            while choice < 1 or choice > 2:
                print('1 - Yes')
                print('2 - No')
                choice = int(input())
            if choice == 2:
                session.execute(delete(Order).where(Order.id == orderId))


    def getOrder(self, orderId):
        for order in self.currentCustomer.orders:
            if order.id == orderId:
                return order
        return None


    def printOrder(self, order):
        print(f'You ordered {len(order.pizzas)} pizzas:')
        for pizza in order.pizzas:
            print(f'- {pizza.pizza_name} {self.pizzaPrice(pizza)}€')
        print(f'Total price: {order.price}')
        print(f'You ordered at: {order.order_time}')
        td = datetime.now() - order.order_time
        if td.seconds < 600:
            print('Your pizza is currently being prepared and will be out for delivery shortly.')
            print(f'It will be out for delivery in approximately {10-int(td.seconds/60)} minutes and delivered at around {order.order_time+timedelta(minutes=40)}')
        if td.seconds > 600 and td.seconds < 2400:
            print(f'Your order is out for delivery. Arrival at approxiamtely {order.order_time+timedelta(minutes=40)}')
        if td.seconds > 2400:
            print(f'Your order has been delivered at {order.order_time + timedelta(minutes=40)}')



    def printMenu(self):
        for pizza in self.pizzaMenu:
            print()
            print(f'{pizza.id}: {pizza.pizza_name}')
            print('Ingredients:')
            for ingredient in pizza.ingredients:
                print(f'{ingredient.ingredient_name}')
            veggieStatus = 'vegetarian' if self.pizzaIsVeggie(pizza) else 'not vegetarian'
            print(f'The pizza is {veggieStatus}')
            print(f'Pizza price: {self.pizzaPrice(pizza)}')


    def getPizza(self, id):
        for pizza in self.pizzaMenu:
            if pizza.id == id:
                return pizza
        return None

    def getOrder(self, orderId):
        for order in self.currentCustomer.orders:
            if order.id == orderId:
                return order
        return None
            
    def pizzaIsVeggie(self, pizza):
        for ingredient in pizza.ingredients:
            if ingredient.vegetarian == False:
                return False
        return True

    def pizzaPrice(self, pizza):
        basePrice = 4
        for ingredient in pizza.ingredients:
            basePrice += ingredient.price
        return basePrice * 1.526

    def orderPrice(self, order):
        price = 0
        for pizza in order.pizzas:
            price += self.pizzaPrice(pizza)
        return price

    def generateDiscountCode(self, length):
        letters = string.ascii_letters
        discountCode = ''.join(random.choice(letters) for i in range(length))
        return discountCode

                

app = TerminalApp()   
app.start()