import sys
import os
import gc

# data manipulation modules
import pandas as pd
import numpy as np

# plot modules
import matplotlib.pyplot as plt
import seaborn as sns

# statistics modules
from scipy.stats import norm
from statistics import stdev, mean



NUM_OF_GHOULS = 0
NUM_OF_GOBLINS = 0
NUM_OF_GHOSTS = 0



def get_type_id_pair(df):
    # use this for metrics calculation.
    id_type_unordered_pair = [(monster_id, monster_type) for monster_id in df['id'] for monster_type in df.loc[(df['id'] == monster_id)]["type"]]
    return id_type_unordered_pair



def calculate_type_appearances(df):
    global NUM_OF_GHOULS, NUM_OF_GOBLINS, NUM_OF_GHOSTS

    NUM_OF_GHOULS = len(df[df.type == 0])
    NUM_OF_GOBLINS = len(df[df.type == 1])
    NUM_OF_GHOSTS = len(df[df.type == 2])



def store_train_data(csv_path: str):
    df = pd.read_csv(csv_path)
    cols = df.columns
    cols = [col for col in cols]

    colour_id_list = [colour_id for colour_id in df.drop_duplicates(subset='color')['color']]

    for i in range(len(df)):
        if df.at[i, 'color'] == colour_id_list[0]:
            df.at[i, 'color'] = 1
        elif df.at[i, 'color'] == colour_id_list[1]:
            df.at[i, 'color'] = 2
        elif df.at[i, 'color'] == colour_id_list[2]:
            df.at[i, 'color'] = 3
        elif df.at[i, 'color'] == colour_id_list[3]:
            df.at[i, 'color'] = 4
        elif df.at[i, 'color'] == colour_id_list[4]:
            df.at[i, 'color'] = 5
        elif df.at[i, 'color'] == colour_id_list[5]:
            df.at[i, 'color'] = 6



        if df.at[i, 'type'] == "Ghoul":
            df.at[i, 'type'] = 0
        elif df.at[i, 'type'] == "Goblin":
            df.at[i, 'type'] = 1
        elif df.at[i, 'type'] == "Ghost":
            df.at[i, 'type'] = 2

    return df


def gauss_pdf(x_value, type_array, feature_id):
    # calcuates the likelihood probability = p(x|omega(type)), given that x follows gaussian distribution

    if feature_id not in range(1, 5):
        sys.exit("Feature id must in range [1, 4].")

    sample_mean = np.mean(type_array, 0)[feature_id]
    sample_variance = np.var(type_array, 0)[feature_id]

    # term11 = -(np.sum(np.log(np.sqrt(sample_variance))))
    # term22 = -(np.sum((x_value - sample_mean) ** 2 / (2 * sample_variance)))

    term1 = 1 / (np.sqrt(2 * np.pi * (sample_variance)))
    gauss_exp_numerator = - np.power((x_value - sample_mean), 2)
    gauss_exp_denominator = 2 * (sample_variance)
    term2 = np.exp(gauss_exp_numerator / gauss_exp_denominator)

    return (term1 * term2)

def main(*args):
    df = store_train_data("train.csv")
    calculate_type_appearances(df)
    classes = np.unique(df.type)

    samples = [np.array(df.loc[df['type'] == idx]) for idx, el in enumerate(classes)]

    ghoul_array = samples[0]
    goblins_array = samples[1]
    ghost_array = samples[2]

    print_test(df, ghoul_array, goblins_array, ghost_array)




def print_test(df, ghoul_array, goblins_array, ghost_array):
    for i in range(len(df)):
        print("Element no. {}:".format(i))
        for j in range(1, 5):
            print(gauss_pdf(np.array(df)[i][j], ghoul_array, j))
            print(gauss_pdf(np.array(df)[i][j], goblins_array, j))
            print(gauss_pdf(np.array(df)[i][j], ghost_array, j))

            if j != 4:
                print('\n' * 1)
        print("-----------------------------------------------------------")

if __name__ == "__main__":
	main()
