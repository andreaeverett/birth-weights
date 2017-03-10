#This file further reduces the data to the set of births I want to focus on for predicting birthweight: single, term, live births.
# First, it saves a version of the data that reflects these conditions, and excludes births where birthweight is missing.
#Separately, it creates new files that mimic the full set of criteria used in Nahum & Stanislaw (2002).

from __future__ import division
import pandas as pd
import numpy as np


#1 - Import recoded data from Recode_missing(3).ipynb
revised2015 = pd.read_csv("../data_files/births2015_recoded.csv")
revised2014 = pd.read_csv("../data_files/births2014_recoded.csv")


#2 -- Keep subset of observations with a) single births (DPLURAL = 1), b) a live infant (ILIVE = 1), and c) data on birthweight (DBWT != np.nan)
revised2015 = revised2015[(revised2015.DPLURAL == 1) & (revised2015.ILIVE == 1) & (np.isnan(revised2015.DBWT) == False)]
revised2014 = revised2014[(revised2014.DPLURAL == 1) & (revised2014.ILIVE == 1) & (np.isnan(revised2014.DBWT) == False)]


#3 - Keep only births that were full-term (37 weeks or longer)
#But there are 2 ways of measuring this recorded in the data, using LMP (last normal menses) and OE (obstetric estimate)

#Numbers of births if we use the LMP method (no longer the standard):
print len(revised2015[revised2015.GESTREC3 == 2])
print len(revised2014[revised2014.GESTREC3 == 2])

#Numbers if we use OE (the new standard -- see p.42-3 of the 2014 Natality user guide)
print len(revised2015[revised2015.OEGest_R3 == 2])
print len(revised2014[revised2014.OEGest_R3 == 2])

#Because they may yield different results and be of different quality, I drop all births coded as < 37 weeks separately
#using both measures and later examine the effect of using each one

#Using LMP: GESTREC3 = 2 is gestation of 37 weeks and over
revised2015_lmp = revised2015[revised2015.GESTREC3 == 2]
revised2014_lmp = revised2014[revised2014.GESTREC3 == 2]

#Using OE: OEGest_R3 = 2 is gestation of 37 weeks and over
revised2015_oe = revised2015[revised2015.OEGest_R3 == 2]
revised2014_oe = revised2014[revised2014.OEGest_R3 == 2]

#Total percentages of large birth-weight pregnancies for 2014 (among single full term live births)
print len(revised2014_lmp[revised2014_lmp.DBWT > 4000])/len(revised2014_lmp)
print len(revised2014_oe[revised2014_oe.DBWT > 4000])/len(revised2014_oe)

#Same percentages for 2015 (among single full term live births). They are very close to the previous year.
print len(revised2015_lmp[revised2015_lmp.DBWT > 4000])/len(revised2015_lmp)
print len(revised2015_oe[revised2015_oe.DBWT > 4000])/len(revised2015_oe)


#4 - Save the Obstetric Estimate files for use in analysis (can do same for LMP estimates later if it appears useful)
revised2014_oe.to_csv('../data_files/largesample/revised2014_oe.csv')
revised2015_oe.to_csv('../data_files/largesample/revised2015_oe.csv')


#5 - Create versions of each dataset that apply the criteria used in Nahum & Stanislaw (2002)

#Keep only a) Caucasian women (MRACE6 == 1), b) nonsmokers during pregnancy (CIG1_R = 0, CIG2_R = 0, CIG3_R = 0),
# c) infants without congenital abnormalities (NO_CONGEN = 1), d) mothers without diabetes, hypertension or eclampsia
# before or during pregnancy (RF_PDIAB = 0, RF_GDIAB = 0,  RF_PHYPE = 0, RF_GHYPE = 0, RF_EHYPE = 0)

replicate2014_lmp = revised2014_lmp[(revised2014_lmp.MRACE6 == 1) & (revised2014_lmp.CIG1_R == 0) & (revised2014_lmp.CIG2_R == 0)
                    & (revised2014_lmp.CIG3_R == 0) & (revised2014_lmp.NO_CONGEN == 1) & (revised2014_lmp.RF_PDIAB == 0)
                    & (revised2014_lmp.RF_GDIAB == 0) & (revised2014_lmp.RF_PHYPE == 0) & (revised2014_lmp.RF_GHYPE == 0) & (revised2014_lmp.RF_EHYPE == 0)]

replicate2015_lmp = revised2015_lmp[(revised2015_lmp.MRACE6 == 1) & (revised2015_lmp.CIG1_R == 0) & (revised2015_lmp.CIG2_R == 0)
                    & (revised2015_lmp.CIG3_R == 0) & (revised2015_lmp.NO_CONGEN == 1) & (revised2015_lmp.RF_PDIAB == 0)
                    & (revised2015_lmp.RF_GDIAB == 0) & (revised2015_lmp.RF_PHYPE == 0) & (revised2015_lmp.RF_GHYPE == 0) & (revised2015_lmp.RF_EHYPE == 0)]

replicate2014_oe = revised2014_oe[(revised2014_oe.MRACE6 == 1) & (revised2014_oe.CIG1_R == 0) & (revised2014_oe.CIG2_R == 0)
                    & (revised2014_oe.CIG3_R == 0) & (revised2014_oe.NO_CONGEN == 1) & (revised2014_oe.RF_PDIAB == 0)
                    & (revised2014_oe.RF_GDIAB == 0) & (revised2014_oe.RF_PHYPE == 0) & (revised2014_oe.RF_GHYPE == 0) & (revised2014_oe.RF_EHYPE == 0)]

replicate2015_oe = revised2015_oe[(revised2015_oe.MRACE6 == 1) & (revised2015_oe.CIG1_R == 0) & (revised2015_oe.CIG2_R == 0)
                    & (revised2015_oe.CIG3_R == 0) & (revised2015_oe.NO_CONGEN == 1) & (revised2015_oe.RF_PDIAB == 0)
                    & (revised2015_oe.RF_GDIAB == 0) & (revised2015_oe.RF_PHYPE == 0) & (revised2015_oe.RF_GHYPE == 0) & (revised2015_oe.RF_EHYPE == 0)]

#How many births are we left with?
print len(replicate2014_lmp)
print len(replicate2014_oe)
print len(replicate2015_lmp)
print len(replicate2015_oe)


#6 - Save these final dataframes
replicate2014_lmp.to_csv('../data_files/toreplicate2002/replicate2014_lmp.csv')
replicate2014_oe.to_csv('../data_files/toreplicate2002/replicate2014_oe.csv')

replicate2015_lmp.to_csv('../data_files/toreplicate2002/replicate2015_lmp.csv')
replicate2015_oe.to_csv('../data_files/toreplicate2002/replicate2015_oe.csv')
