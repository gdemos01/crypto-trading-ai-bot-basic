# Crypto Trading AI Bot - Basic Version
Source code for the Crypto-trading AI Bot used in the following YouTube video

I Coded A Crypto Trading AI And Gave It $1000 To Trade For A Month!
https://www.youtube.com/watch?v=f5ZuF4V9Sl4

## How to Use
Currently you can use this code to:
 - Create crypto-currency datasets
 - Train the integrated AI to predict near-future changes of crypto (Up/Down)
 - Run trading simulations with the AutoTrader bot.

You can make configuration changes at <strong>Config.py</strong>

### Collect Coin Data For a Specific Month
Collects the data using Coinbase's API and stores them in JSON format. \
\
`> python Controller.py --collect_coins --start "2020-01-01" --end "2020-02-01" `

### Train and Trade
Trains the AI using historic crypto information and runs the trading simulation.

`> python Controller.py --train_and_trade`
