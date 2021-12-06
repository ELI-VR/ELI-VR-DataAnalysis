import pandas as pd
import os
import re
import json


def calculateSSQ(df):
    '''
    calculates the scores for the Simulator Sickness Questionnaire (https://doi.org/10.1207/s15327108ijap0303_3)

    subscales:
    O: Oculomotor (items: 1, 2, 3, 4, 5, 9, 11)
    D: Disorientation (items: 5, 8, 10, 11, 12, 13, 14)
    N: Nausea (items: 1, 6, 7, 8, 9, 15, 16)

    ! remark: -7 because the scoring is wrong ([1:4] instead of [0:4])
    '''

    SQ_N_1 = ['SQ01_01', 'SQ01_06', 'SQ01_07', 'SQ01_08', 'SQ01_09', 'SQ01_15', 'SQ01_16',
              'SQ02_01', 'SQ02_06', 'SQ02_07', 'SQ02_08', 'SQ02_09', 'SQ02_15', 'SQ02_16']
    SQ_O_1 = ['SQ01_01', 'SQ01_02', 'SQ01_03', 'SQ01_04', 'SQ01_05', 'SQ01_09', 'SQ01_11',
              'SQ02_01', 'SQ02_02', 'SQ02_03', 'SQ02_04', 'SQ02_05', 'SQ02_09', 'SQ02_11']
    SQ_D_1 = ['SQ01_05', 'SQ01_08', 'SQ01_10', 'SQ01_11', 'SQ01_12', 'SQ01_13', 'SQ01_14',
              'SQ02_05', 'SQ02_08', 'SQ02_10', 'SQ02_11', 'SQ02_12', 'SQ02_13', 'SQ02_14']
    SQ_N_2 = ['SQ03_01', 'SQ03_06', 'SQ03_07', 'SQ03_08', 'SQ03_09', 'SQ03_15', 'SQ03_16',
              'SQ04_01', 'SQ04_06', 'SQ04_07', 'SQ04_08', 'SQ04_09', 'SQ04_15', 'SQ04_16']
    SQ_O_2 = ['SQ03_01', 'SQ03_02', 'SQ03_03', 'SQ03_04', 'SQ03_05', 'SQ03_09', 'SQ03_11',
              'SQ04_01', 'SQ04_02', 'SQ04_03', 'SQ04_04', 'SQ04_05', 'SQ04_09', 'SQ04_11']
    SQ_D_2 = ['SQ03_05', 'SQ03_08', 'SQ03_10', 'SQ03_11', 'SQ03_12', 'SQ03_13', 'SQ03_14',
              'SQ04_05', 'SQ04_08', 'SQ04_10', 'SQ04_11', 'SQ04_12', 'SQ04_13', 'SQ04_14']

    # if the first person condition came first, the first run of the questionnaire is connected to it
    df.loc[df['BE06_01'] == 1, 'SSQ_N_FP'] = (df.loc[:, SQ_N_1].sum(axis=1, skipna=True).astype(float) - 7) * 9.54
    df.loc[df['BE06_01'] == 1, 'SSQ_O_FP'] = (df.loc[:, SQ_O_1].sum(axis=1, skipna=True).astype(float) - 7) * 7.58
    df.loc[df['BE06_01'] == 1, 'SSQ_D_FP'] = (df.loc[:, SQ_D_1].sum(axis=1, skipna=True).astype(float) - 7) * 13.92

    df.loc[df['BE06_01'] == 1, 'SSQ_N_H'] = (df.loc[:, SQ_N_2].sum(axis=1, skipna=True).astype(float) - 7) * 9.54
    df.loc[df['BE06_01'] == 1, 'SSQ_O_H'] = (df.loc[:, SQ_O_2].sum(axis=1, skipna=True).astype(float) - 7) * 7.58
    df.loc[df['BE06_01'] == 1, 'SSQ_D_H'] = (df.loc[:, SQ_D_2].sum(axis=1, skipna=True).astype(float) - 7) * 13.92

    # if the first person condition came second, the second run of the questionnaire is connected to it
    df.loc[df['BE06_01'] == 2, 'SSQ_N_FP'] = (df.loc[:, SQ_N_2].sum(axis=1, skipna=True).astype(float) - 7) * 9.54
    df.loc[df['BE06_01'] == 2, 'SSQ_O_FP'] = (df.loc[:, SQ_O_2].sum(axis=1, skipna=True).astype(float) - 7) * 7.58
    df.loc[df['BE06_01'] == 2, 'SSQ_D_FP'] = (df.loc[:, SQ_D_2].sum(axis=1, skipna=True).astype(float) - 7) * 13.92

    df.loc[df['BE06_01'] == 2, 'SSQ_N_H'] = (df.loc[:, SQ_N_1].sum(axis=1, skipna=True).astype(float) - 7) * 9.54
    df.loc[df['BE06_01'] == 2, 'SSQ_O_H'] = (df.loc[:, SQ_O_1].sum(axis=1, skipna=True).astype(float) - 7) * 7.58
    df.loc[df['BE06_01'] == 2, 'SSQ_D_H'] = (df.loc[:, SQ_D_1].sum(axis=1, skipna=True).astype(float) - 7) * 13.92

    # total score per condition
    df["SSQ_TS_FP"] = df.loc[:, ['SSQ_N_FP', 'SSQ_O_FP', 'SSQ_D_FP']].sum(axis=1, skipna=True).astype(float) * 3.74
    df["SSQ_TS_H"] = df.loc[:, ['SSQ_N_H', 'SSQ_O_H', 'SSQ_D_H']].sum(axis=1, skipna=True).astype(float) * 3.74

    # averages
    df["SSQ_N_AVG"] = df[['SSQ_N_FP', 'SSQ_N_H']].mean(axis=1)
    df["SSQ_O_AVG"] = df[['SSQ_O_FP', 'SSQ_O_H']].mean(axis=1)
    df["SSQ_D_AVG"] = df[['SSQ_D_FP', 'SSQ_D_H']].mean(axis=1)
    df["SSQ_TS_AVG"] = df[['SSQ_TS_FP', 'SSQ_TS_H']].mean(axis=1)

    return df

