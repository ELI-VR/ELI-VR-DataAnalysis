'''
Main script for the data analysis of the ELI-VR study project

Author: Zora Nolte
Last updated: 02.02.2022
'''

from functions_preprocessing import *
from parameters_preprocessing import *
import pandas as pd
import os

search_path = os.getcwd() + '\\data\\' # location of the data files

##### Preprocessing #####
df = pd.read_excel(search_path + "data_questionnaires.xlsx", converters={'BE04_01':str, 'BE04_02':str, 'BE04_03':str})

# in case the id column missing a 0, prepend it
df['BE04_01'] = df['BE04_01'].str.zfill(3)

# in case the columns with the order of areas is missing a 0, prepend it
df['BE04_02'] = df['BE04_02'].apply(lambda x: '0' + x if len(x) == 4 else x)
df['BE04_03'] = df['BE04_03'].apply(lambda x: '0' + x if len(x) == 4 else x)

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
data.to_csv(search_path + "data_questionnaires_preprocessed.csv", index=False)

##### Data analysis #####

