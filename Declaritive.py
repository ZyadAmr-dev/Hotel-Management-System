from typing import List, Dict

# Immutable
rooms: List[Dict] = []

def create_room(rooms: List[Dict], room_number: int, room_type: str, room_price: float, room_availability: bool) -> List[Dict]:
    new_room = {
        "number": room_number,
        "type": room_type,
        "price": room_price,
        "available": room_availability
    }
    print(f"Room {room_number} of type {room_type} added successfully.")
    return rooms + [new_room]  

def is_available(rooms: List[Dict], room_number: int) -> bool:
    return next((room["available"] for room in rooms if room["number"] == room_number), False)

def book_room(rooms: List[Dict], room_number: int) -> List[Dict]:
    def update_room(room):
        if room["number"] == room_number:
            if room["available"]:
                print(f"The room {room_number} has been booked successfully.")
                return {**room, "available": False} 
            else:
                print(f"The room {room_number} is already booked.")
        return room  

    if any(room["number"] == room_number for room in rooms):
        return [update_room(room) for room in rooms]  
    else:
        print(f"No room with number {room_number} found.")
        return rooms  


rooms = create_room(rooms, 101, "SINGLE", 100.0, True)
rooms = create_room(rooms, 102, "DOUBLE", 150.0, False)

print(rooms)
print(f"Room 101 available: {is_available(rooms, 101)}")
rooms = book_room(rooms, 101)
print(f"Room 101 available: {is_available(rooms, 101)}")
rooms = book_room(rooms, 101)
