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
    return CUSTOMERS

def get_single_customer(id):
    requested_customer = None

    for customer in CUSTOMERS:
        if customer["id"] == id:
            requested_customer = customer

    return requested_customer

def create_customer(customer):
  max_id = CUSTOMERS[-1]["id"]
  new_id = max_id + 1
  customer["id"] = new_id
  CUSTOMERS.append(customer)
  return customer