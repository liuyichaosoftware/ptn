# ptn

### 程序介绍
    程序入口是summary里面的pipline, 在pipline中定义要统计的时间段集合, 输入文件夹目录
    
    流程:
    1. 预处理数据, 并给每类数据设置滑点, 写入配置文件
    2. 定义"Pattern"集合, 并在配置文件选取要进行统计的pattern
    3. 定义要统计的target
    4. 设置帅选参数, 运行程序
    
###### 设置滑点
    配置文件在 properties 的 category_slippage.property, 使用Json形式配置,
        {
            # 注释, 以#开头的行是注释
            "AL_m1_processed.csv": [5.0, 3],
            "M_m1_processed.csv": [8.0, 3]
        }
    每一个数据文件的名称 ("AL_m1_processed.csv") 对应的列表 ([5.0, 3]) 有两个元素, 表示该品种每次交易扣5元, 每次统计扣3次, 即总共扣除5*3 = 15元.


###### 定义Pattern并配置
    定义Pattern 在 pattern/pattern_checker.py 
    1. 具体定义写在check函数里面, 我写了注释 "15min" ,在这个里面取定义15min 级别的Pattern; 
       在缩进的下一级里面定义Pattern类型, 这是可以任意定义Pattern类型, 可以任意起名字, 例如 if 'EntryPattern' in check_properties: 就定义了一个新的Pattern 类型 "EntryPattern";  
       再下一个缩进层级里面定义具体的Pattern, 也就是Pattern Number, if '1' in patterns: 定义了该类型下的 "1" 号Pattern, 这里面的"patterns" 由上一层极的 patterns = check_properties['EntryPattern'] 得到,
            然后定义检查该Pattern的具体函数, 返回值为True or False:
                    def check15min_pattern_EntryPattern_1(increase_range = 1.05):
                        if index-2 < 0 or index-1 < 0:
                            return False
                        return self.data.fifteen_mins[index-2].open_price * increase_range < self.data.fifteen_mins[index-1].close_price
            执行该Pattern的检查, 检查到该Pattern 将其添加:
                    if check15min_pattern_EntryPattern_1(** patterns['1']): # 标号 "1"
                        self.add_checked_pattern(ans,'EntryPattern', 1, True) # 标号 1, 具体添加这个Pattern时 是数字 1
            
            * 在pattern_checker 中定义了工具: *
                def upper_level_dataitem(self, check_level, index, target_level):
                当前所在烛线更大级别所对应的烛线到当前烛线之前的部分, 例如15min级别的某烛线, 可以返回当天到该烛线之前的所有部分组成一根新的大级别烛线, 比如, 烛线突破当天最高点可用.
                如果该烛线(index对应)为大一级别第一根烛线, 或者其他无法获取的情况, 返回None, 否则返回大一级别的到当前烛线之前的所有烛线组合.
                    def check15min_pattern_EntryPattern_4():
                        # 今天这根烛线之前的价格合并
                        today = self.upper_level_dataitem('15min', index, 'day')
                        
                        # 该烛线不是当天第一根
                        if today is not None:
                            day_index = self.data.fifteen_mins[index].start_index['day']
                            
                            # 今天这根烛线之前一根再之前的价格合并
                            today_shift = self.upper_level_dataitem('15min', index-1, 'day')
                            
                            # 目标: 今天的高价大于昨天的高价, 并且保证是第一次出现
                            return day_index>=1 and today.high_price > self.data.days[day_index-1].high_price and (today_shift is None or today_shift.high_price<=self.data.days[day_index-1].high_price)
                        return False
                    
                    这只是一个例子, 保证上一根烛线为止,今天的高价第一次大于昨天的高价. 有更好的写法, 该写法只是为了演示 upper_level_dataitem 如何使用.
                
            
    
    2. 定义好Pattern后, 配置需要检查的Pattern, 配置文件在 properties/pattern.property, Json格式, 以 # 开头的行属于注释, 举例:
        {
            # time level
            "15min": {
                "EntryPattern": {
                    "1": {
                        "increase_range": 1.02
                        },
                    "2": {},
                    "3": {}
                },
                "CheckPattern": {
                    "1": {}
                },
                "DatePattern": {
                    "1": {}
                }
            },
            "day": {
                "CheckPattern": {
                    "1": {},
                    "2": {}
                }
            }
        }
        层次同定义, 依次是时间level, Pattern类型, Pattern Number, 每个Pattern的参数. Pattern Number这里写字符串(由于Json 不支持解析key为数字所以用"1")
        Pattern 的参数按照每个Pattern的检查函数的定义配置成字典 {"increase_range": 1.02} 表示该函数里面有一个参数叫increase_range, 值为1.02
    
    
    
##### Target 定义
    定义 Target: target/target_checker.py
    函数: build_target_collection() 里面
        TargetCollection.targets.append(Target("15min", 1, 25, "25"))
        Target() 的参数 时间Level, Target No, 时间段, Target描述(用来给些字符性的描述)
        现在的target计算指标为, [CloseT/Open0-1, HighestT/Open0-1, LowestT/open0-1], 更改的话, 我留了接口, 传入一个func即可,用时再说.
        
        
##### 设置筛选参数:
    summary/filt_pattern.py
    num_ave_per_period_threshold 一个统计周期至少出现多少次该Pattern
    direction 为1 ,做多, 为-1, 做空
    
    
    统计值的顺序: [CloseT/Open0-1, HighestT/Open0-1, LowestT/open0-1]
    
    
    !!!!! *提示 : 如果 direction == -1, 筛选的阈值 如 [0.3, 0.4, -0.2] 要改成 [0.3, -0.2, 0.4] , 最后两个要翻转, !!!!因为三个值描述的是 (收盘时盈利, 最高点时盈利, 最低点是盈利), direction 为 -1 时, 保证最高点时盈利大于某一个负数即可, 最低点时产生最大盈利*
    
    average_thresholds 平均值的阈值
    average_factors 平均值的真实阈值乘数, 如%XX ,就是0.01
    
    mid_thresholds 中值得均值
    mid_factors 中值的真实阈值乘数

##### 运行pipline.py 
    
    统计结果生成在output文件夹
    
    

    