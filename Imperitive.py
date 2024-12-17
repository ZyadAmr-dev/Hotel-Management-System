import json
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Optional

def load_data() -> Dict:
    try:
        with open("db.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "rooms": [],
            "reservations": [],
            "customers": [],
            "availableServices": [
                {"id": 1, "name": "Meal", "price": 50},
                {"id": 2, "name": "Laundry", "price": 20},
                {"id": 3, "name": "Spa", "price": 100}
            ],
            "orderedServices": []
        }


def save_data(data: Dict) -> None:
    with open("db.json", "w") as file:
        json.dump(data, file, indent=4)


def create_room(room_number: int, room_type: str, price: float) -> None:
    data = load_data()
    rooms = data["rooms"]

    if any(room["roomNumber"] == room_number for room in rooms):
        print(f"Room {room_number} already exists.")
        return

    rooms.append({
        "roomNumber": room_number,
        "roomType": room_type.lower(),
        "price": price,
        "available": True
    })
    save_data(data)
    print(f"Room {room_number} ({room_type}) created successfully.")


def check_room_status(room_number: int) -> str:
    data = load_data()
    rooms = data["rooms"]

    for room in rooms:
        if room["roomNumber"] == room_number:
            return "Available" if room["available"] else "Occupied"
    return "Room not found."


def get_customer_info(name: str, contact: str, payment_method: str) -> None:
    data = load_data()
    customers = data["customers"]

    if any(customer["name"] == name and customer["contact"] == contact for customer in customers):
        print(f"Customer {name} with contact {contact} already exists.")
        return

    customers.append({
        "name": name,
        "contact": contact,
        "paymentMethod": payment_method
    })

    save_data(data)
    print(f"Customer {name} added successfully.")


def book_room(customer_name: str, room_number: int, check_in_date: str, stay_length: int, contact: str, payment_method: str) -> None:
    data = load_data()
    rooms = data["rooms"]
    reservations = data["reservations"]

    for room in rooms:
        if room["roomNumber"] == room_number:
            if room["available"]:
                room["available"] = False
                get_customer_info(customer_name, contact, payment_method)

                reservation = {
                    "reservationId": len(reservations) + 1,
                    "customerName": customer_name,
                    "roomNumber": room_number,
                    "checkInDate": check_in_date,
                    "checkOutDate": (datetime.strptime(check_in_date, "%Y-%m-%d") + timedelta(days=stay_length)).strftime("%Y-%m-%d")
                }
                reservations.append(reservation)
                save_data(data)
                print(f"Room {room_number} booked successfully for {customer_name}.")
                return
    print(f"Room {room_number} is not available.")


def check_in(room_number: int) -> None:
    data = load_data()
    reservations = data["reservations"]

    for reservation in reservations:
        if reservation["roomNumber"] == room_number and datetime.strptime(reservation["checkInDate"], "%Y-%m-%d").date() == datetime.now().date():
            print(f"Guest {reservation['customerName']} checked into room {room_number}.")
            return
    print(f"No reservation found for room {room_number} today.")


def check_out(room_number: int) -> None:
    data = load_data()
    rooms = data["rooms"]
    reservations = data["reservations"]

    for room in rooms:
        if room["roomNumber"] == room_number:
            room["available"] = True
            data["reservations"] = [res for res in reservations if res["roomNumber"] != room_number]
            save_data(data)
            print(f"Room {room_number} has been checked out and is now available.")
            return
    print(f"Room {room_number} not found.")


def search_on_customers(customer_name: str) -> List[Dict[str, str]]:
    data = load_data()
    customers = data['customers']

    result = [customer for customer in customers if customer['name'] == customer_name]
    if result:
        print(f"Customer(s) found: {result}")
    else:
        print(f"No customer found with name {customer_name}.")
    return result


