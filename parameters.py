'''
Parameters and variables for the data analysis of the ELI-VR study project

Author: Zora Nolte
Last updated: 08.12.2021
'''

### Simulator Sickness Questionnaire (SSQ)
# items per subscale
'''
    O: Oculomotor (items: 1, 2, 3, 4, 5, 9, 11)
    D: Disorientation (items: 5, 8, 10, 11, 12, 13, 14)
    N: Nausea (items: 1, 6, 7, 8, 9, 15, 16)
'''
items_SSQ = {'SQ_N_1': ['SQ01_01', 'SQ01_06', 'SQ01_07', 'SQ01_08', 'SQ01_09', 'SQ01_15', 'SQ01_16',
                       'SQ02_01', 'SQ02_06', 'SQ02_07', 'SQ02_08', 'SQ02_09', 'SQ02_15', 'SQ02_16'],
            'SQ_O_1': ['SQ01_01', 'SQ01_02', 'SQ01_03', 'SQ01_04', 'SQ01_05', 'SQ01_09', 'SQ01_11',
                       'SQ02_01', 'SQ02_02', 'SQ02_03', 'SQ02_04', 'SQ02_05', 'SQ02_09', 'SQ02_11'],
            'SQ_D_1': ['SQ01_05', 'SQ01_08', 'SQ01_10', 'SQ01_11', 'SQ01_12', 'SQ01_13', 'SQ01_14',
                       'SQ02_05', 'SQ02_08', 'SQ02_10', 'SQ02_11', 'SQ02_12', 'SQ02_13', 'SQ02_14'],
            'SQ_N_2': ['SQ03_01', 'SQ03_06', 'SQ03_07', 'SQ03_08', 'SQ03_09', 'SQ03_15', 'SQ03_16',
                       'SQ04_01', 'SQ04_06', 'SQ04_07', 'SQ04_08', 'SQ04_09', 'SQ04_15', 'SQ04_16'],
            'SQ_O_2': ['SQ03_01', 'SQ03_02', 'SQ03_03', 'SQ03_04', 'SQ03_05', 'SQ03_09', 'SQ03_11',
                       'SQ04_01', 'SQ04_02', 'SQ04_03', 'SQ04_04', 'SQ04_05', 'SQ04_09', 'SQ04_11'],
            'SQ_D_2': ['SQ03_05', 'SQ03_08', 'SQ03_10', 'SQ03_11', 'SQ03_12', 'SQ03_13', 'SQ03_14',
                       'SQ04_05', 'SQ04_08', 'SQ04_10', 'SQ04_11', 'SQ04_12', 'SQ04_13', 'SQ04_14']}
# weights of subscales
weights_SSQ = {'N': 9.54, 'O': 7.58, 'D': 13.92, 'TS': 3.74}

### Presence questionnaire
# generate a list with the item names as they're stored in the df
'''
item names:
    P001_01 - P024_01: german 1st run
    P025_01 - P048_01: english 1st run
    P049_01 - P072_01: german 2nd run
    P073_01 - P096_01: english 2nd run
'''
items_P = []
for i in range(1, 97):
    if i < 10:
        items_P.append("P00" + str(i) + "_01")
    else:
        items_P.append("P0" + str(i) + "_01")

### Embodiment questionnaire
# items per subscale
'''
subscales:
    Spatial Presence (environmental location (EL), possible actions (PA))
    Embodiment (self-location (SL), agency (A), ownership (O))
item names:
    EB01 - EB05: german 1st run
    EB06 - EB10: english 1st run
    EB11 - EB15: german 2nd run
    EB16 - EB20: english 2nd run
'''
items_EB = {'EL_1': ['EB01_01', 'EB01_02', 'EB01_03', 'EB01_04', 'EB06_01', 'EB06_02', 'EB06_03', 'EB06_04'],
           'EL_2': ['EB11_01', 'EB11_02', 'EB11_03', 'EB11_04', 'EB16_01', 'EB16_02', 'EB16_03', 'EB16_04'],
           'PA_1': ['EB02_01', 'EB02_02', 'EB02_03', 'EB02_04', 'EB07_01', 'EB07_02', 'EB07_03', 'EB07_04'],
           'PA_2': ['EB12_01', 'EB12_02', 'EB12_03', 'EB12_04', 'EB17_01', 'EB17_02', 'EB17_03', 'EB17_04'],
           'SL_1': ['EB03_01', 'EB03_02', 'EB08_01', 'EB08_02'],
           'SL_2': ['EB13_01', 'EB13_02', 'EB18_01', 'EB18_02'],
           'A_1': ['EB04_01', 'EB04_02', 'EB04_03', 'EB04_04', 'EB10_01', 'EB10_02', 'EB10_03', 'EB10_04'],
           'A_2': ['EB14_01', 'EB14_02', 'EB14_03', 'EB14_04', 'EB19_01', 'EB19_02', 'EB19_03', 'EB19_04'],
           'O_1': ['EB05_01', 'EB05_02', 'EB05_03', 'EB05_04', 'EB09_01', 'EB09_02', 'EB09_03', 'EB09_04'],
           'O_2': ['EB15_01', 'EB15_02', 'EB15_03', 'EB15_04', 'EB20_01', 'EB20_02', 'EB20_03', 'EB20_04']}

### dictionary for renaming columns
dict_renaming = {"BE04_01": "ID", "BE04_02": "order_1", "BE04_03": "order_2",
                 "BE05": "blob", "BE01": "german"}

### list of columns to keep in the new df
relevant_cols = ["STARTED", "ID", "german", "blob", "order_1", "order_2", # general info
                 # data from simulator sickness questionnaire
                'SSQ_N_FP', 'SSQ_O_FP', 'SSQ_D_FP', 'SSQ_TS_FP',
                'SSQ_N_H', 'SSQ_O_H', 'SSQ_D_H', 'SSQ_TS_H',
                'SSQ_N_AVG', 'SSQ_O_AVG', 'SSQ_D_AVG', 'SSQ_TS_AVG',
                # data from presence questionnaire
                'P_FP', 'P_H', 'P_AVG',
                # data from presence & embodiment questionnaire
                'EB_EL_FP', 'EB_PA_FP', 'EB_EL_H', 'EB_PA_H',
                'EB_SP_FP', 'EB_SP_H', 'EB_SP_AVG',
                'EB_SL_FP', 'EB_A_FP', 'EB_O_FP', 'EB_SL_H', 'EB_A_H', 'EB_O_H',
                'EB_EB_FP', 'EB_EB_H', 'EB_EB_AVG']