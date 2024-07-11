import os
from datetime import datetime
from app import create_app, db
from app.models import User, Product, Order, OrderItem, Payment, Return

# Create the Flask application
app = create_app()

def populate_database():
    # Use the application context
    with app.app_context():
        # Create users

        # Create Products
        product1 = Product(name='Product 1', description='Description for Product 1', price=10.99, stock=100)
        product2 = Product(name='Product 2', description='Description for Product 2', price=19.99, stock=50)
        product3 = Product(name='Product 3', description='Description for Product 3', price=5.99, stock=200)
        product4 = Product(name='Product 4', description='Description for Product 4', price=15.99, stock=75)

        db.session.add_all([product1, product2, product3, product4])
        db.session.commit()


        print("Database populated successfully!")

if __name__ == '__main__':
    populate_database()
