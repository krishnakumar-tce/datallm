import pandas as pd
import numpy as np
import random
from faker import Faker
import openpyxl

# Initialize Faker for generating fake data
fake = Faker()

# Function to generate random data
def generate_data():
    # Generate data for Customers
    customers = pd.DataFrame({
        'customer_id': range(1, 101),
        'first_name': [fake.first_name() for _ in range(100)],
        'last_name': [fake.last_name() for _ in range(100)],
        'email': [fake.email() for _ in range(100)],
        'registration_date': [fake.date_this_decade() for _ in range(100)]
    })

    # Generate data for Products
    products = pd.DataFrame({
        'product_id': range(1, 101),
        'name': [fake.word() for _ in range(100)],
        'description': [fake.sentence() for _ in range(100)],
        'price': np.round(np.random.uniform(5.0, 500.0, 100), 2),
        'category': [fake.word() for _ in range(100)],
        'stock_quantity': np.random.randint(1, 100, 100)
    })

    # Generate data for Orders
    orders = pd.DataFrame({
        'order_id': range(1, 101),
        'customer_id': np.random.choice(customers['customer_id'], 100),
        'order_date': [fake.date_this_year() for _ in range(100)],
        'total_amount': np.round(np.random.uniform(10.0, 1000.0, 100), 2),
        'status': np.random.choice(['Pending', 'Completed', 'Shipped'], 100)
    })

    # Generate data for OrderItems
    order_items = pd.DataFrame({
        'order_item_id': range(1, 301),
        'order_id': np.random.choice(orders['order_id'], 300),
        'product_id': np.random.choice(products['product_id'], 300),
        'quantity': np.random.randint(1, 10, 300),
        'unit_price': np.round(np.random.uniform(5.0, 500.0, 300), 2)
    })

    # Generate data for Reviews
    reviews = pd.DataFrame({
        'review_id': range(1, 101),
        'product_id': np.random.choice(products['product_id'], 100),
        'customer_id': np.random.choice(customers['customer_id'], 100),
        'rating': np.random.randint(1, 6, 100),
        'comment': [fake.sentence() for _ in range(100)]
    })

    return {
        'Customers': customers,
        'Products': products,
        'Orders': orders,
        'OrderItems': order_items,
        'Reviews': reviews
    }

# Generate the data
data = generate_data()

# Create a Pandas Excel writer using XlsxWriter as the engine
with pd.ExcelWriter('database_example.xlsx', engine='openpyxl') as writer:
    for sheet_name, df in data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("Excel file created successfully!")