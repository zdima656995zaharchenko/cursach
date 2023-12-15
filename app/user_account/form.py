from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

class UserSignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('email', css_class='form-control'),
            Field('password1', css_class='form-control'),
            Field('password2', css_class='form-control'),
            Submit('submit', 'Sign Up', css_class='btn btn-primary')
        )

    def clean(self):
        cleaned_data: dict = super().clean()

        if not self.errors:
            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError('Passwords should match!')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.set_password(self.cleaned_data['password1'])
        instance.is_active = False

        instance.save()
        self._send_mail()
        return instance

    def _send_mail(self):
        activate_path = reverse('user_account:activate', args=[self.instance.username])
        subject = 'Thanks for signing up!'
        body = f'''
        {settings.HTTP_PROTOCOL}://{settings.DOMAIN}/{activate_path}
        '''
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [self.instance.email],
            fail_silently=False
        )