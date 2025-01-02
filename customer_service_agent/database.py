import sqlite3
from typing import Dict, Optional

def init_db():
    conn = sqlite3.connect('customer_service.db')
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    # Insert initial data
    customers = [
        ('C1', 'Jane Smith', 'jane@example.com', '987-654-3210'),
        ('C2', 'John Doe', 'john@example.com', '123-456-7890')
    ]
    
    orders = [
        ('O1', 'Widget A', 2, 19.99, 'Shipped'),
        ('O2', 'Gadget B', 1, 49.99, 'Processing')
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?)', customers)
    cursor.executemany('INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?)', orders)
    
    conn.commit()
    conn.close()

def get_customer_info(customer_id: str) -> Optional[Dict]:
    conn = sqlite3.connect('customer_service.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return {
            'name': result[1],
            'email': result[2],
            'phone': result[3]
        }
    return None

def get_order_details(order_id: str) -> Optional[Dict]:
    conn = sqlite3.connect('customer_service.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return {
            'id': result[0],
            'product': result[1],
            'quantity': result[2],
            'price': result[3],
            'status': result[4]
        }
    return None

def cancel_order(order_id: str) -> bool:
    conn = sqlite3.connect('customer_service.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT order_id FROM orders WHERE order_id = ?', (order_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result is not None
