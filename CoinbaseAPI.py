import cbpro
import json
import datetime
import time

class CoinbaseAPI:

    public_clinet = None

    def __init__(self):
        print("Coinbase API Initiated")
        self.public_client = cbpro.PublicClient()

    # [ time, low, high, open, close, volume ],
    def getCoinHistoricData(self,coin_pair,start,end,granularity):
        print("> Collecting historic data for "+coin_pair," from ",start," to ",end," every ",granularity," sec")

        data = []
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")

        while (start_date <= end_date):
            print("> Date: ",start_date)
            start_limit = start_date
            end_limit = start_date + datetime.timedelta(hours=1)

            reversed_response = [] # Put in correct date order
            next_data = self.public_client.get_product_historic_rates(coin_pair, granularity=granularity,start=start_limit,end=end_limit)
            #print(self.public_client.get_products())
            for nd in next_data:
                reversed_response.append(nd)

            data.append(list(reversed(reversed_response)))
            start_date += datetime.timedelta(minutes=61)
            time.sleep(3)

        return data

    # [ time, low, high, open, close, volume ],

    """
    time - bucket start time
    low - lowest price during the bucket interval
    high - highest price during the bucket interval
    open - opening price (first trade) in the bucket interval
    close - closing price (last trade) in the bucket interval
    volume - volume of trading activity during the bucket interval
    """
    def getCoinCurrentData(self,coin_pair):
        data = self.public_client.get_product_historic_rates(coin_pair, granularity=60, start=datetime.datetime.today())

        return data