import requests


class Convertor(object):

    def __init__(self):
        url = 'https://api.exchangerate-api.com/v4/latest/EUR'
        self.data = requests.get(url).json()
        self.currency = self.data['rates']

    def convert(self, _from, to, amount):
        amount_to_convert = amount

        try:
            if _from != 'EUR':  # Takes EURO as based currency
                amount = amount / self.currency[_from]

            amount = round(amount * self.currency[to], 2)  # Limits to 2 decimal places
            return amount

        except:
            return "PLEASE SELECT AN PROPER CURRENCY!"


run = Convertor()
process = run.convert("HUF", "TRY", 100)
print('CONVERTED: {}'.format(process))
