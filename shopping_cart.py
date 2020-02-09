# shopping_cart.py

#from pprint mport pprint

#products = [
#    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50, "price_per": "item"},
#    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99, "price_per": "item"},
#    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49, "price_per": "item"},
#    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99, "price_per": "item"},
#    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99, "price_per": "item"},
#    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99, "price_per": "item"},
#    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50, "price_per": "item"},
#    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25, "price_per": "item"},
#    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50, "price_per": "item"},
#    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99, "price_per": "item"},
#    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99, "price_per": "item"},
#    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50, "price_per": "item"},
#    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00, "price_per": "item"},
#    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99, "price_per": "item"},
#    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50, "price_per": "item"},
#    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50, "price_per": "item"},
#    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99, "price_per": "item"},
#    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50, "price_per": "item"},
#    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99, "price_per": "item"},
#    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25, "price_per": "item"},
#    {"id":21, "name": "Organic Bananas", "department": "fruit", "aisle": "fruit", "price": 0.79, "price_per": "pound"}
#] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017


import datetime
from dotenv import load_dotenv
import os

import pandas
import statistics

#READ CSV FILE
csv_filepath = os.path.join(os.path.dirname(__file__), "products.csv")
products_csv = pandas.read_csv(csv_filepath) # products is a data frame

#CONVERT DATAFRAME TO LIST OF DICTIONARIES
products = products_csv.to_dict("records") 
#print(sales_report)
#print(type(sales_report[0]))

id_list = []
for p in products:
    id_list.append(str(p["id"]))

#id_list_pound = []
#for p in products:
#    id_list.append
def id_pound(p):
    return p["price_per"] == "pound"

id_pound_list = []
for pound_id in list(filter(id_pound,products)):
    id_pound_list.append(str(pound_id["id"]))
#print(id_pound_list)

selected_items = []
selected_pounds = []

while True:
    cashier_input = input("Please input a product identifier: ")
    if cashier_input == "DONE":
        break
    elif cashier_input not in id_list:
        print ("Sorry, item not found. Please try again...")
    elif cashier_input in id_pound_list:
        pounds_input = input("Please input how many pounds: ")        
        selected_pounds.append({"id":cashier_input, "pounds":pounds_input})
    else:
        selected_items.append(cashier_input)

print("-----------------------------------------------------")
print("GU Healthy Foods")
print("3700 O ST NW Washington DC")
print("Phone: (202)-495-3439")
print("Website: www.guhealthyfoods.com")
print("-----------------------------------------------------")

purchase_time = datetime.datetime.now()
print("Checkout at: " + purchase_time.strftime("%Y-%m-%d %I:%M %p"))
print("-----------------------------------------------------")


print("Selected products: ")

total_price = 0
total_price_pounds = 0

for cashier_input in selected_items: 
    matching_products = [p for p in products if str(p["id"]) == str(cashier_input)]
    matching_product = matching_products[0]
    total_price = total_price + matching_product["price"]
    price_usd = "${0:.2f}".format(matching_product["price"])
    print("... " + matching_product["name"] + " (" + str(price_usd) + ")")

for d in selected_pounds:
    matching_products = [p for p in products if str(p["id"]) == str(d["id"])]
    matching_product = matching_products[0]
    total_pounds = matching_product["price"]*(float(d["pounds"]))
    total_price = total_price + total_pounds
    price_pounds_usd = "${0:.2f}".format(total_pounds)
    print("... " + matching_product["name"] + " (" + str(price_pounds_usd) + ")")


print("-----------------------------------------------------")
total_price_usd = "${0:.2f}".format(total_price)
print("Subtotal: " + str(total_price_usd))

#FURTHER CHALLENGE: configuring sales tax rate
#Code source for this challenge: Online notes on dotenv package:
#https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/dotenv.md

load_dotenv() 

tax_rate_input = float(os.environ.get("tax_rate"))
tax = total_price*(tax_rate_input)
tax_usd = "${0:.2f}".format(tax)
print("Tax: " + str(tax_usd))

total_amount = total_price + tax
total_amount_usd = "${0:.2f}".format(total_amount)
print("Total: " + str(total_amount_usd))

