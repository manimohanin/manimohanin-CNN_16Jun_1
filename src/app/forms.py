from django import forms
from django.contrib.auth.forms import AuthenticationForm


class ImageTestForm(forms.Form):
    """Image upload form."""
    test_image = forms.ImageField()