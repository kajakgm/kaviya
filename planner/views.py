import matplotlib
matplotlib.use('Agg')
import io
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import FloorPlan
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RoomForm,HomePlanForm
#from django.shortcuts import render
from .utils import get_building_materials, generate_2d_design
from django.core.files.base import ContentFile 
######
 # Use non-GUI backend before importing pyplot
import matplotlib.pyplot as plt
####

import numpy as np

from matplotlib.patches import Arc, Rectangle, Circle
from matplotlib.lines import Line2D

###



##

from planner.models import FloorPlan  # Ensure FloorPlan model is imported


# Import the required forms
#from .forms import , RoomForm
#from .utils import, get_building_materials  # Assuming a 2D design utility exists
#####
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io, base64
from django.shortcuts import render
from django.http import HttpResponse

def generate_2d_plan(request):
    if request.method == "POST":
        try:
            length = float(request.POST.get("length", 40))  # Default 40 ft
            width = float(request.POST.get("width", 40))    # Default 40 ft

            fig, ax = plt.subplots(figsize=(10, 10))

            # Draw house boundary (fully covered)
            ax.add_patch(patches.Rectangle((0, 0), length, width, fill=None, edgecolor="black", linewidth=3))

            # Define rooms ensuring full coverage
            rooms = [
                {"name": "Master Bedroom", "x": 0, "y": width-14, "w": 14, "h": 14, "color": "lightblue"},
                {"name": "Bedroom 2", "x": 14, "y": width-14, "w": 14, "h": 14, "color": "cyan"},
                {"name": "Living Room", "x": 0, "y": width-26, "w": 20, "h": 12, "color": "lightgreen"},
                {"name": "Kitchen", "x": 20, "y": width-26, "w": 14, "h": 12, "color": "orange"},
                {"name": "Master Bath", "x": 10, "y": width-10, "w": 4, "h": 7, "color": "pink"},
                {"name": "Bedroom 2 Bath", "x": 24, "y": width-10, "w": 4, "h": 7, "color": "pink"},
                {"name": "Portico", "x": 0, "y": 0, "w": 12, "h": 10, "color": "yellow"},
                {"name": "Car Parking", "x": 12, "y": 0, "w": 16, "h": 10, "color": "gray"},
                {"name": "Garden", "x": 28, "y": 0, "w": 12, "h": 10, "color": "lightgreen"},
            ]

            for room in rooms:
                ax.add_patch(patches.Rectangle((room["x"], room["y"]), room["w"], room["h"], 
                                               fc=room["color"], edgecolor="black", linewidth=2))
                ax.text(room["x"] + room["w"]/2, room["y"] + room["h"]/2, f"{room['name']}\n{room['w']}x{room['h']} ft", 
                        fontsize=10, ha="center", va="center", color="black")

            # Main Door (Red Arc) in Living Room, South Side
            main_door = patches.Arc((10, 0), 4, 4, angle=0, theta1=0, theta2=180, color='red', linewidth=3)
            ax.add_patch(main_door)
            
            # Room doors (Brown lines)
            room_doors = [
                ((12, width-14), (14, width-14)),  # Master Bedroom Door
                ((26, width-14), (28, width-14)),  # Bedroom 2 Door
                ((20, width-20), (22, width-20)),  # Kitchen Entry
                ((10, width-7), (12, width-7)),  # Master Bath Door
                ((24, width-7), (26, width-7)),  # Bedroom 2 Bath Door
            ]
            for d in room_doors:
                ax.plot([d[0][0], d[1][0]], [d[0][1], d[1][1]], 'brown', linewidth=3)

            # Windows (Blue lines)
            windows = [
                ((6, width-14), (6, width-12)),  # Master Bedroom
                ((22, width-14), (22, width-12)),  # Bedroom 2
                ((10, width-26), (12, width-26)),  # Living Room
                ((24, width-26), (26, width-26)),  # Kitchen
            ]
            for w in windows:
                ax.plot([w[0][0], w[1][0]], [w[0][1], w[1][1]], 'blue', linewidth=3)

            # Four Pillars
            pillar_size = 1.5
            pillar_positions = [(0, 0), (length - pillar_size, 0), (0, width - pillar_size), (length - pillar_size, width - pillar_size)]
            for px, py in pillar_positions:
                ax.add_patch(patches.Rectangle((px, py), pillar_size, pillar_size, fc='black', edgecolor='black', linewidth=2))

            # Set axis limits
            ax.set_xlim([0, length])
            ax.set_ylim([0, width])
            ax.set_xlabel("Length (ft)")
            ax.set_ylabel("Width (ft)")
            ax.set_title("Generated 2D Home Plan (Vastu Compliant)")
            ax.grid(True)

            # Footnote Outside the Grid (Row-wise legend)
            footnote_y = -5
            legend = [
                ("lightblue", "Master Bedroom"),
                ("cyan", "Bedroom 2"),
                ("lightgreen", "Living Room"),
                ("orange", "Kitchen"),
                ("pink", "Bathrooms"),
                ("yellow", "Portico"),
                ("gray", "Car Parking"),
                ("lightgreen", "Garden"),
                ("red", "Main Door"),
                ("brown", "Room Doors"),
                ("blue", "Windows"),
                ("black", "Pillars"),
            ]
            for i, (color, label) in enumerate(legend):
                ax.add_patch(patches.Rectangle((i*5, footnote_y), 4, 2, fc=color, edgecolor='black'))
                ax.text(i*5 + 4.5, footnote_y + 1, label, fontsize=8, va='center')

            # Convert plot to image
            img = io.BytesIO()
            plt.savefig(img, format="png")
            img.seek(0)
            encoded_img = base64.b64encode(img.getvalue()).decode()
            img.close()
            plt.close(fig)

            return render(request, "planner/design.html", {"plan_image": encoded_img, "length": length, "width": width})
        
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    return render(request, "planner/design.html")

















