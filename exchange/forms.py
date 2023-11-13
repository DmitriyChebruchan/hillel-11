from django import forms
from django.core.exceptions import ValidationError


class UserInputForm(forms.Form):
    choices = [
        ("default", "Select currency"),
        ("USD", "USD"),
        ("EUR", "EUR"),
    ]
    currency_to = forms.ChoiceField(label="Currency to", choices=choices)
    amount = forms.FloatField(label="Quantity", min_value=0, step_size=0.01)

    def __init__(self, *args, **kwargs):
        initial_currencies = kwargs.pop("initial", None)
        super(UserInputForm, self).__init__(*args, **kwargs)
        if initial_currencies:
            currencies_to = [
                currency for currency in initial_currencies["currencies_to"]
            ]
            self.fields["currency_to"].choices = [
                ("default", "Select currency")
            ] + currencies_to

    def clean_currency_to(self):
        currency_to = self.cleaned_data.get("currency_to")

        # Check if the selected currency is the default option
        if currency_to == "default":
            raise ValidationError("Please select a valid currency.")

        return currency_to
