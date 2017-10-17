import json

import numpy
import talib

from data.data_structure import DataStructure
from pattern.pattern_checker import PatternCheker


class Target:
    def __init__(self, level, targetno, period=15, target_desc="", call_func = None):
        self.targetno = targetno
        self.level = level
        self.period = period
        self.target_desc = target_desc

        def call_func_method(index:int, data_array:list):
            period_data = data_array[index:index+period]
            if call_func:
                return call_func(period_data)
            else:
                open_price = period_data[0].open_price
                close_price = period_data[-1].close_price
                high_price = max(map(lambda item:item.high_price, period_data)) * 1.0
                low_price = min(map(lambda item:item.low_price, period_data)) * 1.0
                return (close_price / open_price - 1.0, high_price / open_price - 1.0, low_price / open_price - 1.0)

        self.calculate_func = call_func_method


class TargetCollection:

    targets = []
    level_targets = {}

    @staticmethod
    def build_target_collection():
        '''
        添加所有target
        '''
        TargetCollection.targets.append(Target("15min", 1, 25, "25"))
        TargetCollection.targets.append(Target("15min", 2, 50, "50"))
        TargetCollection.targets.append(Target("15min", 3, 75, "75"))
        TargetCollection.targets.append(Target("15min", 4, 100, "100"))
        TargetCollection.targets.append(Target("15min", 5, 150, "150"))

        for target in TargetCollection.targets:
            if target.level not in TargetCollection.level_targets:
                TargetCollection.level_targets[target.level] = []

            TargetCollection.level_targets[target.level].append(target)
        return TargetCollection.level_targets




class TargetChecker:

    level_targets = TargetCollection.build_target_collection()


    @staticmethod
    def check_pattern_targets(checked_pattern_structure, time_start, time_end):

        day_start_index = 0
        day_end_index = len(checked_pattern_structure['data'].days)
        if time_start and time_end:
            flag = True
            for i in range(len(checked_pattern_structure['data'].days)):
                if checked_pattern_structure['data'].days[i].date_time >= time_start and flag:
                    day_start_index = i
                    flag = False
                if checked_pattern_structure['data'].days[i].date_time >= time_end:
                    day_end_index = i
                    break


        point_targets = {}

        for level in checked_pattern_structure['checked_pattern'].keys():
            point_targets[level] = {}

            targets = TargetChecker.level_targets[level]
            sd = checked_pattern_structure['data'].days[day_start_index]
            ed = checked_pattern_structure['data'].days[day_end_index-1]

            csindex = sd.start_index[level]
            ceindex = ed.end_index[level]

            for i in range(csindex, ceindex):
                if i in checked_pattern_structure['checked_pattern'][level]:
                    for target in targets:
                        if i + target.period <= ceindex:
                            target_value = target.calculate_func(i, checked_pattern_structure['data'].data[level])
                            '''
                            if (target_value[0] - 0) <= 0.00000001 and (target_value[0] - 0) >= -0.00000001:
                                print("QQQQQQQQQ")
                                print(checked_pattern_structure['data'].data[level][i].date_time)
                                print(target.period)
                                print(target_value)
                                print(checked_pattern_structure['data'].data[level][i])
                                print(checked_pattern_structure['data'].data[level][i+target.period - 1])
                            '''
                            if i not in point_targets[level]:
                                point_targets[level][i] = []
                            point_targets[level][i].append((target.targetno, target.target_desc,target.period ,target_value))

        checked_pattern_structure['point_targets'] = point_targets
        return checked_pattern_structure


if __name__ == '__main__':
    d = DataStructure('/Users/liuyichao/PycharmProjects/ptn/raw_data/主力数据/AL_m1_processed.csv', 'cu')
    properties= json.loads(open('/Users/liuyichao/PycharmProjects/ptn/properties/pattern.property').read())
    ptc = PatternCheker(properties=properties, data_structure=d)
    import datetime
    import time
    t = time.time()
    print(t)
    start = datetime.datetime(2004,1,1)
    end = datetime.datetime(2017,1,1)
    ans = ptc.ckeck_patterns_for_all_levels(start, end)
    print ("pattern check over")

    ans = TargetChecker.check_pattern_targets(ans, start, end)


    print("target check over")

    import csv
    write_lines = []

    for i in ans['checked_pattern']['15min']:
        print('checked--------------')
        print('check',ans['checked_pattern']['15min'][i])
        print('targets:')
        if i in ans['point_targets']['15min']:
            for target in ans['point_targets']['15min'][i]:
                write_lines.append([target[2], str(target[3]), ans['data'].data['15min'][i].date_time, ans['data'].data['15min'][i+target[2]-1].date_time])
                print('**')
                print('target is :', target)
                print(target[2])
                for ide in range(i,i+target[2]):
                    print(ans['data'].data['15min'][ide])

    writer = csv.writer(open("pattern_target.csv", 'w'))
    writer.writerows(write_lines)
















