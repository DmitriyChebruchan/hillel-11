from django.http import JsonResponse
from django.shortcuts import render

from .forms import UserInputForm
from .models import Rate
from .supporting_functions import result_calculator, info_dict_generator


def main_view(request):
    """View showing rate of exchange"""

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
    """View with exchange calculator"""

    info_dict = info_dict_generator()
    if request.method == "POST":
        posted_form = UserInputForm(request.POST)
        if posted_form.is_valid():
            info_dict["quantity"] = result_calculator(posted_form)
        else:
            info_dict["errors"] = posted_form.errors
        return render(request, "exchange_window.html", info_dict)

    return render(request, "exchange_window.html", info_dict)
