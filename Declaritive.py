from enum import Enum

class RoomType(Enum):
    SINGLE = 1
    DOUBLE = 2
    SUITE = 3

rooms = []

def create_room(room_number: int, room_type: RoomType, room_price: float, room_availability: bool):
    rooms.append({
        "number": room_number,
        "type": room_type,
        "price": room_price,
        "available": room_availability
    })
    print(f"Room {room_number} of type {room_type.name} added successfully.")

create_room(101, RoomType.SINGLE, 100.0, True)
create_room(102, RoomType.DOUBLE, 150.0, False)

def is_available(room_number):
    return next((room["available"] for room in rooms if room["number"] == room_number), False)

def book_room(room_number):
    room = next((room for room in rooms if room["number"] == room_number), None)
    if room:
        if room["available"]:
            room["available"] = False
            print(f"The room {room_number} has been booked successfully.")
        else:
            print(f"The room {room_number} is already booked.")
    else:
        print(f"No room with number {room_number} found.")

print(rooms)
print(f"Room 101 available: {is_available(101)}")
book_room(101)
print(f"Room 101 available: {is_available(101)}")
book_room(101)