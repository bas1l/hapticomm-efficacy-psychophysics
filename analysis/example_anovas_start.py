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

from functions_local import *


def example_anova1():
    group_list = ['control', 'patient1', 'patient2']
    subs_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']

    # read data into dataframe
    df_1way = pd.DataFrame(columns=["group", "my_value"])
    my_row = 0
    for ind_g, group in enumerate(group_list):
        for sub in subs_list:
            # generate random value here as example
            my_val = np.random.normal(ind_g, 1, 1)[0]
            df_1way.loc[my_row] = [group, my_val]
            my_row = my_row + 1

    # inspect data
    sns.catplot(x="group", y="my_value", data=df_1way, dodge=True, kind='violin', aspect=3)
    plt.show()

    # generate model for linear regression
    my_model = smf.ols(formula='my_value ~ group', data=df_1way)

    # fit model to data to obtain parameter estimates
    my_model_fit = my_model.fit()

    # print summary of linear regression
    print(my_model_fit.summary())

    # show anova table
    anova_table = sm.stats.anova_lm(my_model_fit, typ=2)
    print(anova_table)

    F, p = stats.f_oneway(df_1way[df_1way['group'] == 'control'].my_value,
                          df_1way[df_1way['group'] == 'patient1'].my_value,
                          df_1way[df_1way['group'] == 'patient2'].my_value)
    print(p)


def example_anova2():
    # information on experimental design
    group_list = ['control', 'patient1', 'patient2']
    language_list = ['English', 'German', 'French']
    subs_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']

    # read data into dataframe
    df_2way = pd.DataFrame(columns=["group", "language", "my_value"])
    my_row = 0
    for ind_g, group in enumerate(group_list):
        for ind_l, lan in enumerate(language_list):
            for sub in subs_list:
                # generate random value here as example
                my_val = np.random.normal(ind_g + ind_l, 1, 1)[0]
                df_2way.loc[my_row] = [group, lan, my_val]
                my_row = my_row + 1

    # plot data
    sns.catplot(x="language", y="my_value", data=df_2way, dodge=True, hue='group', kind='violin', aspect=3)
    plt.show()

    # fit model to data to obtain parameter estimates
    my_model_fit = smf.ols(formula='my_value ~ group * language', data=df_2way).fit()
    # print summary of linear regression
    print(my_model_fit.summary())
    # show anova table
    print(sm.stats.anova_lm(my_model_fit, typ=2))


def refactor_data(data, answer_id):
    type_list = ['slide', 'tap', 'tap-and-hold']
    size_list = ['2-4', '5-8', '9-12']

    # read data into dataframe
    df_2way = pd.DataFrame(columns=["type", "size", "my_value"])
    my_row = 0

    for p in range(data.shape[0]):
        for cond in range(1, 10):
            # get lines corresponding to the condition
            idx = np.where(data[p, :, 0] == cond)[0]

            type_v = type_list[data[p, idx[0], 1] - 1]
            size_v = size_list[data[p, idx[0], 2] - 1]

            # get mean of the 6 answers
            avg_accuracy = np.mean(data[p, idx, answer_id])

            print("condition " + str(cond) + ":")
            print("accuracy=" + str(avg_accuracy))
            print(idx)
            print(data[p, idx, 3])
            print("---")
            # store the triplet into the DataFrame
            df_2way.loc[my_row] = [type_v, size_v, avg_accuracy]
            my_row = my_row + 1

    return df_2way

def example_anova2_withmydata():
    path = "data\\"
    files = ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10']
    # files = ['P01', 'P02']
    answer_id = 3  # 3=type, 4=size (answer's column)
    data, header = read_csvfile(path, files)
    # print(data)
    df_2way = refactor_data(data, answer_id)
    # print(df_2way)

    # plot data
    sns.catplot(x="size", y="my_value", data=df_2way, dodge=True, hue='type', kind='violin', aspect=3)
    # plt.show()

    # fit model to data to obtain parameter estimates
    my_model_fit = smf.ols(formula='my_value ~ type * size', data=df_2way).fit()
    # print summary of linear regression
    print(my_model_fit.summary())
    # show anova table
    print(sm.stats.anova_lm(my_model_fit, typ=2))


