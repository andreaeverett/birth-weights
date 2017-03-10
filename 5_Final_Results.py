#This file produces the final results I presented orally & online about the project.
#It does not include many other models and subsets of data I tested along the way.

from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#get_ipython().magic(u'matplotlib inline')

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score

import xgboost as xgb
from xgboost import XGBRegressor
import seaborn as sns

#Import data using obstetric estimates of birthweight for single, live, term births (from 4_Apply_conditions.py)
fullsample2014_oe = pd.read_csv('data_files/largesample/revised2014_oe.csv')
fullsample2015_oe = pd.read_csv('data_files/largesample/revised2015_oe.csv')


#Further narrow these data to low-risk pregnancies: drop mothers who smoke, who have
# high risk conditions like diabetes and hypertension, and whose infants have major
#congenital anomalies. BUT: keep women of all races (unlike Nahum & Stanislaw 2002).

withrace2014_oe = fullsample2014_oe[(fullsample2014_oe.CIG1_R == 0) & (fullsample2014_oe.CIG2_R == 0)
                & (fullsample2014_oe.CIG3_R == 0) & (fullsample2014_oe.NO_CONGEN == 1) & (fullsample2014_oe.RF_PDIAB == 0)
                & (fullsample2014_oe.RF_GDIAB == 0) & (fullsample2014_oe.RF_PHYPE == 0) & (fullsample2014_oe.RF_GHYPE == 0)
                & (fullsample2014_oe.RF_EHYPE == 0)]

withrace2015_oe = fullsample2015_oe[(fullsample2015_oe.CIG1_R == 0) & (fullsample2015_oe.CIG2_R == 0)
                & (fullsample2015_oe.CIG3_R == 0) & (fullsample2015_oe.NO_CONGEN == 1) & (fullsample2015_oe.RF_PDIAB == 0)
                & (fullsample2015_oe.RF_GDIAB == 0) & (fullsample2015_oe.RF_PHYPE == 0) & (fullsample2015_oe.RF_GHYPE == 0)
                & (fullsample2015_oe.RF_EHYPE == 0)]


#Select the variables previously identified to include in the best model
withracemat2015 = withrace2015_oe[['DBWT', 'OEGest_Comb', 'SEX', 'BMI', 'DWgt_R', 'WTGAIN', 'TBO_REC', 'MRACEHISP', 'MAGER', 'MEDUC']].dropna(how='any')
withracemat2014 = withrace2014_oe[['DBWT', 'OEGest_Comb', 'SEX', 'BMI', 'DWgt_R', 'WTGAIN', 'TBO_REC', 'MRACEHISP', 'MAGER', 'MEDUC']].dropna(how='any')

#Concatenate together these 2014 and 2015 dataframes
bothyears = pd.concat([withracemat2014, withracemat2015])


#What portion are born > 4000 grams?
print "Percent > 4000 grams: ", len(bothyears[bothyears.DBWT > 4000])/len(bothyears)


#What does the distribution of birthweight look like?
sns.set_style("whitegrid", {'axes.grid' : False})
hist_DBWT_20142015 = sns.distplot(bothyears.DBWT, axlabel="Birthweight (grams)", color="#f8481c", kde=False);
fig = hist_DBWT_20142015.get_figure()
fig.savefig('hist_DBWT_20142015.png')

#Examine summary statistics for this dataset
print bothyears.describe()


#Function to return and print mean absolute error, mean absolute percentage error,
#& percent of predictions within 10 and 15% of true values

def model_scores(y, y_pred):
    # 1) Mean absolute error
    absolute_error = abs(y - y_pred)

    # 2) Mean absolute percentage error
    percentage_error = abs(y - y_pred)/y

    # 3) Percentage of birth weights correctly predicted to within 10% and 15% of actual birthweight.
    within10 = [0]*len(y)
    within15 = [0]*len(y)

    for i in range(len(y)):
        if .85*y[i] <= y_pred[i] and y_pred[i] <= 1.15*y[i]:
            within15[i]= 1
            if  .9*y[i] <= y_pred[i] and y_pred[i] <= 1.1*y[i]:
                within10[i]= 1

    print "Mean absolute error: ", absolute_error.mean()
    print "Mean percentage error: ", percentage_error.mean()
    print "Percent within + or - 10%: ", sum(within10)/len(within10)
    print "Percent within + or - 15%: ", sum(within15)/len(within15)

    return absolute_error, percentage_error, within10, within15


