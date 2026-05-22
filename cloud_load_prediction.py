import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

#====================1.准备输出文件夹及查看基本信息=================
out_dir=Path("experiment_3_output")
out_dir.mkdir(parents=True,exist_ok=True)
file_dir="实验课3_云计算资源监测模拟数据集.csv"
df=pd.read_csv(file_dir)

print(f"原始csv数据形状为：{df.shape}")
print(df.head())
print(f"基本信息：{df.info()}")

#==================2.查看数据质量==============================
#缺失值
missing_value=df.isnull().sum()
missing_value_data=missing_value[missing_value>0]
print(f"存在缺失值的数据列: {missing_value_data}")

#重复值
duplicated_value=df.duplicated().sum()
print(f"重复值共有{duplicated_value}条")

#异常值
cpu_outliers=df[(df["cpu_usage"])<0 | (df["cpu_usage"])>100]
print(f"cpu使用存在异常的情况：{cpu_outliers}")

memory_outliers=df[(df["memory_usage"])<0 | (df["memory_usage"])>100]
print(f"内存使用存在异常的情况：{memory_outliers}")


#==================3.数据清洗和预处理======================
#处理有重复值的行
df_clean=df.drop_duplicates()
print("重复值已清理")

#定义数值列
numeric_clos={
    "cpu_usage", "memory_usage", "network_in", "network_out",
    "disk_io", "request_count", "response_time",
    "active_users", "energy_consumption", "next_cpu_usage"
}

#处理数值列中的空值，用每列的中位数填充
for col in numeric_clos:
    median_val=df_clean[col].median()
    df_clean[col].fillna(median_val)


#移除cpu和内存的使用异常数
df_clean=df_clean[(df_clean["cpu_usage"])>0 & (df_clean["cpu_usage"])<100]
print("cpu异常值已移除")

df_clean=df_clean[(df_clean["memory_usage"])>0 & (df["memory_usage"])<100]
print("内存使用异常值已移除")


#======================4.特征工程==========================
df_clean["timestamp"]=pd.to_datetime(df["timestamp"])

df_clean["hour"]=df_clean["timestamp"].dt.hour
df_clean["dayofweek"]=df_clean["timestamp"].dt.dayofweek

def classify_load(cpu):
    if cpu>=80:
        return "高负载"
    if cpu>=50:
        return "中负载"
    return "低负载"

df_clean["load_level"]=df_clean["cpu_usage"].apply(classify_load)

clean_data_path=out_dir / 'clean_cloud_resource_data'
df_clean.to_csv(clean_data_path,index=False,encoding='utf-8-sig')
print(f"清洗后的数据已保存至：{clean_data_path}")


#=======================5.统计分析=============================
#整体资源使用情况
summary_resource=df_clean[numeric_clos].describe()
summary_resource_path=out_dir / 'overall_resource_summary.csv'
summary_resource.to_csv(summary_resource_path,index=False,encoding='utf-8-sig')
print(f"整体资源使用情况已保存至：{summary_resource_path}")

#按服务器类型分组计算每组的平均负载
server_aver_load=df_clean.groupby("server_type").agg(
    {
        "cpu_usage": "mean",        # CPU使用率均值
        "memory_usage": "mean",     # 内存使用率均值
        "request_count": "mean",    # 请求数均值
        "response_time": "mean"   
    }
).round(3)

server_type_summary_path=out_dir / 'server_type_summary.csv'
server_aver_load.to_csv(server_type_summary_path,index=False,encoding='utf-8-sig')
print(f"按服务器类型分组的平均负载记录已保存至：{server_type_summary_path}")

#对不同类型的负载做一统计
load_level_count=df_clean["load_level"].value_counts()
load_level_count_path=out_dir / 'load_level_count.csv'
load_level_count.to_csv(load_level_count_path,index=False,encoding='utf-8-sig')


#============================6.相关性分析=========================
corre_cols={
    "cpu_usage", "memory_usage", "network_in", "network_out",
    "disk_io", "request_count", "response_time",
    "active_users", "energy_consumption", "next_cpu_usage"
}

#计算相关性矩阵
correlation_matrix=df_clean[corre_cols].corr().round(3)

correlation_matrix_path=out_dir / 'correlation_matrix.csv'
correlation_matrix.to_csv(correlation_matrix_path,index=False,encoding='utf-8-sig')

#打印前五个与cpu_usage相关性最高的特征
top_5_features=correlation_matrix["next_cpu_usage"].drop("next_cpu_usage").abs().sort_values(ascending=False)
for feature,correlation in top_5_features.head().items():
    print(f"{feature}与cpu_usage的相关性为：{correlation_matrix.loc(feature,)}")



#===========================7.构建预测模型=========================
#用于构建预测模型的列
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

#定义特征矩阵X和目标变量y
x=df_clean[feature_cols]
y=df_clean["cpu_usage"]

#构建训练集和测试集
x_train,x_test,y_train,y_test=x.train_test_split(){
    x,test_size=0.2,random_state=42
}

#构建随机森林回归模型
forest_model=RandomForestRegressor(n_estimators=100,random_state=42)

#训练模型
forest_model.fit(x_train,y_train)

#预测
y_pred=forest_model.predict(x_test)


#=============================8.模型评估======================
#计算MAE
mae=mean_absolute_error(y_test,y_pred)

#计算RMSE
rmse=np.sqrt(mean_squared_error(y_test,y_pred))

#计算R的平方R2
r2=r2_score(y_test,y_pred)

#打印输出评估
print("模型评估如下：")
print(f"MAE的计算结果为：{mae:.4f}")
print(f"RMSE的计算结果为：{rmse:.4f}")
print(f"R2的计算结果为{r2:.4f}")

#将报告写入model_evaluation_report txt文件
model_evaluation_report=out_dir / 'model_evaluation_report.txt'
with open(model_evaluation_report,"w") as f:
    f.write(f"MAE的计算结果为：{mae:.4f}")
    f.write(f"RMSE的计算结果为：{rmse:.4f}")
    f.write(f"R2的计算结果为{r2:.4f}")
print(f"已将模型评估报告写入{model_evaluation_report}")


#=====================9.高负载预警=======================
prediction=x_test.copy()

#添加实际的值
prediction["actual_next_cpu_usage"]=y_test.values

#添加预测值
prediction["predicted_next_cpu_usage"]=y_pred

#添加实际值和预测值之间的误差
prediction["prediction_error"]=prediction["actual_next_cpu_usage"]-prediction["predicted_next_cpu_usage"]

#添加绝对值误差
prediction["absolute_error"]=prediction["prediction_error"].abs()

#生成预警等级函数
def warning_level(predict_cpu):
    """根据预测的CPU使用率生成预警标签"""
    if predicted_cpu >= 80:
        return "高负载预警"
    else:
        return "正常"
    
#使用函数来生成预警列
prediction["warning"]=prediction["predicted_next_cpu_usage"].apply(warning_level)

total_count=prediction["warning"].value_count()
high_warning_count=prediction["warning"].value_count()
print(f"高负载预警有：{high_warning_count}条")
print(f"占比为：{high_warning_count/total_count}")

load_warning_result_path=out_dir / 'load_warning_result'
prediction.to_csv(load_level_count_path,index=False,encoding='utf-8-sig')
print(f"预警信息已保存至：{load_level_count_path}")