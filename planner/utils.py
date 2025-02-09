import requests


#########
# planner/utils.py

def get_building_materials():
    # Example function to get building materials
    return [
        {"name": "Wood", "price": "$10 per sqft"},
        {"name": "Steel", "price": "$20 per sqft"},
        {"name": "Concrete", "price": "$15 per sqft"},
    ]

def generate_2d_design(num_rooms, square_feet, room_type, width, length):
    # Example function to generate a simple 2D design
    design = {
        "num_rooms": num_rooms,
        "square_feet": square_feet,
        "room_type": room_type,
        "dimensions": {"width": width, "length": length},
    }
    return design
