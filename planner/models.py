#from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

#from django.db import models
#from django.contrib.auth.models import User

class FloorPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Unique floor plan per user
    plan_name = models.CharField(max_length=100, default="My Floor Plan")
    length = models.FloatField(default=0)  # Store the length of the house
    width = models.FloatField(default=0)   # Store the width of the house
    layout_data = models.JSONField(default=dict)  # Store room layout as JSON
    layout_image = models.ImageField(upload_to="floor_plans/", blank=True, null=True)  # Store 2D plan image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plan_name} ({self.user.username})"


