from django import forms


class UserInputForm(forms.Form):
    choices = [("USD", "USD"), ("EUR", "EUR")]
    currency_to = forms.ChoiceField(label="Currency to", choices=choices)
    amount = forms.FloatField(label="Quantity", min_value=0, step_size=0.1)

    def __init__(self, *args, **kwargs):
        initial_currencies = kwargs.pop("initial", None)
        super(UserInputForm, self).__init__(*args, **kwargs)
        if initial_currencies:
            currencies_to = [
                currency for currency in initial_currencies["currencies_to"]
            ]
            self.fields["currency_to"].choices = currencies_to
