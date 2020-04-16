# shopping-cart/app/shopping_cart.py

import datetime
from dotenv import load_dotenv
import pandas
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import sendgrid
from sendgrid.helpers.mail import * 


load_dotenv()

# Google Sheets API Key
DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
SHEET_NAME = os.environ.get("SHEET_NAME", "products")

# Sendgrid API Key
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS")
MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS")


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    
    Param: my_price (int or float) like 4000.444444
    
    Example: to_usd(4000.444444)
    
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" 

def find_product(product_id, all_products):
    """
    Finds and returns the information of the product (from a list of products) that matches the product ID entered 
    
    Source: https://github.com/s2t2/shopping-cart-screencast/blob/testing/shopping_cart.py
    
    Param: product_id is the name of the variable that stores the product ID entered (string), all_products is a list like products
    
    Example: find_product(cashier_input, products)
    
    Returns: assuming the cashier_input was 1, the result would be 
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50, "price_per": "item"}
    """
    matching_products = [p for p in all_products if str(p["id"]) == str(product_id)]
    matching_product = matching_products[0]
    return matching_product

def id_pound(item):
    """
    Filters the items that are priced by "pound", to be used as filtering condition later in a list filter
    
    Source: https://github.com/prof-rossetti/intro-to-python/blob/7adaa47921be090406fd43e2e67cbd7c72092bde/notes/python/datatypes/lists.md
    
    Param: item (any string)
    """
    return item["price_per"] == "pound"

def calculate_taxes_owed(my_price, my_tax_rate):
    """
    Calculates taxes owed by multiplying price times the appropriate tax rate
    
    Param: my_price (int or float) like 100.5, my_tax_rate (float) is the tax rate in decimal format like 0.12
    
    Example: calculate_taxes_owed(100.5, 0.12)
    
    Returns: 12.06
    """
    return my_price * my_tax_rate

def calculate_total_price (my_subtotal, my_taxes):
    """
    Calculates total price by adding subtotal plus taxes
    
    Param: my_subtotal (int or float) like 23.5, my_taxes (int or float) like 1.75
    
    Example: calculate_total_price(23.5, 1.75)
    
    Returns: 25.25
    """
    return my_subtotal + my_taxes


