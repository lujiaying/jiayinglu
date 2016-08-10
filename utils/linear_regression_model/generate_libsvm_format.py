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
    dump_svmlight_file(X, y, './uv_5features_price.dat')

if __name__ == '__main__':
    df = pd.read_csv('./deal_features.csv')
    generate_price_category(df)
