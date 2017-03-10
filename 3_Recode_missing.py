#This file recodes missing data and replaces variable values as appropriate in the reduced-size 2014 and 2015 CSV files from Reduce_size(2).ipynb

import pandas as pd
import numpy as np

#1 - Read in the data
all2015 = pd.read_csv("../data_files/births2015_noflags.csv")
all2014 = pd.read_csv("../data_files/births2014_noflags.csv")


#2 - Replace values that need to be replaced in the same way regardless of which variable they're found in
# Yes --> 1; # No --> 0; # Anomaly Confirmed --> 2; # Anomaly Pending --> 1; # Unknown -- > missing (Not a Number); # Male --> 1;
# Female --> 0; Not applicable --> Not a Number.

replacements = ['Y', 'N', 'C', 'P', 'U', 'M', 'F', 'X']
replace_vals = [1, 0, 2, 1, np.nan, 1, 0, np.nan]

all2015.replace(to_replace=replacements, value=replace_vals, inplace=True)
all2014.replace(to_replace=replacements, value=replace_vals, inplace=True)


#3 - Replace missing values where the value that represents 'missing' varies according to the scale of the variable

    #Create a dictionary to record relevant values that need to be changed to missing for different variables:
    #Note: FRACEHISP is included under both 8 and 9 b/c 8 & 9 are diff. forms of missing

missing_dict = {3: ['BFACIL3', 'MBSTATE_REC', 'GESTREC3', 'OEGest_R3'],
                4: ['BWTR4'],
                5: ['PRECARE5', 'APGAR5R', 'APGAR10R'],
                6: ['CIG0_R', 'CIG1_R', 'CIG2_R', 'CIG3_R'],
                8: ['MRACEHISP', 'FRACEHISP'],
                9: ['FRACEHISP', 'BFACIL', 'MHISP_R', 'DMAR', 'MEDUC', 'FRACE6', 'FBRACE', 'FHISP_R', 'FEDUC', 'UBFACIL', 'URF_DIAB', 'URF_CHYPER', 'URF_PHYPER', 'URF_ECLAM', 'UME_FORCP', 'UME_VAC', 'UOP_INDUC', 'ULD_BREECH', 'UCA_ANEN', 'UCA_SPINA', 'UCA_OMPHA', 'UCA_CELFTLP', 'UCA_HERNIA', 'UCA_DOWNS', 'NO_CONGEN', 'LBO_REC', 'TBO_REC', 'SETORDER_R', 'BMI_R', 'WTGAIN_REC', 'NO_RISKS', 'NO_INFEC', 'NO_LBRDLV', 'ME_PRES', 'ME_ROUT', 'RDMETH_REC', 'DMETH_REC', 'NO_MMORB', 'ATTEND', 'PAY', 'PAY_REC'],
                11: ['FAGEREC11'],
                12: ['PREVIS_REC', 'BWTR12'],
                88: ['APGAR10'],
                99: ['DLMP_MM', 'COMBGEST', 'GESTREC10', 'PREVIS', 'CIG_0', 'CIG_1', 'CIG_2', 'CIG_3', 'M_Ht_In', 'APGAR5', 'APGAR10', 'OEGest_Comb', 'OEGest_R10', 'DLMP_MM', 'COMBGEST', 'GESTREC10', 'RF_CESARN', 'WTGAIN', 'OEGest_Comb', 'OEGest_R10', 'PRECARE', 'FAGECOMB', 'FRACE31', 'FRACE15', 'PRIORLIVE', 'ILP_R11', 'PRIORDEAD', 'PRIORTERM', 'ILLB_R11', 'ILOP_R11'],
                99.9: ['BMI'],
                999: ['ILLB_R', 'ILOP_R', 'ILP_R', 'PWgt_R', 'DWgt_R'],
                9999: ['DOB_TT', 'DLMP_YY', 'DBWT', 'DLMP_YY', 'DBWT'],
                }

    #Write and run a function to replace those values

def fix_missing(df, missing_dict):
    """Replace entries in a dataframe with np.nan based on a dictionary that encodes the entries
    that need to be changed (as keys) and the variables where that change is relevant (each dictionary
    value is a list of variable names)"""
    for key in missing_dict.keys():
        for var in missing_dict[key]:
            df.loc[df[var] == key, var] = np.nan

fix_missing(all2015, missing_dict)
fix_missing(all2014, missing_dict)


#4 - Create and run functions to replace values in 2 variables where there is a single specific
# change needed only in that variable

#DMAR: 1 Married, 2 Unmarried: just need to recode 2 as 0
def fix_married(df):
    df.loc[df['DMAR'] == 2, 'DMAR'] = 0

#PRECARE (Month that prenatal care began): no prenatal care is coded 0, otherwise goes from 0 to 10.
#I recode 0 as 11 so it reflects later in time as in related variables.
def fix_precare(df):
    df.loc[df['PRECARE'] == 0, 'PRECARE'] = 11

fix_married(all2015)
fix_precare(all2015)
fix_married(all2014)
fix_precare(all2014)


#5 - Save to new CSV files
all2015.to_csv("../data_files/births2015_recoded.csv")
all2014.to_csv("../data_files/births2014_recoded.csv")