#Function to calculate metrics of interest for binary predictions of large baby
#or not, at different cut-off values

def binary_scores(y, y_pred):
    #Define possible cut-offs over the range of the predicted values
    cut_offs = [2450, 2500, 2550, 2600, 2650, 2700, 2750, 2800, 2850, 2900, 2950,
                3000, 3050, 3100, 3150, 3200, 3250, 3300, 3350, 3400, 3450, 3500,
                3550, 3600, 3650, 3700, 3750, 3800, 3850, 3900, 3950, 4000, 4050,
                4100, 4150, 4200, 4250]

    #Generate indicator for whether true value is over 4000 grams
    y_large = [0]*len(y)
    for i in range(len(y)):
        if y[i] > 4000:
            y_large[i] = 1

    #Create empty lists to hold the metrics
    accuracy_list = []
    precision_list = []
    recall_list = []
    specificity_list = []
    neg_pred_val_list = []
    fp_rate = []

    for cut_off in cut_offs:
        #Generate lists to hold indicators for whether baby is predicted large
        #and for true negatives, false negatives, and false positives
        y_pred_large = [0]*len(y)
        tn = [0]*len(y)
        fn = [0]*len(y)
        fp = [0]*len(y)

        for i in range(len(y)):
            if y_pred[i] > cut_off:
                y_pred_large[i] = 1
            if y_large[i] == 0 and y_pred_large[i] == 0:
                tn[i] = 1
            if y_large[i] == 0 and y_pred_large[i] == 1:
                fp[i] = 1
            if y_large[i] == 1 and y_pred_large[i] == 0:
                fn[i] = 1

        #Calculate metrics for the given cuf-off
        accuracy_list.append(accuracy_score(y_large, y_pred_large))
        precision_list.append(precision_score(y_large, y_pred_large))
        recall_list.append(recall_score(y_large, y_pred_large))
        specificity_list.append(sum(tn)/(sum(tn) + sum(fp)))
        neg_pred_val_list.append(sum(tn)/(sum(tn) + sum(fn)))
        fp_rate.append(sum(fp)/(sum(fp) + sum(tn)))

    columns = ['Cut-off', 'Accuracy', 'Precision/PosPredVal', 'Recall/Sensitivity/TPR', 'Specificity/TNR', 'NegPredictedVal', 'FPR']
    df = pd.DataFrame(zip(cut_offs, accuracy_list, precision_list, recall_list, specificity_list, neg_pred_val_list, fp_rate), columns=columns)
    return df

#Function to produce a table of feature importances after XGBoost model

def get_xgb_feat_importances(clf):
    if isinstance(clf, xgb.XGBModel):
        # clf created by calling xgb.XGBClassifier.fit() or xgb.XGBRegressor().fit()
        fscore = clf.booster().get_fscore()
    else:
        # clf has been created by calling xgb.train & is an instance of xgb.Booster.
        fscore = clf.get_fscore()

    feat_importances = []
    for ft, score in fscore.iteritems():
        feat_importances.append({'Feature': ft, 'Importance': score})
    feat_importances = pd.DataFrame(feat_importances)
    feat_importances = feat_importances.sort_values(
        by='Importance', ascending=False).reset_index(drop=True)

    # Divide importances by the sum of all importances to get relative importances.
    #Thus, sum of all importances = 1, i.e. np.sum(feat_importances['importance']) == 1
    feat_importances['Importance'] /= feat_importances['Importance'].sum()
    print feat_importances
    return feat_importances


#Divide data into training and test set for cross-validation
y_all = bothyears.DBWT
X_all = bothyears.iloc[:, 1:]
Xall_train, Xall_test, yall_train, yall_test = train_test_split(X_all, y_all, test_size=0.33, random_state=42)


#XGBoost model tuned to maximize performance on test set
xgb_all = XGBRegressor(max_depth=5, min_child_weight=10, learning_rate=.10)
xgb_all.fit(Xall_train, yall_train)
y_pred_xgb_all = xgb_all.predict(Xall_test)


#What is the minimum predicted value?
print "Minimum predicted value: ", min(y_pred_xgb_all)

#And the maximum predicted value?
print "Maximum predicted value: ", max(y_pred_xgb_all)


