# shopping-cart/test/shopping_cart_test.py

from app.shopping_cart import to_usd, time_format, calculate_taxes_owed, calculate_total_price

def test_to_usd():
    result = to_usd(1500)
    assert result == "$1,500.00"

#def test_time_format():
#    result = time_format(2012-1-1 21:21:21)
#    assert result == "2020-10-10 02:31 PM"

def test_calculate_taxes_owed():
    result = calculate_taxes_owed(100,0.05)
    assert result == 5

def test_calculate_total_price():
    result = calculate_total_price(125,4.5)
    assert result == 129.5