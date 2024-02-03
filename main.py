import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta

class CurrencyRates:
    API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date={}"

    async def fetch_data(self, date):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.API_URL.format(date)) as response:
                return await response.json()

    async def get_currency_rates(self, days):
        rates = []
        current_date = datetime.now()

        for day in range(days):
            target_date = current_date - timedelta(days=day)
            formatted_date = target_date.strftime("%d.%m.%Y")

            try:
                data = await self.fetch_data(formatted_date)
                rates.append({
                    formatted_date: {
                        'EUR': {
                            'sale': data['exchangeRate'][0]['saleRateNB'],
                            'purchase': data['exchangeRate'][0]['purchaseRateNB']
                        },
                        'USD': {
                            'sale': data['exchangeRate'][19]['saleRateNB'],
                            'purchase': data['exchangeRate'][19]['purchaseRateNB']
                        }
                    }
                })
            except Exception as e:
                print(f"Error fetching data for {formatted_date}: {e}")

        return rates

async def main():
    parser = argparse.ArgumentParser(description='Get currency rates from PrivatBank API.')
    parser.add_argument('days', type=int, help='Number of days to retrieve currency rates for (up to 10 days).')
    args = parser.parse_args()

    if args.days > 10:
        print("Error: Maximum number of days allowed is 10.")
        return

    currency_rates = CurrencyRates()
    rates = await currency_rates.get_currency_rates(args.days)
    print(rates)

if __name__ == "__main__":
    asyncio.run(main)
