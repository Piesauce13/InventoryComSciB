import re
from datetime import datetime

def validate_date_format(date_str):
    """Validate if a string has the YYYY-MM-DD format"""
    if not date_str:
        return True
    
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        return False
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def format_currency(amount):
    """Format a number as currency"""
    return f"${amount:.2f}"

def format_product_display(product):
    """Format a product for display"""
    expiry = product['expiry_date'] if product['expiry_date'] else 'N/A'
    return (
        f"ID: {product['id']}\n"
        f"Name: {product['name']}\n"
        f"Category: {product['category']}\n"
        f"Price: {format_currency(product['price'])}\n"
        f"Quantity: {product['quantity']}\n"
        f"Expiry Date: {expiry}\n"
        f"Min Stock Level: {product['min_stock_level']}"
    )

def validate_positive_number(value_str):
    """Validate if a string can be converted to a positive number"""
    try:
        value = float(value_str)
        return value >= 0
    except ValueError:
        return False

def get_validated_input(prompt, validator=None, error_message=None):
    """Get user input with validation"""
    while True:
        value = input(prompt)
        if validator is None or validator(value):
            return value
        print(error_message or "Invalid input. Please try again.")