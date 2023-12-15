from django import forms
from .models import Source, ContactUs, Rate
from .choices import CurrencyChoices, SourceChoices
from django.contrib.auth.forms import PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['buy', 'sell', 'currency', 'source']

    source = forms.ModelChoiceField(
        queryset=Source.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Source'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('buy', css_class='form-control'),
            Field('sell', css_class='form-control'),
            Field('currency', css_class='form-control'),
            Field('source', css_class='form-control'),
            Submit('submit', 'Create', css_class='btn btn-primary')
        )
class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'reply_to', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('reply_to', css_class='form-control'),
            Field('subject', css_class='form-control'),
            Field('body', css_class='form-control'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['name', 'source_url', 'exchange_address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('source_url', css_class='form-control'),
            Field('exchange_address', css_class='form-control'),
            Field('phone_number', css_class='form-control'),
            Submit('submit', 'Create', css_class='btn btn-primary')
        )

class SupportForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=128)
    reply_to = forms.EmailField(label='Email для ответа')
    subject = forms.CharField(label='Тема', max_length=128)
    body = forms.CharField(label='Сообщение', widget=forms.Textarea)



class CustomPasswordChangeForm(PasswordChangeForm):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


