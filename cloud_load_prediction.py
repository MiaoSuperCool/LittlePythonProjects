# import os
import pandas as pd
import numpy as np
from pathlib import Path
# 从sklearn库导入数据分割功能，将数据分为训练集和测试集
from sklearn.model_selection import train_test_split

# 导入随机森林回归模型，用于预测连续数值（CPU使用率）
from sklearn.ensemble import RandomForestRegressor

# 导入模型评价指标：平均绝对误差、均方根误差（通过均方误差计算）、R平方
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score


#=======================1.准备输出结果文件夹======================
output_dir=Path("experiment_3_out")

output_dir.mkdir(parents=True,exist_ok=True)


#定义csv数据文件的路径
file_path="实验课3_云计算资源监测模拟数据集.csv"

#使用pandas的read_csv函数读取CSV文件，存入DataFrame对象df
df=pd.read_csv(file_path)

# 查看数据的形状（行数和列数）
print(f"原始数据形状（行数, 列数）：{df.shape}")
# 查看数据的前5行，了解数据结构
print("\n前5行数据预览：")
print(df.head())
# 查看数据的基本信息：每列的类型、非空值数量等
print("\n数据基本信息：")
print(df.info())

#==============================2.检查数据质量============================

#缺失值检查
missing_value=df.isnull().sum()

#筛选出有缺失值的列（当缺失值数量>0）
missing_with_data=missing_value[missing_value>0]
if len(missing_with_data)>0:
    print("存在缺失值的列：")
    print(missing_with_data)
else:
    print("没有缺失值，数据很完整")

#计算重复记录的数量
duplicate_count=df.duplicated().sum()
print(f"重复记录的数量：{duplicate_count}" )


#异常值检查：检查CPU使用率是否在[0，100]以内并筛选出来
cpu_outliers=df[(df["cpu_usage"]<0)|(df["cpu_usage"]>100)]
print(f"CPU使用率的异常记录数：{len(cpu_outliers)}")

#检查memory_usage小于0或大于100的记录
memory_outliers=df[(df["memory_usage"]<0)|(df["memory_usage"]>100)]
print(f"内存使用率异常记录数：{len(memory_outliers)}")


#==========================3.数据清洗与预处理===================

#使用drop_duplicates方法删除重复的行
df_clean=df.drop_duplicates()
print(f"删除重复值后的数据行数：{len(df_clean)}")

#定义数值列（即需要进行缺失值填充的列）
#这些列都是数值类型的指标
numeric_cols=[
    "cpu_usage", "memory_usage", "network_in", "network_out",
    "disk_io", "request_count", "response_time",
    "active_users", "energy_consumption", "next_cpu_usage"
]

#用中位数填充缺失值
#对每一列，用该列的中位数填充空值
for col in numeric_cols:
    #计算中位数
    median_val=df_clean[col].median() 
    #用中位数填充
    df_clean[col]=df_clean[col].fillna(median_val)
print("缺失值已用中位数填充")


#剔除CPU异常值
before_cpu_filter=len(df_clean)
df_clean=df_clean[(df_clean["cpu_usage"]>=0) & (df_clean["cpu_usage"]<=100)]
after_cpu_filter=len(df_clean)
print(f"剔除CPU有异常的记录数有:{before_cpu_filter-after_cpu_filter}条")

#剔除内存使用率异常值
before_memory_filter=len(df_clean)
df_clean=df_clean[(df_clean["memory_usage"]>=0)&(df_clean["memory_usage"]<=100)]
after_memory_filter=len(df_clean)
print(f"剔除的内存异常记录数有{before_memory_filter-after_memory_filter}条")


#=======================4.特征工程=============================

#将timestamp列转换成datetime类型，这样可以从时间中提取小时，星期等信息
df_clean["timestamp"]=pd.to_datetime(df_clean["timestamp"])

#提取小时特征：一天中的第几个小时
df_clean["hour"]=df_clean["timestamp"].dt.hour

#提取星期信息：一天中的第几天（周一=0，周日=6）
df_clean["dayofweek"]=df_clean["timestamp"].dt.dayofweek

#创建负载等级特征，根据CPU使用率返回负载等级
#先创建应用分类函数
def classify_load(cpu):
    if cpu>=80:
        return "高负载"
    elif cpu>=50:
        return "中负载"
    else:
        return "低负载"

