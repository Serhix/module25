from datetime import datetime, timedelta
from base import BASE_CURRENC, AVAILABLE_CURRENC


def get_period_from_concole(consol_args):
    """
    args:
        consol_args: аргументи з консолі
    return:
        int: кількість днів для періоду запитів
    """
    if len(consol_args) > 1:
        try:
            period = int(consol_args[1])
        except ValueError:
            period = 1
    if not 0 < period <= 10:
        print("Information can be obtained only for the last 10 days")
        period = 1
    return period


def get_period_list_for_url(days: int) -> list:
    """
    args:
        days: число отримане з консолі, валідоване фугкцією get_period_from_concole
    return:
        list: писок параметрів дати для запитів
    """
    return [
        datetime.strftime(datetime.now() - timedelta(days=day), "%d.%m.%Y")
        for day in range(days)
    ]


def get_currenc(consol_args):
    """
    args:
        consol_args: аргументи з консолі
    return:
        set: множина параметрів валют для запитів
    """
    args = consol_args[2:]
    currencies = BASE_CURRENC
    [currencies.append(arg) for arg in args if arg in AVAILABLE_CURRENC]
    return set(currencies)
