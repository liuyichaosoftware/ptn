from summary.pattern_target_summary import PatternTargetSummary
import csv

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
    line = ['number','>10']
    lines.append(line)
    line = ['CloseT/Open0-1', '>0.3', '>0.3']
    lines.append(line)
    line = ['HighestT/Open0-1', '>0.4', '>0.4']
    lines.append(line)
    line = ['LowestT.open0-1', '>-0.2', '>-0.2']
    lines.append(line)

    lines.append([])
    lines.append(['patterns'])

    return lines


def judge_pattern(param):
    delta = 0.01
    delta_2 = 0.01
    if param['num_ave'] > 10 :
        metrics = param['pattern_sum_metrics']
        if metrics is not None and len(metrics) == 4:
            average = metrics[0]
            mid = metrics[1]
            if len(average) >= 3 and len(mid) >= 3:
                if average[0] > 0.3*delta and average[1] > 0.4*delta and average[2] > -0.2*delta_2 and mid[0] > 0.3*delta and mid[1] >0.4*delta and mid[2] >-0.2*delta_2:
                    return True


    return False


def category_output(name, date_periods, target_ans, target_desc, path):

    write_list = []
    title = ['category', name]
    write_list.append(title)

    target_pattern_category = {}

    for target_no in target_desc:
        target_pattern_category[target_no] = {}

        write_list.append(['target_number', target_no, '', 'target description', target_desc[target_no]['target_desc'], '', 'level', target_desc[target_no]['level']])
        target_title1 = ['','summary','','','','','']
        for date_period in date_periods:
            target_title1 += [str(date_period[0]) + '-' + str(date_period[1]), '', '', '', '']
        write_list.append(target_title1)

        target_title2 = ['pattern','num','average_number','average', 'mid_value','25%_value', '75%_value']
        for date_period in date_periods:
            target_title2 += ['num','average', 'mid_value','25%_value', '75%_value']
        write_list.append(target_title2)

        filtered_patterns = []

        for pattern in target_ans[target_no]:



            if judge_pattern(target_ans[target_no][pattern]):
                filtered_patterns.append(str(pattern[0]) +'-' + str(pattern[1]) +'-'+ str(pattern[2]))
                target_pattern_category[target_no][pattern]=name

            pattern_line = []
            pattern_line.append(str(pattern[0]) +'-' + str(pattern[1]) +'-'+ str(pattern[2]))
            pattern_line.append(str(target_ans[target_no][pattern]['sum_num']))
            pattern_line.append(str(target_ans[target_no][pattern]['num_ave']))

            sum_metrics = target_ans[target_no][pattern]['pattern_sum_metrics']


            #print("metric",target_ans[target_no][pattern])
            #print(sum_metrics)

            if sum_metrics is None or len(sum_metrics) == 0:
                pattern_line += [None,None,None,None]
            else:
                pattern_line += [str(item) for item in sum_metrics]

            nums = target_ans[target_no][pattern]['num']
            metrics = target_ans[target_no][pattern]['pattern_target_metrics']
            for i in range(len(nums)):
                date_metrics = [str(nums[i])]
                if metrics[i] is None or len(metrics[i]) == 0:
                    date_metrics += [None, None, None, None]
                else:
                    date_metrics += [str(item) for item in metrics[i]]
                pattern_line += date_metrics

            write_list.append(pattern_line)
        write_list.append([])


        write_list += filt_desc()
        write_list.append(filtered_patterns)
        write_list.append([])
        write_list.append([])





    writer = csv.writer(open(path, 'w'))
    writer.writerows(write_list)
    return target_pattern_category





def category_process(date_periods, name, patterns, pattern_targets, path):
    '''

    :param date_periods: 时间段们
    :param name: 品类名称
    :param patterns: 所有的Pattern
    :param pattern_targets: 每个时间段对应的summary
    :return:
    '''
    target_ans = {}
    target_desc = {}
    for pattern in patterns:
        pattern_level = pattern[0]
        pattern_type = pattern[1]
        pattern_no = pattern[2]

        #print('pattern', (pattern_level, pattern_type, pattern_no))

        targets = []

        for i in range(len(pattern_targets)):
            pattern_target = pattern_targets[i]
            target = PatternTargetSummary(pattern_level, pattern_type, pattern_no, pattern_target)
            target = target.summary()
            targets.append(target)



            #print(target)

            for target_no in target:
                if target_no not in target_ans:
                    target_ans[target_no] = {}

                    target_desc[target_no] = {}
                    target_desc[target_no]['level'] = pattern_level
                    target_desc[target_no]['target_desc'] = target[target_no]['target_desc']
                    target_desc[target_no]['target_period'] = target[target_no]['target_period']

                if (pattern_level, pattern_type, pattern_no) not in target_ans[target_no]:
                    target_ans[target_no][(pattern_level, pattern_type, pattern_no)] = {}
                    target_ans[target_no][(pattern_level, pattern_type, pattern_no)]['pattern_target_metrics'] = []
                    target_ans[target_no][(pattern_level, pattern_type, pattern_no)]['num'] = []


                #print("TEST")
                #print(target_ans[target_no])
                #print((pattern_level, pattern_type, pattern_no))
                #print(target_ans[target_no][(pattern_level, pattern_type, pattern_no)])

                target_ans[target_no][(pattern_level, pattern_type, pattern_no)]['pattern_target_metrics'].append(target[target_no].get('target_metric_merge', None))
                target_ans[target_no][(pattern_level, pattern_type, pattern_no)]['num'].append(target[target_no].get('num', 0))






        total_target = PatternTargetSummary.merge_target_sums(targets)
        #print(len(targets))
        #print("targets", targets)
        #print("total_mearged", total_target)

        for target_no in total_target:
            target_ans[target_no][(pattern_level, pattern_type, pattern_no)]['pattern_sum_metrics'] = total_target[target_no].get('target_metric_merge', None)
            target_ans[target_no][(pattern_level, pattern_type, pattern_no)]['sum_num'] = total_target[target_no]['num']
            target_ans[target_no][(pattern_level, pattern_type, pattern_no)]['num_ave'] = total_target[target_no]['num_ave']
            target_ans[target_no][(pattern_level, pattern_type, pattern_no)]['target_values'] = total_target[target_no].get('target_values', [[], [], []])
            target_ans[target_no][(pattern_level, pattern_type, pattern_no)]['periods'] = len(date_periods)


        target_pattern_category = category_output(name, date_periods, target_ans, target_desc, path)

    return target_ans, target_pattern_category








