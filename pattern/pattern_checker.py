from data.data_structure import DataStructure, DataItem
import json
from bisect import bisect_left

import talib
import numpy as np

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




























