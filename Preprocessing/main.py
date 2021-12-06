from functions import *
import pandas as pd
import os

df = pd.read_excel("pilot_data_questionnaires.xlsx", converters={'BE04_01':str, 'BE04_02':str, 'BE04_03':str})
search_path = os.getcwd() + '\\data\\' # location of the data files

# calculate scores for the questionnaires
df = calculateSSQ(df)
df = calculateP(df)
df = calculateEB(df)

# rename columns for more clarity
renameColumns(df)

# sort by participant ID
df = df.sort_values(by=['ID'])

# create data frame with only the relevant columns
data = getRelevantColumns(df)

# add the data from the in-game motion sickness questionnaire
data = getInGameMS(data, search_path)

# save new data frame to csv
data.to_csv("pilot_data_questionnaires_preprocessed.csv", index=False)

