from django import forms

class CartQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=999, initial=1)

class NewsletterForm(forms.Form):
    email = forms.EmailField(max_length=254)
