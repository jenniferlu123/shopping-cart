# shopping-cart

## Introduction:  

This python program was written to facilitate the checkout process at the GU Healthy Foods grocery store. 

## Prerequisites:

  + Anaconda 3.7
  + Python 3.7
  + Pip

## Instalation: 

Fork this [remote repository](https://github.com/jenniferlu123/shopping-cart) under your own control, then "clone" or download your remote copy onto your local computer.

Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

```sh
cd ~/Desktop/Shopping-cart
```

Use Anaconda to create and activate a new virtual environment, perhaps called "game-env":

```sh
conda create -n shopping-env python=3.7 # (first time only)
conda activate shopping-env
```

From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

## Setup

In the file ".env", please update the tax rate to the one applicable to your state:

    tax_rate = 0.0875

If you are interested in using the email capabilities to send out receipts to the customers, please update the SENDGRID_API_KEY and your email address: 

    SENDGRID_API_KEY= "EXAMPLE" # use your own API Key!
    MY_EMAIL_ADDRESS="EXAMPLE" # use the email address you associated with the SendGrid service

If you are interested in using a Google Sheet Database, please update Google Sheet ID:

    GOOGLE_SHEET_ID = "EXAMPLE" # the unique identifier is found in the document's URL

## Usage

Run the python script:

```py
python shopping_cart.py
```

The "steps" of this program are:
1. Enter the each of the item's identifiers
2. After you entered all the identifers, enter DONE
3. The program will ask the customer to enter their email address where they would like to receive a copy of the receipt. If they want to opt out of this option, enter NO
4. The receipt will be automatically generated on the screen with the grocery store's information, checkout time, purchased items, tax owed and total purchase price.
5. A txt file will be automatically generated in the "receipts" file, and ti will include all the details found on the receipt. This can be used to print out a paper receipt.
6. If the customer entered their email address, then they will receive a copy of the receipt in their email as well. 



