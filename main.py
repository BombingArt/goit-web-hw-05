import sys
import asyncio
import aiohttp
from datetime import datetime, timedelta
import json


async def fetch_currency_rates(days):
    async with aiohttp.ClientSession() as session:
        currency_rates = []
        for i in range(days):
            date = (datetime.today() - timedelta(days=i)).strftime("%d.%m.%Y")
            url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
            async with session.get(url) as response:
                data = await response.json()
                rates = {}
                for rate in data['exchangeRate']:
                    if rate['currency'] in ['USD', 'EUR']:
                        currency = rate['currency']
                        sale_rate = rate.get('saleRate', None)
                        purchase_rate = rate.get('purchaseRate', None)
                        rates[currency] = {"sale": sale_rate, "purchase": purchase_rate}
                currency_rates.append({date: rates})
        return currency_rates

async def main(days):
    currency_rates = await fetch_currency_rates(days)
    print('\nВідповідь:\n\n' + json.dumps(currency_rates, indent=2))


if __name__ == "__main__":
    try:
        days = int(sys.argv[1])
        if days > 10:
            print("Кількість днів не може перевищувати 10")
            sys.exit(1)
        print("Опрацювання...")
        asyncio.run(main(days))
    except (IndexError, ValueError):
        print("Використання: python main.py <кількість днів>")