def calculateP(df):
    '''
    calculates the scores for the Presence Questionnaire

    total score = sum over all 32 items (1-7 scale)

    item names:
    P001_01 - P024_01: german 1st run
    P025_01 - P048_01: english 1st run
    P049_01 - P072_01: german 2nd run
    P073_01 - P096_01: english 2nd run

    Witmer, B. G., & Singer, M. J. (1998). Measuring presence in virtual environments: A presence questionnaire. Presence, 7(3), 225-240.
    '''

    # generate a list with the item names as they're stored in the df
    items = []
    for i in range(1, 97):
        if i < 10:
            items.append("P00" + str(i) + "_01")
        else:
            items.append("P0" + str(i) + "_01")

    # if first person condition came before hybrid condition
    df.loc[df['BE06_01'] == 1, 'P_FP'] = df.loc[:, items[:48]].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'P_H'] = df.loc[:, items[48:97]].sum(axis=1, skipna=True)

    # if hybrid condition came first
    df.loc[df['BE06_01'] == 2, 'P_H'] = df.loc[:, items[:48]].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'P_FP'] = df.loc[:, items[48:97]].sum(axis=1, skipna=True)

    # average
    df["P_AVG"] = df[['P_H', 'P_FP']].mean(axis=1)

    return df


def calculateEB(df):
    '''
    calculates the scores for the Presence and Embodiment Questionnaire

    subscales:  Spatial Presence (SP)
                    environmental location (EL)
                    possible actions (PA)
                Embodiment (EB)
                    self-location (SL)
                    agency (A)
                    ownership (O)

    item names:
    EB01 - EB05: german 1st run
    EB06 - EB10: english 1st run
    EB11 - EB15: german 2nd run
    EB16 - EB20: english 2nd run

    Gorisse, G., Christmann, O., Amato, E. A., & Richir, S. (2017). First-and third-person perspectives in immersive
    virtual environments: presence and performance analysis of embodied users. Frontiers in Robotics and AI, 4, 33.
    '''

    EL_1 = ['EB01_01', 'EB01_02', 'EB01_03', 'EB01_04', 'EB06_01', 'EB06_02', 'EB06_03', 'EB06_04']
    EL_2 = ['EB11_01', 'EB11_02', 'EB11_03', 'EB11_04', 'EB16_01', 'EB16_02', 'EB16_03', 'EB16_04']
    PA_1 = ['EB02_01', 'EB02_02', 'EB02_03', 'EB02_04', 'EB07_01', 'EB07_02', 'EB07_03', 'EB07_04']
    PA_2 = ['EB12_01', 'EB12_02', 'EB12_03', 'EB12_04', 'EB17_01', 'EB17_02', 'EB17_03', 'EB17_04']
    SL_1 = ['EB03_01', 'EB03_02', 'EB08_01', 'EB08_02']
    SL_2 = ['EB13_01', 'EB13_02', 'EB18_01', 'EB18_02']
    A_1 = ['EB04_01', 'EB04_02', 'EB04_03', 'EB04_04', 'EB10_01', 'EB10_02', 'EB10_03', 'EB10_04']
    A_2 = ['EB14_01', 'EB14_02', 'EB14_03', 'EB14_04', 'EB19_01', 'EB19_02', 'EB19_03', 'EB19_04']
    O_1 = ['EB05_01', 'EB05_02', 'EB05_03', 'EB05_04', 'EB09_01', 'EB09_02', 'EB09_03', 'EB09_04']
    O_2 = ['EB15_01', 'EB15_02', 'EB15_03', 'EB15_04', 'EB20_01', 'EB20_02', 'EB20_03', 'EB20_04']

    # if the first person condition came first, the first run of the questionnaire is connected to it
    df.loc[df['BE06_01'] == 1, 'EB_EL_FP'] = df.loc[:, EL_1].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_PA_FP'] = df.loc[:, PA_1].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_SL_FP'] = df.loc[:, SL_1].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_A_FP'] = df.loc[:, A_1].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_O_FP'] = df.loc[:, O_1].sum(axis=1, skipna=True)

    df.loc[df['BE06_01'] == 1, 'EB_EL_H'] = df.loc[:, EL_2].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_PA_H'] = df.loc[:, PA_2].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_SL_H'] = df.loc[:, SL_2].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_A_H'] = df.loc[:, A_2].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_O_H'] = df.loc[:, O_2].sum(axis=1, skipna=True)

    # if the hybrid condition came first
    df.loc[df['BE06_01'] == 2, 'EB_EL_FP'] = df.loc[:, EL_2].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_PA_FP'] = df.loc[:, PA_2].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_SL_FP'] = df.loc[:, SL_2].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_A_FP'] = df.loc[:, A_2].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_O_FP'] = df.loc[:, O_2].sum(axis=1, skipna=True)

    df.loc[df['BE06_01'] == 2, 'EB_EL_H'] = df.loc[:, EL_1].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_PA_H'] = df.loc[:, PA_1].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_SL_H'] = df.loc[:, SL_1].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_A_H'] = df.loc[:, A_1].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_O_H'] = df.loc[:, O_1].sum(axis=1, skipna=True)

    # total score spatial presence & embodiment per condition
    df["EB_SP_FP"] = df.loc[:, ['EB_EL_FP', 'EB_PA_FP']].sum(axis=1, skipna=True)
    df["EB_SP_H"] = df.loc[:, ['EB_EL_H', 'EB_PA_H']].sum(axis=1, skipna=True)
    df["EB_EB_FP"] = df.loc[:, ['EB_SL_FP', 'EB_A_FP', 'EB_O_FP']].sum(axis=1, skipna=True)
    df["EB_EB_H"] = df.loc[:, ['EB_SL_H', 'EB_A_H', 'EB_O_H']].sum(axis=1, skipna=True)

    # averages
    df["EB_SP_AVG"] = df[['EB_SP_FP', 'EB_SP_H']].mean(axis=1)
    df["EB_EB_AVG"] = df[['EB_EB_FP', 'EB_EB_H']].mean(axis=1)

    return df