#Look at the error summaries
absolute_xgb_all, percentage_xgb_all, within10_xgb_all, within15_xgb_all = model_scores(yall_test.values, y_pred_xgb_all)

#Which features are most important?
get_xgb_feat_importances(xgb_all)
#Order of features: 'OEGest_Comb', 'SEX', 'BMI', 'DWgt_R', 'WTGAIN', 'TBO_REC', 'MRACEHISP', 'MAGER', 'MEDUC'

#Translate into binary predictions
binaryscores_xgb_all = binary_scores(yall_test.values, y_pred_xgb_all)
print binaryscores_xgb_all


#Manually calculate AUC value
print "AUC: ", (((binaryscores_xgb_all["Recall/Sensitivity/TPR"].shift(1) + binaryscores_xgb_all["Recall/Sensitivity/TPR"])/2 ) *
 (binaryscores_xgb_all.FPR.shift(1) - binaryscores_xgb_all.FPR)).sum()

#Plot ROC curve manually
plt.figure()
ROC_20142015 = plt.plot(binaryscores_xgb_all['FPR'], binaryscores_xgb_all['Recall/Sensitivity/TPR'], color="#01c08d")
plt.plot(.28, .62, 'o-', color="#f8481c") #Actual performance in US medical system (based on Cheng et al (2015))
plt.plot(.235, .623, 'o-', color="#f8481c") #Using a cutoff of 3550g predicted birthweight for predicted macrosomia


plt.annotate('Cheng et al (2015): (.28, .62)', xy = (.29, .62), xytext=(.4, .65),
            arrowprops=dict(facecolor="#f8481c", shrink=0.05),
            )

plt.annotate('(.24, .62)', xy = (.22, .62), xytext=(.05, .7),
            arrowprops=dict(facecolor="#f8481c", shrink=0.05),
            )

plt.text(.85, .03, 'AUC = .77')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve');

plt.savefig('ROC_20142015.png')


#Next make visuals for some of the variables and binary relationships

#Histogram of delivery weight in pounds for training & test data combined
plt.figure()
hist_DWgt_R_20142015 = sns.distplot(bothyears.DWgt_R, axlabel="Delivery weight (lbs)", color="#01c08d", kde=False);
fig = hist_DWgt_R_20142015.get_figure()
fig.savefig('hist_DWgt_R_20142015.png')


#Scatterplot of mother's weight at delivery vs. birthweight for both test and training data combined
plt.figure()
scatter_deliv_bweight = plt.scatter(Xall_test.DWgt_R, yall_test, c = "#01c08d", alpha=.1)
plt.xlim(100,400)
plt.xlabel('Maternal Delivery Weight')
plt.ylabel('Infant weight at birth (grams)');
fig = scatter_deliv_bweight.get_figure()
fig.savefig('scatter_deliv_bweight.png')


#Histogram of length of gestation for training and test data combined
plt.figure()
hist_OEGEST_20142015 = sns.distplot(bothyears.OEGest_Comb, axlabel="Length of gestation (weeks)", color="#f8481c", bins=11, kde=False);
fig = hist_OEGEST_20142015.get_figure()
fig.savefig('hist_OEGEST_20142015.png')

#Check portion of the data for which gestation length is > 42 weeks
print "Percent born > 42 weeks: ", (Xall_test.OEGest_Comb > 42).sum()/len(Xall_test.OEGest_Comb)

#Want to show effect of gestation length on birthweight, but only where gestation
#length is 42 weeks or less (as we just saw, >99.9 % of observations). To do that,
#create dataset from these observations, based on both training and test set
gestation_df = pd.DataFrame(zip(Xall_test.OEGest_Comb, yall_test), columns=['Weeks of Gestation', 'Birthweight (grams)'])
gestation_df = gestation_df[gestation_df['Weeks of Gestation'] <= 42]
gestation_df.info()

plt.figure()
gestation_barplot = sns.barplot(x=gestation_df['Weeks of Gestation'], y=gestation_df['Birthweight (grams)'], palette="OrRd", ci=None)
fig = gestation_barplot.get_figure()
fig.savefig('gestation_barplot.png')

#Summarize the values represented in the plot
print gestation_df.groupby('Weeks of Gestation').mean()


