import aiohttp
import asyncio

from parametr import (
    get_period_from_concole as days,
    get_period_list_for_url as days_list,
    get_currenc as currencies,
)
from base import BASE_URL, BASE_CURRENC


async def request_to_pb(date: str):
    params = {"date": date}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error status: {response.status} for {response.url}")
        except aiohttp.ClientConnectionError as e:
            print(f"Connection error {response.url}: {e}")


async def get_exchange_rates_for_days(days):
    tasks = [request_to_pb(day) for day in days]
    return await asyncio.gather(*tasks, return_exceptions=True)


async def adapt_responses_data(responses_data, currencies=BASE_CURRENC):
    message = []
    for respons in responses_data:
        message.append('\n'.join([f'{respons["date"]}:\n {rate["currency"]}: sale: {rate["saleRateNB"]} purchase: {rate["purchaseRateNB"]}'
             for rate in respons["exchangeRate"]
             if rate["currency"] in currencies]))
    return '\n'.join(message)


async def main(message: str):
    period = days_list(days(message.split()))
    currenc = currencies(message.split())
    exchange_rates = await get_exchange_rates_for_days(period)
    return await adapt_responses_data(exchange_rates, currenc)
