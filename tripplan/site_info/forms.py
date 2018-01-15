from django import forms
from django.contrib.auth import get_user_model

from account_info.models import Vehicle, EmergencyContact

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, MultiField, Field
from crispy_forms.bootstrap import FormActions

class ContactForm(forms.Form):

    class Meta:
        fields = ['name', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_id = 'id-ProfileForm'
        # self.helper.form_class = 'account_info_forms'
        self.helper.form_method = 'post'
        # self.helper.form_action = ''
        # self.helper.field_class = '6u 12u(mobilep)'
        self.fields['name'].label = False
        self.fields['email'].label = False
        self.fields['subject'].label = False
        self.fields['message'].label = False
        self.helper.layout = Layout (
            Div(
                Field(
                    'name',
                    id='name',
                    value='',
                    placeholder='Name',
                    wrapper_class='6u 12u(mobilep)',
                ),
                Field(
                    'email',
                    id='email',
                    value='',
                    placeholder='Email',
                    wrapper_class='6u 12u(mobilep)',
                ),
                css_class='row uniform 50%',
            ),
            Div(
                Field(
                    'subject',
                    id='subject',
                    value='',
                    placeholder='Subject',
                    wrapper_class='12u',
                ),
                css_class='row uniform 50%',
            ),
            Div(
                Field(
                    'message',
                    id='message',
                    value='',
                    placeholder='Message',
                    wrapper_class='12u',
                ),
                css_class='row uniform 50%',
            )
        )



    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=255, required=True)
    subject = forms.CharField(max_length=255, required=True)
    message = forms.CharField(
        max_length=1023,
        required=True,
        widget=forms.Textarea
    )

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


        # self.helper.layout = Layout(
        #     MultiField(
        #         '',
        #         'name'
        #         # Div(
        #         #     Div(
        #         #         'name'
        #         #     ),
        #         # ),
        #     )
        # )


        #     Div(
        #         css_class='row uniform 50%',
        #         Div(
        #             css_class='6u 12u(mobilep)',
        #         #     Field(
        #         #         'name',
        #         #         id='name',
        #         #         value='',
        #         #         placeholder='Name'
        #         #     )
        #         ),
        #     ),
        # )


        #     'full_name',
        #     'preferred_name',
        #     'relationship',
        #     'primary_phone',
        #     'secondary_phone',
        #     'street_address_line1',
        #     'street_address_line2',
        #     'city',
        #     'state',
        #     'zip_code',
        #     FormActions(
        #         Submit('submit', '{{ save_button_title }}', css_class='btn btn-success btn-lg click-disable'),
        #         HTML('<a class="btn btn-secondary" href="{% url cancel_button_path %}" name="cancel">Cancel Changes</a>')
        #     )
        # )
# class EmergencyContactForm(forms.ModelForm):
#     class Meta:
#         model = EmergencyContact
#         fields = ['full_name', 'preferred_name', 'relationship',
#             'primary_phone', 'secondary_phone', 'street_address_line1',
#             'street_address_line2', 'city', 'state', 'zip_code']
#
#     def __init__(self, *args, **kwargs):
#         super(EmergencyContactForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-EmergencyContactForm'
#         self.helper.form_class = 'account_info_forms'
#         self.helper.form_method = 'post'
#         self.helper.form_action = ''
#         self.helper.field_class = 'col-md-9'
#         self.fields['primary_phone'].label = "Phone (primary)"
#         self.fields['secondary_phone'].label = "Phone (secondary)"
#         self.fields['street_address_line1'].label = "Address 1"
#         self.fields['street_address_line2'].label = "Address 2"
#         self.fields['zip_code'].label = "ZIP code"
#         self.helper.layout = Layout (
#             Fieldset(
#                 '',
#                 'full_name',
#                 'preferred_name',
#                 'relationship',
#                 'primary_phone',
#                 'secondary_phone',
#                 'street_address_line1',
#                 'street_address_line2',
#                 'city',
#                 'state',
#                 'zip_code'),
#             FormActions(
#                 Submit('submit', '{{ save_button_title }}', css_class='btn btn-success btn-lg click-disable'),
#                 HTML('<a class="btn btn-secondary" href="{% url cancel_button_path %}" name="cancel">Cancel</a>')
#             )
#         )
#
# class VehicleForm(forms.ModelForm):
#
#     class Meta:
#         model = Vehicle
#         fields = ['make', 'model', 'color', 'year', 'lic_plate_num',
#             'lic_plate_st']
#
#     def __init__(self, *args, **kwargs):
#         super(VehicleForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-VehicleForm'
#         self.helper.form_class = 'account_info_forms'
#         self.helper.form_method = 'post'
#         self.helper.form_action = ''
#         self.helper.field_class = 'col-md-9'
#         self.fields['lic_plate_num'].label = "License plate number"
#         self.fields['lic_plate_st'].label = "License plate state"
#         self.helper.layout = Layout (
#             Fieldset(
#                 '',
#                 'make',
#                 'model',
#                 'color',
#                 'year',
#                 'lic_plate_num',
#                 'lic_plate_st'),
#             FormActions(
#                 Submit('submit', '{{ save_button_title }}', css_class='btn btn-success btn-lg click-disable'),
#                 HTML('<a class="btn btn-secondary" href="{% url cancel_button_path %}" name="cancel">Cancel</a>')
#             )
#         )
