from sklearn import model_selection
from sklearn import preprocessing
from sklearn.utils import shuffle
import numpy as np
import json
import math
from Config import *

class Dataset:

    def __init__(self):
        print("> Dataset Class Initialized")
        self.feature_names = [] # For feature comparison and visualization

    """
        Stores Raw historic data of a particular coin in JSON format
    """
    def storeRawCoinHistoricData(self, name, coin_name, data):
        print("> Storing Raw Historic Data for ", coin_name)
        with open('raw_historic_data/' + name + "_" + coin_name + '.json', 'w') as outfile:
            json.dump(data, outfile)

    """
        Loads raw historic data of a particular coin and converts to JSON format
    """
    def loadRawCoinHistoricData(self, coin_name):
        print("> Loading Raw Historic Data for ", coin_name)

        data = None

        with open('raw_historic_data/' + coin_name + '.json', ) as json_file:
            data = json.load(json_file)

        return data

    """
        Loads all the coin data, for the selected months, into an ordered array. 
        Each row represents a the status of the coin each minute.
    """
    def loadCoinData(self,coin_name,months):
        print("> Loading data for ",coin_name)
        ordered_data = []
        for month in months:
            print(">> Loading month: ",month)
            file_path = DATASET_DIR + coin_name + '/' + month +"__"+ coin_name + '.json'
            with open(file_path) as json_file:
                raw_data = json.load(json_file)

            for data in raw_data:
                if len(data) != 0:
                    for minute_info in data: # Data stored every minute
                        ordered_data.append(minute_info)

        return ordered_data

    """
        Creates the train/test sets (X,Y) based on a selection of windows and features.
        Raw variable headings: [time, low, high, open, close, volume]
    """
    def createTrainTestSets(self,coin_name, coin_data, training_window = 180, labeling_window = 60, feature_window = 30):
        print("> Creating X,Y sets for ",coin_name)
        x = []
        y = []
        prices = []

        positive = 0
        negative = 0
        block = 60  # Move 1 hour
        start_index = 0
        end_index = training_window -1

        while end_index < len(coin_data) - labeling_window -block - 1:
            features = []
            self.feature_names = []

            # Latest Values
            latest_low_price = coin_data[end_index][1]
            latest_high_price = coin_data[end_index][2]
            latest_open_price = coin_data[end_index][3]
            latest_close_price = coin_data[end_index][4]
            latest_volume = coin_data[end_index][5]

            # Accelerations and Differences
            acc_index = 0
            total_window_volume = 0
            prev_window_volume_acceleration = 0
            window_volume_acceleration = 0
            average_volume_acceleration = 0 # The average volume acceleration based on the feature window (local)
            average_close_price_acceleration = 0 # The average close price acceleration based on the feature window (local)
            average_close_price_diff = 0 # The average close price difference based on the feature window (local)

            # Averages
            average_close_price = 0
            average_volume = 0

            for i in range(start_index,end_index):
                cur_close_price = coin_data[i][4]
                cur_volume = coin_data[i][5]
                total_window_volume += cur_volume
                window_volume_acceleration += cur_volume
                average_close_price += cur_close_price

                # Local Accelerations
                acc_index += 1
                if acc_index % feature_window == 0:
                    # Local Close Price Acceleration
                    close_price_acceleration = (cur_close_price / coin_data[i-feature_window][4]) - 1
                    features.append(close_price_acceleration)
                    self.feature_names.append("close_price_acc_"+str(acc_index))
                    average_close_price_acceleration += close_price_acceleration

                    # Local Close Price Difference - Only overal average added in features
                    close_price_diff = cur_close_price - coin_data[i-feature_window][4]
                    average_close_price_diff +=  close_price_diff

                    # Local Volume Acceleration
                    if prev_window_volume_acceleration != 0:
                        volume_acceleration = (window_volume_acceleration / prev_window_volume_acceleration) - 1
                        features.append(volume_acceleration)
                        self.feature_names.append("volume_acc_"+str(acc_index))
                    average_volume_acceleration += window_volume_acceleration
                    prev_window_volume_acceleration = window_volume_acceleration
                    window_volume_acceleration = 0

            # Overall Averages
            average_close_price /= training_window
            average_close_price_acceleration /= training_window
            average_volume /= training_window
            average_volume_acceleration /= training_window

            # Price
            overall_price_difference = latest_close_price - coin_data[start_index][4]
            overall_price_acceleration = (latest_close_price / coin_data[start_index][4]) - 1

            # Adding Features and Feature Names
            features.append(total_window_volume)
            self.feature_names.append("volume_total")
            features.append(latest_low_price)
            self.feature_names.append("low_price_latest")
            features.append(latest_high_price)
            self.feature_names.append("high_price_latest")
            features.append(latest_open_price)
            self.feature_names.append("open_price_latest")

            features.append(average_close_price)
            self.feature_names.append("close_price_av")
            features.append(average_close_price_acceleration)
            self.feature_names.append("close_price_acc_av")
            features.append(average_close_price_diff)
            self.feature_names.append("close_price_diff_av")
            features.append(average_volume)
            self.feature_names.append("volume_av")
            features.append(average_volume_acceleration)
            self.feature_names.append("volume_acc_av")
            features.append(overall_price_difference)
            self.feature_names.append("overall_price_diff")
            features.append(overall_price_acceleration)
            self.feature_names.append("overal_price_acc")

            # Last feature holds the latest price
            features.append(latest_close_price)
            self.feature_names.append("close_price_latest")
            prices.append(latest_close_price)

            x.append(features) # Add to training set
            # Simple Up or Down Labeling
            next_close_price = coin_data[end_index + labeling_window +1][4]

            change_rate = (next_close_price/latest_close_price) - 1

            if change_rate > 0:
                y.append(1)
                positive += 1
            else:
                y.append(0)
                negative +=1

            # Experiment between Rectangular and Moving Windows
            start_index += block
            end_index += block

        print("> Finished Creating set - Size: ",len(x)," ",len(y)," P: ",positive," N: ",negative)

        x = preprocessing.scale(x)
        x, y, prices = shuffle(x,y,prices)

        return np.array(x), np.array(y), prices