import sys
import statsmodels.api as sm
import csv
import numpy as np


def read_csvfile(path, files):

    n_participant = len(files)
    n_col = 4
    n_type = 3
    n_size = 3
    n_rep = 6
    n_line = n_type * n_size * n_rep

    d_header = ["" for x in range(n_col)]
    d = np.zeros((n_participant, n_line, n_col))

    for ind_f, f in enumerate(files):
        firstLine = True
        with open(path+f+".csv", newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')

            for ind_r, row in enumerate(spamreader):
                if firstLine: # remove header
                    firstLine = False
                    d_header = row[1:]
                    continue
                #print('+'.join(row))
                d[ind_f][ind_r-1] = [int(numeric_string) for numeric_string in row[1:]]

    return d, d_header


def preprocess_data(data):
    d = 0

    return d


def execute_analysis(data):
    data = sm.datasets.scotland.load()
    data.exog = sm.add_constant(data.exog)

    # Instantiate a gamma family model with the default link function.
    gamma_model = sm.GLM(data.endog, data.exog, family=sm.families.Gamma())
    gamma_results = gamma_model.fit()

    print(gamma_results.summary())


def execute():
    path = "data\\"
    #files = ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10']
    files = ['P01', 'P02']
    data, header = read_csvfile(path, files)
    #data = preprocess_data(data)
    #glm_binom = sm.GLM(data.endog, data.exog, family=sm.families.Binomial())
    print(data)



if __name__ == '__main__':

    execute()

    sys.exit(1)