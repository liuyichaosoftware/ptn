from data.data_structure import DataStructure
from pattern.pattern_checker import PatternCheker
import datetime
import os, sys, json
import time

from summary.singular_category_process import category_process
from summary.total_category_process import categories_sum_process

from target.target_checker import TargetChecker

def extract_patterns(properties):
    patterns = []
    for level in properties:
        pattern_types = properties[level]
        for pattern_type in pattern_types:
            pattern_nos = pattern_types[pattern_type]
            for pattern_no in pattern_nos:
                patterns.append((level, pattern_type, int(pattern_no)))
    return patterns





if __name__ == '__main__':
    data_dir = '/Users/liuyichao/PycharmProjects/ptn/raw_data/data'

    output_path = '/Users/liuyichao/PycharmProjects/ptn/output'
    properties= json.loads(open('/Users/liuyichao/PycharmProjects/ptn/properties/pattern.property').read())


    print(os.listdir(data_dir))

    start_time = time.time()

    data_structures = [DataStructure(data_dir+os.sep+item) for item in os.listdir(data_dir)]

    print("read data over!",time.time() - start_time)

    patterns = extract_patterns(properties)
    #print(patterns)

    time_periods = [((2004,1,1),(2005,1,1)), ((2005,1,1),(2006,1,1)), ((2006,1,1),(2007,1,1)), ((2007,1,1),(2008,1,1)),
                    ((2008,1,1),(2009,1,1)), ((2009,1,1),(2010,1,1)), ((2010,1,1),(2011,1,1)), ((2012,1,1),(2013,1,1)),
                    ((2013,1,1),(2014,1,1)), ((2014,1,1),(2015,1,1)), ((2015,1,1),(2016,1,1)), ((2016,1,1),(2017,1,1))]

    date_periods = [(datetime.datetime(*item[0]), datetime.datetime(*item[1])) for item in time_periods]

    ptcs = [PatternCheker(properties=properties, data_structure=d) for d in data_structures]

    all_targets = {}

    category_sum_targets = []
    target_pattern_categories = []

    names = []

    periods = []


    for ptc in ptcs:
        category_targets = []
        date_periods_category = []
        for date_period in date_periods:
            if date_period[0] < ptc.data.days[-1].date_time:
                date_periods_category.append(date_period)
        for date_period in date_periods_category:
            pattern_res = ptc.ckeck_patterns_for_all_levels(date_period[0], date_period[1])
            targets_res = TargetChecker.check_pattern_targets(pattern_res, date_period[0], date_period[1])


            category_targets.append(targets_res)
        periods.append(date_periods_category)




        all_targets[ptc.data.name] = category_targets

        category_path = output_path + os.sep + ptc.data.name
        target_sum, target_pattern_category= category_process(date_periods_category, ptc.data.name, patterns, category_targets, category_path)
        category_sum_targets.append(target_sum)
        target_pattern_categories.append(target_pattern_category)
        names.append(ptc.data.name)

        print("process category",ptc.data.name,"over!", time.time() - start_time)

    targets = TargetChecker.level_targets

    total_path = output_path + os.sep + 'total_summary.csv'

    categories_sum_process(patterns, targets, names, periods, category_sum_targets, target_pattern_categories, total_path)

    print("finished!", time.time() - start_time)




















