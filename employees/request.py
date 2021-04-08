EMPLOYEES = [
    {
      "id": 1,
      "name": "Kelly Clarkson",
      "locationId": 1
    },
    {
      "id": 2,
      "name": "Jim Masterson",
      "locationId": 1
    },
    {
      "id": 3,
      "name": "Gilly Goober",
      "locationId": 2
    },
    {
      "id": 4,
      "name": "Mitchell Frankson",
      "locationId": 2
    },
    {
      "id": 5,
      "name": "Bibel Fooster",
      "locationId": 3
    },
    {
      "id": 6,
      "name": "God Himself",
      "locationId": 3
    }
  ]

def get_all_employees():
    return EMPLOYEES

def get_single_employee(id):
    requested_employee = None

    for employee in EMPLOYEES:
        if employee["id"] == id:
            requested_employee = employee
    
    return requested_employee