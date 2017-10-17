import csv
import datetime

def mkdatetimefromstr(datetime_str):
    sp = datetime_str.split(' ')
    date_str = sp[0]
    time_str = sp[1]
    dates = date_str.split('-')
    times = time_str.split(':')
    return datetime.datetime(int(dates[0]), int(dates[1]), int(dates[2]), int(times[0]), int(times[1]), int(times[2]))



class DataStructure:
    time_levels = ["day", "15min", "5min", "1min"]
    def __init__(self, path, name=None):

        self.path = path
        self.file_name = path.split('\\')[-1]
        if '/' in self.file_name:
            self.file_name = self.file_name.split('/')[-1]

        if name:
            self.name = name
        else:
            self.name = self.file_name
        br = csv.reader(open(path, 'r', encoding = 'gbk'))
        raw_data = []
        for row in br:
            raw_data.append(row)
        title = raw_data[0]
        #print(title)


        #raw_data = raw_data[1:]

        raw_data = raw_data[0:]
        #print("read over!")
        #print(raw_data[0])
        #print(raw_data[1])
        #print(raw_data[2])



        self.one_mins = []


        for i in range(len(raw_data)):
            item = raw_data[i]
            if len(item) == 11:
                item_temp = [item[0]+' '+item[1], item[9], item[10]]
                item_temp += item[2:9]
                item = item_temp

            data_item = DataItem(marcket_code = item[1], contract_code=item[2], date_time=mkdatetimefromstr(item[0]),
                     open_price=float(item[3]), high_price=float(item[4]), low_price=float(item[5]), close_price=float(item[6]), volume=float(item[7]),
                     amount=float(item[8]), open_interest=float(item[9]), index=i)
            data_item.start_index[DataStructure.time_levels[-1]] = i
            data_item.end_index[DataStructure.time_levels[-1]] = i+1

            self.one_mins.append(data_item)


        # 5mins
        self.five_mins = []

        end_indexes = list(map(lambda item:item.end_index[DataStructure.time_levels[-1]] ,filter(lambda item:item.date_time.minute % 5 ==0, self.one_mins)))
        #print(end_indexes[0])
        start_indexes = [0] + end_indexes[:-1]

        for start,end in zip(start_indexes, end_indexes):
            index = len(self.five_mins)
            data_item = DataItem.merge_dataitems(self.one_mins[start:end], index)
            data_item.start_index[DataStructure.time_levels[-2]] = index
            data_item.end_index[DataStructure.time_levels[-2]] = index + 1

            data_item.start_index[DataStructure.time_levels[-1]] = start
            data_item.end_index[DataStructure.time_levels[-1]] = end

            for i in range(start, end):
                self.one_mins[i].start_index[DataStructure.time_levels[-2]] = index
                self.one_mins[i].end_index[DataStructure.time_levels[-2]] = index + 1

            self.five_mins.append(data_item)


        # 15mins
        self.fifteen_mins = []

        end_indexes = list(map(lambda item:item.end_index[DataStructure.time_levels[-2]], filter(lambda item:item.date_time.minute % 15 ==0, self.five_mins)))
        start_indexes = [0] + end_indexes[:-1]


        for start,end in zip(start_indexes, end_indexes):
            index = len(self.fifteen_mins)
            data_item = DataItem.merge_dataitems(self.five_mins[start:end], index)
            data_item.start_index[DataStructure.time_levels[-3]] = index
            data_item.end_index[DataStructure.time_levels[-3]] = index + 1

            data_item.start_index[DataStructure.time_levels[-2]] = start
            data_item.end_index[DataStructure.time_levels[-2]] = end

            for i in range(start, end):
                self.five_mins[i].start_index[DataStructure.time_levels[-3]] = index
                self.five_mins[i].end_index[DataStructure.time_levels[-3]] = index + 1

            one_min_start = self.five_mins[start].start_index[DataStructure.time_levels[-1]]
            one_min_end = self.five_mins[end-1].end_index[DataStructure.time_levels[-1]]

            data_item.start_index[DataStructure.time_levels[-1]] = one_min_start
            data_item.end_index[DataStructure.time_levels[-1]] = one_min_end

            #print(one_min_start,one_min_end)

            for i in range(one_min_start, one_min_end):
                self.one_mins[i].start_index[DataStructure.time_levels[-3]] = index
                self.one_mins[i].end_index[DataStructure.time_levels[-3]] = index + 1
                #print(self.one_mins[i].start_index)

            self.fifteen_mins.append(data_item)


        # days
        self.days = []
        end_indexes = []
        for i in range(len(self.fifteen_mins) - 1):
            if not (self.fifteen_mins[i].date_time.year == self.fifteen_mins[i+1].date_time.year and
                self.fifteen_mins[i].date_time.month == self.fifteen_mins[i+1].date_time.month and
                self.fifteen_mins[i].date_time.day == self.fifteen_mins[i+1].date_time.day):
                end_indexes.append(i+1)
        end_indexes.append(len(self.fifteen_mins))
        start_indexes = [0] + end_indexes[:-1]

        for start,end in zip(start_indexes, end_indexes):
            index = len(self.days)
            data_item = DataItem.merge_dataitems(self.fifteen_mins[start:end], index)
            data_item.start_index[DataStructure.time_levels[-4]] = index
            data_item.end_index[DataStructure.time_levels[-4]] = index + 1

            data_item.start_index[DataStructure.time_levels[-3]] = start
            data_item.end_index[DataStructure.time_levels[-3]] = end

            five_min_start = self.fifteen_mins[start].start_index[DataStructure.time_levels[-2]]
            five_min_end = self.fifteen_mins[end-1].end_index[DataStructure.time_levels[-2]]

            data_item.start_index[DataStructure.time_levels[-2]] = five_min_start
            data_item.end_index[DataStructure.time_levels[-2]] = five_min_end

            one_min_start = self.five_mins[five_min_start].start_index[DataStructure.time_levels[-1]]
            one_min_end = self.five_mins[five_min_end-1].end_index[DataStructure.time_levels[-1]]

            data_item.start_index[DataStructure.time_levels[-1]] = one_min_start
            data_item.end_index[DataStructure.time_levels[-1]] = one_min_end

            for i in range(start, end):
                self.fifteen_mins[i].start_index[DataStructure.time_levels[-4]] = index
                self.fifteen_mins[i].end_index[DataStructure.time_levels[-4]] = index + 1

            for i in range(five_min_start, five_min_end):
                self.five_mins[i].start_index[DataStructure.time_levels[-4]] = index
                self.five_mins[i].end_index[DataStructure.time_levels[-4]] = index + 1

            for i in range(one_min_start, one_min_end):
                self.one_mins[i].start_index[DataStructure.time_levels[-4]] = index
                self.one_mins[i].end_index[DataStructure.time_levels[-4]] = index + 1

            self.days.append(data_item)

        self.data = {'day':self.days, '15min':self.fifteen_mins, '5min':self.five_mins, '1min':self.one_mins}

    def output(self, level, path):
        output_data = self.data[level]
        write_lines = []
        for data in output_data:
            date = str(data.date_time).split(' ')
            write_lines.append([date[0], date[1], data.open_price, data.high_price, data.low_price, data.close_price, data.volume, data.amount, data.open_interest, data.marcket_code, data.contract_code])

        writer = csv.writer(open(path, 'w'))
        writer.writerows(write_lines)




















        #map(lambda item:{'market_code': item[0], ''} ,)



