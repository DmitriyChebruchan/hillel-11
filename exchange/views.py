from django.http import JsonResponse
from django.shortcuts import render

from .forms import UserInputForm
from .models import Rate


def main_view(request):
    response_data = {
        "current_rates": [
            {
                "id": rate.id,
                "date": rate.date,
                "vendor": rate.provider,
                "currency_a": rate.currency_from,
                "currency_b": rate.currency_to,
                "sell": rate.sell,
                "buy": rate.buy,
            }
            for rate in Rate.objects.all()
        ]
    }
    return JsonResponse(response_data)


def exchange_window(request):
    # TODO: Method Post, grab information from sites
    currencies_from = ["USD", "EURO", "GBP"]
    currencies_to = ["USD", "EURO", "GBP"]
    form = UserInputForm(
        initial={
            "currencies_from": currencies_from,
            "currencies_to": currencies_to,
        }
    )
    info_dict = {"form": form}
    if request.method == "POST":
        lowest_rate = 2
        # revise below
        # posted_form = UserInputForm(request.POST)
        # info_dict["quantity"] = posted_form.cleaned_data["amount"] * lowest_rate
        return render(request, "exchange_window.html", info_dict)

    print(form)
    return render(request, "exchange_window.html", info_dict)
