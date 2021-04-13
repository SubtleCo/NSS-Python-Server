import sqlite3, json
from models import Customer

CUSTOMERS = [
    {
      "email": "Billy@ray.com",
      "name": "Billy Ray Cyrus",
      "id": 1
    },
    {
      "email": "wario@nintendo.com",
      "name": "Wario Nintendo",
      "id": 2
    },
    {
      "email": "frodo@shire.com",
      "name": "Frodo Baggins",
      "id": 3
    }
  ]

def get_all_customers():
    with sqlite3.connect("./kennel.db") as conn:
      conn.row_factory = sqlite3.Row
      db_cursor = conn.cursor()

      db_cursor.execute("""
      SELECT
        c.id,
        c.name,
        c.email
      FROM customer c
      """)

      customers = []

      dataset = db_cursor.fetchall()

      for row in dataset:
        customer = Customer(row['id'], row['name'], row['email'])
        customers.append(customer.__dict__)

    return json.dumps(customers)
    

def get_single_customer(id):
    with sqlite3.connect("./kennel.db") as conn:
      conn.row_factory = sqlite3.Row
      db_cursor = conn.cursor()

      db_cursor.execute("""
      SELECT
        c.id,
        c.name,
        c.email
      FROM customer c
      WHERE c.id = ?
      """, (id, ))

      data = db_cursor.fetchone()

      customer = Customer(data['id'], data['name'], data['email'])
      return json.dumps(customer.__dict__)

def get_customer_by_email(email):
    with sqlite3.connect("./kennel.db") as conn:
      conn.row_factory = sqlite3.Row
      db_cursor = conn.cursor()

      db_cursor.execute("""
      SELECT
        c.id,
        c.name,
        c.email
      FROM customer c
      WHERE c.email = ?
      """, (email, ))

      customers = []

      dataset = db_cursor.fetchall()

      for row in dataset:
        customer = Customer(row['id'], row['name'], row['email'])
        customers.append(customer.__dict__)

    return json.dumps(customers)

def create_customer(customer):
  max_id = CUSTOMERS[-1]["id"]
  new_id = max_id + 1
  customer["id"] = new_id
  CUSTOMERS.append(customer)
  return customer

def delete_customer(id):
  customer_index = -1

  for index, customer in enumerate(CUSTOMERS):
    if customer["id"] == id:
      customer_index = index

  if customer_index >= 0:
    CUSTOMERS.pop(customer_index)

def update_customer(id, new_customer):
  for index, customer in enumerate(CUSTOMERS):
    if customer["id"] == id:
      CUSTOMERS[index] = new_customer
      break