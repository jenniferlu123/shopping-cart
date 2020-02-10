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


# FURTHER CHALLENGE: integrating with a Google Sheets datastore
# Code source: online notes on gspread package 
# Also consulted Ahmad Wilson on some set-up questions. 
# https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/gspread.md

import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
SHEET_NAME = os.environ.get("SHEET_NAME", "products")

# AUTHORIZATION

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "auth", "spreadsheet_credentials.json")

AUTH_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)

# READ SHEET VALUES

client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>

doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>

sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>

rows = sheet.get_all_records() #> <class 'list'>
products = [r for r in rows]



## FUTHER CHALLENGE: reading from CSV FILE
#
#csv_filepath = os.path.join(os.path.dirname(__file__), "products.csv")
#products_csv = pandas.read_csv(csv_filepath) # products is a data frame
#
#Convert dataframe to list of dictionaries
#products = products_csv.to_dict("records") 


# Create lists to store cashier inputs:

id_list = []
for p in products:
    id_list.append(str(p["id"]))

def id_pound(p):
    return p["price_per"] == "pound"

id_pound_list = []
for pound_id in list(filter(id_pound,products)):
    id_pound_list.append(str(pound_id["id"]))

selected_items = []
selected_pounds = []

# WHILE LOOP used for cashier to enter product identifiers (ids):
while True:
    cashier_input = input("Please input a product identifier: ")
    if cashier_input == "DONE":
        customer_email_address = input("Please enter your email address to receive a copy of your receipt. Otherwise enter NO: ")
        break
    elif cashier_input not in id_list:
        print ("Sorry, item not found. Please try again...")
    elif cashier_input in id_pound_list:
        pounds_input = input("Please input how many pounds rounded to the nearest integer: ")
        if pounds_input.isnumeric():
            selected_pounds.append({"id":cashier_input, "pounds":pounds_input})
        else:       
            print ("Please try again and enter a valid number.")
    else:
        selected_items.append(cashier_input)


# Print grocery store information (shown on receipt header):

print("-----------------------------------------------------")
print("GU Healthy Foods")
print("3700 O ST NW Washington DC")
print("Phone: (202)-495-3439")
print("Website: www.guhealthyfoods.com")
print("-----------------------------------------------------")

purchase_time = datetime.datetime.now()
print("Checkout at: " + purchase_time.strftime("%Y-%m-%d %I:%M %p"))
print("-----------------------------------------------------")


# Print list of items purchased:

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

# Print subtotal:

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

# Print total purchase price:

total_amount = total_price + tax
total_amount_usd = "${0:.2f}".format(total_amount)
print("Total: " + str(total_amount_usd))

# Print thank you message:

print("-----------------------------------------------------")
print("Thanks for shopping with us!")
print("Hope to see you again soon.")
print("-----------------------------------------------------")


# FURTHER CHALLENGE: writing receipts to file
# Code source for this challenge: Online notes on python file management:
# Consulted Ahmad Wilson in creating a variable to store the receipt message
# https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/file-management.md

# Variable "receipt_message" is created to store the entire message to be shown on the receipt 

receipt_message = "-----------------------------------------------------"
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "GU Healthy Foods"
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "3700 O ST NW Washington DC"
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "Phone: (202)-495-3439"
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "Website: www.guhealthyfoods.com"
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "-----------------------------------------------------"
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "Checkout at: " + purchase_time.strftime("%Y-%m-%d %I:%M %p")
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "-----------------------------------------------------"
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "Selected products: "
receipt_message = receipt_message + "\n"
for cashier_input in selected_items:
    matching_products = [p for p in products if str(p["id"]) == str(cashier_input)]
    matching_product = matching_products[0]
    total_price = total_price + matching_product["price"]
    price_usd = "${0:.2f}".format(matching_product["price"])
    receipt_message = receipt_message + "... " + matching_product["name"] + " (" + str(price_usd) + ")"
    receipt_message = receipt_message + "\n"
for d in selected_pounds:
    matching_products = [p for p in products if str(p["id"]) == str(d["id"])]
    matching_product = matching_products[0]
    total_pounds = matching_product["price"]*(float(d["pounds"]))
    total_price = total_price + total_pounds
    price_pounds_usd = "${0:.2f}".format(total_pounds)
    receipt_message = receipt_message + "... " + matching_product["name"] + " (" + str(price_pounds_usd) + ")"
    receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "-----------------------------------------------------"
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "Subtotal: " + str(total_price_usd)
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "Tax: " + str(tax_usd)
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "Total: " + str(total_amount_usd)
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "-----------------------------------------------------"
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "Thanks for shopping with us!"
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "Hope to see you again soon."
receipt_message = receipt_message + "\n"
receipt_message = receipt_message + "-----------------------------------------------------"

# txt file automatically created containing receipt details:

file_name = "receipts//" + purchase_time.strftime("%Y-%m-%d-%H-%M-%S-%f") + ".txt"
with open(file_name, "w") as file:
    file.write(receipt_message)


# FURTHER CHALLENGE: sending receipts via email
# Code source for this challenge: Online notes on Sendgrid
# https://github.com/prof-rossetti/notification-service-py/blob/master/app/send_email.py 

import os
import pprint
    
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import * # source of Email, Content, Mail, etc.

if customer_email_address == "NO":
    pass
else:
    load_dotenv()

    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
    MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")

    # AUTHENTICATE

    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

    # PREPARE THE EMAIL

    from_email = Email(MY_EMAIL_ADDRESS)
    to_email = Email(customer_email_address) #asked for customer address during checkout process after "DONE"
    subject = "GU Healthy Foods Receipt"
    message_text = receipt_message
    content = Content("text/plain", message_text)
    mail = Mail(from_email, subject, to_email, content)

    # SEND EMAIL

    response = sg.client.mail.send.post(request_body=mail.get())
