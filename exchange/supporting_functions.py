from exchange.forms import UserInputForm


def result_calculator(posted_form):
    return posted_form.cleaned_data["amount"] * 2


def info_dict_generator(curr_from=None, curr_to=None):
    if curr_to is None:
        curr_to = ["USD", "EURO", "GBP"]
    if curr_from is None:
        curr_from = ["USD", "EURO", "GBP"]

    currencies_from = currency_normalizer(curr_from)
    currencies_to = currency_normalizer(curr_to)
    form = UserInputForm(
        initial={
            "currencies_from": currencies_from,
            "currencies_to": currencies_to,
        }
    )
    info_dict = {"form": form}
    return info_dict


def currency_normalizer(currencies):
    return [(currency, currency) for currency in currencies]
