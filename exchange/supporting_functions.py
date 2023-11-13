from django.utils import timezone

from exchange.forms import UserInputForm
from exchange.models import Rate


def result_calculator(posted_form):
    required_currency_to = posted_form.cleaned_data["currency_to"]

    lowest_rate = (
        Rate.objects.filter(
            date=timezone.now().date(),
            currency_from=required_currency_to,
        )
        .order_by("sell")
        .first()
    )
    provider = lowest_rate.provider

    if not lowest_rate:
        print("No lowest_rate found.")
        return "No rate is found today."

    required_amount = posted_form.cleaned_data["amount"]
    result_amount = round(
        float(required_amount) * float(lowest_rate.sell),
        2,
    )

    result = (
        f"To buy {required_amount} of {required_currency_to} "
        + f"you will need {result_amount} of UAH. The provider is "
        f'"{provider}".'
    )
    return result


def info_dict_generator(curr_to=None):
    if curr_to is None:
        curr_to = ["USD", "EUR"]

    currencies_to = currency_normalizer(curr_to)
    form = UserInputForm(
        initial={
            "currencies_to": currencies_to,
        }
    )
    info_dict = {"form": form}
    return info_dict


def currency_normalizer(currencies):
    return [(currency, currency) for currency in currencies]
