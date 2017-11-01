from data.data_structure import DataStructure


def category_period_market_summary(start_time, end_time, category_data, level):
    '''

    :param start_time:
    :param end_time:
    :param category_data:
    :param level:
    :return: price_change, total_num, yang_num, ying_num, shizi_num
    '''

    start_index = 0
    end_index = len(category_data.data[level])
    for index in range(len(category_data.data[level])):
        #print('index', index, start_time, category_data.data[level][index].date_time)
        if start_time <= category_data.data[level][index].date_time:
            start_index = index
            break

    for index in range(start_index, len(category_data.data[level])):
        #print('index2', index, start_time, category_data.data[level][index].date_time)
        if end_time <= category_data.data[level][index].date_time:
            end_index = index
            break

    #print(start_index, end_index)

    total_num = end_index - start_index
    yang_num = 0
    yin_num = 0
    shizi_num = 0

    price_change = (category_data.data[level][end_index-1].close_price * 1.0 - category_data.data[level][start_index].open_price) / category_data.data[level][start_index].open_price * 100.0


    for index in range(start_index, end_index):
        data_item = category_data.data[level][index]
        item_price_change = data_item.close_price - data_item.open_price
        if item_price_change > 0.0001:
            yang_num += 1
        elif item_price_change < -0.0001:
            yin_num += 1
        else:
            shizi_num += 1

    return price_change, total_num, yang_num, yang_num*100.0/total_num, yin_num, yin_num*100.0/total_num ,shizi_num, shizi_num*100.0/total_num

import time, os, datetime


if __name__ == '__main__':
    time_periods = [((2004,1,1),(2005,1,1)), ((2005,1,1),(2006,1,1)), ((2006,1,1),(2007,1,1)), ((2007,1,1),(2008,1,1)),
                    ((2008,1,1),(2009,1,1)), ((2009,1,1),(2010,1,1)), ((2010,1,1),(2011,1,1)), ((2012,1,1),(2013,1,1)),
                    ((2013,1,1),(2014,1,1)), ((2014,1,1),(2015,1,1)), ((2015,1,1),(2016,1,1)), ((2016,1,1),(2017,1,1))]


    data_dir = '/Users/liuyichao/PycharmProjects/ptn/raw_data/data'

    start_time = time.time()

    file_list = [data_dir+os.sep+item for item in os.listdir(data_dir)]

    date_periods = [(datetime.datetime(*item[0]), datetime.datetime(*item[1])) for item in time_periods]

    for file_name in file_list:
        data_structure = DataStructure(file_name)
        print(date_periods[0][0], date_periods[0][1])
        print(category_period_market_summary(date_periods[5][0], date_periods[5][1], data_structure, '15min'))



















