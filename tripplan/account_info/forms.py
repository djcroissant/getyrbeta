from django import forms
from django.contrib.auth import get_user_model

from account_info.models import Vehicle, EmergencyContact

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from crispy_forms.bootstrap import FormActions

User = get_user_model()

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['full_name', 'preferred_name', 'primary_phone',
            'secondary_phone', 'street_address_line1', 'street_address_line2',
            'city', 'state', 'zip_code']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['primary_phone'].label = "Phone (primary)"
        self.fields['secondary_phone'].label = "Phone (secondary)"
        self.fields['street_address_line1'].label = "Address 1"
        self.fields['street_address_line2'].label = "Address 2"
        self.fields['zip_code'].label = "ZIP code"

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['full_name', 'preferred_name', 'relationship',
            'primary_phone', 'secondary_phone', 'street_address_line1',
            'street_address_line2', 'city', 'state', 'zip_code']

    def __init__(self, *args, **kwargs):
        super(EmergencyContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-EmergencyContactForm'
        self.helper.form_class = 'account_info_forms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.field_class = 'col-md-9'
        self.fields['primary_phone'].label = "Phone (primary)"
        self.fields['secondary_phone'].label = "Phone (secondary)"
        self.fields['street_address_line1'].label = "Address 1"
        self.fields['street_address_line2'].label = "Address 2"
        self.fields['zip_code'].label = "ZIP code"
        self.helper.layout = Layout (
            Fieldset(
                '',
                'full_name',
                'preferred_name',
                'relationship',
                'primary_phone',
                'secondary_phone',
                'street_address_line1',
                'street_address_line2',
                'city',
                'state',
                'zip_code'),
            FormActions(
                Submit('submit', '{{ save_button_title }}', css_class='btn btn-success btn-lg'),
                HTML('<a class="btn btn-secondary" href="{% url cancel_button_path %}" name="cancel">Cancel</a>')
            )
        )

class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'color', 'year', 'lic_plate_num',
            'lic_plate_st']

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-VehicleForm'
        self.helper.form_class = 'account_info_forms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.field_class = 'col-md-9'
        self.fields['lic_plate_num'].label = "License plate number"
        self.fields['lic_plate_st'].label = "License plate state"
        self.helper.layout = Layout (
            Fieldset(
                '',
                'make',
                'model',
                'color',
                'year',
                'lic_plate_num',
                'lic_plate_st'),
            FormActions(
                Submit('submit', '{{ save_button_title }}', css_class='btn btn-success btn-lg'),
                HTML('<a class="btn btn-secondary" href="{% url cancel_button_path %}" name="cancel">Cancel</a>')
            )
        )
