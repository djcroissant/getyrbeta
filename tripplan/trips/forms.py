# from django import forms
import floppyforms.__future__ as forms

from account_info.models import User

from .models import Trip, TripLocation, TripMember

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Field, Div
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'start_date', 'number_nights']

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-TripForm'
        self.helper.form_class = 'trip_forms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.field_class = 'col-md-9'
        self.fields['number_nights'].label = 'Number of Nights'
        self.fields['title'].label = 'Trip Title'
        self.helper.layout = Layout (
            Fieldset(
                '',
                'title',
                'start_date',
                'number_nights'),
            FormActions(
                Submit('submit', '{{ submit_button_title }}', css_class='btn btn-success btn-lg'),
                HTML('<a class="btn btn-secondary" href="{% url cancel_button_path %}" name="cancel">Cancel</a>')
            )
        )

class LocationForm(forms.ModelForm):
    class Meta:
        model = TripLocation
        fields = ['trip', 'location_type', 'title', 'date',
            'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(LocationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-LocationForm'
        self.helper.form_class = 'trip_forms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.fields['title'].label = 'Title for Trip Plan'
        self.fields['date'].label = 'Date'
        self.fields['date'] = forms.ChoiceField(choices=choices)
        self.helper.layout = Layout (
            Fieldset(
                '',
                'title',
                Div(
                    'latitude',
                    'longitude',
                    css_class='coordinate-fields'
                ),
                'date'),
            Field('trip', type='hidden'),
            Field('location_type', type='hidden'),
            FormActions(
                Submit('submit', '{{ submit_button_title }}', css_class='btn btn-success btn-lg'),
                HTML('<a class="btn btn-secondary" href="{% url cancel_button_path trip_id %}" name="cancel">Cancel</a>')
            )
        )

        latitude = forms.DecimalField(
            max_value=90,
            min_value=-90
        )

        latitude = forms.DecimalField(
            max_value=180,
            min_value=-180
        )

class SearchForm(forms.Form):
    class Meta:
        fields = ['email_search']

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'trip-member-search'
        self.helper.form_class = 'trip-forms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.field_class = 'search-field trip-info'
        self.helper.layout = Layout (
            FieldWithButtons('email_search', StrictButton("Search", css_class="btn-success", css_id="email-search-button"))
        )

    email_search = forms.EmailField(
        label='Enter email address below:',
        max_length=255,
        required=False
    )

class TripMemberForm(forms.ModelForm):
    class Meta:
        model = TripMember
        fields = []
