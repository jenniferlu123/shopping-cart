# shopping-cart

# Introduction:  

This python program was written to facilitate the checkout process at the GU Healthy Foods grocery store. 

# Prerequisites:

  + Anaconda 3.7
  + Python 3.7
  + Pip

# Instalation: 

Fork this [remote repository](https://github.com/jenniferlu123/shopping-cart) to your own GitHub repository, then clone (download) your remote copy onto your local computer.

Then navigate there from the command line :

```sh
cd ~/shopping-cart
```

# Setup:

## Virtual environment set up

Use Anaconda to create and activate a new virtual environment named "shopping-env":

```sh
conda create -n shopping-env python=3.7 # (first time only)
conda activate shopping-env
```

## Required package installation

From inside the virtual environment, install all necessary packages by running the following code:

```sh
pip install -r requirements.txt
```

## Tax rate set up

Open the file named ".env" and update the tax rate to the one that is appropriate for your state (this is the tax rate that will be used to calculate taxes owed by customers during checkout process):

    tax_rate = EXAMPLE # enter a decimal number with no quotation marks 

## Email template set up

If you are interested in using this program's email capabilities to send out receipts to customers, please update the SendGrid API key (obtained using your SendGrid account) and your email address in the ".env" file: 

    SENDGRID_API_KEY= "EXAMPLE" 
    MY_EMAIL_ADDRESS= "EXAMPLE" 

## Google Sheet Database set up

If you are interested in using a Google Sheet Database, please update the Google Sheet ID in the ".env" file using the unique identifier found in the URL of the document that contains information about your store's products:

    GOOGLE_SHEET_ID = "EXAMPLE" 

# Usage:

Run the python script:

```py
python shopping_cart.py
```

## Overview of the "steps" of the shopping-cart program:

1. Enter each of the product's identifiers

2. After you have entered all the identifers, enter DONE

3. The program will ask for the customer's email address where they would like to receive a copy of the receipt. If they prefer to opt out of this option, enter NO

4. The receipt will be automatically generated on the screen with the grocery store's information, checkout time, purchased items, tax, and total purchase price

5. A txt file will be automatically generated inside the "receipts" folder. The txt file will include full receipt details. It can be used to print out a paper receipt, if needed

6. If the customer entered their email address, then they will receive a copy of the receipt in their email as well



