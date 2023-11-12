from django.http import HttpResponse
from django.utils import timezone

from exchange.forms import UserInputForm
from exchange.models import Rate


def result_calculator(posted_form):
    required_currency_to = posted_form.cleaned_data["currency_to"]

    # rates = (
    #     Rate.objects.filter(date=timezone.now().date()).order_by("sell").first()
    # )
    # to do CORRECT BELOW LOWERS RATE
    lowest_rate = (
        Rate.objects.filter(
            date=timezone.now().date(),
            currency_to=required_currency_to,
        )
        .order_by("sell")
        .first()
    )

    if not lowest_rate:
        print("Not lowest_rate")
        return HttpResponse("No rate is found today")

    result = str(
        round(
            float(posted_form.cleaned_data["amount"]) * float(lowest_rate.sell),
            2,
        )
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
