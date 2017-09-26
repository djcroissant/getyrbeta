from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.template import engines, Context, Template

from account_info.forms import ProfileForm, EmergencyContactForm, VehicleForm
from account_info.models import EmergencyContact

# from crispy_forms.tests.forms import TestForm
# from crispy_forms.tests.layout import Layout

User = get_user_model()

'''
Testing checks that all fields are listed and labeled correctly. Future testing
will check that help text is displayed correctly
'''

class ProfileFormTests(TestCase):
    def test_full_name_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['full_name'].label, 'Full name')

    def test_preferred_name_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['preferred_name'].label, 'Preferred name')

    def test_primary_phone_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['primary_phone'].label, 'Phone (primary)')

    def test_secondary_phone_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['secondary_phone'].label, 'Phone (secondary)')

    def test_street_address_line_1_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['street_address_line1'].label, 'Address 1')

    def test_street_address_line_2_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['street_address_line2'].label, 'Address 2')

    def test_city_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['city'].label, 'City')

    def test_state_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['state'].label, 'State')

    def test_zip_code_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['zip_code'].label, 'ZIP code')

class EmergencyContactFormTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_primary_phone_field_label(self):
        form = EmergencyContactForm()
        self.assertEqual(form.fields['primary_phone'].label, 'Phone (primary)')

    def test_secondary_phone_field_label(self):
        form = EmergencyContactForm()
        self.assertEqual(form.fields['secondary_phone'].label, 'Phone (secondary)')

    def test_street_address_line_1_field_label(self):
        form = EmergencyContactForm()
        self.assertEqual(form.fields['street_address_line1'].label, 'Address 1')

    def test_street_address_line_2_field_label(self):
        form = EmergencyContactForm()
        self.assertEqual(form.fields['street_address_line2'].label, 'Address 2')

    def test_zip_code_field_label(self):
        form = EmergencyContactForm()
        self.assertEqual(form.fields['zip_code'].label, 'ZIP code')

    # def test_valid_data(self):
    #     ec = EmergencyContact.objects.create(full_name='Don Gately',
    #         relationship='Buddy', user = self.user)
    #     request = self.factory.post('/fake/')
    #     request.user = self.user
    #     form = EmergencyContactForm(request.POST, instance=ec)
    #     self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = EmergencyContactForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'full_name': ['This field is required.'],
            'relationship': ['This field is required.'],
        })

    def test_form_id(self):
        form = EmergencyContactForm()
        self.assertEqual(form.helper.form_id, 'id-EmergencyContactForm')

    def test_form_class(self):
        form = EmergencyContactForm()
        self.assertEqual(form.helper.form_class, 'account_info_forms')

    def test_form_method(self):
        form = EmergencyContactForm()
        self.assertEqual(form.helper.form_method, 'post')

    def test_form_action(self):
        form = EmergencyContactForm()
        self.assertEqual(form.helper.form_action, '')

    def test_form_field_class(self):
        form = EmergencyContactForm()
        self.assertEqual(form.helper.field_class, 'col-md-9')

    def test_submit_cancel_form_actions(self):
        """
        Test the existence of submit/cancel buttons
        """
        template = engines['django'].from_string("""
        {% load crispy_forms_tags %}
            {% crispy form %}
        """)
        form = EmergencyContactForm()
        context = {'form': form, 'cancel_button_path': 'welcome'}
        html = template.render(context)
        self.assertEqual(html.count('input type="submit"'), 1)
        self.assertEqual(html.count('name="cancel">Cancel</a>'), 1)

class VehicleFormTests(TestCase):
    def test_lic_plate_num_field_label(self):
        form = VehicleForm()
        self.assertEqual(form.fields['lic_plate_num'].label, 'License plate number')

    def test_lic_plate_st_field_label(self):
        form = VehicleForm()
        self.assertEqual(form.fields['lic_plate_st'].label, 'License plate state')

    def test_blank_data(self):
        form = EmergencyContactForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'full_name': ['This field is required.'],
            'relationship': ['This field is required.'],
        })

    def test_form_id(self):
        form = VehicleForm()
        self.assertEqual(form.helper.form_id, 'id-VehicleForm')

    def test_form_class(self):
        form = VehicleForm()
        self.assertEqual(form.helper.form_class, 'account_info_forms')

    def test_form_method(self):
        form = VehicleForm()
        self.assertEqual(form.helper.form_method, 'post')

    def test_form_action(self):
        form = VehicleForm()
        self.assertEqual(form.helper.form_action, '')

    def test_form_field_class(self):
        form = VehicleForm()
        self.assertEqual(form.helper.field_class, 'col-md-9')

    def test_submit_cancel_form_actions(self):
        """
        Test the existence of submit/cancel buttons
        """
        template = engines['django'].from_string("""
        {% load crispy_forms_tags %}
            {% crispy form %}
        """)
        form = VehicleForm()
        context = {'form': form, 'cancel_button_path': 'welcome'}
        html = template.render(context)
        self.assertEqual(html.count('input type="submit"'), 1)
        self.assertEqual(html.count('name="cancel">Cancel</a>'), 1)