#应用分类函数（上面的这个函数）创建load_level列
df_clean["load_level"]=df_clean["cpu_usage"].apply(classify_load)

#保存第三步中清洗后的文件和时间特性及负载等级特征到清洗后的CSV文件
clean_data_path=output_dir/ 'clean_cloud_resource_data.csv'
df_clean.to_csv(clean_data_path,index=False,encoding='utf-8-sig')
print("已添加时间特征（hour，dayofweek）和负载等级特征(load_level)")


#=====================5.统计分析==========================

#整体资源使用情况统计
#对数值列计算：均值，标准差，最小值，25%分位，50%分位，75%分位，最大值
overall_summary=df_clean[numeric_cols].describe()
#保存到CSV文件
overall_summary_path=output_dir/'overall_resource_summary.cscv'
overall_summary.to_csv(overall_summary_path,encoding="utf-8-sig")
print(f"整体资源统计已保存至: {overall_summary_path}")


#按服务器类型分组统计平均负载
#groupby按server_type分组，agg计算各组各列的均值，round保留2位小数
server_type_summary=df_clean.groupby("server_type").agg(
    {
        "cpu_usage": "mean",        # CPU使用率均值
        "memory_usage": "mean",     # 内存使用率均值
        "request_count": "mean",    # 请求数均值
        "response_time": "mean"     # 响应时间均值
    }
).round(2)

server_type_path=output_dir/'server_type_summary.csv'
server_type_summary.to_csv(server_type_path,encoding="utf-8-sig")
print(f"服务器类型统计已保存至: {server_type_path}")

#统计各负载等级的数量
load_level_count=df_clean["load_level"].value_counts()
load_level_path=output_dir/ 'load_level_count.csv'
load_level_count.to_csv(load_level_path,encoding="utf-8-sig")
print(f"负载等级统计已保存至：{load_level_path}")


# ==================== 6：相关性分析 ====================

# 6.1 定义需要进行相关性分析的列（数值列）
corr_cols = [
    "cpu_usage", "memory_usage", "network_in", "network_out",
    "disk_io", "request_count", "response_time",
    "active_users", "energy_consumption", "next_cpu_usage"
]

# 6.2 计算相关系数矩阵（皮尔逊相关系数）
# corr()计算两两之间的相关系数，范围[-1, 1]，round(3)保留3位小数
corr_matrix = df_clean[corr_cols].corr().round(3)

# 6.3 保存相关性矩阵到CSV文件
corr_path = output_dir/ 'correlation_matrix.csv'
corr_matrix.to_csv(corr_path, encoding="utf-8-sig")
print(f"相关性矩阵已保存至：{corr_path}")

# 6.4 打印与next_cpu_usage相关性最高的5个特征
print("\n与目标变量(next_cpu_usage)相关性最高的5个特征：")
# 提取next_cpu_usage列的相关性，排除自身，按绝对值降序排列
target_corr = corr_matrix["next_cpu_usage"].drop("next_cpu_usage").abs().sort_values(ascending=False)
for feature, corr_val in target_corr.head(5).items():
    print(f"  {feature}: {corr_matrix.loc[feature, 'next_cpu_usage']:.3f}")



# ==================== 7：构建预测模型 ====================
print("\n【步骤7】正在构建预测模型...")

# 7.1 选择特征列（模型输入X）
# 这些特征将用于预测下一时刻的CPU使用率
feature_cols = [
    "memory_usage",      # 当前内存使用率
    "network_in",        # 入站网络流量
    "network_out",       # 出站网络流量
    "disk_io",           # 磁盘读写量
    "request_count",     # 请求数量
    "response_time",     # 响应时间
    "active_users",      # 活跃用户数
    "energy_consumption", # 能耗
    "hour",              # 小时（时间特征）
    "dayofweek"          # 星期几（时间特征）
]

# 7.2 定义特征矩阵X和目标变量y
X = df_clean[feature_cols]      # 输入特征
y = df_clean["next_cpu_usage"]  # 预测目标：下一时刻CPU使用率

print(f"特征列：{feature_cols}")
print(f"特征矩阵形状：{X.shape}")
print(f"目标变量形状：{y.shape}")

