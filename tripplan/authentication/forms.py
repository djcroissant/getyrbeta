from allauth.account import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions, PrependedText


class LoginForm(forms.LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['login'].label = ''
        self.fields['password'].label = ''
        self.helper.layout = Layout (
            PrependedText('login', '<i class="fa fa-envelope-o" aria-hidden="true"></i>', placeholder="E-mail address"),
            PrependedText('password', '<i class="fa fa-lock" aria-hidden="true"></i>', placeholder="Password"),
            'remember',
            FormActions(
                Submit('submit', 'Sign In', css_class="btn btn-primary click-disable"),
                HTML('<a class="button secondaryAction" href="/accounts/password/reset/">Forgot Password?</a>')
            )
        )

class SignupForm(forms.SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.helper.layout = Layout (
            PrependedText('email', '<i class="fa fa-envelope-o" aria-hidden="true"></i>', placeholder="E-mail address"),
            PrependedText('password1', '<i class="fa fa-lock" aria-hidden="true"></i>', placeholder="Password"),
            HTML('<input type="checkbox" id="id_show_password" onchange=\'document.getElementById("id_password1").type = this.checked ? "text" : "password"\'>'),
            HTML('<label for="id_show_password">Show password</label>'),
            FormActions(
                Submit('submit', 'Sign Up', css_class="btn btn-primary click-disable"),
            ),
        )
