rooms = []

def create_room(room_number: int, room_type: str, room_price: float, room_availability: bool):
    rooms.append({
        "number": room_number,
        "type": room_type,  
        "price": room_price,
        "available": room_availability
    })
    print(f"Room {room_number} of type {room_type} added successfully.")

def is_available(room_number: int) -> bool:
    for room in rooms:
        if room["number"] == room_number:
            return room["available"]
    return False

def book_room(room_number: int):
    for room in rooms:
        if room["number"] == room_number:
            if room["available"]:
                room["available"] = False
                print(f"The room {room_number} has been booked successfully.")
                return
            else:
                print(f"The room {room_number} is already booked.")
                return
    print(f"No room with number {room_number} found.")

create_room(101, "SINGLE", 100.0, True)
create_room(102, "DOUBLE", 150.0, False)

print(rooms)
print(f"Room 101 available: {is_available(101)}")
book_room(101)
print(f"Room 101 available: {is_available(101)}")
book_room(101)
