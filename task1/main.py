import platform
import aiohttp

import asyncio
import sys

from parametr import (
    get_period_from_concole as days,
    get_period_list_for_url as days_list,
    get_currenc as currencies,
)
from base import BASE_URL


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


async def adapt_responses_data(responses_data, currencies):
    adapted_data = []
    for respons in responses_data:
        adapted_data.append(
            {
                respons["date"]: {
                    rate["currency"]: {
                        "sale": rate["saleRateNB"],
                        "purchase": rate["purchaseRateNB"],
                    }
                    for rate in respons["exchangeRate"]
                    if rate["currency"] in currencies
                }
            }
        )
    print(adapted_data)


async def main():
    period = days_list(days(sys.argv))
    currenc = currencies(sys.argv)
    print(currenc)
    exchange_rates = await get_exchange_rates_for_days(period)
    await adapt_responses_data(exchange_rates, currenc)


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