def renameColumns(df):
    '''
    renames the columns with general info to clearer names
    '''
    df["BE05"] = df["BE05"] - 1 # avatar is 0, blob is 1
    df["BE01"] = df["BE01"] - 1 # english is 0, german is 1

    df.rename(columns={"BE04_01": "ID", "BE04_02": "order_1", "BE04_03": "order_2",
                       "BE05": "blob", "BE01": "german"}, inplace=True)
    return df


def getRelevantColumns(df):
    temp = df[["STARTED", "ID", "german", "blob", "order_1", "order_2", # general info
               # data from simulator sickness questionnaire
               'SSQ_N_FP', 'SSQ_O_FP', 'SSQ_D_FP', 'SSQ_TS_FP',
               'SSQ_N_H', 'SSQ_O_H', 'SSQ_D_H', 'SSQ_TS_H',
               'SSQ_N_AVG', 'SSQ_O_AVG', 'SSQ_D_AVG', 'SSQ_TS_AVG',
               # data from presence questionnaire
               'P_FP', 'P_H', 'P_AVG',
               # data from presence & embodiment questionnaire
               'EB_SP_FP', 'EB_SP_H', 'EB_SP_AVG',
               'EB_EB_FP', 'EB_EB_H', 'EB_EB_AVG']].copy()
    return temp

