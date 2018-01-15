from django import forms
from django.core.mail import send_mail


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, ButtonHolder


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
            ),
            Div(
                ButtonHolder(
                    Submit(
                        'submit',
                        value='Send Message',
                        css_class='actions align-center',
                    ),
                    css_class='12u align-center',
                ),
                css_class='row uniform',
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
        # import pdb; pdb.set_trace()
        subject = "[GYB Contact] " + self.cleaned_data['subject']
        from_email = self.cleaned_data['email']
        to_email = ("derek.covey@gmail.com",)
        message = "Name: %s\nEmail: %s\n\n" % (
            self.cleaned_data['name'],
            from_email,
        )
        message += self.cleaned_data['message']

        send_mail(
            subject,
            message,
            from_email,
            to_email,
            fail_silently=False,
        )
