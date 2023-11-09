import dataclasses
from abc import ABC, abstractmethod
from typing import Optional

import requests


@dataclasses.dataclass
class SellBuy:
    sell: Optional[float]
    buy: Optional[float]


class RateNotFound(Exception):
    pass


class ProviderBase(ABC):
    name = None

    def __init__(self, currency_from: str, currency_to: str):
        self.currency_from = currency_from
        self.currency_to = currency_to

    @abstractmethod
    def get_rate(self) -> SellBuy:
        pass


class MonoProvider(ProviderBase):
    name = "monobank"

    iso_from_country_code = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    def get_rate(self) -> SellBuy:
        url = "https://api.monobank.ua/bank/currency"
        response = requests.get(url)
        response.raise_for_status()

        currency_from_code = self.iso_from_country_code[self.currency_from]
        currency_to_code = self.iso_from_country_code[self.currency_to]

        for currency in response.json():
            if (
                currency["currencyCodeA"] == currency_from_code
                and currency["currencyCodeB"] == currency_to_code
            ):
                value = SellBuy(
                    sell=float(currency["rateSell"]),
                    buy=float(currency["rateBuy"]),
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to "
            + f"{self.currency_to} in provider {self.name}"
        )


class PrivatbankProvider(ProviderBase):
    name = "privatbank"

    def get_rate(self) -> SellBuy:
        url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"
        response = requests.get(url)
        response.raise_for_status()
        for currency in response.json():
            if (
                currency["ccy"] == self.currency_from
                and currency["base_ccy"] == self.currency_to
            ):
                value = SellBuy(
                    buy=float(currency["buy"]), sell=float(currency["sale"])
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to"
            + f" {self.currency_to} in provider {self.name}"
        )


class VKurseProvider(ProviderBase):
    name = "vkurse"

    def get_rate(self) -> SellBuy:
        url = "https://vkurse.dp.ua/course.json"
        response = requests.get(url)
        response.raise_for_status()

        if self.currency_from == "USD":
            value = SellBuy(
                buy=float(response.json()["Dollar"]["buy"]),
                sell=float(response.json()["Dollar"]["sale"]),
            )
        elif self.currency_from == "EUR":
            value = SellBuy(
                buy=float(response.json()["Euro"]["buy"]),
                sell=float(response.json()["Euro"]["sale"]),
            )
        else:
            raise RateNotFound(
                f"Cannot find rate for {self.currency_from} "
                + f"in provider {self.name}"
            )
        return value


class BankGovProvider(ProviderBase):
    name = "bank_gov"

    def get_rate(self) -> SellBuy:
        url = (
            "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        )
        response = requests.get(url)
        response.raise_for_status()

        for currency in response.json():
            if currency["cc"] == self.currency_from:
                value = SellBuy(
                    sell=None,
                    buy=float(currency["rate"]),
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to "
            + f"{self.currency_to} in provider {self.name}"
        )


class MinFinProvider(ProviderBase):
    name = "minfin"

    def get_rate(self) -> SellBuy:
        url = "https://api.minfin.com.ua/mb/113034f214e94c9cc053e8a498afb02e47a1c1f8/"
        response = requests.get(url)
        response.raise_for_status()

        for currency in response.json():
            if (
                currency["currency"].lower() == self.currency_to.lower()
                and currency["currency"].lower() == self.currency_from.lower()
            ):
                value = SellBuy(
                    sell=float(currency["ask"]),
                    buy=float(currency["bid"]),
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to "
            + f"{self.currency_to} in provider {self.name}"
        )


PROVIDERS = [
    MonoProvider,
    PrivatbankProvider,
    VKurseProvider,
    MinFinProvider,
    BankGovProvider,
]
