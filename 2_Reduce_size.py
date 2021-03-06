#This file opens the final CSVs created in Import_Data(1).ipynb, reduces their
# size by cutting columns that are only indicators for reporting flags, and
# saves the results in new CSVs

import pandas as pd

#Read in data
all2015 = pd.read_csv("../data_files/allbirths2015.csv", index_col=0)
all2014 = pd.read_csv("../data_files/allbirths2014.csv", index_col=0)

#Columns to cut since they just are the reporting flag variables
cols_to_cut = ["Unnamed: 0.1", "F_FACILITY", "F_MHISP", "F_MAR_P", "F_MEDUC", "F_FHISP", "FILLER_F", "F_MPCB", "F_TPCV", "F_WIC", "F_CIGS_0",
              "F_CIGS_1", "F_CIGS_2", "F_CIGS_3", "F_TOBACO", "F_M_HT", "F_PWGT", "F_DWGT", "F_WTGAIN", "F_RF_PDIAB", "F_RF_GDIAB",
              "F_RF_PHYPER", "F_RF_GHYPER", "F_RF_ECLAMP", "F_RF_PPB", "F_RF_INF_DRG", "F_RF_INF_ART", "F_RF_CESAR", "F_RF_NCESAR",
              "F_IP_GONOR", "F_IP_SYPH", "F_IP_CHLAM", "F_IP_HEPATB", "F_IP_HEPATC", "F_OB_SUCC", "F_OB_FAIL", "F_LD_INDL",
              "F_LD_AUGM", "F_LD_STER", "F_LD_ANTB", "F_LD_CHOR", "F_LD_ANES", "F_ME_PRES", "F_ME_ROUT", "F_ME_TRIAL", "F_DMETH_REC",
              "F_MM_MTR", "F_MM_ PLAC", "F_MM_RUPT", "F_MM_UHYST", "F_MM_AICU", "F_PAY", "F_PAY_REC", "F_APGAR5", "F_AB_VENT",
              "F_AB_VENT6", "F_AB_NIUC", "F_AB_SURFAC", "F_AB_ANTIBIO", "F_AB_SEIZ", "F_CA_ANEN", "F_CA_MENIN", "F_CA_HEART",
              "F_CA_HERNIA", "F_CA_OMPHA", "F_CA_GASTRO", "F_CA_LIMB", "F_CA_CLEFTLP", "F_CA_CLEFT", "F_CA_DOWNS", "F_CA_CHROM",
              "F_CA_HYPOS", "F_BFED"]

#Drop those columns and save as new CSVs
all2015.drop(cols_to_cut, axis=1).to_csv("../data_files/births2015_noflags.csv")
all2014.drop(cols_to_cut, axis=1).to_csv("../data_files/births2014_noflags.csv")
