import sqlite3, json
from models import Location

LOCATIONS =  [
    {
      "id": 1,
      "name": "Nashville North Crampus",
      "address": "8422 Johnson Pike",
    },
    {
      "id": 2,
      "name": "Nashville South",
      "address": "209 Emory Drive",
    },
    {
      "id": 3,
      "name": "Midtown",
      "address": "103 Elliston Place"
    }
  ]

def get_all_locations():
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
          l.id,
          l.name,
          l.address
        FROM location l
        """)

        dataset = db_cursor.fetchall()

        locations = []

        for row in dataset:
          location = Location(row['id'], row['name'], row['address'])
          locations.append(location.__dict__)
        
    return json.dumps(locations)

def get_single_location(id):
      with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
          l.id,
          l.name,
          l.address
        FROM location l
        WHERE l.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        location = Location(data['id'], data['name'], data['address'])

      return json.dumps(location.__dict__)

def create_location(location):
  max_id = LOCATIONS[-1]["id"]
  new_id = max_id + 1
  location["id"] = new_id
  LOCATIONS.append(location)
  return location

def delete_location(id):
  location_index = -1

  for index, location in enumerate(LOCATIONS):
    if location["id"] == id:
      location_index = index

  if location_index >= 0:
    LOCATIONS.pop(location_index)

def update_location(id, new_location):
  for index, location in enumerate(LOCATIONS):
    if location["id"] == id:
      LOCATIONS[index] = new_location