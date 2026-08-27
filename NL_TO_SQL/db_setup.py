import sqlite3

def init_in_memory_db() -> sqlite3.Connection:
    """Creates an in-memory SQLite database and seeds it with mock data."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create Tables
    cursor.executescript("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            signup_date TEXT NOT NULL,
            region TEXT NOT NULL
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(customer_id),
            order_date TEXT NOT NULL,
            status TEXT CHECK (status IN ('completed', 'pending', 'cancelled')),
            total_amount REAL NOT NULL
        );

        CREATE TABLE order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER REFERENCES orders(order_id),
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL
        );
    """)

    # Seed Mock Data
    cursor.executescript("""
        INSERT INTO customers VALUES 
            (1, 'Alice Smith', 'alice@example.com', '2025-01-15', 'East'),
            (2, 'Bob Jones', 'bob@example.com', '2025-02-10', 'West'),
            (3, 'Charlie Brown', 'charlie@example.com', '2025-03-05', 'East');

        INSERT INTO orders VALUES 
            (101, 1, '2025-05-12', 'completed', 450.00),
            (102, 2, '2025-06-18', 'completed', 1200.50),
            (103, 1, '2025-07-22', 'completed', 850.00),
            (104, 3, '2025-08-01', 'pending', 300.00);

        INSERT INTO order_items VALUES 
            (1, 101, 'Mechanical Keyboard', 2, 150.00),
            (2, 101, 'Gaming Mouse', 3, 50.00),
            (3, 102, '4K Monitor', 2, 600.25),
            (4, 103, 'USB-C Dock', 1, 850.00);
    """)

    conn.commit()
    return conn