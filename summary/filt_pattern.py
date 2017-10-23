num_ave_per_period_threshold = 10


'''
tuple order : [CloseT/Open0-1, HighestT/Open0-1, LowestT/open0-1]
'''


# average value
average_thresholds = [0.3, 0.4, -0.2]
average_factors = [0.01, 0.01, 0.01]


# mid value
mid_thresholds = [0.3, 0.4, -0.2]
mid_factors = [0.01, 0.01, 0.01]


# direction, long 1.0, short -1.0

direction = 1.0



def filt_desc():
    '''
    返回过滤条件描述
    :return: [[]]
    '''
    lines = []
    line = ['summary_target', 'CloseT/Open0-1', 'HighestT/Open0-1', 'LowestT.open0-1']
    lines.append(line)
    line = ['filter', 'average', 'mid_value']
    lines.append(line)
    line = ['number','>',num_ave_per_period_threshold]
    lines.append(line)

    if len(average_thresholds) > 0 and len(mid_thresholds) > 0:
        line = ['CloseT/Open0-1 * '+str(direction) ,'>' + str(average_thresholds[0]), '>'+str(mid_thresholds[0])]
        lines.append(line)

    if len(average_thresholds) > 1 and len(mid_thresholds) > 1:
        line = ['HighestT/Open0-1 * '+str(direction), '>' + str(average_thresholds[1]), '>'+str(mid_thresholds[1])]
        lines.append(line)

    if len(average_thresholds) > 2 and len(mid_thresholds) > 2:
        line = ['LowestT/open0-1 * '+str(direction), '>' + str(average_thresholds[2]), '>'+str(mid_thresholds[2])]
        lines.append(line)

    lines.append([])
    lines.append(['patterns'])

    return lines





def judge_pattern(param):
    '''        tuple order : [CloseT/Open0-1, HighestT/Open0-1, LowestT/open0-1]

    :param param:
    :return:
    '''


    num_ave_per_period = param.get('num_ave', None)

    if num_ave_per_period is not None and num_ave_per_period > num_ave_per_period_threshold:
        metrics = param['pattern_sum_metrics']
        average_tuple = metrics[0]
        mid_tuple = metrics[1]

        '''
        tuple order : [CloseT/Open0-1, HighestT/Open0-1, LowestT/open0-1]
        '''

        if len(average_tuple) >= len(average_thresholds) and len(mid_tuple) >= len(mid_thresholds):
            flag = True
            for i in range(len(average_thresholds)):
                if average_tuple[i]*direction >  average_thresholds[i] * average_factors[i]:
                    continue
                else:
                    flag = False
                    break
            for i in range(len(mid_thresholds)):
                if mid_tuple[i]*direction > mid_thresholds[i] * mid_factors[i]:
                    pass
                else:
                    flag = False
                    break
            return flag
    return False





'''
    if param['num_ave'] > 10 :
        metrics = param['pattern_sum_metrics']
        if metrics is not None and len(metrics) == 4:
            average = metrics[0]
            mid = metrics[1]
            if len(average) >= 3 and len(mid) >= 3:
                if average[0] > 0.3*delta and average[1] > 0.4*delta and average[2] > -0.2*delta_2 and mid[0] > 0.3*delta and mid[1] >0.4*delta and mid[2] >-0.2*delta_2:
                    return True


    return False
'''