DATASET_DIR = "datasets/"
COIN_PAIR = "BTC-USD"
GRANULARITY = 60 # Data every 1 minute

TRAINING_MONTHS = ["2018_06","2018_07","2018_08","2018_09","2018_10","2018_11","2018_12","2019_01",
                   "2019_02","2019_03","2019_04","2019_05","2019_06","2019_07","2019_08","2019_09",
                   "2019_10","2019_11","2019_12","2020_01","2020_02","2020_03","2020_04","2020_05",
                    "2020_06","2020_07","2020_08","2020_09"]

TESTING_MONTHS = ["2020_10"]

# Model and Auto Trader
CHANGE_RATE_THRESHOLD = 0.005
TRAINING_WINDOW = 360 # Window to use for training in minutes
LABELING_WINDOW = 360 # How far ahead to look for labeling / prediction
