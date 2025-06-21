from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []

class OrderCloseForm(forms.Form):
    confirm_close = forms.BooleanField(
        required=True,
        label="Confirm closing the order"
    )
