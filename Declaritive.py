from enum import Enum

class RoomType(Enum):
    SINGLE = 1
    DOUBLE = 2
    SUITE = 3

rooms = []

def create_room(room_number: int, room_type: RoomType, room_price: float, room_availability: bool):
    room = {
        "number": room_number,
        "type": room_type,
        "price": room_price,
        "available": room_availability
    }
    rooms.append(room)
    print(f"Room {room_number} of type {room_type.name} added successfully.")

create_room(101, RoomType.SINGLE, 100.0, True)
create_room(102, RoomType.DOUBLE, 150.0, False)

def isAvailable(room_number):
    for room in rooms:
        if room["number"] == room_number:
            return room["available"]
    return False  

def book_room(room_number):
    for room in rooms:
        if room["number"] == room_number:
            if room["available"]:
                room["available"] = False
                print("The room has been booked successfully.")
            else:
                print("The room is already booked.")
            return
    print(f"No available room with number: {room_number}")       
        
print(rooms)
book_room(101)
book_room(101)
  