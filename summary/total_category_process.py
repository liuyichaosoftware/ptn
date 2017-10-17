from summary.singular_category_process import filt_desc
import csv

def merge_category_targets(category_sum_targets):
    target_pattern_category = {}
    for category_sum_target in category_sum_targets:
        for target_no in category_sum_target:
            if target_no not in target_pattern_category:
                target_pattern_category[target_no] = {}
            for pattern in category_sum_target[target_no]:
                if pattern not in target_pattern_category[target_no]:
                    target_pattern_category[target_no][pattern] = {}
                if 'periods' not in target_pattern_category[target_no][pattern]:
                    target_pattern_category[target_no][pattern]['periods'] = 0
                if 'target_values' not in target_pattern_category[target_no][pattern]:
                    target_pattern_category[target_no][pattern]['target_values'] = [[], [], []]
                if 'sum_num' not in target_pattern_category[target_no][pattern]:
                    target_pattern_category[target_no][pattern]['sum_num'] = 0


                if 'periods' in category_sum_target[target_no][pattern]:
                    target_pattern_category[target_no][pattern]['periods'] += category_sum_target[target_no][pattern]['periods']
                if 'target_values' in category_sum_target[target_no][pattern]:
                    for i in range(len(target_pattern_category[target_no][pattern]['target_values'])):
                        if i < len(category_sum_target[target_no][pattern]['target_values']):
                            target_pattern_category[target_no][pattern]['target_values'][i] += category_sum_target[target_no][pattern]['target_values'][i]
                if 'sum_num' in category_sum_target[target_no][pattern]:
                    target_pattern_category[target_no][pattern]['sum_num'] += category_sum_target[target_no][pattern]['sum_num']

    for target_no in target_pattern_category:
        for pattern in target_pattern_category[target_no]:
            ave_num = target_pattern_category[target_no][pattern]['sum_num']/target_pattern_category[target_no][pattern]['periods'] if target_pattern_category[target_no][pattern]['periods']!=0 else 0
            target_pattern_category[target_no][pattern]['ave_num'] = ave_num

            target_values = target_pattern_category[target_no][pattern]['target_values']


            if target_values is None or len(target_values) == 0 or len(target_values[0]) ==0:
                continue

            metrics = []
            for target_value in target_values:
                target_value.sort(reverse=True)
                ave_value = sum(target_value)*1.0 / len(target_value)
                mid_value = target_value[len(target_value)//2] * 0.5 + target_value[(len(target_value)-1)//2] * 0.5
                value_25 = target_value[(len(target_value)-1) // 4]
                value_75 = target_value[(len(target_value)-1)//4 + len(target_value)//2]
                metrics.append([ave_value, mid_value, value_25, value_75])

            target_metric_merge = list(zip(*metrics))
            #print("CHECK")
            #print(target_metric_merge)
            target_pattern_category[target_no][pattern]['target_metric_merge'] = target_metric_merge

    return target_pattern_category




def merge_total_target_pattern_categories(target_pattern_categories):
    target_pattern_sum = {}
    for target_pattern_category in target_pattern_categories:
        #print(target_pattern_category)
        for target_no in target_pattern_category:
            if target_no not in target_pattern_sum:
                target_pattern_sum[target_no] = {}
            patterns = target_pattern_category[target_no]
            if patterns is None or len(patterns) == 0:
                continue
            for pattern in patterns:
                if pattern not in target_pattern_sum[target_no]:
                    target_pattern_sum[target_no][pattern] = set()
                target_pattern_sum[target_no][pattern].add(patterns[pattern])
    #print("CHACHA")
    #print(target_pattern_sum)
    return target_pattern_sum











def categories_sum_process(patterns, targets, names, periods, category_sum_targets, target_pattern_categories, total_path):
    write_lines = []
    merged_pattern_targets = merge_category_targets(category_sum_targets)

    target_pattern_sum = merge_total_target_pattern_categories(target_pattern_categories)

    title = ["categories summary"]
    write_lines.append(title)
    write_lines.append([])

    for level in targets:
        for target in targets[level]:
            target_no = target.targetno
            target_level = target.level
            target_period = target.period
            sub_title = ['target_number', target_no, None, 'target_period', target_period, None, 'target_level',target_level,None, 'summary_metric','[CloseT/Open0-1, HighestT/Open0-1, LowestT.open0-1]']
            write_lines.append(sub_title)
            write_lines.append([])
            total_periods = sum([len(item) for item in periods])
            ave_periods = total_periods * 1.0 / len(periods) if len(periods) != 0 else 0
            sub_title = ['','summary','total_periods', total_periods, 'average_periods', ave_periods,'']
            for name, period in zip(names, periods):
                sub_title += [name, 'periods', len(period),'','']

            write_lines.append(sub_title)

            sub_title = ['patterns', 'total_number', 'average_number', 'average_value','mid_value','25%_value', '75%_value']
            for name in names:
                 sub_title += ['num','average', 'mid_value','25%_value', '75%_value']
            write_lines.append(sub_title)

            for pattern in patterns:
                pattern_line = []
                pattern_str = str(pattern[0]) +'-'+ str(pattern[1]) + '-'+str(pattern[2])
                pattern_line.append(pattern_str)
                sum_num = 0
                ave_num = 0
                if 'sum_num' in merged_pattern_targets[target_no][pattern]:
                    sum_num = merged_pattern_targets[target_no][pattern]['sum_num']
                    if len(periods) > 0:
                        ave_num = sum_num*1.0 / len(periods)

                pattern_line += [sum_num, ave_num]
                sum_metrics = None
                if 'target_metric_merge' in merged_pattern_targets[target_no][pattern]:
                    sum_metrics = merged_pattern_targets[target_no][pattern]['target_metric_merge']
                if sum_metrics is None or len(sum_metrics) == 0:
                    pattern_line += [None,None,None,None]
                else:
                    pattern_line += [str(item) for item in sum_metrics]

                for category_sum_target in category_sum_targets:
                    category_metric = []
                    num = None
                    metric = [None, None, None, None]
                    if target_no in category_sum_target and pattern in category_sum_target[target_no]:
                        tpmp = category_sum_target[target_no][pattern]
                        if 'sum_num' in tpmp:
                            num = tpmp['sum_num']
                        if 'pattern_sum_metrics' in tpmp:
                            metric = [str(item) for item in tpmp['pattern_sum_metrics']]

                    category_metric.append(num)
                    category_metric += metric

                    pattern_line += category_metric

                write_lines.append(pattern_line)

            write_lines.append([])

            write_lines += filt_desc()

            write_lines.append(['patterns', 'num', 'categories'])

            for pattern in patterns:
                if target_no in target_pattern_sum and pattern in target_pattern_sum[target_no]:
                    #print("CAONIMA")
                    pattern_str = str(pattern[0]) +'-' + str(pattern[1]) +'-'+ str(pattern[2])
                    write_lines.append([pattern_str, len(target_pattern_sum[target_no][pattern]), str(list(target_pattern_sum[target_no][pattern]))])

            write_lines.append([])
            write_lines.append([])

    writer = csv.writer(open(total_path, 'w'))
    writer.writerows(write_lines)
