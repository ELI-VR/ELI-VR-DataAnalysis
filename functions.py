'''
Functions for the data analysis of the ELI-VR study project

Author: Zora Nolte
Last updated: 08.12.2021
'''

import pandas as pd
import os
import re
import json


def calculateSSQ(df, items, weights):
    '''
    calculates the scores for the Simulator Sickness Questionnaire (https://doi.org/10.1207/s15327108ijap0303_3)

    subscales:
    O: Oculomotor (items: 1, 2, 3, 4, 5, 9, 11)
    D: Disorientation (items: 5, 8, 10, 11, 12, 13, 14)
    N: Nausea (items: 1, 6, 7, 8, 9, 15, 16)

    Args:
        df (pd.DataFrame): df with the data
        weights (dict): dictionary with the subscale weights
        items (dict): dictionary containing a list of items for each subscale

    ! remark: -7 because the scoring is wrong ([1:4] instead of [0:4])
    '''
    # if the first person condition came first, the first run of the questionnaire is connected to it
    df.loc[df['BE06_01'] == 1, 'SSQ_N_FP'] = (df.loc[:, items['SQ_N_1']].sum(axis=1, skipna=True).astype(float) - 7) * weights['N']
    df.loc[df['BE06_01'] == 1, 'SSQ_O_FP'] = (df.loc[:, items['SQ_O_1']].sum(axis=1, skipna=True).astype(float) - 7) * weights['O']
    df.loc[df['BE06_01'] == 1, 'SSQ_D_FP'] = (df.loc[:, items['SQ_D_1']].sum(axis=1, skipna=True).astype(float) - 7) * weights['D']

    df.loc[df['BE06_01'] == 1, 'SSQ_N_H'] = (df.loc[:, items['SQ_N_2']].sum(axis=1, skipna=True).astype(float) - 7) * weights['N']
    df.loc[df['BE06_01'] == 1, 'SSQ_O_H'] = (df.loc[:, items['SQ_O_2']].sum(axis=1, skipna=True).astype(float) - 7) * weights['O']
    df.loc[df['BE06_01'] == 1, 'SSQ_D_H'] = (df.loc[:, items['SQ_D_2']].sum(axis=1, skipna=True).astype(float) - 7) * weights['D']

    # if the first person condition came second, the second run of the questionnaire is connected to it
    df.loc[df['BE06_01'] == 2, 'SSQ_N_FP'] = (df.loc[:, items['SQ_N_2']].sum(axis=1, skipna=True).astype(float) - 7) * weights['N']
    df.loc[df['BE06_01'] == 2, 'SSQ_O_FP'] = (df.loc[:, items['SQ_O_2']].sum(axis=1, skipna=True).astype(float) - 7) * weights['O']
    df.loc[df['BE06_01'] == 2, 'SSQ_D_FP'] = (df.loc[:, items['SQ_D_2']].sum(axis=1, skipna=True).astype(float) - 7) * weights['D']

    df.loc[df['BE06_01'] == 2, 'SSQ_N_H'] = (df.loc[:, items['SQ_N_1']].sum(axis=1, skipna=True).astype(float) - 7) * weights['N']
    df.loc[df['BE06_01'] == 2, 'SSQ_O_H'] = (df.loc[:, items['SQ_O_1']].sum(axis=1, skipna=True).astype(float) - 7) * weights['O']
    df.loc[df['BE06_01'] == 2, 'SSQ_D_H'] = (df.loc[:, items['SQ_D_1']].sum(axis=1, skipna=True).astype(float) - 7) * weights['D']

    # total score per condition
    df["SSQ_TS_FP"] = df.loc[:, ['SSQ_N_FP', 'SSQ_O_FP', 'SSQ_D_FP']].sum(axis=1, skipna=True).astype(float) * weights['TS']
    df["SSQ_TS_H"] = df.loc[:, ['SSQ_N_H', 'SSQ_O_H', 'SSQ_D_H']].sum(axis=1, skipna=True).astype(float) * weights['TS']

    # averages
    df["SSQ_N_AVG"] = df[['SSQ_N_FP', 'SSQ_N_H']].mean(axis=1)
    df["SSQ_O_AVG"] = df[['SSQ_O_FP', 'SSQ_O_H']].mean(axis=1)
    df["SSQ_D_AVG"] = df[['SSQ_D_FP', 'SSQ_D_H']].mean(axis=1)
    df["SSQ_TS_AVG"] = df[['SSQ_TS_FP', 'SSQ_TS_H']].mean(axis=1)

    return df