#Now focus on representing the relationship between true values and predictions in the test set
#First create df containing just test-set true values and predictions
df = pd.DataFrame(zip(yall_test, y_pred_xgb_all), columns=['Birthweight', 'Prediction'])

#Histogram of absolute percentage error (in predicted values)
percent_error = 100*(abs(df.Birthweight - df.Prediction)/df.Birthweight)
plt.figure()
error_barplot = sns.distplot(percent_error, axlabel='Absolute Percentage Error', kde=False, color="#f8481c")
fig = error_barplot.get_figure()
fig.savefig('error_barplot.png');

#What is the maximum error?
print "Maximum absolute percentage error: ", 100*max(abs(df.Birthweight - df.Prediction)/df.Birthweight)

#Same histogram, but limited to those within 75% of true value (the vast majority)
percent_error_75 = percent_error[(percent_error >= 0) & (percent_error < 76)]
plt.figure()
error_barplot2 = sns.distplot(percent_error_75, axlabel='Absolute Percentage Error', kde=False, color="#f8481c")
fig = error_barplot2.get_figure()
fig.savefig('error_barplot2.png');

#Scatterplot of true birthweight vs. prediction
plt.figure()
scatter_true_pred = sns.jointplot(x="Birthweight", y="Prediction", data=df, color="#01c08d", xlim=(0, 9000), ylim=(0, 9000))
scatter_true_pred.savefig('scatter_true_pred.png');

#Finally make a couple of joint kernel density plots using Plotly
# (user will need to fill in own username and key)

import scipy.stats as st
import plotly.plotly as py
from plotly.graph_objs import *

#Set color scale
cubehelix_cs=[[0.0, '#e5f5f9'],
 [0.16666666666666666, '#ccece6'],
 [0.3333333333333333, '#99d8c9'],
 [0.5, '#66c2a4'],
 [0.6666666666666666, '#41ae76'],
 [0.8333333333333333, '#238b45'],
 [1.0, '#005824']]


#Functions for calculating the density and making the plot taken from Plotly example
def kde_scipy( vals1, vals2, (a,b), (c,d), N ):

    #vals1, vals2 are the values of two variables (columns)
    #(a,b) interval for vals1; (c,d) interval for vals2

    x=np.linspace(a,b,N)
    y=np.linspace(c,d,N)
    X,Y=np.meshgrid(x,y)
    positions = np.vstack([Y.ravel(), X.ravel()])

    values = np.vstack([vals1, vals2])
    kernel = st.gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)

    return [x, y, Z]


def make_kdeplot(varX, varY, (a,b), (c,d), N, colorsc, title):

    x, y, Z = kde_scipy(varY, varX, (a,b), (c,d), N )

    data = Data([
       Contour(
           z=Z,
           x=x,
           y=y,
           colorscale=colorsc,
           #reversescale=True,
           opacity=0.9,
           contours=Contours(
               showlines=False)
        ),
     ])

    layout = Layout(
        title= title,
        font= Font(family='Georgia, serif',  color='#635F5D'),
        showlegend=False,
        autosize=False,
        width=650,
        height=650,
        xaxis=XAxis(
            range=[a,b],
            showgrid=False,
            nticks=7
        ),
        yaxis=YAxis(
            range=[c,d],
            showgrid=False,
            nticks=7
        ),
        margin=Margin(
            l=40,
            r=40,
            b=85,
            t=100,
        ),
    )

    return Figure(data=data, layout=layout )


#Plot birthweight vs. prediction for range 2000 to 5000, covering the vast majority
#of true birthweights and all the predictions
N=200
a,b=(2000,5000)
c,d=(2000, 5000)
fig=make_kdeplot(df.Birthweight, df.Prediction, (a,b), (c,d),
                 N, cubehelix_cs,'KDE plot of birthweight vs. prediction' )

py.sign_in('username', 'key')
py.iplot(fig, filename='kde-birthweight-prediction')


#Finally, kernel density plot for Delivery Weight vs. birthweight, with test set only
N=200
a,b=(100,300)
c,d=(750, 8000)
fig=make_kdeplot(Xall_test.DWgt_R, yall_test, (a,b), (c,d),
                 N, cubehelix_cs,'KDE plot of Maternal delivery weight vs. Infant birthweight' )

py.sign_in('username', 'key')
py.iplot(fig, filename='kde-delivery-vs-birthweight')