class DataItem:
    def __init__(self, marcket_code, contract_code, date_time, open_price, high_price, low_price, close_price, volume, amount, open_interest, index):
        self.marcket_code = marcket_code
        self.contract_code = contract_code
        self.date_time = date_time
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
        self.amount = amount
        self.open_interest = open_interest
        self.index = index
        self.start_index = {}
        self.end_index = {}

    def __str__(self):
        return "marcket_code:"+self.marcket_code+"\tcontract_code:"+self.contract_code+"\tself.date_time:"+str(self.date_time)+\
               "\topen_price:"+str(self.open_price)+"\thigh_price:"+str(self.high_price)+"\tlow_price:"+str(self.low_price)+\
               "\tclose_price:"+str(self.close_price)+"\tvolume:"+str(self.volume)+"\tamount:"+str(self.amount)+"\topen_interest:"+str(self.open_interest)+\
               "\tindex:"+str(self.index)+"\tstart_index:"+str(self.start_index)+"\tend_index:"+str(self.end_index)+"\n"





    def set_level_indexes(self, start_index, end_index):
        '''

        :param start_index: a dict, with each level
        :param end_index: a dict, with each level
        :return:
        '''
        self.start_index = start_index
        self.end_index = end_index


    def merge_dataitems(dataitems, index):
        marcket_code = dataitems[-1].marcket_code
        contract_code = dataitems[-1].contract_code
        date_time = max(map(lambda item:item.date_time, dataitems))
        open_price = dataitems[0].open_price
        high_price = max(map(lambda item:item.high_price, dataitems))
        low_price =  min(map(lambda item:item.low_price, dataitems))
        close_price = dataitems[-1].close_price
        volume = sum(map(lambda item:item.volume, dataitems))
        amount = sum(map(lambda item:item.amount, dataitems))
        open_interest = dataitems[-1].open_interest
        return DataItem(marcket_code, contract_code, date_time, open_price, high_price, low_price, close_price, volume, amount, open_interest, index)






if __name__ == '__main__':


    d = DataStructure('/Users/liuyichao/PycharmProjects/ptn/raw_data/data/AL_m1_processed.csv', 'cu')
    d.output('15min', '/Users/liuyichao/PycharmProjects/ptn/raw_data/processed/AL_m1_processed_15min.csv')

    print(d.one_mins[0])
    print(d.one_mins[1])
    print(d.one_mins[2])
    print('----')


    print(d.five_mins[0])
    print(d.five_mins[1])


    print('----')
    print(d.fifteen_mins[0])
    print(d.fifteen_mins[1])
    print('---')
    print(d.days[0])
    print(d.days[1])

