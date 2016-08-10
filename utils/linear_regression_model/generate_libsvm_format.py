#coding: utf-8

import pandas as pd
import numpy as np
from sklearn.datasets import dump_svmlight_file
import sys

def generate_week(df):
    """
    生成1维特征
    """
    X = df[['uv_0612_0618']]
    y = df.uv_0626_0702
    dump_svmlight_file(X, y, './uv_week.dat')

def generate_weekday_weekend(df):
    """
    生成3维特征
    """
    X = df[['uv_0612_0618', 'uv_weekday', 'uv_weekend']]
    y = df.uv_0626_0702
    dump_svmlight_file(X, y, './uv_weekday_weekend.dat')

def generate_weekday_newbuyer_exposure(df):
    """
    加入新客数，曝光数
    """
    X = df[['uv_0612_0618', 'uv_weekday', 'uv_weekend', 'no_subsidy_exposure', 'newbuyer_6_18']]
    y = df.uv_0626_0702
    dump_svmlight_file(X, y, './uv_weekday_weekend_newbuyer_exposure_without_outliers.dat')

def generate_price_category(df):
    """
    加入价格因素，并作离散化
    """
    bins = [0, 11, 20, 30, 50, sys.maxint]
    price_discretized = pd.cut(df.price, bins, right=False, labels=range(len(bins)-1))  # pd.Series
    price_discretized_one_hot = pd.get_dummies(price_discretized)   # pd.DataFrame
    features = pd.concat([df[['uv_0612_0618', 'uv_weekday', 'uv_weekend', 'no_subsidy_exposure', 'newbuyer_6_18']], price_discretized_one_hot], axis=1)

    X = features
    y = df.uv_0626_0702
    dump_svmlight_file(X, y, './uv_5features_price_without_outliers.dat')

def generate_uv_increase_ratio(df):
    """
    加入uv增长率特征
    """
    uv_dates = ['0612', '0613', '0614', '0615', '0616', '0617', '0618']
    df['uv_mean_inc_ratio'] = pd.Series(np.zeros(df.shape[0]))
    for index, uv_date in enumerate(uv_dates):
        if index == 0:
            continue
        df['uv_%s_inc_ratio'%(uv_date)] = (df['uv_%s'%(uv_date)]+1) / (df['uv_%s'%(uv_dates[index-1])]+1) - 1
        df['uv_mean_inc_ratio'] += df['uv_%s_inc_ratio'%(uv_date)]
    df['uv_mean_inc_ratio'] /= (len(uv_date) - 1)
    print 'df.uv_mean_inc_ratio.describe():\n', df.uv_mean_inc_ratio.describe()

    bins = [0, 11, 20, 30, 50, sys.maxint]
    price_discretized = pd.cut(df.price, bins, right=False, labels=range(len(bins)-1))  # pd.Series
    price_discretized_one_hot = pd.get_dummies(price_discretized)   # pd.DataFrame
    features = pd.concat([df[['uv_0612_0618', 'uv_weekday', 'uv_weekend', 'no_subsidy_exposure', 'newbuyer_6_18', 'uv_mean_inc_ratio']], price_discretized_one_hot], axis=1)

    X = features
    y = df.uv_0626_0702
    dump_svmlight_file(X, y, './uv_incRatio_without_outliers.dat')


def clear_outlier():
    """
    根据数据集去除离群点

    假设补贴后uv满足正态分布，则 [mean-3*std, mean+3*std] 外的为离群点
    """
    df = pd.read_csv('./deal_features.csv')
    uv_mean = df.uv_0626_0702.mean()
    uv_std = df.uv_0626_0702.std()
    df = df[(df.uv_0626_0702 <= uv_mean + 3*uv_std) & (df.uv_0626_0702 >= uv_mean - 3*uv_std)]
    df.to_csv('./deal_features_without_outliers.csv', index=False)


if __name__ == '__main__':
    #clear_outlier()

    df = pd.read_csv('./deal_features_without_outliers.csv')
    generate_uv_increase_ratio(df)
