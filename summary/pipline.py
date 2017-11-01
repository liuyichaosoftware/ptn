from data.data_structure import DataStructure
from pattern.pattern_checker import PatternCheker
import datetime
import os, sys, json
import time

from summary.singular_category_process import category_process
from summary.total_category_process import categories_sum_process

from target.target_checker import TargetChecker

from multiprocessing import cpu_count, Pool


def load_property(path):
    lines = open(path).readlines()
    lines = filter(lambda line :not line.strip().startswith('#'), lines)
    text = '\n'.join(lines)
    return json.loads(text)



def extract_patterns(properties):
    patterns = []
    for level in properties:
        pattern_types = properties[level]
        for pattern_type in pattern_types:
            pattern_nos = pattern_types[pattern_type]
            for pattern_no in pattern_nos:
                patterns.append((level, pattern_type, int(pattern_no)))
    return patterns



# mullti process read slower!!!
def mkDataStructure(item):
    a = DataStructure(item)
    return a

def mk_data_structures(file_list):
    pool = Pool(processes=cpu_count())
    res = [pool.apply_async(mkDataStructure, (item,)) for item in file_list]
    pool.close()
    pool.join()
    return [item.get() for item in res]



## mullti summary slower!!!

def category_sub_process(ptc, date_periods_category):
    category_targets = []
    for date_period in date_periods_category:
        print("Start", time.time() - start_time)
        pattern_res = ptc.ckeck_patterns_for_all_levels(date_period[0], date_period[1])
        slippage_property = slippage_properties.get(ptc.data.name, [0.0, 0])
        slippage = slippage_property[0]
        slippage_num = slippage_property[1]
        targets_res = TargetChecker.check_pattern_targets(pattern_res, date_period[0], date_period[1], slippage, slippage_num)
        print("End", time.time()-start_time)
        category_targets.append(targets_res)
    return category_targets


def mull_process_process(ptcs, date_periods):
    pool = Pool(processes=cpu_count())
    ptc_res = []
    for ptc in ptcs:
        date_periods_category = []
        for date_period in date_periods:
            if date_period[0] < ptc.data.days[-1].date_time:
                date_periods_category.append(date_period)
        ptc_res.append(pool.apply_async(category_sub_process,(ptc, date_periods_category)))
    pool.close()
    pool.join()
    return [item.get() for item in ptc_res]






if __name__ == '__main__':

    time_periods = [((2004,1,1),(2005,1,1)), ((2005,1,1),(2006,1,1)), ((2006,1,1),(2007,1,1)), ((2007,1,1),(2008,1,1)),
                    ((2008,1,1),(2009,1,1)), ((2009,1,1),(2010,1,1)), ((2010,1,1),(2011,1,1)), ((2012,1,1),(2013,1,1)),
                    ((2013,1,1),(2014,1,1)), ((2014,1,1),(2015,1,1)), ((2015,1,1),(2016,1,1)), ((2016,1,1),(2017,1,1))]

    data_dir = '/Users/liuyichao/PycharmProjects/ptn/raw_data/data'
    output_path = '/Users/liuyichao/PycharmProjects/ptn/output'

    properties= load_property('/Users/liuyichao/PycharmProjects/ptn/properties/pattern.property')

    slippage_properties = load_property('/Users/liuyichao/PycharmProjects/ptn/properties/category_slippage.property')



    print(os.listdir(data_dir))

    start_time = time.time()

    file_list = [data_dir+os.sep+item for item in os.listdir(data_dir)]

    patterns = extract_patterns(properties)

    date_periods = [(datetime.datetime(*item[0]), datetime.datetime(*item[1])) for item in time_periods]


    all_targets = {}

    category_sum_targets = []
    target_pattern_categories = []

    names = []

    periods = []



    for file_name in file_list:
        data_structure = DataStructure(file_name)

        ptc = PatternCheker(properties=properties, data_structure=data_structure)
        print("read data over!", ptc.data.name,time.time() - start_time)

        category_targets = []
        date_periods_category = []
        for date_period in date_periods:
            if date_period[0] < ptc.data.days[-1].date_time:
                date_periods_category.append(date_period)

        periods.append(date_periods_category)


        for date_period in date_periods_category:


            pattern_res = ptc.ckeck_patterns_for_all_levels(date_period[0], date_period[1])

            slippage_property = slippage_properties.get(ptc.data.name, [0.0, 0])
            slippage = slippage_property[0]
            slippage_num = slippage_property[1]
            targets_res = TargetChecker.check_pattern_targets(pattern_res, date_period[0], date_period[1], slippage, slippage_num)

            category_targets.append(targets_res)




        all_targets[ptc.data.name] = category_targets

        category_path = output_path + os.sep + ptc.data.name
        target_sum, target_pattern_category= category_process(date_periods_category, ptc.data.name, patterns, category_targets, category_path, data_structure)


        category_sum_targets.append(target_sum)
        target_pattern_categories.append(target_pattern_category)
        names.append(ptc.data.name)

        print("process category",ptc.data.name, "over!", time.time() - start_time)

    targets = TargetChecker.level_targets

    total_path = output_path + os.sep + 'total_summary.csv'

    categories_sum_process(patterns, targets, names, periods, category_sum_targets, target_pattern_categories, total_path)

    print("finished!", time.time() - start_time)
