from data.data_structure import DataStructure, DataItem
import json
from bisect import bisect_left

import talib
import numpy as np
from talib import ATR

class PatternCheker:
    '''
    Json property demo
    {
        "15min":{
              "EntryPattern":{1:{"xxx":0.5}, ...},


              "CheckPattern":{1:{}}

              "DatePattern":{},

        },
        "day":{
        }
    }

    '''



    def __init__(self, properties, data_structure):
        self.data = data_structure
        self.properties = properties


    def upper_level_dataitem(self, check_level, index, target_level):
        '''
        upper level item util before this time
        :param check_level:
        :param index:
        :param target_level:
        :return:
        '''
        target_index = self.data.data[check_level][index].start_index[target_level]
        now_start_index = self.data.data[target_level][target_index].start_index[check_level]
        if now_start_index < index:
            return DataItem.merge_dataitems(self.data.data[check_level][now_start_index:index], target_index)
        else:
            return None

    def add_checked_pattern(self, ans, pattern_type, pattern_no, pattern_answer = True, pattern_name=None):
        if pattern_type not in ans:
            ans[pattern_type] = {}

        if pattern_answer not in ans[pattern_type]:
            ans[pattern_type][pattern_answer] = []
        ans[pattern_type][pattern_answer].append((pattern_no, pattern_name))



    def check(self, level, index):
        ans = {}

        if level == DataStructure.time_levels[1]:
            '''
            15min level
            '''
            check_properties = self.properties[level]

            if 'MomentumPattern' in check_properties:
                patterns = check_properties['MomentumPattern']

                ''' upside momentum  '''
                if '1' in patterns:
                    def check15min_pattern_MomentumPattern_1(before_day = 1):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index-1-before_day].close_price >\
                                   self.data.fifteen_mins[index-2-before_day].close_price \
                                   and self.data.fifteen_mins[index-2-before_day].close_price > \
                                       self.data.fifteen_mins[index-3-before_day].close_price
                        return False

                    if check15min_pattern_MomentumPattern_1(** patterns['1']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 1, True)

                if '2' in patterns:
                    def check15min_pattern_MomentumPattern_2(before_day=4):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index - 1 - before_day].close_price > \
                                   self.data.fifteen_mins[index - 2 - before_day].close_price \
                                   and self.data.fifteen_mins[index - 2 - before_day].close_price > \
                                       self.data.fifteen_mins[index - 3 - before_day].close_price
                        return False

                    if check15min_pattern_MomentumPattern_2(**patterns['2']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 2, True)

                if '3' in patterns:
                    def check15min_pattern_MomentumPattern_3(before_day=1):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index - 1 - before_day].high_price > \
                                   self.data.fifteen_mins[index - 2 - before_day].high_price \
                                   and self.data.fifteen_mins[index - 2 - before_day].high_price > \
                                       self.data.fifteen_mins[index - 3 - before_day].high_price
                        return False

                    if check15min_pattern_MomentumPattern_3(**patterns['3']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 3, True)

                if '4' in patterns:
                    def check15min_pattern_MomentumPattern_4(before_day=4):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index - 1 - before_day].high_price > \
                                   self.data.fifteen_mins[index - 2 - before_day].high_price \
                                   and self.data.fifteen_mins[index - 2 - before_day].high_price > \
                                       self.data.fifteen_mins[index - 3 - before_day].high_price
                        return False

                    if check15min_pattern_MomentumPattern_4(**patterns['4']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 4, True)

                if '5' in patterns:
                    def check15min_pattern_MomentumPattern_5(before_day=1):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index - 1 - before_day].low_price > \
                                   self.data.fifteen_mins[index - 2 - before_day].low_price \
                                   and self.data.fifteen_mins[index - 2 - before_day].low_price > \
                                       self.data.fifteen_mins[index - 3 - before_day].low_price
                        return False

                    if check15min_pattern_MomentumPattern_5(**patterns['5']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 5, True)

                if '6' in patterns:
                    def check15min_pattern_MomentumPattern_6(before_day=4):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index - 1 - before_day].low_price > \
                                   self.data.fifteen_mins[index - 2 - before_day].low_price \
                                   and self.data.fifteen_mins[index - 2 - before_day].low_price > \
                                       self.data.fifteen_mins[index - 3 - before_day].low_price
                        return False

                    if check15min_pattern_MomentumPattern_6(**patterns['6']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 6, True)


                '''continuous risen num'''
                if '7' in patterns:
                    def check15min_pattern_MomentumPattern_7(days = 4):
                        if index >= days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index -i -1]
                                if item.close_price <= item.open_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_7(** patterns['7']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 7, True)

                if '8' in patterns:
                    def check15min_pattern_MomentumPattern_8(days=7):
                        if index >= days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index - i - 1]
                                if item.close_price <= item.open_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_8(**patterns['8']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 8, True)

                if '9' in patterns:
                    def check15min_pattern_MomentumPattern_9(days=10):
                        if index >= days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index - i - 1]
                                if item.close_price <= item.open_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_9(**patterns['9']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 9, True)

                '''continuous highest num'''
                if '10' in patterns:
                    def check15min_pattern_MomentumPattern_10(days=4):
                        if index > days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index - i - 1]
                                item_before = self.data.fifteen_mins[index -i -2]
                                if item.high_price <= item_before.high_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_10(**patterns['10']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 10, True)

                if '11' in patterns:
                    def check15min_pattern_MomentumPattern_11(days=7):
                        if index > days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index - i - 1]
                                item_before = self.data.fifteen_mins[index -i -2]
                                if item.high_price <= item_before.high_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_11(**patterns['11']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 11, True)

                if '12' in patterns:
                    def check15min_pattern_MomentumPattern_12(days=10):
                        if index > days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index - i - 1]
                                item_before = self.data.fifteen_mins[index -i -2]
                                if item.high_price <= item_before.high_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_12(**patterns['12']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 12, True)

                '''ATR up'''
                if '13' in patterns:
                    def check15min_pattern_MomentumPattern_13(atr1=10, atr2=50):
                        if index > max(atr1, atr2):
                            atr1_range_data = self.data.fifteen_mins[index - atr1 - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, atr1_range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, atr1_range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, atr1_range_data)))
                            atr1_prices = talib.ATR(high_prices, low_prices, close_prices, atr1)
                            atr1_price = atr1_prices[-1]
                            atr1_price_b = atr1_prices[-2]

                            atr2_range_data = self.data.fifteen_mins[index - atr2 - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, atr2_range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, atr2_range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, atr2_range_data)))
                            atr2_prices = talib.ATR(high_prices, low_prices, close_prices, atr2)
                            atr2_price = atr2_prices[-1]
                            atr2_price_b = atr2_prices[-2]

                            if atr1_price > atr2_price and atr1_price_b <= atr2_price_b:
                                return True
                        return False

                    if check15min_pattern_MomentumPattern_13(** patterns['13']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 13, True)

                if '14' in patterns:
                    def check15min_pattern_MomentumPattern_14(atr1=20, atr2=80):
                        if index > max(atr1, atr2):
                            atr1_range_data = self.data.fifteen_mins[index - atr1 - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, atr1_range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, atr1_range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, atr1_range_data)))
                            atr1_prices = talib.ATR(high_prices, low_prices, close_prices, atr1)
                            atr1_price = atr1_prices[-1]
                            atr1_price_b = atr1_prices[-2]

                            atr2_range_data = self.data.fifteen_mins[index - atr2 - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, atr2_range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, atr2_range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, atr2_range_data)))
                            atr2_prices = talib.ATR(high_prices, low_prices, close_prices, atr2)
                            atr2_price = atr2_prices[-1]
                            atr2_price_b = atr2_prices[-2]

                            if atr1_price > atr2_price and atr1_price_b <= atr2_price_b:
                                return True
                        return False

                    if check15min_pattern_MomentumPattern_14(**patterns['14']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 14, True)



                ''' downside momentum  '''
                if '15' in patterns:
                    def check15min_pattern_MomentumPattern_15(before_day=1):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index - 1 - before_day].close_price < \
                                   self.data.fifteen_mins[index - 2 - before_day].close_price \
                                   and self.data.fifteen_mins[index - 2 - before_day].close_price < \
                                       self.data.fifteen_mins[index - 3 - before_day].close_price
                        return False

                    if check15min_pattern_MomentumPattern_15(**patterns['15']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 15, True)

                if '16' in patterns:
                    def check15min_pattern_MomentumPattern_16(before_day=4):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index - 1 - before_day].close_price < \
                                   self.data.fifteen_mins[index - 2 - before_day].close_price \
                                   and self.data.fifteen_mins[index - 2 - before_day].close_price < \
                                       self.data.fifteen_mins[index - 3 - before_day].close_price
                        return False

                    if check15min_pattern_MomentumPattern_16(**patterns['16']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 16, True)

                if '17' in patterns:
                    def check15min_pattern_MomentumPattern_17(before_day=1):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index - 1 - before_day].high_price < \
                                   self.data.fifteen_mins[index - 2 - before_day].high_price \
                                   and self.data.fifteen_mins[index - 2 - before_day].high_price < \
                                       self.data.fifteen_mins[index - 3 - before_day].high_price
                        return False

                    if check15min_pattern_MomentumPattern_17(**patterns['17']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 17, True)

                if '18' in patterns:
                    def check15min_pattern_MomentumPattern_18(before_day=4):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index - 1 - before_day].high_price < \
                                   self.data.fifteen_mins[index - 2 - before_day].high_price \
                                   and self.data.fifteen_mins[index - 2 - before_day].high_price < \
                                       self.data.fifteen_mins[index - 3 - before_day].high_price
                        return False

                    if check15min_pattern_MomentumPattern_18(**patterns['18']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 18, True)

                if '19' in patterns:
                    def check15min_pattern_MomentumPattern_19(before_day=1):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index - 1 - before_day].low_price < \
                                   self.data.fifteen_mins[index - 2 - before_day].low_price \
                                   and self.data.fifteen_mins[index - 2 - before_day].low_price < \
                                       self.data.fifteen_mins[index - 3 - before_day].low_price
                        return False

                    if check15min_pattern_MomentumPattern_19(**patterns['19']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 19, True)

                if '20' in patterns:
                    def check15min_pattern_MomentumPattern_20(before_day=4):
                        if index >= before_day + 3:
                            return self.data.fifteen_mins[index - 1 - before_day].low_price < \
                                   self.data.fifteen_mins[index - 2 - before_day].low_price \
                                   and self.data.fifteen_mins[index - 2 - before_day].low_price < \
                                       self.data.fifteen_mins[index - 3 - before_day].low_price
                        return False

                    if check15min_pattern_MomentumPattern_20(**patterns['20']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 20, True)

                '''continuous decrease num'''
                if '21' in patterns:
                    def check15min_pattern_MomentumPattern_21(days=4):
                        if index >= days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index - i - 1]
                                if item.close_price >= item.open_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_21(**patterns['21']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 21, True)

                if '22' in patterns:
                    def check15min_pattern_MomentumPattern_22(days=7):
                        if index >= days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index - i - 1]
                                if item.close_price >= item.open_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_22(**patterns['22']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 22, True)

                if '23' in patterns:
                    def check15min_pattern_MomentumPattern_23(days=10):
                        if index >= days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index - i - 1]
                                if item.close_price >= item.open_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_23(**patterns['23']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 23, True)

                '''continuous lowest num'''
                if '24' in patterns:
                    def check15min_pattern_MomentumPattern_24(days=4):
                        if index > days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index - i - 1]
                                item_before = self.data.fifteen_mins[index - i - 2]
                                if item.high_price >= item_before.high_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_24(**patterns['24']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 24, True)

                if '25' in patterns:
                    def check15min_pattern_MomentumPattern_25(days=7):
                        if index > days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index - i - 1]
                                item_before = self.data.fifteen_mins[index - i - 2]
                                if item.high_price >= item_before.high_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_25(**patterns['25']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 25, True)

                if '26' in patterns:
                    def check15min_pattern_MomentumPattern_26(days=10):
                        if index > days:
                            for i in range(0, days):
                                item = self.data.fifteen_mins[index - i - 1]
                                item_before = self.data.fifteen_mins[index - i - 2]
                                if item.high_price >= item_before.high_price:
                                    return False
                            return True
                        return False

                    if check15min_pattern_MomentumPattern_26(**patterns['26']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 26, True)

                '''ATR down'''
                if '27' in patterns:
                    def check15min_pattern_MomentumPattern_27(atr1=10, atr2=50):
                        if index > max(atr1, atr2):
                            atr1_range_data = self.data.fifteen_mins[index - atr1 - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, atr1_range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, atr1_range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, atr1_range_data)))
                            atr1_prices = talib.ATR(high_prices, low_prices, close_prices, atr1)
                            atr1_price = atr1_prices[-1]
                            atr1_price_b = atr1_prices[-2]

                            atr2_range_data = self.data.fifteen_mins[index - atr2 - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, atr2_range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, atr2_range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, atr2_range_data)))
                            atr2_prices = talib.ATR(high_prices, low_prices, close_prices, atr2)
                            atr2_price = atr2_prices[-1]
                            atr2_price_b = atr2_prices[-2]

                            if atr1_price < atr2_price and atr1_price_b >= atr2_price_b:
                                return True
                        return False

                    if check15min_pattern_MomentumPattern_27(**patterns['27']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 27, True)

                if '28' in patterns:
                    def check15min_pattern_MomentumPattern_28(atr1=20, atr2=80):
                        if index > max(atr1, atr2):
                            atr1_range_data = self.data.fifteen_mins[index - atr1 - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, atr1_range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, atr1_range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, atr1_range_data)))
                            atr1_prices = talib.ATR(high_prices, low_prices, close_prices, atr1)
                            atr1_price = atr1_prices[-1]
                            atr1_price_b = atr1_prices[-2]

                            atr2_range_data = self.data.fifteen_mins[index - atr2 - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, atr2_range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, atr2_range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, atr2_range_data)))
                            atr2_prices = talib.ATR(high_prices, low_prices, close_prices, atr2)
                            atr2_price = atr2_prices[-1]
                            atr2_price_b = atr2_prices[-2]

                            if atr1_price < atr2_price and atr1_price_b >= atr2_price_b:
                                return True
                        return False

                    if check15min_pattern_MomentumPattern_28(**patterns['28']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 28, True)


                '''WPR fluctuate'''
                if '29' in patterns:
                    def check15min_pattern_MomentumPattern_29():
                        if index > 1:
                            item_1 = self.data.fifteen_mins[index - 2]
                            item_2 = self.data.fifteen_mins[index - 1]
                            if (item_1.close_price - item_1.high_price)/(item_1.high_price-item_1.low_price) > -5 * 0.01 and (item_2.close_price - item_2.high_price)/(item_2.high_price-item_2.low_price) < -20 * 0.01:
                                return True
                        return False

                    if check15min_pattern_MomentumPattern_29(**patterns['29']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 29, True)

                if '30' in patterns:
                    def check15min_pattern_MomentumPattern_30():
                        if index > 1:
                            item_1 = self.data.fifteen_mins[index - 2]
                            item_2 = self.data.fifteen_mins[index - 1]
                            if (item_1.close_price - item_1.high_price)/(item_1.high_price-item_1.low_price) < -95 * 0.01 and (item_2.close_price - item_2.high_price)/(item_2.high_price-item_2.low_price) > -80 * 0.01:
                                return True
                        return False

                    if check15min_pattern_MomentumPattern_30(**patterns['30']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 30, True)


                '''stochastic'''
                if '31' in patterns:
                    def check15min_pattern_MomentumPattern_31(periods = 10):
                        if index > periods + 1:
                            range_data = self.data.fifteen_mins[index - periods - 2: index-1]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_before = sto[0][-1]

                            range_data = self.data.fifteen_mins[index - periods - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_now = sto[0][-1]
                            return sto_before < 5 and sto_now > 20
                        return False

                    if check15min_pattern_MomentumPattern_31(** patterns['31']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 31, True)

                if '32' in patterns:
                    def check15min_pattern_MomentumPattern_32(periods=20):
                        if index > periods + 1:
                            range_data = self.data.fifteen_mins[index - periods - 2: index - 1]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_before = sto[0][-1]

                            range_data = self.data.fifteen_mins[index - periods - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_now = sto[0][-1]
                            return sto_before < 5 and sto_now > 20
                        return False

                    if check15min_pattern_MomentumPattern_32(**patterns['32']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 32, True)

                if '33' in patterns:
                    def check15min_pattern_MomentumPattern_33(periods=40):
                        if index > periods + 1:
                            range_data = self.data.fifteen_mins[index - periods - 2: index - 1]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_before = sto[0][-1]

                            range_data = self.data.fifteen_mins[index - periods - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_now = sto[0][-1]
                            return sto_before < 5 and sto_now > 20
                        return False

                    if check15min_pattern_MomentumPattern_33(**patterns['33']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 33, True)


                if '34' in patterns:
                    def check15min_pattern_MomentumPattern_34(periods = 10):
                        if index > periods + 1:
                            range_data = self.data.fifteen_mins[index - periods - 2: index-1]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_before = sto[0][-1]

                            range_data = self.data.fifteen_mins[index - periods - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_now = sto[0][-1]
                            return sto_before > 95 and sto_now < 80
                        return False

                    if check15min_pattern_MomentumPattern_34(** patterns['34']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 34, True)

                if '35' in patterns:
                    def check15min_pattern_MomentumPattern_35(periods=20):
                        if index > periods + 1:
                            range_data = self.data.fifteen_mins[index - periods - 2: index - 1]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_before = sto[0][-1]

                            range_data = self.data.fifteen_mins[index - periods - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_now = sto[0][-1]
                            return sto_before > 95 and sto_now < 80
                        return False

                    if check15min_pattern_MomentumPattern_35(**patterns['35']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 35, True)

                if '36' in patterns:
                    def check15min_pattern_MomentumPattern_36(periods=40):
                        if index > periods + 1:
                            range_data = self.data.fifteen_mins[index - periods - 2: index - 1]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_before = sto[0][-1]

                            range_data = self.data.fifteen_mins[index - periods - 1: index]
                            high_prices = np.array(list(map(lambda item: item.high_price, range_data)))
                            low_prices = np.array(list(map(lambda item: item.low_price, range_data)))
                            close_prices = np.array(list(map(lambda item: item.close_price, range_data)))
                            sto = talib.ATR(high_prices, low_prices, close_prices)
                            sto_now = sto[0][-1]
                            return sto_before > 95 and sto_now < 80
                        return False

                    if check15min_pattern_MomentumPattern_36(**patterns['36']):
                        self.add_checked_pattern(ans, 'MomentumPattern', 36, True)









            if 'EntryPattern' in check_properties:
                patterns = check_properties['EntryPattern']
                if '1' in patterns:
                    '''content of pattern 1'''
                    def check15min_pattern_EntryPattern_1(increase_range = 1.05):
                        if index-2 < 0 or index-1 < 0:
                            return False
                        return self.data.fifteen_mins[index-2].open_price * increase_range < self.data.fifteen_mins[index-1].close_price

                    if check15min_pattern_EntryPattern_1(** patterns['1']):
                        self.add_checked_pattern(ans,'EntryPattern', 1, True)


                if '2' in patterns:
                    '''same as 1'''
                    def check15min_pattern_EntryPattern_2(rate = 1.005):
                        return index>0 and self.data.fifteen_mins[index-1].close_price / self.data.fifteen_mins[index-1].open_price > rate

                    if check15min_pattern_EntryPattern_2(** patterns['2']):
                        self.add_checked_pattern(ans,'EntryPattern', 2, True)

                if '3' in patterns:
                    '''same as 1'''
                    def check15min_pattern_EntryPattern_3(num = 50):
                        if index < num+1:
                            return False
                        range_data = self.data.fifteen_mins[index-num-1:index]

                        high_prices = np.array(list(map(lambda item:item.high_price, range_data)))
                        low_prices = np.array(list(map(lambda item:item.low_price, range_data)))
                        close_prices = np.array(list(map(lambda item:item.close_price, range_data)))

                        atr_prices = talib.ATR(high_prices, low_prices, close_prices, num)
                        atr_price = atr_prices[-1]

                        return self.data.fifteen_mins[index-1].close_price - self.data.fifteen_mins[index-1].open_price > 3.0 * atr_price

                    if check15min_pattern_EntryPattern_3(** patterns['3']):
                        self.add_checked_pattern(ans,'EntryPattern', 3, True)

                if '4' in patterns:
                    def check15min_pattern_EntryPattern_4():
                        today = self.upper_level_dataitem('15min', index, 'day')
                        if today is not None:
                            day_index = self.data.fifteen_mins[index].start_index['day']
                            today_shift = self.upper_level_dataitem('15min', index-1, 'day')
                            return day_index>=1 and today.high_price > self.data.days[day_index-1].high_price and (today_shift is None or today_shift.high_price<=self.data.days[day_index-1].high_price)
                        return False

                    if check15min_pattern_EntryPattern_4():
                        self.add_checked_pattern(ans,'EntryPattern', 4, True)








            if 'CheckPattern' in check_properties:
                patterns = check_properties['CheckPattern']
                if '1' in patterns:
                    def check15min_pattern_CheckPattern_1(day_before=1):
                        day_index = self.data.fifteen_mins[index].start_index['day']
                        if day_index <0:
                            return False
                        high = self.data.days[day_index - day_before].high_price
                        today = self.upper_level_dataitem('15min', index, 'day')
                        return today is not None and today.high_price > high

                    if check15min_pattern_CheckPattern_1(** patterns['1']):
                        self.add_checked_pattern(ans, 'CheckPattern', 1, True)



                '''
                same as 1 to add pattern
                '''

            if 'DatePattern' in check_properties:
                patterns = check_properties['DatePattern']
                if '1' in patterns:
                    def check15min_pattern_DatekPattern_1(weekday=1):
                        return self.data.fifteen_mins[index].date_time.weekday() + 1 == weekday

                    if check15min_pattern_DatekPattern_1(**patterns['1']):
                        self.add_checked_pattern(ans, 'DatePattern', 1, True)


        if level == DataStructure.time_levels[0]:
            '''
            day level
            '''
            check_properties = self.properties[level]

            if 'CheckPattern' in check_properties:
                patterns = check_properties['CheckPattern']
                if '1' in patterns:
                    def checkday_pattern_CheckPattern_1():
                        return self.data.days[index-1].close_price > self.data.days[index-2].close_price
                    if checkday_pattern_CheckPattern_1(**patterns['1']):
                        self.add_checked_pattern(ans, 'CheckPattern', 1, True)

                if '2' in patterns:
                    def checkday_pattern_CheckPattern_2():
                        if index < 3:
                            return False
                        return self.data.days[index-1].high_price > self.data.days[index-2].high_price and self.data.days[index-1].high_price > self.data.days[index-3].high_price

                    if checkday_pattern_CheckPattern_1(**patterns['2']):
                        self.add_checked_pattern(ans, 'CheckPattern', 2, True)

        return ans




    def ckeck_patterns_for_all_levels(self, time_start=None, time_end=None):
        day_start_index = 0
        day_end_index = len(self.data.days)
        if time_start and time_end:
            flag = True
            for i in range(len(self.data.days)):
                if self.data.days[i].date_time >= time_start and flag:
                    day_start_index = i
                    flag = False
                if self.data.days[i].date_time >= time_end:
                    day_end_index = i
                    break

        checked_pattern_points = {}

        for level in DataStructure.time_levels:
            sd = self.data.days[day_start_index]
            ed = self.data.days[day_end_index-1]
            #print(sd.start_index)
            #print(ed.end_index)
            #print(sd)
            #print(ed)



            if level in self.properties:
                csindex = sd.start_index[level]
                ceindex = ed.end_index[level]

                #print(level,self.data.data[level][csindex])
                #print(level,self.data.data[level][ceindex])

                checked_pattern_points[level] = {}
                for i in range(csindex, ceindex):
                    #print(level, i)
                    checked = self.check(level, i)
                    if len(checked) != 0:
                        checked_pattern_points[level][i] = checked

        return {'data':self.data, 'checked_pattern':checked_pattern_points}



if __name__ == '__main__':
    d = DataStructure('/Users/liuyichao/PycharmProjects/ptn/raw_data/主力数据/a_continuous.csv', 'cu')
    properties= json.loads(open('/Users/liuyichao/PycharmProjects/ptn/properties/pattern.property').read())
    ptc = PatternCheker(properties=properties, data_structure=d)
    import datetime
    import time
    t = time.time()
    print(t)
    start = datetime.datetime(2004,1,1)
    end = datetime.datetime(2017,1,1)
    ans = ptc.ckeck_patterns_for_all_levels(start, end)
    print(ans)
    for key in ans['checked_pattern']:
        print("KEY ",key)
        print(len(ans['checked_pattern'][key]))
        print(ans['checked_pattern'][key])
        for i in ans['checked_pattern'][key]:
            print('checked')
            print(key, ans['data'].data[key][i])
            #if len(ans['checked_pattern'][key][i]) > 1:
            print("QQQQQQQQ", ans['checked_pattern'][key][i])
            print("-------")
    print(time.time())
    print(time.time() - t)




























