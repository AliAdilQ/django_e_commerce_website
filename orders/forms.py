from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    checkout_token = forms.UUIDField(widget=forms.HiddenInput)
    payment_method = forms.ChoiceField(choices=Order.Payment.choices, widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ("full_name", "email", "phone", "address", "city", "postal_code", "country", "payment_method")
        widgets = {"address": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        autocomplete = {"full_name": "name", "email": "email", "phone": "tel", "address": "street-address",
                        "city": "address-level2", "postal_code": "postal-code", "country": "country-name"}
        for name in autocomplete:
            self.fields[name].widget.attrs.update({"class": "form-control", "autocomplete": autocomplete[name]})

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if sum(c.isdigit() for c in phone) < 7:
            raise forms.ValidationError("Enter a phone number with at least 7 digits.")
        return phone
