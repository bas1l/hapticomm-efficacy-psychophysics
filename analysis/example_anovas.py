import sys
import statsmodels.api as sm
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.stats.anova import AnovaRM
from scipy import stats
import statistics
from statsmodels.graphics.api import abline_plot

from functions_local import *
import msvcrt as m


def wait():
    m.getch()


def refactor_data_rm_all(data, ans_sel_id):
    type_list = ['slide', 'tap', 'tap-and-hold']
    size_list = ['2-4', '5-8', '9-12']

    # read data into dataframe
    df_ans = pd.DataFrame(columns=["N_SUCCESS", "N_FAILURE"])
    df_var = pd.DataFrame(columns=["participant",
                                   "type_slide", "type_tap", "type_tap_n_hold",
                                   "size_24", "size_58", "size_912"])
    my_row = 0
    for p in range(data.shape[0]):
        for cond in range(1, 10):
            # get lines corresponding to the condition
            idx = np.where(data[p, :, 0] == cond)[0]

            t = [0, 0, 0]
            s = [0, 0, 0]
            t[data[p, idx[0], 1] - 1] = 1
            s[data[p, idx[0], 2] - 1] = 1

            # get mean of the 6 answers
            success = np.sum(data[p, idx, ans_sel_id])
            failure = 6-success

            # store the quadruplet into the DataFrame
            df_ans.loc[my_row] = [success, failure]
            df_var.loc[my_row] = [str(p), t[0], t[1], t[2], s[0], s[1], s[2]]
            my_row = my_row + 1

    return df_ans, df_var


def example_anova2_rm_glm(ans_sel=3):   # 3="type", 4="size"
    path = "data\\"
    files = ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10']
    data, header = read_csvfile(path, files)

    ans, cond = refactor_data_rm_all(data, ans_sel)
    exog = sm.add_constant(cond, prepend=False)

    print(ans)
    print(exog)

    glm_binom = sm.GLM(ans, exog.astype(float), family=sm.families.Binomial(link=sm.families.links.logit()))
    result = glm_binom.fit()
    #table = sm.stats.anova_lm(result, typ=2)  # Type 2 ANOVA DataFrame
    #print(table)
    print(result)
    print(result.summary())

    nobs = result.nobs
    y = ans.iloc[:, 0] / ans.sum(1)
    yhat = result.mu
    print(yhat)

    fig, ax = plt.subplots()
    ax.scatter(yhat, y)
    line_fit = sm.OLS(y, sm.add_constant(yhat, prepend=True)).fit()
    abline_plot(model_results=line_fit, ax=ax)
    ax.set_title('Model Fit Plot')
    ax.set_ylabel('Observed values')
    ax.set_xlabel('Fitted values');
    plt.show()

    fig, ax = plt.subplots()
    ax.scatter(yhat, result.resid_pearson)
    ax.hlines(0, 0, 1)
    ax.set_xlim(0, 1)
    ax.set_title('Residual Dependence Plot')
    ax.set_ylabel('Pearson Residuals')
    ax.set_xlabel('Fitted values')
    plt.show()

    return result


def example_glm_binomial():
    data = sm.datasets.star98.load()
    data.exog = sm.add_constant(data.exog, prepend=False)
    print(data.endog)
    print(data.exog)
    glm_binom = sm.GLM(data.endog, data.exog, family=sm.families.Binomial())
    res = glm_binom.fit()
    print(res.summary())


if __name__ == '__main__':
    example_glm_binomial()
    example_anova2_rm_glm(3)
