import sqlalchemy
from datetime import timedelta, datetime
from sqlalchemy import delete
import random, string
from tracemalloc import start
from ClassCreator import Address, Customer, Employee, OrderDesertAmount, OrderDrinkAmount, OrderPizzaAmount, Pizza, Ingredient, Order, Desert, Drink
from PizzaPopulator import session
class TerminalApp:
    
    def __init__(self):
        self.pizzaMenu = session.query(Pizza).all()
        self.desertMenu = session.query(Desert).all()
        self.drinkMenu = session.query(Drink).all()
    
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
            address = Address(street, housenumber, zipcode, city)
        

        self.currentCustomer = Customer(firstName, lastName)
        self.currentCustomer.address = address
        session.add_all([self.currentCustomer, address])
        session.commit()
        print(f'Your customer ID is {self.currentCustomer.id}. Please remember this number!')


    # Make a new Order and add it to the database
    def makeOrder(self):
        deliveryGuy = self.driversAvailable()
        if deliveryGuy is None:
            print('There are currently no employees availabe to deliver to your area. Sorry!')
            return
        order = Order(self.currentCustomer.id, deliveryGuy)
        # pizzaList = []
        # desertList = []
        # drinkList = []
        self.printMenu()
        n = 0
        pizzaAmount = 0
        print('How many different kinds of Pizza would you like to order?')
        while n < 1:
            n = int(input())
        for i in range(n):
            pizzaN = 0
            print("Please enter the id of the pizza you would like to order")
            while pizzaN < 1 or pizzaN > 10:
                pizzaN = int(input())
            print('Please enter the amount you would like to order of this pizza: ')
            pizzaAmount = int(input())
            session.add(OrderPizzaAmount(order.id, pizzaN, pizzaAmount))
        
        n = -1
        print('How many different kinds of desert would you like to order?')
        while n < 0:
            n = int(input())
        for i in range(n):
            desertN = 0
            print("Please enter the id of the desert you would like to order")
            while desertN < 1 or desertN > 2:
                desertN = int(input())
            print('Please enter the amount you would like to order of this desert: ')
            desertAmount = int(input())
            session.add(OrderDesertAmount(order.id, desertN, desertAmount))

        n = -1
        print('How many different kinds of drinks would you like to order?')
        while n < 0:
            n = int(input())
        for i in range(n):
            drinkN = 0
            print("Please enter the id of the desert you would like to order")
            while drinkN < 1 or drinkN > 2:
                drinkN = int(input())
            print('Please enter the amount you would like to order of this desert: ')
            drinkAmount = int(input())
            session.add(OrderDrinkAmount(order.id, drinkN, drinkAmount))

        # order.pizzas = pizzaList
        # order.deserts = desertList
        # order.drinks = drinkList
        print(f'The Price of your order will be {self.orderPrice(order)}€')
        self.currentCustomer.pizzaCounter += pizzaAmount
        if self.currentCustomer.discountCode is None and self.currentCustomer.pizzaCounter > 10:
            self.currentCustomer.discountCode = self.generateDiscountCode()
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


    # Giving the customer options to view his order and cancel if it's still early enough
    def viewOrder(self):
        orderID = -1
        order = None
        while order is None:
            print('Please enter your order Id')
            orderID = int(input())
            order = self.getOrder(orderID)
        self.printOrder(order)
        td = datetime.now() - order.order_time
        if td.seconds < 300:
            print('Your order is younger than 5 minutes. Do you wish to cancel your order?')
            choice = 0
            while choice < 1 or choice > 2:
                print('1 - Yes')
                print('2 - No')
                choice = int(input())
            if choice == 1:
                session.delete(order)
                session.commit()


    def getOrder(self, orderID):
        for order in self.currentCustomer.orders:
            if order.id == orderID:
                return order
        return None


    def printOrder(self, order):
        print('\n YOUR ORDER')
        print('-------------------------------')
        print(f'Your order id is {order.id}. Please remember this number!')
        pizzaAmounts = session.query(OrderPizzaAmount).filter(OrderPizzaAmount.order_id == order.id).all()
        pizzaN = 0
        for pizzaAmount in pizzaAmounts:
            pizzaN += pizzaAmount.pizza_amount
        print(f'You ordered {pizzaN} pizzas:')
        for pizzaAmount in pizzaAmounts:
            pizza = self.getPizza(pizzaAmount.pizza_id)
            print(f'- {pizzaAmount.pizza_amount}x {pizza.pizza_name} {self.pizzaPrice(pizza)*pizzaAmount.pizza_amount}€')
        print()

        desertAmounts = session.query(OrderDesertAmount).filter(OrderDesertAmount.order_id == order.id).all()
        desertN = 0
        for desertAmount in desertAmounts:
            desertN += desertAmount.desert_amount
        print(f'You ordered {desertN} deserts:')
        for desertAmount in desertAmounts:
            desert = self.getDesert(desertAmount.desert_id)
            print(f'- {desertAmount.pizza_amount}x {desert.desert_name} {desert.desert_price * desertAmount.desert_amount}€')
        print()

        drinkAmounts = session.query(OrderDrinkAmount).filter(OrderDrinkAmount.order_id == order.id).all()
        drinkN = 0
        for drinkAmount in drinkAmounts:
            drinkN += drinkAmount.drink_amount
        print(f'You ordered {drinkN} drinks:')
        for drinkAmount in drinkAmounts:
            drink = self.getDrink(drinkAmount.drink_id)
            print(f'- {drinkAmount.drink_amount}x {drink.drink_name} {drink.drink_price * drinkAmount.drink_amount}€')


        print(f'\nTotal price: {self.orderPrice(order)}€')
        print(f'You ordered at: {order.order_time}')
        td = datetime.now() - order.order_time
        if td.seconds < 600:
            print('Your order is currently being prepared and will be out for delivery shortly.')
            print(f'It will be out for delivery in approximately {10-int(td.seconds/60)} minutes and delivered at around {order.order_time+timedelta(minutes=40)}')
        if td.seconds > 600 and td.seconds < 2400:
            print(f'Your order is out for delivery. Arrival at approxiamtely {order.order_time+timedelta(minutes=40)}')
        if td.seconds > 2400:
            print(f'Your order has been delivered at {order.order_time + timedelta(minutes=40)}')



    def printMenu(self):
        print('PIZZAS')
        print('-------------------------------------------------')
        for pizza in self.pizzaMenu:
            print(f'\n{pizza.id}: {pizza.pizza_name}')
            print('Ingredients:')
            for ingredient in pizza.ingredients:
                print(f'- {ingredient.ingredient_name}')
            veggieStatus = 'vegetarian' if self.pizzaIsVeggie(pizza) else 'not vegetarian'
            print(f'The pizza is {veggieStatus}')
            print(f'Pizza price: {self.pizzaPrice(pizza)}€')
        print('\nDESERTS')
        print('-------------------------------------------------')
        for desert in self.desertMenu:
            print(f'\n {desert.id}: {desert.desert_name}')
            print(f'Desert price: {desert.desert_price}€')
        print('\nDRINKS')
        print('-------------------------------------------------')
        for drink in self.drinkMenu:
            print(f'\n{drink.id}: {drink.drink_name} {drink.drink_amount}l')
            print(f'Drink price: {drink.drink_price}')
        



    def getPizza(self, id):
        for pizza in self.pizzaMenu:
            if pizza.id == id:
                return pizza

    def getDesert(self, id):
        for desert in self.desertMenu:
            if desert.id == id:
                return desert

    def getDrink(self, id):
        for drink in self.drinkMenu:
            if drink.id == id:
                return drink

    def getOrder(self, orderId):
        for order in self.currentCustomer.orders:
            if order.id == orderId:
                return order
            
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
        pizzas = session.query(OrderPizzaAmount).filter(OrderPizzaAmount.order_id == order.id).all()
        for pizza in pizzas:
            price += self.pizzaPrice(self.getPizza(pizza.pizza_id)) * pizza.pizza_amount

        deserts = session.query(OrderDesertAmount).filter(OrderDesertAmount.order_id == order.id).all()
        for desert in deserts:
            price += self.getDesert(desert.desert_id).desert_price * desert.desert_amount

        drinks = session.query(OrderDrinkAmount).filter(OrderDrinkAmount.order_id == order.id).all()
        for drink in drinks:
            price += self.getDrink(drink.drink_id).drink_price * drink.drink_amount
        # for pizza in order.pizzas:
        #     price += self.pizzaPrice(pizza)
        # for desert in order.deserts:
        #     price += desert.desert_price
        # for drink in order.drinks:
        #     price += drink.drink_price
        return price

    def generateDiscountCode(self, length):
        letters = string.ascii_letters
        discountCode = ''.join(random.choice(letters) for i in range(length))
        return discountCode

                

app = TerminalApp()   
app.start()