def refactor_data_rm(data, answer_id):
    type_list = ['slide', 'tap', 'tap-and-hold']
    size_list = ['2-4', '5-8', '9-12']

    # read data into dataframe
    df_2way = pd.DataFrame(columns=["participant", "type", "size", "my_value"])
    my_row = 0

    for p in range(data.shape[0]):
        for cond in range(1, 10):
            # get lines corresponding to the condition
            idx = np.where(data[p, :, 0] == cond)[0]

            type_v = type_list[data[p, idx[0], 1] - 1]
            size_v = size_list[data[p, idx[0], 2] - 1]

            # get mean of the 6 answers
            avg_accuracy = np.mean(data[p, idx, answer_id])

            # store the quadruplet into the DataFrame
            df_2way.loc[my_row] = [str(p), type_v, size_v, avg_accuracy]
            my_row = my_row + 1

    return df_2way

def example_anova2_repeated_withmydata():
    path = "data\\"
    files = ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10']
    # files = ['P01', 'P02']
    answer_id = 3  # 3=type, 4=size (answer's column)
    data, header = read_csvfile(path, files)
    # print(data)
    df_2way_rm = refactor_data_rm(data, answer_id)

    # conduct ANOVA using mixedlm
    my_model_fit = smf.mixedlm("my_value ~ type * size", df_2way_rm, groups=df_2way_rm["participant"]).fit()
    # get random effects
    print(my_model_fit.random_effects)
    # get fixed effects (no f-test implemented)
    print(my_model_fit.summary())

    # conduct ANOVA using AnovaRM
    my_model_fit = AnovaRM(df_2way_rm, 'my_value', 'participant', within=['type', 'size']).fit()
    print(my_model_fit.anova_table)



def refactor_data_rm_all(data):
    type_list = ['slide', 'tap', 'tap-and-hold']
    size_list = ['2-4', '5-8', '9-12']

    # read data into dataframe
    df_2way = pd.DataFrame(columns=["participant", "type", "size", "ans_type", "ans_size"])
    my_row = 0

    for p in range(data.shape[0]):
        for cond in range(1, 10):
            # get lines corresponding to the condition
            idx = np.where(data[p, :, 0] == cond)[0]

            type_v = type_list[data[p, idx[0], 1] - 1]
            size_v = size_list[data[p, idx[0], 2] - 1]

            # get mean of the 6 answers
            type_acc = np.mean(data[p, idx, 3])
            size_acc = np.mean(data[p, idx, 4])

            # store the quadruplet into the DataFrame
            df_2way.loc[my_row] = [str(p), type_v, size_v, type_acc, size_acc]
            my_row = my_row + 1

    return df_2way






def example_anova2_rm_glm():
    path = "data\\"
    files = ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10']
    # files = ['P01', 'P02']
    data, header = read_csvfile(path, files)
    # print(data)
    df_2way_rm = refactor_data_rm_all(data)

    endog = np.zeros((2, len(df_2way_rm["ans_type"])))  #, dtype=np.int32)
    endog[0, :] = df_2way_rm["ans_type"]
    endog[1, :] = (1-endog[0, :])  #, "ans_size"]]
    endog *= 6

    exog = df_2way_rm[["type", "size"]]
    exog = sm.add_constant(exog, prepend=False)
    print(endog)
    print(exog)
    glm_binom = smf.glm(endog, exog, family=sm.families.Binomial(link=sm.families.links.logit()))

    result = glm_binom.fit()
    print(result)
    print(result.summary())

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
    # example_anova1()
    # example_anova2()
    # example_anova2_withmydata()
    #example_anova2_repeated_withmydata()
    #example_anova2_rm_glm()
    example_glm_binomial()

    sys.exit(1)