print("-----------------------------------------------------")
print("Thanks for shopping with us!")
print("Hope to see you again soon.")
print("-----------------------------------------------------")


#FURTHER CHALLENGE: writing receipts to file
#Code source for this challenge: Online notes on python file management:
#https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/file-management.md

file_name = "receipts//" + purchase_time.strftime("%Y-%m-%d-%H-%M-%S-%f") + ".txt"

with open(file_name, "w") as file: 
    file.write("-----------------------------------------------------")
    file.write("GU Healthy Foods")
    file.write("\n")
    file.write("3700 O ST NW Washington DC")
    file.write("\n")
    file.write("Phone: (202)-495-3439")
    file.write("\n")
    file.write("Website: www.guhealthyfoods.com")
    file.write("\n")
    file.write("-----------------------------------------------------")
    file.write("\n")
    file.write("Checkout at: " + purchase_time.strftime("%Y-%m-%d %I:%M %p"))
    file.write("\n")
    file.write("-----------------------------------------------------")
    file.write("\n")
    file.write("Selected products: ")
    file.write("\n")
    for cashier_input in selected_items:
        matching_products = [p for p in products if str(p["id"]) == str(cashier_input)]
        matching_product = matching_products[0]
        total_price = total_price + matching_product["price"]
        price_usd = "${0:.2f}".format(matching_product["price"])
        file.write("... " + matching_product["name"] + " (" + str(price_usd) + ")")
        file.write("\n")
    for d in selected_pounds:
        matching_products = [p for p in products if str(p["id"]) == str(d["id"])]
        matching_product = matching_products[0]
        total_pounds = matching_product["price"]*(float(d["pounds"]))
        total_price = total_price + total_pounds
        price_pounds_usd = "${0:.2f}".format(total_pounds)
        file.write("... " + matching_product["name"] + " (" + str(price_pounds_usd) + ")")
        file.write("\n")
    file.write("-----------------------------------------------------")
    file.write("\n")
    file.write("Subtotal: " + str(total_price_usd))
    file.write("\n")
    file.write("Tax: " + str(tax_usd))
    file.write("\n")
    file.write("Total: " + str(total_amount_usd))
    file.write("\n")
    file.write("-----------------------------------------------------")
    file.write("\n")
    file.write("Thanks for shopping with us!")
    file.write("\n")
    file.write("Hope to see you again soon.")
    file.write("\n")
    file.write("-----------------------------------------------------")

    
    

#FURTHER CHALLENGE: sending receipts via email
#Code source for this challenge: Online notes on Sendgrid
# https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/packages/sendgrid.md

#import os
#from dotenv import load_dotenv
#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail
#
#load_dotenv()
#
#SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
#SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
#MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")
#
##print("API KEY:", SENDGRID_API_KEY)
##print("TEMPLATE ID:", SENDGRID_TEMPLATE_ID)
##print("EMAIL ADDRESS:", MY_ADDRESS)
#
#template_data = {
#    "total_price_usd": total_amount_usd,
#    "human_friendly_timestamp": purchase_time.strftime("%Y-%m-%d %I:%M %p") ,
#    "products":[
#        {"id":1, "name": "Product 1"},
#        {"id":2, "name": "Product 2"},
#        {"id":3, "name": "Product 3"},
#        {"id":2, "name": "Product 2"},
#        {"id":1, "name": "Product 1"}
#    ]
#} # or construct this dictionary dynamically based on the results of some other process :-D
#
#client = SendGridAPIClient(SENDGRID_API_KEY)
#print("CLIENT:", type(client))
#
#message = Mail(from_email=MY_ADDRESS, to_email=MY_ADDRESS)
#print("MESSAGE:", type(message))
#
#message.template_id = SENDGRID_TEMPLATE_ID
#
#message.dynamic_template_data = template_data
#
#try:
#    response = client.send(message)
#    print("RESPONSE:", type(response))
#    print(response.status_code)
#    print(response.body)
#    print(response.headers)
#
#except Exception as e:
#    print("OOPS", e)