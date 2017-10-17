class PatternTargetSummary:

    def __init__(self, pattern_level, pattern_type, pattern_no, pattern_targets_structure, summary_func=None):
        self.pattern_level = pattern_level
        self.pattern_type = pattern_type
        self.pattern_no = pattern_no
        #self.pattern_points = pattern_points
        self.pattern_targets_structure = pattern_targets_structure
        if summary_func is None:
            def summary_cal_func(points, targets):
                targets_sum = {}
                for point in points:
                    if point in targets:
                        for target in targets[point]:
                            #print('target')
                            #print(target)
                            if target[0] not in targets_sum:
                                targets_sum[target[0]] = {}
                            if 'target_desc' not in targets_sum[target[0]]:
                                targets_sum[target[0]]['target_desc'] = target[1]
                            if 'target_period' not in targets_sum[target[0]]:
                                targets_sum[target[0]]['target_period'] = target[2]
                            if 'target_value' not in targets_sum[target[0]]:
                                targets_sum[target[0]]['target_value'] = []
                            targets_sum[target[0]]['target_value'].append(target[3])

                for target_no in targets_sum:
                    targets_sum[target_no]['num'] = len(targets_sum[target_no]['target_value'])

                    target_metric = []
                    target_values = []
                    if targets_sum[target_no]['num'] != 0:
                        #print("TEST")
                        #print(targets_sum[target_no]['target_value'][0])
                        for i in range(0, len(targets_sum[target_no]['target_value'][0])):
                            target_value = []
                            for value in targets_sum[target_no]['target_value']:
                                target_value.append(value[i])
                            target_value.sort(reverse=True)
                            target_values.append(target_value)
                            ave = sum(target_value) * 1.0/ len(target_value)
                            #print(target_value)
                            midvalue = target_value[len(target_value) // 2] if len(target_value) % 2 == 1 else (target_value[len(target_value) // 2] + target_value[len(target_value) // 2 -1]) * 0.5
                            value_25 = target_value[(len(target_value)-1) // 4]
                            value_75 = target_value[len(target_value)//2 + (len(target_value)-1)//4]

                            target_metric.append([ave, midvalue, value_25, value_75])

                        targets_sum[target_no]['target_metric'] = target_metric
                        targets_sum[target_no]['target_values'] = target_values
                        targets_sum[target_no]['target_metric_merge'] = list(zip(*target_metric))
                return targets_sum

            self.summary_func = summary_cal_func
        else:
            self.summary_func = summary_func
        #print(self.summary_func, self.pattern_targets_structure)

    def summary(self):
        pattern_points_structure = self.pattern_targets_structure['checked_pattern'][self.pattern_level]
        #print('pattern_points_structure')
        #print(pattern_points_structure)
        pattern_points = []
        for i in pattern_points_structure:
            if self.pattern_type in pattern_points_structure[i]:
                #print('QQ')
                flag = False
                if True not in pattern_points_structure[i][self.pattern_type]:
                    continue
                for item in pattern_points_structure[i][self.pattern_type][True]:
                    #print(item, self.pattern_no)
                    #print(item[0], self.pattern_no,type(item[0]), type(self.pattern_no))
                    if item[0] == self.pattern_no:
                        #print('checked', item[0], item, i)
                        flag = True
                        break
                if flag:
                    pattern_points.append(i)

        #print("pattern_points")
        #print(pattern_points)

        targets = self.pattern_targets_structure['point_targets'][self.pattern_level]

        targets_sum = self.summary_func(pattern_points, targets)

        return targets_sum
    @staticmethod
    def merge_target_sums(targets_sums):
        sum_metric = {}
        for targets_sum in targets_sums:
            for target_no in targets_sum:
                if target_no not in sum_metric:
                    sum_metric[target_no] = {}
                if 'num' not in sum_metric[target_no]:
                    sum_metric[target_no]['num'] = 0





                if 'target_values' in targets_sum[target_no]:
                    if 'target_values' not in sum_metric[target_no]:
                        sum_metric[target_no]['target_values'] = []
                        for i in range(len(targets_sum[target_no]['target_values'])):
                            sum_metric[target_no]['target_values'].append([])
                        #print("SUM")
                        #print(sum_metric[target_no]['target_values'])

                    for i in range(0,len(sum_metric[target_no]['target_values'])):
                        sum_metric[target_no]['target_values'][i] += targets_sum[target_no]['target_values'][i]
                        #print("CHECKED")
                        #print(len(targets_sum[target_no]['target_values'][i]))
                        #print(targets_sum[target_no]['target_values'][i])
                        #print(targets_sum[target_no]['num'])


                #sum_metric[target_no]['target_values'] += targets_sum[target_no].get('target_values', [])
                #print('num', sum_metric[target_no]['num'], targets_sum[target_no]['num'])
                sum_metric[target_no]['num'] += targets_sum[target_no]['num']




        for target_no in sum_metric:
            #print('-------num--------')
            #print(sum_metric[target_no]['num'])
            sum_metric[target_no]['num_ave'] = sum_metric[target_no]['num']*1.0 / len(targets_sums)
            target_values = sum_metric[target_no].get('target_values', None)
            if target_values is None:
                #print("XXX1")
                continue

            #print('check_values')
            #print(len(taget_values))

            target_metric = []
            if len(target_values) == 0 or len(target_values[0]) ==0 :
                #print("XXXX")
                continue

            for values in target_values:
                #print('-------values------')
                #print(len(values))
                #print(values)
                values.sort(reverse=True)
                ave = None
                midvalue = None
                value_25 = None
                value_75 = None

                if len(values) != 0:
                    ave = sum(values) * 1.0 / len(values)
                    midvalue = values[(len(values)-1) // 2] if len(values)%2 == 1 else (values[(len(values)-1)//2] + values[len(values)//2]) * 0.5
                    value_25 = values[(len(values)-1) // 4]
                    value_75 = values[(len(values)-1)//4 + len(values)//2]

                target_metric.append([ave, midvalue, value_25, value_75])

            sum_metric[target_no]['target_metric'] = target_metric
            sum_metric[target_no]['target_metric_merge'] = list(zip(*target_metric))

        return sum_metric

if __name__ == '__main__':
    from data.data_structure import DataStructure
    from pattern.pattern_checker import PatternCheker
    from target.target_checker import TargetChecker
    import json

    #d = DataStructure('/Users/liuyichao/PycharmProjects/ptn/raw_data/主力数据/a_continuous.csv', 'cu')
    d = DataStructure('/Users/liuyichao/PycharmProjects/ptn/raw_data/data/AL_m1_processed.csv', 'cu')

    properties= json.loads(open('/Users/liuyichao/PycharmProjects/ptn/properties/pattern.property').read())
    ptc = PatternCheker(properties=properties, data_structure=d)
    import datetime
    import time
    t = time.time()
    print(t)
    start = datetime.datetime(2004,1,1)
    end = datetime.datetime(2005,1,1)

    ans = ptc.ckeck_patterns_for_all_levels(start, end)
    print ("pattern check over")
    print(ans['checked_pattern'])


    ans = TargetChecker.check_pattern_targets(ans, start, end)
    print("target check over")
    print(ans['point_targets'])

    target1 = PatternTargetSummary('15min', 'EntryPattern', 3, ans)
    target1 = target1.summary()

    print('target1')
    print(target1)


    start = datetime.datetime(2005,1,1)
    end = datetime.datetime(2006,1,1)

    ans = ptc.ckeck_patterns_for_all_levels(start, end)
    print("pattern check over")

    ans = TargetChecker.check_pattern_targets(ans, start, end)

    print("target check over")

    target2 = PatternTargetSummary('15min', 'EntryPattern', 3, ans)
    target2 = target2.summary()

    print('target2')
    print(target2)

    print('------')

    t = PatternTargetSummary.merge_target_sums([target1, target2])

    print('total')
    print(t)

    pass