def calculate_bill(reservation_id: int, tax_rate: float = 0.15, discount: float = 0.2) -> None:
    data = load_data()
    reservations = data["reservations"]
    services = data["orderedServices"]
    available_services = data["availableServices"]

    reservation = next((res for res in reservations if res["reservationId"] == reservation_id), None)
    if not reservation:
        print(f"No reservation found with ID {reservation_id}")
        return

    check_in = datetime.strptime(reservation["checkInDate"], "%Y-%m-%d")
    check_out = datetime.strptime(reservation["checkOutDate"], "%Y-%m-%d")
    stay_duration = (check_out - check_in).days

    room = next(room for room in data["rooms"] if room["roomNumber"] == reservation["roomNumber"])
    room_charges = room["price"] * stay_duration

    service_charges = sum(
        service["price"]
        for ordered in services if ordered["reservationId"] == reservation_id
        for service in available_services if service["id"] == ordered["serviceId"]
    )

    subtotal = room_charges + service_charges
    tax = subtotal * tax_rate
    discount_amount = subtotal * discount
    total = subtotal + tax - discount_amount

    print("\n----- BILL -----")
    print(f"Customer Name: {reservation['customerName']}")
    print(f"Room Number: {reservation['roomNumber']}")
    print(f"Stay Duration: {stay_duration} days")
    print(f"Room Charges: ${room_charges:.2f}")
    print(f"Service Charges: ${service_charges:.2f}")
    print(f"Tax ({tax_rate * 100}%): ${tax:.2f}")
    print(f"Discount ({discount * 100}%): -${discount_amount:.2f}")
    print(f"Total Amount: ${total:.2f}")
    print("----------------\n")


def get_room_occupancy_rate() -> float:
    data = load_data()
    total_rooms = len(data["rooms"])
    occupied_rooms = sum(1 for room in data["rooms"] if not room["available"])
    
    if total_rooms == 0:
        return 0 
    return (occupied_rooms / total_rooms) * 100


def get_revenue_report(start_date: Optional[str] = None, end_date: Optional[str] = None) -> float:
    data = load_data()
    reservations = data["reservations"]
    total_revenue = 0

    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        start_date = datetime.min
        end_date = datetime.max

    for reservation in reservations:
        check_in = datetime.strptime(reservation["checkInDate"], "%Y-%m-%d")
        check_out = datetime.strptime(reservation["checkOutDate"], "%Y-%m-%d")
        
        if start_date <= check_in <= end_date:
            room = next(room for room in data["rooms"] if room["roomNumber"] == reservation["roomNumber"])
            stay_duration = (check_out - check_in).days
            room_revenue = room["price"] * stay_duration
            total_revenue += room_revenue
    
    return total_revenue


def get_customer_statistics() -> Dict[str, any]:
    data = load_data()
    customers = data["customers"]
    total_customers = len(customers)
    
    contact_methods = defaultdict(int)
    for customer in customers:
        contact_methods[customer["contact"]] += 1
    
    return {
        "total_customers": total_customers,
        "contact_methods": dict(contact_methods)
    }

def generate_report(period: str = "daily") -> None:
    if period == "daily":
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = start_date
    elif period == "weekly":
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
    elif period == "monthly":
        start_date = (datetime.now().replace(day=1)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
    else:
        print("Invalid period specified. Please choose 'daily', 'weekly', or 'monthly'.")
        return
    
    print(f"Generating {period} report from {start_date} to {end_date}...\n")
    
    occupancy_rate = get_room_occupancy_rate()
    revenue = get_revenue_report(start_date, end_date)
    customer_stats = get_customer_statistics()
    
    print(f"Room Occupancy Rate: {occupancy_rate:.2f}%")
    print(f"Total Revenue: ${revenue:.2f}")
    print(f"Customer Statistics: {customer_stats}\n")


def generate_financial_summary(period: str = "daily") -> None:
    if period == "daily":
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = start_date
    elif period == "weekly":
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
    elif period == "monthly":
        start_date = (datetime.now().replace(day=1)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
    else:
        print("Invalid period specified. Please choose 'daily', 'weekly', or 'monthly'.")
        return
    
    revenue = get_revenue_report(start_date, end_date)
    print(f"Financial Summary for {period} (from {start_date} to {end_date}):")
    print(f"Total Revenue: ${revenue:.2f}\n")


if __name__ == "__main__":
    create_room(101, "Single", 100)
    create_room(102, "Double", 150)
    create_room(103, "Suite", 250)
    create_room(104, "Single", 100)
    create_room(105, "Suite", 200)
    
    print(check_room_status(101))
    print(check_room_status(102))
    print(check_room_status(103))
    print(check_room_status(104))
    print(check_room_status(105))

    book_room("Alice", 101, "2024-12-17", 3, "555-1234", "Credit Card")
    book_room("Bob", 102, "2024-12-18", 2, "555-5678", "Debit Card")

    check_in(101)
    check_in(102)

    check_out(101)

    generate_report("daily")
    generate_financial_summary("daily")
    
    search_on_customers("Alice")
    search_on_customers("Bob")

    calculate_bill(1)  
    calculate_bill(2)
