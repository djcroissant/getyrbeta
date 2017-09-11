from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['full_name', 'preferred_name', 'primary_phone',
            'secondary_phone', 'street_address_line1', 'street_address_line2',
            'city', 'state', 'zip_code']
