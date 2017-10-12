from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.template import engines, Context, Template

from trips.forms import TripForm, LocationForm
from trips.models import Trip, TripLocation

'''
Current testing checks that all fields are listed and labeled correctly.
'''

class TripFormTests(TestCase):
    def test_title_field_label(self):
        form = TripForm()
        self.assertEqual(form.fields['title'].label, 'Trip Title')

    def test_number_nights_field_label(self):
        form = TripForm()
        self.assertEqual(form.fields['number_nights'].label, 'Number')

    def test_number_nights_field_label(self):
        form = TripForm()
        self.assertEqual(form.fields['start_date'].label, 'Start date')

    def test_form_id(self):
        form = TripForm()
        self.assertEqual(form.helper.form_id, 'id-TripForm')

    def test_form_class(self):
        form = TripForm()
        self.assertEqual(form.helper.form_class, 'trip_forms')

    def test_form_method(self):
        form = TripForm()
        self.assertEqual(form.helper.form_method, 'post')

    def test_form_action(self):
        form = TripForm()
        self.assertEqual(form.helper.form_action, '')

    def test_form_field_class(self):
        form = TripForm()
        self.assertEqual(form.helper.field_class, 'col-md-9')

    def test_submit_cancel_form_actions(self):
        """
        Test the existence of submit/cancel buttons
        """
        template = engines['django'].from_string("""
        {% load crispy_forms_tags %}
            {% crispy form %}
        """)
        form = TripForm()
        context = {'form': form, 'cancel_button_path': 'welcome'}
        html = template.render(context)
        self.assertEqual(html.count('input type="submit"'), 1)
        self.assertEqual(html.count('name="cancel">Cancel</a>'), 1)

class LocationFormTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.trip = Trip.objects.create(
            title='title',
            start_date=timezone.now().date(),
            number_nights=1
        )

    def test_title_field_label(self):
        kwargs={'choices': 'fake'}
        form = LocationForm(**kwargs)
        self.assertEqual(form.fields['title'].label, 'Description')

    def test_date_field_label(self):
        kwargs={'choices': 'fake'}
        form = LocationForm(**kwargs)
        self.assertEqual(form.fields['date'].label, None)

    def test_latitude_field_label(self):
        kwargs={'choices': 'fake'}
        form = LocationForm(**kwargs)
        self.assertEqual(form.fields['latitude'].label, 'Latitude')

    def test_longitude_field_label(self):
        kwargs={'choices': 'fake'}
        form = LocationForm(**kwargs)
        self.assertEqual(form.fields['longitude'].label, 'Longitude')

    def test_form_id(self):
        kwargs={'choices': 'fake'}
        form = LocationForm(**kwargs)
        self.assertEqual(form.helper.form_id, 'id-LocationForm')

    def test_form_class(self):
        kwargs={'choices': 'fake'}
        form = LocationForm(**kwargs)
        self.assertEqual(form.helper.form_class, 'trip_forms')

    def test_form_method(self):
        kwargs={'choices': 'fake'}
        form = LocationForm(**kwargs)
        self.assertEqual(form.helper.form_method, 'post')

    def test_form_action(self):
        kwargs={'choices': 'fake'}
        form = LocationForm(**kwargs)
        self.assertEqual(form.helper.form_action, '')

    def test_form_field_class(self):
        kwargs={'choices': 'fake'}
        form = LocationForm(**kwargs)
        self.assertEqual(form.helper.field_class, 'col-md-9')

    def test_submit_cancel_form_actions(self):
        """
        Test the existence of submit/cancel buttons
        """
        template = engines['django'].from_string("""
        {% load crispy_forms_tags %}
            {% crispy form %}
        """)
        kwargs={'choices': (('fake', 'fake'),)}
        form = LocationForm(**kwargs)
        context = {'form': form, 'cancel_button_path': 'trips:trip_detail', 'trip_id': self.trip.id}
        html = template.render(context)
        self.assertEqual(html.count('input type="submit"'), 1)
        self.assertEqual(html.count('name="cancel">Cancel</a>'), 1)
