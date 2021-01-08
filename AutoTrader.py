from VirtualAccount import VirtualAccount
import numpy as np
from Config import *
import time

class AutoTrader:

    def __init__(self,model):
        self.advisor = model
        self.account = VirtualAccount()
        self.trade_amount = 100

    def buy(self):
        prev_bought_at = self.account.bought_btc_at # How much did I buy BTC for before
        if self.account.usd_balance - self.trade_amount >= 0:
            if prev_bought_at == 0 or self.account.last_transaction_was_sell or (prev_bought_at > self.account.btc_price): #or (self.account.btc_price/prev_bought_at -1 > 0.005):
                print(">> BUYING $",self.trade_amount," WORTH OF BITCOIN")
                self.account.btc_amount += self.trade_amount / self.account.btc_price
                self.account.usd_balance -= self.trade_amount
                self.account.bought_btc_at = self.account.btc_price
                self.account.last_transaction_was_sell = False
            else:
                print(">> Not worth buying more BTC at the moment")
        else:
            print(">> Not enough USD left in your account to buy BTC ")

    def sell(self):
        if self.account.btc_balance - self.trade_amount >= 0:
            if self.account.btc_price > self.account.bought_btc_at: # Is it profitable?
                print(">> SELLING $",self.trade_amount," WORTH OF BITCOIN")
                self.account.btc_amount -= (self.trade_amount / self.account.btc_price)
                self.account.usd_balance += self.trade_amount
                self.account.last_transaction_was_sell = True
            else:
                print(">> Declining sale: Not profitable to sell BTC")
        else:
            print(">> Not enough BTC left in your account to buy USD ")

    def runSimulation(self,samples,prices):
        print("> Trading Automatically for ",TESTING_MONTHS)
        day_count = 0
        for i in range(0,len(samples)):

            if i % 24 == 0:
                day_count += 1
                print("#################################################################################################")
                print("#           Account Balance: $", (self.account.usd_balance + self.account.btc_balance), " BTC: $",
                      self.account.btc_balance, " USD: $", self.account.usd_balance, "")
                print("#################################################################################################")
                print("##########################################   DAY ",day_count,"   #########################################")


            if i % 6 == 0: # Perform a prediction every 6 hours
                prediction = self.advisor.predict(np.array([samples[i]]))
                #btc_price = samples[i][len(samples[i])-1]
                btc_price = prices[i]

                if self.account.btc_price != 0:
                    self.account.btc_balance = self.account.btc_amount * btc_price

                self.account.btc_price = btc_price

                if prediction == 1:
                    self.buy()
                else:
                    self.sell()

                self.account.btc_balance = self.account.btc_amount * btc_price

                time.sleep(1)  # Only for Visual Purposes

        print("#################################################################################################")
        print("#           Account Balance: $", (self.account.usd_balance + self.account.btc_balance), " BTC: $",
              self.account.btc_balance, " USD: $", self.account.usd_balance, "")
        print("#################################################################################################")