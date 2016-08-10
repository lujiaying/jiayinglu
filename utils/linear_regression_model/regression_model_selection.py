# coding: utf-8

from sklearn import linear_model
from sklearn import ensemble
from sklearn.datasets import load_svmlight_file
from sklearn import cross_validation
from sklearn import metrics
from numpy import log1p, expm1
import scipy
import copy
import tqdm
import itertools


if __name__ == '__main__':
    fopen = open('./report_price', 'w')

    X, y = load_svmlight_file('./uv_incRatio_without_outliers.dat')
    fopen.write('Regresser\talpha\tMAE\tMSE\tMedianAE\tR^2\tCorrCoef\tP-Value\t')
    coefs = []
    for i in range(X.shape[1]):
        coefs.append('coef_%s' % (i))
    fopen.write('\t'.join(coefs))
    fopen.write('\n')

    alphas = [0.1, 1.0, 10.0]
    l1_ratio = [0.3, 0.5, 0.8]
    regressors = {}
    ## LinearRegression
    regressors[linear_model.LinearRegression()] = ('Linear Regression', 'None')    # (name, alpha) 
    ## LassoRegression
    for alpha in alphas:
        regressors[linear_model.Lasso(alpha=alpha)] = ('Lasso Regression', '%s'%(alpha))
    ## RidgeRegression
    for alpha in alphas:
        regressors[linear_model.Ridge(alpha=alpha)] = ('Ridge Regression', '%s'%(alpha))
    ## ElasticNet
    for alpha, l1_ratio in itertools.product(alphas, l1_ratio):
        regressors[linear_model.ElasticNet(alpha=alpha, l1_ratio=l1_ratio)] = ('ElasticNet', '%s, l1_ratio=%s'%(alpha, l1_ratio))
    ## Stochastic Gradient Descent
    for alpha in alphas:
        regressors[linear_model.SGDRegressor(alpha=alpha)] = ('SGD Regression', '%s'%(alpha))
    ## Gradient Boosting Regression Tree
    learning_rate_list = [0.01, 0.1, 1]
    n_estimators_list = [100, 200, 300, 500]
    max_depth_list = [3, 4]
    for learning_rate, n_estimators, max_depth in itertools.product(learning_rate_list, n_estimators_list, max_depth_list):
        regressors[ensemble.GradientBoostingRegressor(learning_rate=learning_rate, n_estimators=n_estimators, max_depth=max_depth)] = ('GBRT', 'learn_rate=%s, n_estimators=%s, max_depth=%s' % (learning_rate, n_estimators, max_depth))
    

    # Model Selection
    for clf, (clf_name, clf_param) in tqdm.tqdm(regressors.iteritems()):
        print '\n' + '-' * 40 
        print '%s alpha = %s' % (clf_name, clf_param)
        ## Stage cal metrics by cross_validation
        pred = cross_validation.cross_val_predict(clf, X.toarray(), y, cv=10)
        MAE = metrics.mean_absolute_error(y, pred)
        MSE = metrics.mean_squared_error(y, pred)
        MedianAE = metrics.median_absolute_error(y, pred)
        r2_score = metrics.r2_score(y, pred)
        corr_coef, p_value = scipy.stats.pearsonr(y, pred) 
        print 'mean_absolute_error:', MAE
        print 'mean_squared_error:', MSE
        print 'median_absolute_error:', MedianAE
        print 'r2_score:', r2_score
        print 'correlation coefficient of true and pred:', corr_coef, ', p-value:', p_value
        fopen.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' % (clf_name, clf_param, MAE, MSE, MedianAE, r2_score, corr_coef, p_value))
        """
        离线评价指标，A = (预测值－实际值) / 实际值 * 100%
        A取值    | (-inf, -1) | [-1, -0.75) | [-0.75, 0.5) | [-0.5, -0.25) | [-0.25, 0) | [0, 0.25) | [0.25, 0.5) | [0.5, 0.75) | [0.75, 1) | [1, inf)
        评估标准 |                    < 5%                 |      < 10%    |            > 70%       |     < 10%   |                < 5%
        """
        A = (pred-y)/y
        print 'A belongs to [-0.25, 0.25) = ', A[(A >= -0.25) & (A <0.25)].shape[0] / float(A.shape[0])
        print 'A belongs to [-0.5, -0.25) & [0.25, 0.5) = ', (A[(A >= -0.5) & (A < -0.25)].shape[0] + A[(A >= 0.25) & (A < 0.5)].shape[0] ) / float(A.shape[0])
        ## Stage fit all sample
        print '# fit loss'
        clf.fit(X, y)
        pred_fit = clf.predict(X.toarray())
        MAE_fit = metrics.mean_absolute_error(y, pred_fit)
        MSE_fit = metrics.mean_squared_error(y, pred_fit)
        MedianAE_fit = metrics.median_absolute_error(y, pred_fit)
        r2_score_fit = metrics.r2_score(y, pred_fit)
        print 'mean_absolute_error:', MAE_fit
        print 'mean_squared_error:', MSE_fit
        print 'median_absolute_error:', MedianAE_fit
        print 'r2_score:', r2_score_fit
        coefs = []
        if clf_name == 'GBRT':
            print 'feature_importances_:', clf.feature_importances_
            for i in range(X.shape[1]):
                coefs.append('%s' % (clf.feature_importances_[i]))
        else:
            print 'coef:', clf.coef_
            for i in range(X.shape[1]):
                coefs.append('%s' % (clf.coef_[i]))
        fopen.write('\t'.join(coefs))
        fopen.write('\n')
        print '-' * 40 + '\n'

    fopen.close()
