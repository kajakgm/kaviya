from django import forms

class RoomForm(forms.Form):
    room_type = forms.ChoiceField(choices=[('kitchen', 'Kitchen'), ('bedroom', 'Bedroom'), ('toilet', 'Toilet')])
    width = forms.FloatField()
    length = forms.FloatField()
class HomePlanForm(forms.Form):
    num_rooms = forms.IntegerField(min_value=1, label="Number of Rooms")
    square_feet = forms.FloatField(min_value=1, label="Total Square Footage")
