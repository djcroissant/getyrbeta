'''
test that the expected fields are listed, labeled, and help texted
'''

from django.test import TestCase

from account_info.forms import ProfileForm

class ProfileFormTests(TestCase):
    def test_full_name_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['full_name'].label, 'Full name')

    def test_preferred_name_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['preferred_name'].label, 'Preferred name')

    def test_primary_phone_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['primary_phone'].label, 'Primary phone')

    def test_secondary_phone_field_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields['secondary_phone'].label, 'Secondary phone')

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
