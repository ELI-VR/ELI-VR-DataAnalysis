from functions import *
import pandas as pd

df = pd.read_excel("pilot_data_questionnaires.xlsx", converters={'BE04_02':str,'BE04_03':str})

# calculate scores for the questionnaires
calculateSSQ(df)
calculateP(df)
calculateEB(df)

# rename columns for more clarity
renameColumns(df)

# create data frame with only the relevant columns
data = getRelevantColumns(df)

# save new data frame to csv
data.to_csv("pilot_data_questionnaires_preprocessed.csv", index=False)

