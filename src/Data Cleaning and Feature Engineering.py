"""Favorita Grocery Sales Forecasting """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""Holidays table"""
# Import our holidays dataset
holidays = pd.read_csv('holidays_events.csv')

"""Data Exploration on the holidays table"""
# Let's have a look at the holidays table structure
holidays.head()
# Check if there are any nulls
holidays.info()
# Check the type of values in each column
holidays.describe()
# Check out the types of holidays in the table
set(holidays['type'])
# Check out the different locales in the table
set(holidays['locale'])
# Check out the locale names in the table
set(holidays['locale_name'])

"""
Data cleaning and wrangling.
Since holidays are not celebrated on the "transferred" days, and are instead
celebrated on the type column "Transfer" days, we should drop all those days
from the list.
Also, we are only interested if a particular day was a holiday and not interested
in the nature of the holiday. Therefore, we should drop the "transferred",
"description" and "type" columns for simplicity.
"""
# Drop all rows with the value True in the "transferred" column
holidays = holidays[holidays['transferred'] == False]
print("There are only {} rows left.".format(len(holidays)))

# Drop the 3 columns
holidays_clean = holidays.drop(["type", "description", "transferred"], axis = 1)
# Let's have a look at the new holidays table
holidays_clean.head()


"""Oil table"""
# Import our oil dataset
oil = pd.read_csv('oil.csv')

"""Data Exploration on the oil table"""
# Let's have a look at the oil table structure
oil.head(20)
# Check if there are any nulls
oil.info()
# Check out the range of the oil prices
oil.describe()
"""
Data cleaning.
We need to fill those missing values by first forward filling then backfill to
minimise peeking into the future
"""
# Remove missing values from the oil table by first forward fill then backfill
oil.fillna(method='ffill', inplace=True)
oil.fillna(method='backfill', inplace=True)
# Check out the prices flucutation
oil.plot()

"""Feature Engineering on the oil table"""
# Calculate oil price changes
oil['oil_change'] = (oil['dcoilwtico'].astype(float)/oil['dcoilwtico'].astype(float).shift(1)) - 1
# We use the oil price changes of the past 7 days
for i in range(1, 7):
    oil['oil_' + str(i) + 'LaggingDays'] = oil['oil_change'].shift(i)
# Drop the original column
oil.drop('dcoilwtico', axis = 1, inplace = True)

"""Stores tables"""
# Import our stores dataset
stores = pd.read_csv('stores.csv')

"""Data Exploration on the stores table"""
# Let's have a look at the stores table structure
stores.head()
# Check if there are any nulls
stores.info()
# Check the type of values in each column
stores.describe()
# Check out the types of stores in the table
set(stores['type'])
# Check out the different cities in the table
set(stores['city'])
# Check out the different states in the table
set(stores['state'])
# Check out the different clusters in the table
set(stores['cluster'])

#"""Training data"""
## Import our training data post-feature engineering with PowerBI
#train = pd.read_csv('me/train.csv')
## LOL
#train.replace(to_replace = '2017-08-01 12:00:00.000', value = '1', inplace = True)
#train.replace(to_replace = '2017-08-02 12:00:00.000', value = '2', inplace = True)
#train.replace(to_replace = '2017-08-03 12:00:00.000', value = '3', inplace = True)
#train.replace(to_replace = '2017-08-04 12:00:00.000', value = '4', inplace = True)
#train.replace(to_replace = '2017-08-05 12:00:00.000', value = '5', inplace = True)
#train.replace(to_replace = '2017-08-06 12:00:00.000', value = '6', inplace = True)
#train.replace(to_replace = '2017-08-07 12:00:00.000', value = '7', inplace = True)
#train.replace(to_replace = '2017-08-08 12:00:00.000', value = '8', inplace = True)
#train.replace(to_replace = '2017-08-09 12:00:00.000', value = '9', inplace = True)
#train.replace(to_replace = '2017-08-10 12:00:00.000', value = '10', inplace = True)
#train.replace(to_replace = '2017-08-11 12:00:00.000', value = '11', inplace = True)
#train.replace(to_replace = '2017-08-12 12:00:00.000', value = '12', inplace = True)
#train.replace(to_replace = '2017-08-13 12:00:00.000', value = '13', inplace = True)
#train.replace(to_replace = '2017-08-14 12:00:00.000', value = '14', inplace = True)
#train.replace(to_replace = '2017-08-15 12:00:00.000', value = '15', inplace = True)
## Changing our boolean columns to int
#train['item_perishable'] = train['item_perishable'].astype(int)
#train['onpromotion'] = train['onpromotion'].astype(int)
#train['holiday'] = train['holiday'].astype(int)
## Dropping city and state columns
#train = train.drop(['store_city', 'store_state'], axis = 1)
## Sort columns
#train = train.sort_values(['date', 'store_nbr', 'item_nbr'], ascending=[True, True, True])
#train.reset_index(inplace=True)
#train.drop('index', axis = 1, inplace=True)
## Need to change column data types to string in order to OneHotEncode
#train['store_cluster'] = train['store_cluster'].astype(str)
#train['item_nbr'] = train['item_nbr'].astype(str)
#train['item_class'] = train['item_class'].astype(str)
#train.info()
## OneHotEncode our categorical features
#cat_features_raw = ['store_nbr', 'store_type', 'store_cluster', 'item_nbr', 'item_class']
#train.shape
#cat_features = pd.get_dummies(train[cat_features_raw])
#cat_features.shape

"""Training data"""
# Import our training data post-feature engineering with PowerBI
df = pd.read_csv('me/train3.csv')
# Remove features
df.drop(['id', 'store_city', 'store_state'], axis = 1, inplace=True)
# Correcting the order before label enconding
df.replace(to_replace = '8/1/2017', value = '8/01/2017', inplace = True)
df.replace(to_replace = '8/2/2017', value = '8/02/2017', inplace = True)
df.replace(to_replace = '8/3/2017', value = '8/03/2017', inplace = True)
df.replace(to_replace = '8/4/2017', value = '8/04/2017', inplace = True)
df.replace(to_replace = '8/5/2017', value = '8/05/2017', inplace = True)
df.replace(to_replace = '8/6/2017', value = '8/06/2017', inplace = True)
df.replace(to_replace = '8/7/2017', value = '8/07/2017', inplace = True)
df.replace(to_replace = '8/8/2017', value = '8/08/2017', inplace = True)
df.replace(to_replace = '8/9/2017', value = '8/09/2017', inplace = True)
# Label encode our dates
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(df['date'])
df['date'] = le.transform(df['date'])
le.fit(df['item_nbr'])
df['item_nbr'] = le.transform(df['item_nbr'])
# Sort it to look pretty
df = df.sort_values(['store_nbr', 'item_nbr', 'date'], ascending=[True, True, True])
df.reset_index(inplace=True)
df.drop('index', axis = 1, inplace=True)
df = df[['store_type', 'store_cluster', 'store_transactions', 'item_family', 
         'item_class', 'item_perishable', 'onpromotion', 'holiday', 
         'store_nbr', 'item_nbr', 'date', 'unit_sales']]
"""Lagging Raw for calculating moving average only"""
#for i in range(1, len(df)):
#    if df['item_nbr'][i] == df['item_nbr'][i - 1] and df['date'][i] == df['date'][i - 1] + 1:
#        df['unit_sales_lag1'][i] = df['unit_sales'][i - 1]
#    elif df['item_nbr'][i] == df['item_nbr'][i - 1] and df['date'][i] != df['date'][i - 1] + 1:
#        df['unit_sales_lag1'][i] = 0
#    # when iteration gets to a new item_nbr (new item or beginning new store) and we have no day 7 prior
#    elif df['item_nbr'][i] != df['item_nbr'][i - 1] and df['date'][i] < 7:
#        df['unit_sales_lag1'][i] = 0
#    else:
#        pass
from tqdm import tqdm

#for i in tqdm(range(1, len(df))):
#    if df['item_nbr'][i] == df['item_nbr'][i - 1] and df['date'][i] == df['date'][i - 1] + 1:
#        df.set_value(i, 'unit_sales_lag1', df['unit_sales'][i - 1])
#    elif df['item_nbr'][i] == df['item_nbr'][i - 1] and df['date'][i] != df['date'][i - 1] + 1:
#        df.set_value(i, 'unit_sales_lag1', 0)
#    # when iteration gets to a new item_nbr (new item or beginning new store) and we have no first day sales data
#    # elif df['item_nbr'][i] != df['item_nbr'][i - 1] and df['date'][i] > 0:
#    elif df['item_nbr'][i] != df['item_nbr'][i - 1]:
#        df.set_value(i, 'unit_sales_lag1', 0)
#    else:
#        pass
from tqdm import tqdm
# the unit_sales column is going to be our target, therefore we cannot use it to generate MA features
# to get MA of 7 days, we need to have a lagging of the last 8 days
for ii in range(1, 9):
    for i in tqdm(range(ii, len(df))):
        if df['item_nbr'][i] == df['item_nbr'][i - ii] and df['date'][i] == df['date'][i - ii] + ii:
            df.set_value(i, 'unit_sales_lag' + str(ii), df['unit_sales'][i - ii])
        elif df['item_nbr'][i] == df['item_nbr'][i - ii] and df['date'][i] != df['date'][i - ii] + ii:
            df.set_value(i, 'unit_sales_lag' + str(ii), 0)
        # when iteration gets to a new item_nbr (new item or beginning new store) and we have no first day sales data
        # elif df['item_nbr'][i] != df['item_nbr'][i - 1] and df['date'][i] > 0:
        elif df['item_nbr'][i] != df['item_nbr'][i - ii]:
            df.set_value(i, 'unit_sales_lag' + str(ii), 0)
        else:
            pass
df.fillna(value = 0, inplace=True)
# remove the first 7 days
df = df[(df.date != 0) & (df.date != 1) & (df.date != 2) & (df.date != 3) & (df.date != 4) & (df.date != 5) & (df.date != 6)]
df.reset_index(inplace=True)
df.drop('index', axis = 1, inplace=True)
# create target
target = df.unit_sales
df.drop('unit_sales', axis = 1, inplace = True)

"""Moving average"""
#for i in tqdm(range(0, len(df))):
#    for k in range(2, 8):
#        SUM = 0
#        a = 1
#        MA = 0
#        while a != k:
#            SUM += df.iloc[i][11 + (k - 1)]
#            a += 1
#        MA = SUM / k
#        df.set_value(i, 'unit_sales_MA' + str(k), MA)
# MA2
for i in tqdm(range(0, len(df))):
    df.set_value(i, 'unit_sales_MA2', (df.iloc[i]['unit_sales_lag1'] + df.iloc[i]['unit_sales_lag2']) / 2)

# MA3
for i in tqdm(range(0, len(df))):
    df.set_value(i, 'unit_sales_MA3', 
                 (df.iloc[i]['unit_sales_lag1'] + df.iloc[i]['unit_sales_lag2'] + df.iloc[i]['unit_sales_lag3']) / 3)

# MA4
for i in tqdm(range(0, len(df))):
    df.set_value(i, 
                 'unit_sales_MA4', 
                 (df.iloc[i]['unit_sales_lag1'] + df.iloc[i]['unit_sales_lag2'] + df.iloc[i]['unit_sales_lag3'] + df.iloc[i]['unit_sales_lag4']) / 4)
    
# MA5
for i in tqdm(range(0, len(df))):
    df.set_value(i, 
                 'unit_sales_MA5', 
                 (df.iloc[i]['unit_sales_lag1'] + df.iloc[i]['unit_sales_lag2'] + df.iloc[i]['unit_sales_lag3'] + df.iloc[i]['unit_sales_lag4'] + df.iloc[i]['unit_sales_lag5']) / 5)

# MA6, 7, 8
for i in tqdm(range(0, len(df))):
    df.set_value(i, 'unit_sales_MA6', (df.iloc[i]['unit_sales_lag1'] + df.iloc[i]['unit_sales_lag2'] + df.iloc[i]['unit_sales_lag3'] + df.iloc[i]['unit_sales_lag4'] + df.iloc[i]['unit_sales_lag5'] + df.iloc[i]['unit_sales_lag6']) / 6)
for i in tqdm(range(0, len(df))):
    df.set_value(i, 'unit_sales_MA7', (df.iloc[i]['unit_sales_lag1'] + df.iloc[i]['unit_sales_lag2'] + df.iloc[i]['unit_sales_lag3'] + df.iloc[i]['unit_sales_lag4'] + df.iloc[i]['unit_sales_lag5'] + df.iloc[i]['unit_sales_lag6'] + df.iloc[i]['unit_sales_lag7']) / 7)
for i in tqdm(range(0, len(df))):
    df.set_value(i, 'unit_sales_MA8', (df.iloc[i]['unit_sales_lag1'] + df.iloc[i]['unit_sales_lag2'] + df.iloc[i]['unit_sales_lag3'] + df.iloc[i]['unit_sales_lag4'] + df.iloc[i]['unit_sales_lag5'] + df.iloc[i]['unit_sales_lag6'] + df.iloc[i]['unit_sales_lag7']) + df.iloc[i]['unit_sales_lag8'] / 8)

"""Adding oil table to the training set"""
# Import our oil dataset
oil = pd.read_csv('oil.csv')
# Remove missing values from the oil table by first forward fill then backfill
oil.fillna(method='ffill', inplace=True)
oil.fillna(method='backfill', inplace=True)
# Based on indexing
oil = oil[1173:1206]
oil.reset_index(inplace = True)
oil.drop("index", axis = 1, inplace=True)
# Fill in the missing dates
oil.loc[33] = ['2017-07-01', np.nan]
oil.loc[34] = ['2017-07-02', np.nan]
oil.loc[35] = ['2017-07-08', np.nan]
oil.loc[36] = ['2017-07-09', np.nan]
oil.loc[37] = ['2017-07-15', np.nan]
oil.loc[38] = ['2017-07-16', np.nan]
oil.loc[39] = ['2017-07-22', np.nan]
oil.loc[40] = ['2017-07-23', np.nan]
oil.loc[41] = ['2017-07-29', np.nan]
oil.loc[42] = ['2017-07-30', np.nan]
oil.loc[43] = ['2017-08-05', np.nan]
oil.loc[44] = ['2017-08-06', np.nan]
oil.loc[45] = ['2017-08-12', np.nan]
oil.loc[46] = ['2017-08-13', np.nan]
oil = oil.sort_values(['date'], ascending=[True])
oil.reset_index(inplace = True)
oil.drop("index", axis = 1, inplace=True)
oil.fillna(method='ffill', inplace=True)
oil.fillna(method='backfill', inplace=True)
oil = oil[11:]
# Calculate oil price changes
oil['oil_change'] = (oil['dcoilwtico'].astype(float)/oil['dcoilwtico'].astype(float).shift(1)) - 1
# We use the oil price changes of the past 7 days
for i in range(1, 7):
    oil['oil_' + str(i) + 'LaggingDays'] = oil['oil_change'].shift(i)
oil.reset_index(inplace = True)
oil.drop("index", axis = 1, inplace=True)
# OneHotEncode the dates
le = preprocessing.LabelEncoder()
le.fit(oil['date'])
oil['date'] = le.transform(oil['date'])
oil = oil[7:]
# Join oil to main table
df2 = pd.merge(df, oil, on=['date'])
df2.drop('dcoilwtico', axis = 1, inplace = True)

"""OneHotEncode our Categorical features"""
df2['store_cluster'] = df2['store_cluster'].astype(str)
df2['item_class'] = df2['item_class'].astype(str)
df2['store_nbr'] = df2['store_nbr'].astype(str)
# Not doing transactions for now and also dropping item_nbr
df2.drop(['store_transactions', 'item_nbr'], axis = 1, inplace = True)
# OneHotEncode
cat_features_raw = ['store_nbr', 'store_type', 'store_cluster', 'item_nbr', 'item_class']
cat_features = pd.get_dummies(train[cat_features_raw])
cat_features.shape
other_features = df2.drop(cat_features_raw, axis = 1)
# Combine the two tables
train = pd.concat([cat_features, other_features], axis=1)
train.shape

"""PCA to reduce number of features"""
from sklearn.decomposition import PCA
pca = PCA(n_components = 20)
pca.fit(train)
print(pca.explained_variance_ratio_)
print("Our reduced dimensions can explain {:.4f}".format(sum(pca.explained_variance_ratio_)),
      "% of the variance in the original data")
reduced_train = pca.transform(train)
reduced_train = pd.DataFrame(reduced_train, columns = ['Dimension 1', 
                                                       'Dimension 2','Dimension 3', 
                                                       'Dimension 4','Dimension 5', 
                                                       'Dimension 6','Dimension 7', 
                                                       'Dimension 8','Dimension 9', 
                                                       'Dimension 10', 'Dimension 11', 
                                                       'Dimension 12', 'Dimension 13', 
                                                       'Dimension 14', 'Dimension 15', 
                                                       'Dimension 16', 'Dimension 17', 
                                                       'Dimension 18', 'Dimension 19', 
                                                       'Dimension 20'])

"""XGBoost"""
from xgboost import XGBRegressor
from xgboost import plot_importance
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import TimeSeriesSplit
# Cant be bothered doing a proper split tonight, lets see how a random split would do
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(reduced_train, target, test_size=0.2, random_state=0)
from sklearn import metrics
clf_XGB = XGBRegressor(seed = 0)
# fit the clf_XGB on training data
clf_XGB.fit(X_train, y_train)
# make predictions with test data
clf_XGB_predictions = clf_XGB.predict(X_test)
# evaluate predictions with accuracy metric
clf_XGB_loss = metrics.mean_absolute_error(y_test, clf_XGB_predictions)