# 7.3 划分训练集和测试集
# test_size=0.2表示20%的数据作为测试集，random_state=42保证结果可重复
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"训练集大小：{len(X_train)}，测试集大小：{len(X_test)}")

# 7.4 创建随机森林回归模型
# n_estimators=100表示使用100棵决策树，random_state保证可重复性
model = RandomForestRegressor(n_estimators=100, random_state=42)
print("随机森林回归模型已创建")

# 7.5 训练模型
print("正在训练模型...")
model.fit(X_train, y_train)
print("模型训练完成！")

# 7.6 对测试集进行预测
print("正在进行预测...")
y_pred = model.predict(X_test)
print("预测完成！")


# ==================== 8：模型评价 ====================
print("\n正在进行模型评价...")

# 8.1 计算平均绝对误差（MAE）
# MAE = 平均(|真实值 - 预测值|)，越小越好
mae = mean_absolute_error(y_test, y_pred)

# 8.2 计算均方根误差（RMSE）
# RMSE = sqrt(平均((真实值-预测值)^2))，对大误差更敏感
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# 8.3 计算R平方（R2 Score）
# R2 = 1 - (SS_res / SS_tot)，范围[0,1]，越接近1模型解释能力越强
r2 = r2_score(y_test, y_pred)

# 8.4 打印评价指标
print("\n--- 模型评价指标 ---")
print(f"平均绝对误差（MAE）：{mae:.4f}")
print(f"均方根误差（RMSE）：{rmse:.4f}")
print(f"R平方（R?）：{r2:.4f}")

# 8.5 保存评价指标到文本文件
eval_report_path = output_dir/ 'model_evaluation_report.txt'
with open(eval_report_path, "w", encoding="utf-8") as f:
    f.write("=" * 50 + "\n")
    f.write("云计算资源负载预测模型评价报告\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"模型类型：随机森林回归（Random Forest Regressor）\n")
    f.write(f"决策树数量：100\n\n")
    f.write(f"评价指标：\n")
    f.write(f"  MAE（平均绝对误差）：{mae:.4f}\n")
    f.write(f"    → 平均预测误差为 {mae:.2f} 个百分点\n")
    f.write(f"  RMSE（均方根误差）：{rmse:.4f}\n")
    f.write(f"    → 对大误差的惩罚程度\n")
    f.write(f"  R?（决定系数）：{r2:.4f}\n")
    f.write(f"    → 模型能解释 {r2*100:.1f}% 的CPU使用率变化\n")
print(f"模型评价报告已保存至：{eval_report_path}")


# ====================9：高负载预警 ====================
print("\n【步骤9】正在进行高负载预警分析...")

# 9.1 创建预测结果DataFrame
prediction_result = X_test.copy()
# 添加真实值列
prediction_result["actual_next_cpu_usage"] = y_test.values
# 添加预测值列
prediction_result["predicted_next_cpu_usage"] = y_pred
# 添加预测误差列（真实值 - 预测值，正数表示预测偏低）
prediction_result["prediction_error"] = (
    prediction_result["actual_next_cpu_usage"] - prediction_result["predicted_next_cpu_usage"]
)
# 添加绝对误差列
prediction_result["absolute_error"] = np.abs(prediction_result["prediction_error"])

# 9.2 生成预警标签
# 如果预测的CPU使用率 >= 80%，则标记为"高负载预警"，否则为"正常"
def generate_warning(predicted_cpu):
    """根据预测的CPU使用率生成预警标签"""
    if predicted_cpu >= 80:
        return "高负载预警"
    else:
        return "正常"

prediction_result["warning"] = prediction_result["predicted_next_cpu_usage"].apply(generate_warning)

# 9.3 统计预警结果
warning_count = prediction_result["warning"].value_counts()
print("\n--- 预警统计 ---")
print(warning_count)

# 9.4 计算预警占比
total_records = len(prediction_result)
high_load_count = warning_count.get("高负载预警", 0)
high_load_ratio = (high_load_count / total_records) * 100
print(f"高负载预警记录数：{high_load_count} / {total_records}（占比{high_load_ratio:.2f}%）")

# 9.5 保存预测结果和预警表
warning_result_path = output_dir/ 'load_warning_result.csv'
prediction_result.to_csv(warning_result_path, index=False, encoding="utf-8-sig")
print(f"预测结果与预警表已保存至：{warning_result_path}")
