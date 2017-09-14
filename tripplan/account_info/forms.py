from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['full_name', 'preferred_name', 'primary_phone',
            'secondary_phone', 'street_address_line1', 'street_address_line2',
            'city', 'state', 'zip_code']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['street_address_line1'].label = "Address 1"
        self.fields['street_address_line2'].label = "Address 2"
        self.fields['zip_code'].label = "ZIP code"