# home_planner/views.py
def generate_2d_design(num_rooms, square_feet):
    avg_room_size = square_feet / num_rooms
    design = {
        'num_rooms': num_rooms,
        'avg_room_size': avg_room_size,
        'layout': '...SVG or JSON design structure here'
    }
    return design

###
def home_planner_view(request):
    materials = get_building_materials()  # Fetch materials for home planner

    if request.method == 'POST':
        # Handle both forms
        home_plan_form = HomePlanForm(request.POST)
        room_form = RoomForm(request.POST)

        if home_plan_form.is_valid() and room_form.is_valid():
            # Process HomePlanForm data
            num_rooms = home_plan_form.cleaned_data['num_rooms']
            square_feet = home_plan_form.cleaned_data['square_feet']
            # Process RoomForm data
            room_type = room_form.cleaned_data['room_type']
            width = room_form.cleaned_data['width']
            length = room_form.cleaned_data['length']

            # Generate the 2D design (you can create a utility function for this)
            design = generate_2d_design(num_rooms, square_feet, room_type, width, length)

            # Example: Save layout data (you might want to add it to the user's floor plan)
            layout_data = {'num_rooms': num_rooms, 'square_feet': square_feet, 'room': {'type': room_type, 'width': width, 'length': length}}

            # If needed, save layout_data to the FloorPlan model here

            return render(request, 'planner/design.html', {'design': design, 'materials': materials})

    else:
        # Initialize forms when request is GET
        home_plan_form = HomePlanForm()
        room_form = RoomForm()

    return render(request, 'home_planner/home_planner.html', {
        'home_plan_form': home_plan_form,
        'room_form': room_form,
        'materials': materials
    })

####




# Home page view
def home(request):
    return render(request, 'planner/home.html')

# About page view
def about(request):
    return render(request, 'planner/about.html')

# Contact page view
def contact(request):
    return render(request, 'planner/contact.html')

# Dashboard view (Requires login)

@login_required
def dashboard(request):
    # Fetch all the floor plans for the logged-in user
    floor_plans = FloorPlan.objects.filter(user=request.user)

    # Generate a floor plan image if the user has at least one floor plan
    if floor_plans.exists():  # Use .exists() instead of checking `if floor_plans:`
        layout_data = floor_plans[0].layout_data  # Use the first floor plan for 2D generation

        # Debug print to check the structure of layout_data
        print("Layout Data:", layout_data)

        # Ensure layout_data is a valid list of dictionaries
        if isinstance(layout_data, list) and all(isinstance(room, dict) for room in layout_data):
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.set_aspect('equal')

            current_y_position = 0  # Start at the top of the plot
            for room in layout_data:
                room_type = room.get('room_type', 'Room')
                width = room.get('width', 10)  # Default values if missing
                length = room.get('length', 10)

                # Draw rectangle (room) on the plot
                ax.add_patch(plt.Rectangle((0, current_y_position), width, length, fill=None, edgecolor='blue'))
                ax.text(width / 2, current_y_position + length / 2, room_type, 
                        horizontalalignment='center', verticalalignment='center')

                # Update the y position for the next room
                current_y_position += length

            ax.autoscale()
            ax.set_xticks([])
            ax.set_yticks([])

            # Save the floor plan as an image in memory
            image_stream = BytesIO()
            plt.savefig(image_stream, format='png')
            plt.close(fig)  # Close the figure to free memory
            image_stream.seek(0)

            # Convert the image to base64 for embedding in the template
            image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
            image_data = f"data:image/png;base64,{image_base64}"

            return render(request, 'planner/dashboard.html', {
                'floor_plans': floor_plans,
                'image_data': image_data  # Pass image as a base64 string
            })

    # If no valid plans, just render the template
    return render(request, 'planner/dashboard.html', {'floor_plans': floor_plans})

# Add room to floor plan
@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room_type = form.cleaned_data['room_type']
            width = form.cleaned_data['width']
            length = form.cleaned_data['length']

            # Example layout_data (could be more complex depending on your requirements)
            layout_data = {
                'room_type': room_type,
                'width': width,
                'length': length
            }

            # Get or create the floor plan for the user
            floor_plan, created = FloorPlan.objects.get_or_create(
                user=request.user,
                defaults={'plan_name': 'My Floor Plan', 'layout_data': [layout_data]}
            )

            # If the floor plan already exists, update the layout_data
            if not created:
                floor_plan.layout_data.append(layout_data)
                floor_plan.save()

            return redirect('dashboard')  # Redirect to the user's dashboard
    else:
        form = RoomForm()

    return render(request, 'planner/add_room.html', {'form': form})

# Save floor plan to the database (No longer used, since we're saving in the add_room view)
def save_floor_plan(request, layout_data):
    floor_plan = FloorPlan.objects.create(
        user=request.user,
        plan_name="My Floor Plan",  # You can also make this dynamic based on user input
        layout_data=layout_data
    )
    return floor_plan

# View a specific floor plan by its ID
def view_plan(request, plan_id):
    # Get the specific floor plan by its ID
    plan = FloorPlan.objects.get(id=plan_id)
    return render(request, 'planner/view_plan.html', {'plan': plan})


########
######


# User Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
