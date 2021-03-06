from animals.request import get_animals_by_status
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from animals import get_all_animals, get_single_animal, create_animal, delete_animal, update_animal, get_animals_by_location
from customers import get_single_customer, get_all_customers, create_customer, delete_customer, update_customer, get_customer_by_email
from employees import get_single_employee, get_all_employees, create_employee, delete_employee, update_employee, get_employees_by_location
from locations import get_single_location, get_all_locations, create_location, delete_location, update_location
import json

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:
            resource, param = resource.split("?")
            key, value = param.split("=")

            return (resource, key, value)
            
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

            return (resource, id)

    # Here's a class function

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        # Set the response code to 'Ok'
        self._set_headers(200)

        # Your new console.log() that outputs to the terminal
        response = {}

        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            resource, id = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"

                else:
                    response = f"{get_all_animals()}"

            if resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"

                else:
                    response = f"{get_all_locations()}"

            if resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"

                else:
                    response = f"{get_all_employees()}"

            if resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"

                else:
                    response = f"{get_all_customers()}"
        
        elif len(parsed) == 3:
            resource, key, value = parsed

            if key == "email" and resource == "customers":
                response = f"{get_customer_by_email(value)}"

            if key == "location_id" and resource == "animals":
                response = f"{get_animals_by_location(value)}"

            if key == "location_id" and resource == "employees":
                response = f"{get_employees_by_location(value)}"

            if key == "status" and resource == "animals":
                response = f"{get_animals_by_status(value)}"

        # This weird code sends a response back to the client
        self.wfile.write(f"{response}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        # Set response code to 'Created'
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        resource, id = self.parse_url(self.path)

        new_item = None

        if resource == "animals":
            new_item = create_animal(post_body)
        elif resource == "locations":
            new_item = create_location(post_body)
        elif resource == "employees":
            new_item = create_employee(post_body)
        elif resource == "customers":
            new_item = create_customer(post_body)

        self.wfile.write(f"{new_item}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        resource, id = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        elif resource == "customers":
            update_customer(id, post_body)
        elif resource == "employees":
            update_employee(id, post_body)
        elif resource == "locations":
            update_location(id, post_body)

        if success: self._set_headers(204)
        else: self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        self._set_headers(204)
        resource, id = self.parse_url(self.path)

        if resource == "animals":
            delete_animal(id)
        elif resource == "customers":
            delete_customer(id)
        elif resource == "employees":
            delete_employee(id)
        elif resource == "locations":
            delete_location(id)

        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
