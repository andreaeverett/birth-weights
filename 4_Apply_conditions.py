#This file further reduces the data to the set of births I want to focus on for
# predicting birthweight: single, term, live births. It also excludes births
# where birthweight is missing. Separately, I create new files that mimic the
# criteria used in Nahum & Stanislaw (2002).

from __future__ import division
import pandas as pd
import numpy as np

#Import recoded data from 3_Recode_missing.py
revised2015 = pd.read_csv("data_files/births2015_recoded.csv")
revised2014 = pd.read_csv("data_files/births2014_recoded.csv")

#First, drop multiple births: DPLURAL = 1 means the birth was of a single infant
revised2015 = revised2015[revised2015.DPLURAL == 1]
revised2014 = revised2014[revised2014.DPLURAL == 1]

#Next drop births where infant wasn't live: ILIVE = 1 means 'Infant living at time of report'
revised2015 = revised2015[revised2015.ILIVE == 1]
revised2014 = revised2014[revised2014.ILIVE == 1]

#Next drop births that weren't full-term (< 37 weeks)
#But there are 2 measures for this in the data, using LMP (last normal menses)
#and OE (obstetric estimate).

# Numbers of births if we use the LMP method (no longer the standard):

print len(revised2015[revised2015.GESTREC3 == 2])
print len(revised2014[revised2014.GESTREC3 == 2])

# Numbers if we use OE (the new standard -- see p.42-3 of the 2014 Natality user guide)

print len(revised2015[revised2015.OEGest_R3 == 2])
print len(revised2014[revised2014.OEGest_R3 == 2])

#Because they may yield different results and be of different quality, drop all
#births coded as < 37 weeks separately using both measures and later run models using each version

#First using LMP: GESTREC3 = 2 is >= 37 weeks
revised2015_lmp = revised2015[revised2015.GESTREC3 == 2]
revised2014_lmp = revised2014[revised2014.GESTREC3 == 2]

#Next using OE: OEGest_R3 = 2 is >= 37 weeks
revised2015_oe = revised2015[revised2015.OEGest_R3 == 2]
revised2014_oe = revised2014[revised2014.OEGest_R3 == 2]


#Next drop births where the target variable, birth weight, is missing
revised2014_lmp = revised2014_lmp[np.isnan(revised2014_lmp.DBWT) == False]
revised2015_lmp = revised2015_lmp[np.isnan(revised2015_lmp.DBWT) == False]

revised2014_oe = revised2014_oe[np.isnan(revised2014_oe.DBWT) == False]
revised2015_oe = revised2015_oe[np.isnan(revised2015_oe.DBWT) == False]


#Total percentages of large birth-weight pregnancies for 2014 (among single full term live births)
print len(revised2014_lmp[revised2014_lmp.DBWT > 4000])/len(revised2014_lmp)
print len(revised2014_oe[revised2014_oe.DBWT > 4000])/len(revised2014_oe)

#Same percentages for 2015 (among single full term live births). They are very close to the previous year.
print len(revised2015_lmp[revised2015_lmp.DBWT > 4000])/len(revised2015_lmp)
print len(revised2015_oe[revised2015_oe.DBWT > 4000])/len(revised2015_oe)


#Save the Obstetric Estimate files for use in primary analysis
# (can do same for LMP estimates later if it appears useful)
revised2014_oe.to_csv('data_files/largesample/revised2014_oe.csv')
revised2015_oe.to_csv('data_files/largesample/revised2015_oe.csv')



#Next, create another version of the dataset that applies the criteria used in Nahum & Stanislaw (2002)

#First, capture caucasian women only by dropping births to women of other races
replicate2014_lmp = revised2014_lmp[revised2014_lmp.MRACE6 == 1]
replicate2015_lmp = revised2015_lmp[revised2015_lmp.MRACE6 == 1]

replicate2014_oe = revised2014_oe[revised2014_oe.MRACE6 == 1]
replicate2015_oe = revised2015_oe[revised2015_oe.MRACE6 == 1]


