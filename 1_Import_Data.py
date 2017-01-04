#This file imports National Vital Statistics births data for 2014 and 2015 and
# transforms from fixed-width into CSV format

import pandas as pd

#Positions corresponding to variables in the fixed-width text files

positions = [(8,12), (13,14), (18,22), (22,23), (31,32), (32,33), (49,50),
             (72, 73), (73,74), (74,76), (76,78), (78,79), (83,84), (103,104),
             (104,106), (106,107), (107,109), (109,110), (110,111), (114,115),
             (115,116), (116,117), (118,119), (119,120), (120,121), (122, 123),
             (123, 124), (125,126), (141,142), (146,148), (148,150), (150, 152),
             (152,153), (153,155), (155,156), (159,160), (160,161), (161,162), (162,163),
             (164,165), (170,172), (172,174), (174,176), (178,179), (181,182), (197,200),
             (200,202), (205,208), (208,210), (213,216), (216,218), (223,225), (225,226),
             (226,227), (237,239), (241,243), (243,244), (250,251), (251,252), (252,254),
             (254,256), (256,258), (258,260), (260,261), (261,262), (262,263), (263,264),
             (264,265), (265,266), (266,267), (267,268), (268,269), (269,270), (279,281),
             (281, 282), (282, 286), (286,287), (291,294), (294,295), (298,301), (302,303),
             (303,305), (305,306), (306,307), (312,313), (313,314), (314,315), (315,316),
             (316,317), (317,318), (318,319), (319, 320), (320,321), (321,322), (322,323),
             (323,324), (324,325), (325,326), (326,327), (328, 329), (329,330), (330,331),
             (331,333), (334,335), (335,336), (336,337), (342,343), (343,344), (344,345),
             (345, 346), (346,347), (347,348), (348,349), (349,350), (350,351), (351,352),
             (352,353), (359,360), (360,361), (362,363), (363,364), (382,383), (383,384), (384,385),
             (385,386), (386,387), (387,388), (388,389), (389,390), (390,391), (391,392),
             (392,393), (393,394), (394,395), (400,401), (401,402), (402,403), (403,404),
             (404,405), (405,406), (406,407), (407,408), (408,409), (414,415), (415,416), (416,417),
             (417,418), (418,419), (420, 421), (421,422), (422,423), (423,424), (424,425),
             (426,427), (432,433), (433,434), (434,435), (435,436), (436,437), (437,438),
             (443,445), (445,446), (446,447), (447,449), (449,450), (453,454), (455,456),
             (458,459), (474,475), (475,476), (476,478), (480,484), (487,488), (488,489),
             (489,491), (491,493), (493,494), (497,498), (498,500), (500,502), (502,503),
             (503,507), (508,510), (510,511), (516,517), (517,518), (518,519), (519,520),
             (520,521), (521,522), (523,524), (524,525), (525,526), (526,527), (527,528),
             (528,529), (530,531), (536,537), (537,538), (538,539), (539,540), (540,541),
             (541,542), (542,543), (543,544), (544,545), (545,546), (546,547), (547,548),
             (548,549), (549,550), (550,551), (551,552), (552,553), (553,554), (554,555),
             (555,556), (556,557), (557,558), (558,559), (559,560), (560,561), (566,567),
             (567,568), (568,569), (569,570), (1329,1330), (1330,1331), (1331,1332), (1332,1333),
             (1333,1334), (1334,1335), (1335,1336), (1336,1337), (1337,1338), (1339,1340),
             (1340,1341), (1341,1342), (1342,1343), (1343,1344), (1344,1345)]

#Variable names corresponding to the fixed-width positions

