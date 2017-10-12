# from django import forms
import floppyforms.__future__ as forms

from account_info.models import User

from .models import Trip, TripLocation

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Field
from crispy_forms.bootstrap import FormActions


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
        fields = ['title', 'date', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(LocationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-LocationForm'
        self.helper.form_class = 'trip_forms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.field_class = 'col-md-9'
        self.fields['title'].label = 'Description'
        self.fields['date'].label = 'Date'
        self.fields['date'] = forms.ChoiceField(choices=choices)
        self.helper.layout = Layout (
            Fieldset(
                '',
                'title',
                'date',
                'latitude',
                'longitude'),
            FormActions(
                Submit('submit', '{{ submit_button_title }}', css_class='btn btn-success btn-lg'),
                HTML('<a class="btn btn-secondary" href="{% url cancel_button_path trip_id %}" name="cancel">Cancel</a>')
            )
        )