#Next capture only women who didn't smoke during pregnancy
replicate2014_lmp = replicate2014_lmp[replicate2014_lmp.CIG1_R == 0]
replicate2014_lmp = replicate2014_lmp[replicate2014_lmp.CIG2_R == 0]
replicate2014_lmp = replicate2014_lmp[replicate2014_lmp.CIG3_R == 0]

replicate2014_oe = replicate2014_oe[replicate2014_oe.CIG1_R == 0]
replicate2014_oe = replicate2014_oe[replicate2014_oe.CIG2_R == 0]
replicate2014_oe = replicate2014_oe[replicate2014_oe.CIG3_R == 0]

replicate2015_lmp = replicate2015_lmp[replicate2015_lmp.CIG1_R == 0]
replicate2015_lmp = replicate2015_lmp[replicate2015_lmp.CIG2_R == 0]
replicate2015_lmp = replicate2015_lmp[replicate2015_lmp.CIG3_R == 0]

replicate2015_oe = replicate2015_oe[replicate2015_oe.CIG1_R == 0]
replicate2015_oe = replicate2015_oe[replicate2015_oe.CIG2_R == 0]
replicate2015_oe = replicate2015_oe[replicate2015_oe.CIG3_R == 0]


#Next eliminate infants with a congenital abnormality: cut the observations where NO_CONGEN !=1
replicate2014_lmp = replicate2014_lmp[replicate2014_lmp.NO_CONGEN == 1]
replicate2014_oe = replicate2014_oe[replicate2014_oe.NO_CONGEN == 1]

replicate2015_lmp = replicate2015_lmp[replicate2015_lmp.NO_CONGEN == 1]
replicate2015_oe = replicate2015_oe[replicate2015_oe.NO_CONGEN == 1]

#Next, exclude high-risk maternal conditions: diabetes and hypertension both
#before and during pregnancy, plus eclampsia (which normally follows preeclampsia)

replicate2014_lmp = replicate2014_lmp[(replicate2014_lmp.RF_PDIAB == 0) & (replicate2014_lmp.RF_GDIAB == 0) & (replicate2014_lmp.RF_PHYPE == 0) & (replicate2014_lmp.RF_GHYPE == 0) & (replicate2014_lmp.RF_EHYPE == 0)]
replicate2014_oe = replicate2014_oe[(replicate2014_oe.RF_PDIAB == 0) & (replicate2014_oe.RF_GDIAB == 0) & (replicate2014_oe.RF_PHYPE == 0) & (replicate2014_oe.RF_GHYPE == 0) & (replicate2014_oe.RF_EHYPE == 0)]

replicate2015_lmp = replicate2015_lmp[(replicate2015_lmp.RF_PDIAB == 0) & (replicate2015_lmp.RF_GDIAB == 0) & (replicate2015_lmp.RF_PHYPE == 0) & (replicate2015_lmp.RF_GHYPE == 0) & (replicate2015_lmp.RF_EHYPE == 0)]
replicate2015_oe = replicate2015_oe[(replicate2015_oe.RF_PDIAB == 0) & (replicate2015_oe.RF_GDIAB == 0) & (replicate2015_oe.RF_PHYPE == 0) & (replicate2015_oe.RF_GHYPE == 0) & (replicate2015_oe.RF_EHYPE == 0)]


#How many births are we left with?
print len(replicate2014_lmp)
print len(replicate2014_oe)
print len(replicate2015_lmp)
print len(replicate2015_oe)


#Finally save these final dataframes
replicate2014_lmp.to_csv('data_files/toreplicate2002/replicate2014_lmp.csv')
replicate2014_oe.to_csv('data_files/toreplicate2002/replicate2014_oe.csv')

replicate2015_lmp.to_csv('data_files/toreplicate2002/replicate2015_lmp.csv')
replicate2015_oe.to_csv('data_files/toreplicate2002/replicate2015_oe.csv')