headers = ["DOB_YY", "DOB_MM", "DOB_TT", "DOB_WK", "BFACIL", "F_FACILITY", "BFACIL3", "MAGE_IMPFLG", "MAGE_REPFLG",
          "MAGER", "MAGER14", "MAGER9", "MBSTATE_REC", "RESTATUS", "MRACE31", "MRACE6", "MRACE15", "MBRACE", "MRACEIMP",
          "MHISP_R", "F_MHISP", "MRACEHISP", "MAR_P", "DMAR", "MAR_IMP", "F_MAR_P", "MEDUC", "F_MEDUC", "FAGERPT_FLG",
          "FAGECOMB", "FAGEREC11", "FRACE31", "FRACE6", "FRACE15", "FBRACE", "FHISP_R", "F_FHISP", "FRACEHISP", "FEDUC",
          "FILLER_F", "PRIORLIVE", "PRIORDEAD", "PRIORTERM", "LBO_REC", "TBO_REC", "ILLB_R", "ILLB_R11", "ILOP_R", "ILOP_R11",
          "ILP_R", "ILP_R11", "PRECARE", "F_MPCB", "PRECARE5", "PREVIS", "PREVIS_REC", "F_TPCV", "WIC", "F_WIC", "CIG_0",
          "CIG_1", "CIG_2", "CIG_3", "CIG0_R", "CIG1_R", "CIG2_R", "CIG3_R", "F_CIGS_0", "F_CIGS_1", "F_CIGS_2", "F_CIGS_3",
          "CIG_REC", "F_TOBACO", "M_Ht_In", "F_M_HT", "BMI", "BMI_R", "PWgt_R", "F_PWGT", "DWgt_R", "F_DWGT", "WTGAIN",
           "WTGAIN_REC", "F_WTGAIN", "RF_PDIAB", "RF_GDIAB", "RF_PHYPE", "RF_GHYPE", "RF_EHYPE", "RF_PPTERM", "F_RF_PDIAB",
          "F_RF_GDIAB", "F_RF_PHYPER", "F_RF_GHYPER", "F_RF_ECLAMP", "F_RF_PPB", "RF_INFTR", "RF_FEDRG", "RF_ARTEC",
           "F_RF_INF_DRG", "F_RF_INF_ART", "RF_CESAR", "RF_CESARN", "F_RF_CESAR", "F_RF_NCESAR", "NO_RISKS", "IP_GON",
          "IP_SYPH", "IP_CHLAM", "IP_HEPB", "IP_HEPC", "F_IP_GONOR", "F_IP_SYPH", "F_IP_CHLAM", "F_IP_HEPATB", "F_IP_HEPATC",
          "NO_INFEC", "OB_ECVS", "OB_ECVF", "F_OB_SUCC", "F_OB_FAIL", "LD_INDL", "LD_AUGM", "LD_STER", "LD_ANTB", "LD_CHOR",
          "LD_ANES", "F_LD_INDL", "F_LD_AUGM", "F_LD_STER", "F_LD_ANTB", "F_LD_CHOR", "F_LD_ANES", "NO_LBRDLV", "ME_PRES",
          "ME_ROUT", "ME_TRIAL", "F_ME_PRES", "F_ME_ROUT", "F_ME_TRIAL", "RDMETH_REC", "DMETH_REC", "F_DMETH_REC", "MM_MTR",
          "MM_PLAC", "MM_RUPT", "MM_UHYST", "MM_AICU", "F_MM_MTR", "F_MM_ PLAC", "F_MM_RUPT", "F_MM_UHYST", "F_MM_AICU",
          "NO_MMORB", "ATTEND", "MTRAN", "PAY", "PAY_REC", "F_PAY", "F_PAY_REC", "APGAR5", "APGAR5R", "F_APGAR5", "APGAR10",
          "APGAR10R", "DPLURAL", "IMP_PLUR", "SETORDER_R", "SEX", "IMP_SEX", "DLMP_MM", "DLMP_YY", "COMPGST_IMP", "OBGEST_FLG",
          "COMBGEST", "GESTREC10", "GESTREC3", "LMPUSED", "OEGest_Comb", "OEGest_R10", "OEGest_R3", "DBWT", "BWTR12", "BWTR4",
          "AB_AVEN1", "AB_AVEN6", "AB_NICU", "AB_SURF", "AB_ANTI", "AB_SEIZ", "F_AB_VENT", "F_AB_VENT6", "F_AB_NIUC",
           "F_AB_SURFAC", "F_AB_ANTIBIO", "F_AB_SEIZ", "NO_ABNORM", "CA_ANEN", "CA_MNSB", "CA_CCHD", "CA_CDH", "CA_OMPH",
          "CA_GAST", "F_CA_ANEN", "F_CA_MENIN", "F_CA_HEART", "F_CA_HERNIA", "F_CA_OMPHA", "F_CA_GASTRO", "CA_LIMB", "CA_CLEFT",
          "CA_CLPAL", "CA_DOWN", "CA_DISOR", "CA_HYPO", "F_CA_LIMB", "F_CA_CLEFTLP", "F_CA_CLEFT", "F_CA_DOWNS", "F_CA_CHROM",
          "F_CA_HYPOS", "NO_CONGEN", "ITRAN", "ILIVE", "BFED", "F_BFED", "UBFACIL", "URF_DIAB", "URF_CHYPER", "URF_PHYPER", "URF_ECLAM",
          "UME_FORCP", "UME_VAC", "UOP_INDUC", "ULD_BREECH", "UCA_ANEN", "UCA_SPINA", "UCA_OMPHA", "UCA_CELFTLP", "UCA_HERNIA",
          "UCA_DOWNS"]

#The original files were large and needed to be chunked into 8 text files each

files2014 = ["births2014.txtaa", "births2014.txtac", "births2014.txtae", "births2014.txtag", "births2014.txtab",
             "births2014.txtad", "births2014.txtaf", "births2014.txtah"]

files2015 = ["births2015.txtaa", "births2015.txtac", "births2015.txtae", "births2015.txtag", "births2015.txtab",
             "births2015.txtad", "births2015.txtaf", "births2015.txtah"]

#Read in the chunked fixed-width files & convert to CSVs

for file in files2014:
    pd.read_fwf(str("data_files/chunks/" + file), header=None, names=headers, colspecs=positions).to_csv(str("data_files/chunks_csv2014/" + file))

for file in files2015:
    pd.read_fwf(str("data_files/chunks2015/" + file), header=None, names=headers, colspecs=positions).to_csv(str("data_files/chunks_csv2015/" + file))


#Next create one CSV per year
import os
path = "./data_files/chunks_csv2014/"
full_fnames = [os.path.join(path, fn) for fn in files2014]

df_from_chunk = (pd.read_csv(f) for f in full_fnames)
births2014 = pd.concat(df_from_chunk, ignore_index=True)

births2014.to_csv("data_files/allbirths2014.csv")

path2 = "./data_files/chunks_csv2015/"
full_fnames2015 = [os.path.join(path2, fn) for fn in files2015]

df_from_chunk = (pd.read_csv(f) for f in full_fnames2015)
births2015 = pd.concat(df_from_chunk, ignore_index=True)

births2015.to_csv("data_files/allbirths2015.csv")
