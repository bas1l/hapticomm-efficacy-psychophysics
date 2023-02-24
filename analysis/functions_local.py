
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
    d = np.zeros((n_participant, n_line, n_col+1), dtype=np.int32)

    for ind_f, f in enumerate(files):
        print("Opening file "+ path+f+".csv...")
        firstLine = True
        with open(path+f+".csv", newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')

            for ind_r, row in enumerate(spamreader):
                if firstLine: # remove header
                    firstLine = False
                    d_header = row[1:]
                    continue
                #print('+'.join(row))
                d[ind_f][ind_r-1][1:] = [int(numeric_string) for numeric_string in row[1:]]
                d[ind_f][ind_r-1][0] = (d[ind_f][ind_r-1][1]-1)*3 + d[ind_f][ind_r-1][2]
        print("done.")
    return d, d_header
