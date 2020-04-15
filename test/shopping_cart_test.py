# shopping-cart/test/shopping_cart_test.py

import pytest # for pytest.raises (see: https://docs.pytest.org/en/latest/assert.html)

from app.shopping_cart import to_usd, find_product, calculate_taxes_owed, calculate_total_price

def test_to_usd():
    result = to_usd(1500)
    assert result == "$1,500.00"

    result = to_usd(98.78384)
    assert result == "$98.78"

    result = to_usd(2.5)
    assert result == "$2.50"

# Python code for test_find_product was written using some code taken from prof-rossetti repository
# https://github.com/s2t2/shopping-cart-screencast/blob/testing/shopping_cart_test.py

def test_find_product():
    products = [
        {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50, "price_per": "item"},
        {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49, "price_per": "item"},
        {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99, "price_per": "item"},
        {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99, "price_per": "item"},
    ]

    matching_product = find_product("2", products)
    assert matching_product["department"] == "pantry"

    matching_product = find_product("4", products)
    assert matching_product["name"] == "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce"

    with pytest.raises(IndexError):
        find_product("5968", products)

def test_calculate_taxes_owed():
    result = calculate_taxes_owed(100,0.05)
    assert result == 5

def test_calculate_total_price():
    result = calculate_total_price(125,4.5)
    assert result == 129.5