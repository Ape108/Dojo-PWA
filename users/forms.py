from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    """
    Custom signup form to ensure the username is a required field.
    """
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(required=True, label='Username')

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)
        return user 