def getInGameMS(df, search_path):
    df["ID"] = df['ID'].astype(str).str.zfill(4)

    # list of filenames that include the in-game motion sickness ratings
    fnames = [x for x in os.listdir(path=search_path) if re.match("\d+_(?:FirstPerson|Hybrid)_\d+.json", x)]

    ids = []
    hybrid = {0: [], 1: [], 2: [], 3: [], 4: []}
    firstPerson = {0: [], 1: [], 2: [], 3: [], 4: []}

    for file in fnames:
        # load json file
        temp = json.load(open(search_path + file))

        # hybrid data
        if "Hybrid" in file:
            # save participant id for later
            ids.append(temp['participantID'])
            # for each area
            for i in range(len(temp['_stationDataFrames'])):
                stationID = int(temp['_stationDataFrames'][i]["stationID"])
                score = int(temp['_stationDataFrames'][i]['MotionsicknessScore'])
                # save motion sickness score
                hybrid[stationID].append(score)

                # first person data
        else:
            # for each area
            for i in range(5):
                stationID = int(temp['_stationDataFrames'][i]["stationID"])
                score = int(temp['_stationDataFrames'][i]['MotionsicknessScore'])
                # save motion sickness score
                firstPerson[stationID].append(score)

    if len(df["ID"]) != len(ids):
        raise ValueError("Number of participants in questionnaire data vs. game data don't match!")

    if df["ID"].tolist() != ids:
        raise ValueError("Participant IDs in questionnaire data vs. game data don't match!")

    # add motion sickness score of each area to the data frame
    df["H_0_MS"] = hybrid[0]
    df["H_1_MS"] = hybrid[1]
    df["H_2_MS"] = hybrid[2]
    df["H_3_MS"] = hybrid[3]
    df["H_4_MS"] = hybrid[4]
    df["H_AVG_MS"] = df[['H_0_MS', 'H_1_MS', 'H_2_MS', 'H_3_MS', 'H_4_MS']].mean(axis=1)

    df["FP_0_MS"] = firstPerson[0]
    df["FP_1_MS"] = firstPerson[1]
    df["FP_2_MS"] = firstPerson[2]
    df["FP_3_MS"] = firstPerson[3]
    df["FP_4_MS"] = firstPerson[4]
    df["FP_AVG_MS"] = df[['FP_0_MS', 'FP_1_MS', 'FP_2_MS', 'FP_3_MS', 'FP_4_MS']].mean(axis=1)

    return df


