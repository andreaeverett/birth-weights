#This file recodes missing data in the reduced-size 2014 and 2015 CSV files from 2_Reduce_size.py

import pandas as pd
import numpy as np

#Read in the data

all2015 = pd.read_csv("data_files/births2015_noflags.csv")
all2014 = pd.read_csv("data_files/births2014_noflags.csv")

#Function to replace values that need to be replaced in the same way regardless of whey're they're found

def replace_vals(df):
    df.replace(to_replace='Y', value=1, inplace=True) # Yes --> 1
    df.replace(to_replace='N', value=0, inplace=True) # No --> 0
    df.replace(to_replace='C', value=2, inplace=True) # Anomaly Confirmed --> 2
    df.replace(to_replace='P', value=1, inplace=True) # Anomaly Pending --> 1
    df.replace(to_replace='U', value=np.nan, inplace=True) # Unknown -- > missing (Not a Number)
    df.replace(to_replace='M', value=1, inplace=True) # Male --> 1
    df.replace(to_replace='F', value=0, inplace=True) # Female --> 0
    df.replace(to_replace='X', value=np.nan, inplace=True) # Not applicable --> Not a Number.  This affects Paternity acknowledged, Fertility Enhancing Drugs, Asst. Reproductive Technology, Trial of Labor Attempted (if cesarean)

#Run this function for both years
replace_vals(all2015)
replace_vals(all2014)


#Next, distinct functions to replace missing values where the value that represents
# 'missing' varies with the scale of the variable.

missing3 = ['BFACIL3', 'MBSTATE_REC', 'GESTREC3', 'OEGest_R3']

def fix_missing3(df):
    for var in missing3:
        df.loc[df[var] == 3, var] = np.nan

missing4 = ['BWTR4']

def fix_missing4(df):
    for var in missing4:
        df.loc[df[var] == 4, var] = np.nan

missing5 = ['PRECARE5', 'APGAR5R', 'APGAR10R']

def fix_missing5(df):
    for var in missing5:
        df.loc[df[var] == 5, var] = np.nan

missing6 = ['CIG0_R', 'CIG1_R', 'CIG2_R', 'CIG3_R']

def fix_missing6(df):
    for var in missing6:
        df.loc[df[var] == 6, var] = np.nan

missing8 = ['MRACEHISP', 'FRACEHISP']

def fix_missing8(df):
    for var in missing8:
        df.loc[df[var] == 8, var] = np.nan

missing9 = ['FRACEHISP', 'BFACIL', 'MHISP_R', 'DMAR', 'MEDUC', 'FRACE6', 'FBRACE', 'FHISP_R', 'FEDUC', 'UBFACIL', 'URF_DIAB', 'URF_CHYPER', 'URF_PHYPER', 'URF_ECLAM', 'UME_FORCP', 'UME_VAC', 'UOP_INDUC', 'ULD_BREECH', 'UCA_ANEN', 'UCA_SPINA', 'UCA_OMPHA', 'UCA_CELFTLP', 'UCA_HERNIA', 'UCA_DOWNS', 'NO_CONGEN', 'LBO_REC', 'TBO_REC', 'SETORDER_R', 'BMI_R', 'WTGAIN_REC', 'NO_RISKS', 'NO_INFEC', 'NO_LBRDLV', 'ME_PRES', 'ME_ROUT', 'RDMETH_REC', 'DMETH_REC', 'NO_MMORB', 'ATTEND', 'PAY', 'PAY_REC']
#Note FRACEHISP is included both here and under missing8, b/c 8 & 9 are diff. forms of missing

def fix_missing9(df):
    for var in missing9:
        df.loc[df[var] == 9, var] = np.nan

missing11 = ['FAGEREC11']

def fix_missing11(df):
    for var in missing11:
        df.loc[df[var] == 11, var] = np.nan

missing12 = ['PREVIS_REC', 'BWTR12']

def fix_missing12(df):
    for var in missing12:
        df.loc[df[var] == 12, var] = np.nan

missing99 = ['DLMP_MM', 'COMBGEST', 'GESTREC10', 'PREVIS', 'CIG_0', 'CIG_1', 'CIG_2', 'CIG_3', 'M_Ht_In', 'APGAR5', 'APGAR10', 'OEGest_Comb', 'OEGest_R10', 'DLMP_MM', 'COMBGEST', 'GESTREC10', 'RF_CESARN', 'WTGAIN', 'OEGest_Comb', 'OEGest_R10', 'PRECARE', 'FAGECOMB', 'FRACE31', 'FRACE15', 'PRIORLIVE', 'ILP_R11', 'PRIORDEAD', 'PRIORTERM', 'ILLB_R11', 'ILOP_R11']

def fix_missing99(df):
    for var in missing99:
        df.loc[df[var] == 99, var] = np.nan

missing99point9 = ['BMI']

def fix_missing99point9(df):
    for var in missing99point9:
        df.loc[df[var] == 99.9, var] = np.nan

missing999 = ['ILLB_R', 'ILOP_R', 'ILP_R', 'PWgt_R', 'DWgt_R']

def fix_missing999(df):
    for var in missing999:
        df.loc[df[var] == 999, var] = np.nan

missing9999 = ['DOB_TT', 'DLMP_YY', 'DBWT', 'DLMP_YY', 'DBWT']

def fix_missing9999(df):
    for var in missing9999:
        df.loc[df[var] == 9999, var] = np.nan

#Next, fix DMAR: begins as 1 Married, 2 Unmarried, so just need to recode 2 as 0

def fix_married(df):
    df.loc[df['DMAR'] == 2, 'DMAR'] = 0

#Next, fix APGAR10 -- only one where missing = 88

def fix_apgar10(df):
    df.loc[df['APGAR10'] == 88, 'APGAR10'] = np.nan

#Fix PRECARE (Month that prenatal care began): no prenatal care is coded 0, otherwise goes from 0 to 10.
#I recode 0 as 11 so it reflects later in time as in related variables.

def fix_precare(df):
    df.loc[df['PRECARE'] == 0, 'PRECARE'] = 11


#Run all these functions on 2015 data
fix_missing3(all2015)
fix_missing4(all2015)
fix_missing5(all2015)
fix_missing6(all2015)
fix_missing8(all2015)
fix_missing9(all2015)
fix_missing11(all2015)
fix_missing12(all2015)
fix_missing99(all2015)
fix_missing99point9(all2015)
fix_missing999(all2015)
fix_missing9999(all2015)
fix_married(all2015)
fix_apgar10(all2015)
fix_precare(all2015)


#And on 2014 data
fix_missing3(all2014)
fix_missing4(all2014)
fix_missing5(all2014)
fix_missing6(all2014)
fix_missing8(all2014)
fix_missing9(all2014)
fix_missing11(all2014)
fix_missing12(all2014)
fix_missing99(all2014)
fix_missing99point9(all2014)
fix_missing999(all2014)
fix_missing9999(all2014)
fix_married(all2014)
fix_apgar10(all2014)
fix_precare(all2014)


#Finally, save to new CSVs again
all2015.to_csv("data_files/births2015_recoded.csv")
all2014.to_csv("data_files/births2014_recoded.csv")
