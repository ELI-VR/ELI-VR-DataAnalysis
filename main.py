'''
Main script for the data analysis of the ELI-VR study project

Author: Zora Nolte
Last updated: 08.12.2021
'''

from functions import *
from parameters import *
import pandas as pd
import os

search_path = os.getcwd() + '\\data\\' # location of the data files

##### Preprocessing #####
df = pd.read_excel(search_path + "pilot_data_questionnaires.xlsx", converters={'BE04_01':str, 'BE04_02':str, 'BE04_03':str})

# calculate scores for the questionnaires (outside VR)
df = calculateSSQ(df, items=items_SSQ, weights=weights_SSQ)
df = calculateP(df, items=items_P)
df = calculateEB(df, items=items_EB)

# rename columns for more clarity
renameColumns(df, dict_renaming)

# sort by participant ID
df = df.sort_values(by=['ID'])

# create data frame with only the relevant columns
data = getRelevantColumns(df, relevant_cols)

# add the data from the in-game motion sickness questionnaire (inside VR)
data = getInGameMS(data, search_path)

# save new data frame to csv
data.to_csv(search_path + "pilot_data_questionnaires_preprocessed.csv", index=False)

##### Data analysis #####