if __name__ == "__main__":

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


    # FURTHER CHALLENGE: integrating with a Google Sheets datastore
    # Code source: online notes on gspread package 
    # https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/gspread.md
    # Also discussed with Ahmad Wilson on set-up instructions

    # AUTHORIZATION

    CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__),"..", "auth", "spreadsheet_credentials.json")

    AUTH_SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets", 
        "https://www.googleapis.com/auth/drive.file" 
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)

    # READ SHEET VALUES

    client = gspread.authorize(credentials) 
    doc = client.open_by_key(DOCUMENT_ID) 
    sheet = doc.worksheet(SHEET_NAME) 

    rows = sheet.get_all_records() 
    products = [r for r in rows]


    # Create lists to store cashier inputs:

    id_list = []
    for p in products:
        id_list.append(str(p["id"]))

    id_pound_list = []
    for pound_id in list(filter(id_pound,products)):
        id_pound_list.append(str(pound_id["id"]))

    # Use WHILE LOOP to allow cashier to enter product identifiers:

    selected_items = []
    selected_pounds = []

    while True:
        cashier_input = input("Please input a product identifier. If finished, enter DONE: ")
        if cashier_input == "DONE":
            customer_email_address = input("Please enter your email address to receive a copy of your receipt. Otherwise enter NO: ")
            break
        elif cashier_input not in id_list:
            print ("Sorry, product not found. Please try again...")
        elif cashier_input in id_pound_list:
            pounds_input = input("Please enter the number of pounds rounded to the nearest integer: ")
            if pounds_input.isnumeric():
                selected_pounds.append({"id":cashier_input, "pounds":pounds_input})
            else:       
                print ("Please try again and enter a valid number.")
        else:
            selected_items.append(cashier_input)


    # Print grocery store information:
    receipt_message = "--------------------------------------------------"
    receipt_message = receipt_message + "\n"
    receipt_message = receipt_message + "GU Healthy Foods"
    receipt_message = receipt_message + "\n"
    receipt_message = receipt_message + "3700 O ST NW Washington DC"
    receipt_message = receipt_message + "\n"
    receipt_message = receipt_message + "Phone: (202)-495-3439"
    receipt_message = receipt_message + "\n"
    receipt_message = receipt_message + "Website: www.guhealthyfoods.com"
    receipt_message = receipt_message + "\n"
    receipt_message = receipt_message + "--------------------------------------------------"
    receipt_message = receipt_message + "\n"

    # Print time of purchase:
    purchase_time = datetime.datetime.now()
    receipt_message = receipt_message + "Checkout at: " + purchase_time.strftime("%Y-%m-%d %I:%M %p")
    receipt_message = receipt_message + "\n"
    receipt_message = receipt_message + "--------------------------------------------------"
    receipt_message = receipt_message + "\n"

    # Print list of items purchased:
    receipt_message = receipt_message + "Selected products: "
    receipt_message = receipt_message + "\n"

    total_price = 0
    for cashier_input in selected_items:
        matching_product = find_product(cashier_input, products)
        total_price = total_price + matching_product["price"]
        receipt_message = receipt_message + "... " + matching_product["name"] + " (" + to_usd(matching_product["price"]) + ")"
        receipt_message = receipt_message + "\n"

    for d in selected_pounds:
        matching_product = find_product(d["id"], products)
        total_pounds = matching_product["price"]*(float(d["pounds"]))
        total_price = total_price + total_pounds
        receipt_message = receipt_message + "... " + matching_product["name"] + " (" + to_usd(total_pounds) + ")"
        receipt_message = receipt_message + "\n"

    receipt_message = receipt_message + "--------------------------------------------------"
    receipt_message = receipt_message + "\n"

    # Print subtotal:
    receipt_message = receipt_message + "Subtotal: " + to_usd(total_price)
    receipt_message = receipt_message + "\n"

    # Print taxes using pre-configured sales tax rate (environment variable):
    tax_rate_input = float(os.environ.get("TAX_RATE"))
    tax = calculate_taxes_owed(total_price,tax_rate_input)
    receipt_message = receipt_message + "Tax: " + to_usd(tax)
    receipt_message = receipt_message + "\n"

    # Print total purchase price:
    total_amount = calculate_total_price(total_price,tax)
    receipt_message = receipt_message + "Total: " + to_usd(total_amount)
    receipt_message = receipt_message + "\n"

    # Print thank you message:
    receipt_message = receipt_message + "--------------------------------------------------"
    receipt_message = receipt_message + "\n"
    receipt_message = receipt_message + "Thanks for shopping with us!"
    receipt_message = receipt_message + "\n"
    receipt_message = receipt_message + "Hope to see you again soon."
    receipt_message = receipt_message + "\n"
    receipt_message = receipt_message + "--------------------------------------------------"

    print(receipt_message)


    # FURTHER CHALLENGE: writing receipts to txt file
    # Code source for this challenge: Online notes on python file management:
    # https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/file-management.md
    # Also discussed with Ahmad Wilson on creating a variable to store the receipt message

    file_name = purchase_time.strftime("%Y-%m-%d-%H-%M-%S-%f") + ".txt"
    file_path = os.path.join(os.path.dirname(__file__), "..", "receipts", file_name)
    with open(file_path, "w") as file:
        file.write(receipt_message)


    # FURTHER CHALLENGE: sending receipts via email
    # Code source for this challenge: Online notes on Sendgrid
    # https://github.com/prof-rossetti/notification-service-py/blob/master/app/send_email.py 

    if customer_email_address == "NO":
        pass
    else:

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
