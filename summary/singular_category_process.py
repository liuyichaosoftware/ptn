from data.data_structure import DataStructure
from market_summary.market_summary import category_period_market_summary
from summary.pattern_target_summary import PatternTargetSummary
import csv

from summary.filt_pattern import *


def category_output(name, date_periods, target_ans, target_desc, path, data_structure):

    write_list = []
    title = ['category', name]
    write_list.append(title)

    target_pattern_category = {}

    write_list.append([])
    write_list.append(['market behavior'])
    market_title = ['level']
    for date_period in date_periods:
        market_title += [str(date_period[0])+'-'+str(date_period[1]),'change_range %', 'total_num', 'positive_shadows','positive_shadows_scale %', 'negative_shadows', 'negative_shadows_scale %', 'calatrava_cross', 'calatrava_cross_scale %']

    write_list.append(market_title)

    for level in DataStructure.time_levels:
        level_data = [level]
        for date_period in date_periods:
            res = category_period_market_summary(date_period[0], date_period[1], data_structure, level)
            level_data += ['', '%.2f'%res[0], res[1], res[2], '%.2f'%res[3], res[4], '%.2f'%res[5], res[6], '%.2f'%res[7]]
        write_list.append(level_data)

    write_list.append([])


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
            pattern_line.append('%.4f'%target_ans[target_no][pattern]['num_ave'])

            sum_metrics = target_ans[target_no][pattern]['pattern_sum_metrics']


            #print("metric",target_ans[target_no][pattern])
            #print(sum_metrics)

            if sum_metrics is None or len(sum_metrics) == 0:
                pattern_line += [None,None,None,None]
            else:
                pattern_line += ['('+', '.join('%.4f'%one for one in item) +')' for item in sum_metrics]

            nums = target_ans[target_no][pattern]['num']
            metrics = target_ans[target_no][pattern]['pattern_target_metrics']
            for i in range(len(nums)):
                date_metrics = [str(nums[i])]
                if metrics[i] is None or len(metrics[i]) == 0:
                    date_metrics += [None, None, None, None]
                else:
                    date_metrics += ['('+', '.join('%.4f'%one for one in item) +')' for item in metrics[i]]
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





def category_process(date_periods, name, patterns, pattern_targets, path, data_structure):
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


        target_pattern_category = category_output(name, date_periods, target_ans, target_desc, path, data_structure)

    return target_ans, target_pattern_category








