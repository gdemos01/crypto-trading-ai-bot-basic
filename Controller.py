from Dataset import Dataset
from Model import Model
from Config import *
from AutoTrader import AutoTrader
import argparse
from CoinbaseAPI import CoinbaseAPI

if __name__ == '__main__':

    print("\n\n\n                   ,.=ctE55ttt553tzs.,                           \n",
          "              ,,c5;z==!!::::  .::7:==it3>.,                      \n",
          "           ,xC;z!::::::    ::::::::::::!=c33x,                   \n",
          "         ,czz!:::::  ::;;..===:..:::   ::::!ct3.                 \n",
          "       ,C;/.:: :  ;=c!:::::::::::::::..      !tt3.               \n",
          "      /z/.:   :;z!:::::J  :E3.  E:::::::..     !ct3.             \n",
          "    ,E;F   ::;t::::::::J  :E3.  E::.     ::.     \ztL            \n",
          "   ;E7.    :c::::F******   **.  *==c;..    ::     Jttk           \n",
          "  .EJ.    ;::::::L                    \:.   ::.    Jttl          \n",
          "  [:.    :::::::::773.    JE773zs.     I:. ::::.    It3L         \n",
          " ;:[     L:::::::::::L    |t::!::J     |::::::::    :Et3         \n",
          " [:L    !::::::::::::L    |t::;z2F    .Et:::.:::.  ::[13  CRYPTO \n",
          " E:.    !::::::::::::L               =Et::::::::!  ::|13  TRADING \n",
          " E:.    (::::::::::::L    .......       \:::::::!  ::|i3  AI      \n",
          " [:L    !::::      ::L    |3t::::!3.     ]::::::.  ::[13          \n",
          " !:(     .:::::    ::L    |t::::::3L     |:::::; ::::EE3         \n",
          "  E3.    :::::::::;z5.    Jz;;;z=F.     :E:::::.::::II3[         \n",
          "  Jt1.    :::::::[                    ;z5::::;.::::;3t3          \n",
          "   \z1.::::::::::l......   ..   ;.=ct5::::::/.::::;Et3L          \n",
          "    \z3.:::::::::::::::J  :E3.  Et::::::::;!:::::;5E3L           \n",
          "     \cz\.:::::::::::::J   E3.  E:::::::z!     ;Zz37`            \n",
          "       \z3.       ::;:::::::::::::::;='      ./355F              \n",
          "         \z3x.         ::~======='         ,c253F                \n",
          "           \ z3=.                      ..c5t32^                  \n",
          "              =zz3==...          ...=t3z13P^                     \n",
          "                   `*=zjzczIIII3zzztE3>*^`                        \n\n\n")


    print("\n> Welcome to Crypto-Trading AI")

    parser = argparse.ArgumentParser()
    parser.add_argument("--collect_coins",action="store_true")
    parser.add_argument("--train_and_trade", action="store_true")
    parser.add_argument("--start")
    parser.add_argument("--end")
    args = parser.parse_args()

    dataset = Dataset()

    if args.collect_coins:
        start_date = args.start if args.start else "2020-01-01"
        end_date = args.end if args.end else "2020-02-02"
        tokens = start_date.split("-")
        month = tokens[0] + "_" + tokens[1] + "_"

        coinbaseAPI = CoinbaseAPI()
        historic_data = coinbaseAPI.getCoinHistoricData(COIN_PAIR, start=start_date, end=end_date,granularity=GRANULARITY)
        dataset.storeRawCoinHistoricData(month,COIN_PAIR,historic_data)

        print("> Using Coinbase API to build dataset for ",COIN_PAIR)

    elif args.train_and_trade:
        print("> Creating Training Data for ", COIN_PAIR)
        data = dataset.loadCoinData(COIN_PAIR, TRAINING_MONTHS)
        x_train, y_train, _ = dataset.createTrainTestSets(COIN_PAIR, data, training_window=TRAINING_WINDOW, labeling_window=LABELING_WINDOW)

        print("> Creating Testing Data for ", COIN_PAIR)
        data = dataset.loadCoinData(COIN_PAIR, TESTING_MONTHS)
        x_test, y_test, prices = dataset.createTrainTestSets(COIN_PAIR, data, training_window=TRAINING_WINDOW, labeling_window=LABELING_WINDOW)

        test_model = Model("AutoTraderAI", x_train)
        test_model.train(x_train, y_train, batch_size=64, epochs=10)
        # test_model.evaluate(x_test,y_test)

        auto_trader = AutoTrader(test_model)
        auto_trader.runSimulation(x_test, prices)
    else:
        print("> The biggest mistake you can make in life is to waste your time. – Jerry Bruckner")
        print("> P.S. Use an argument next time: --collect_coins or --train_and_trade")