def calculateP(df, items):
    '''
    calculates the scores for the Presence Questionnaire

    total score = sum over all 32 items (1-7 scale)

    Witmer, B. G., & Singer, M. J. (1998). Measuring presence in virtual environments: A presence questionnaire. Presence, 7(3), 225-240.

    Args:
        df (pd.DataFrame): df with the data
        items (dict): dictionary containing a list of items for each subscale
    '''

    # if first person condition came before hybrid condition
    df.loc[df['BE06_01'] == 1, 'P_FP'] = df.loc[:, items[:len(items)//2]].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'P_H'] = df.loc[:, items[len(items)//2:]].sum(axis=1, skipna=True)

    # if hybrid condition came first
    df.loc[df['BE06_01'] == 2, 'P_H'] = df.loc[:, items[:len(items)//2]].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'P_FP'] = df.loc[:, items[len(items)//2:]].sum(axis=1, skipna=True)

    # average
    df["P_AVG"] = df[['P_H', 'P_FP']].mean(axis=1)

    return df


def calculateEB(df, items):
    '''
    calculates the scores for the Presence and Embodiment Questionnaire

    subscales:  Spatial Presence (SP)
                    environmental location (EL)
                    possible actions (PA)
                Embodiment (EB)
                    self-location (SL)
                    agency (A)
                    ownership (O)

    Gorisse, G., Christmann, O., Amato, E. A., & Richir, S. (2017). First-and third-person perspectives in immersive
    virtual environments: presence and performance analysis of embodied users. Frontiers in Robotics and AI, 4, 33.

    Args:
        df (pd.DataFrame): df with the data
        items (dict): dictionary containing a list of items for each subscale
    '''

    # if the first person condition came first, the first run of the questionnaire is connected to it
    df.loc[df['BE06_01'] == 1, 'EB_EL_FP'] = df.loc[:, items['EL_1']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_PA_FP'] = df.loc[:, items['PA_1']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_SL_FP'] = df.loc[:, items['SL_1']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_A_FP'] = df.loc[:, items['A_1']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_O_FP'] = df.loc[:, items['O_1']].sum(axis=1, skipna=True)

    df.loc[df['BE06_01'] == 1, 'EB_EL_H'] = df.loc[:, items['EL_2']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_PA_H'] = df.loc[:, items['PA_2']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_SL_H'] = df.loc[:, items['SL_2']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_A_H'] = df.loc[:, items['A_2']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 1, 'EB_O_H'] = df.loc[:, items['O_2']].sum(axis=1, skipna=True)

    # if the hybrid condition came first
    df.loc[df['BE06_01'] == 2, 'EB_EL_FP'] = df.loc[:, items['EL_2']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_PA_FP'] = df.loc[:, items['PA_2']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_SL_FP'] = df.loc[:, items['SL_2']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_A_FP'] = df.loc[:, items['A_2']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_O_FP'] = df.loc[:, items['O_2']].sum(axis=1, skipna=True)

    df.loc[df['BE06_01'] == 2, 'EB_EL_H'] = df.loc[:, items['EL_1']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_PA_H'] = df.loc[:, items['PA_1']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_SL_H'] = df.loc[:, items['SL_1']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_A_H'] = df.loc[:, items['A_1']].sum(axis=1, skipna=True)
    df.loc[df['BE06_01'] == 2, 'EB_O_H'] = df.loc[:, items['O_1']].sum(axis=1, skipna=True)

    # total score spatial presence & embodiment per condition
    df["EB_SP_FP"] = df.loc[:, ['EB_EL_FP', 'EB_PA_FP']].sum(axis=1, skipna=True)
    df["EB_SP_H"] = df.loc[:, ['EB_EL_H', 'EB_PA_H']].sum(axis=1, skipna=True)
    df["EB_EB_FP"] = df.loc[:, ['EB_SL_FP', 'EB_A_FP', 'EB_O_FP']].sum(axis=1, skipna=True)
    df["EB_EB_H"] = df.loc[:, ['EB_SL_H', 'EB_A_H', 'EB_O_H']].sum(axis=1, skipna=True)

    # averages
    df["EB_SP_AVG"] = df[['EB_SP_FP', 'EB_SP_H']].mean(axis=1)
    df["EB_EB_AVG"] = df[['EB_EB_FP', 'EB_EB_H']].mean(axis=1)

    return df

def renameColumns(df, renaming):
    '''
    renames the columns with general info to clearer names

    Args:
        df (pd.DataFrame): df with the data
        renaming (dict): dictionary containing the columns to be renamed and their new names
    '''
    df["BE05"] = df["BE05"] - 1 # avatar is 0, blob is 1
    df["BE01"] = df["BE01"] - 1 # english is 0, german is 1

    df.rename(columns=renaming, inplace=True)
    return df


def getRelevantColumns(df, list_of_cols):
    '''
    creates a new dataframe that contains only the desired columns

    Args:
        df (pd.DataFrame): df with the data
        list_of_cols (list): list with the columns to be kept
    '''
    temp = df[list_of_cols].copy()
    return temp

def getInGameMS(df, search_path):
    '''
    pulls the motion sickness ratings for each area and adds them to the dataframe

    Args:
        df (pd.DataFrame): df with the data
        search_path (str): path to the data folder
    '''
    df["ID"] = df['ID'].astype(str).str.zfill(3)

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


