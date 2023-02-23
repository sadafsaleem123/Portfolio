# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import PowerTransformer
from sklearn.metrics import r2_score,mean_squared_error
plt.style.use('ggplot')

# loading dataset
dataset = pd.read_csv('toyota.csv')

dataset.info()


# task 1: Include two different graphics showing single variables only to demonstrate the characteristics of data

fig, axes = plt.subplots(1,2,figsize=(15,5))
sns.histplot(dataset['price'],ax=axes[0])
axes[0].set_title('The Distribution of Target Variable - Price')
sns.histplot(dataset['price'],log_scale=True,ax=axes[1])
axes[1].set_title('The Distribution of Target Variable - Price (Log Scale)')


dataset['price'] = np.log(dataset['price'])

# Task 2: Include at least one graphic showing two or more variables to represent the relationship between features

sample = dataset[['price','mileage','tax','mpg']]
sns.heatmap(sample.corr(),annot=True).set(title='The Correlation Heatmap between two or more variables');

fig, axes = plt.subplots(1,3,figsize=(15,5))
sns.scatterplot(y=dataset['price'],x=dataset['mpg'], color='blue', hue=dataset['mpg'], ax=axes[0]).set(title='Price vs mpg')
sns.scatterplot(y=dataset['price'],x=dataset['mileage'],color='green', hue=dataset['mileage'], ax=axes[1]).set(title='Price vs Mileage');
sns.scatterplot(y=dataset['price'],x=dataset['tax'],color='red',hue=dataset['tax'], ax=axes[2]).set(title='Price vs tax')

# Convert tax variable into an ordinal variable  
dataset.loc[(dataset['tax'] <= 100,'tax')] = 1
dataset.loc[((dataset['tax'] <= 200) & (dataset['tax'] > 100) ,'tax')] = 2
dataset.loc[((dataset['tax'] <= 300) & (dataset['tax'] > 200) ,'tax')] = 3
dataset.loc[(dataset['tax'] > 300 ,'tax')] = 4

fig, axes = plt.subplots(1,2,figsize=(15,5))
sns.countplot(x=dataset['year'], color='gray',ax=axes[0]).set(title='Count of Cars Sold in Manufacture Year')
sns.countplot(x=dataset['engineSize'],color='gray',ax=axes[1]).set(title='Count of Cars Sold in EngineSize')
axes[0].tick_params(axis='x', labelrotation=45)
axes[1].tick_params(axis='x', labelrotation=45);

fig, axes = plt.subplots(1,3,figsize=(15,5))
sns.countplot(x=dataset['model'],color='gray',ax=axes[0]).set(title='Count of Cars Sold in Model')
sns.countplot(x=dataset['transmission'],color='gray',ax=axes[1]).set(title='Count of Cars Sold in Transmission')
sns.countplot(x=dataset['fuelType'],color='gray',ax=axes[2]).set(title='Count of Cars Sold in Fuel Type')
for ax in fig.axes:
    plt.sca(ax)
    plt.xticks(rotation=90);
    
fig, axes = plt.subplots(1,3,figsize=(20,5))
sns.boxplot(data=dataset, x='model',y='price',ax=axes[0]).set(title='The Distribution of Price by Model')
sns.boxplot(data=dataset, x='transmission',y='price',ax=axes[1]).set(title='The Distribution of Price by Transmission')
sns.boxplot(data=dataset, x='fuelType',y='price',ax=axes[2]).set(title='The Distribution of Price by Fuel Type')
for ax in fig.axes:
    plt.sca(ax)
    plt.xticks(rotation=90);
    
#Preparing data for modeling
label_encoder = LabelEncoder()
dataset['model'] = label_encoder.fit_transform(dataset['model'])
dataset['transmission'] = label_encoder.fit_transform(dataset['transmission'])
dataset['fuelType'] = label_encoder.fit_transform(dataset['fuelType'])

feature_cols = ['year','transmission','fuelType','engineSize','tax','model','mileage']
X = dataset[feature_cols] # Features
y = dataset['price'] # Target variable
# define the scaler 
scaler = PowerTransformer()
# fit and transform the train set
X[['year','engineSize','mileage']] = scaler.fit_transform(X[['year','engineSize','mileage']])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#Linear Regression Model
lr = LinearRegression()
lr.fit(X_train, y_train)

#Finding Feature Importance
resultdict = {}
for i in range(len(feature_cols)):
    resultdict[feature_cols[i]] = lr.coef_[i]
    
plt.bar(resultdict.keys(),resultdict.values())
plt.xticks(rotation='vertical')
plt.title('Feature Importance in Linear Regression Model');

#Decision Tree Regression Model
tree = DecisionTreeRegressor(max_depth=12,min_samples_split=2,random_state=42)
tree.fit(X_train,y_train)
y_pred2 = tree.predict(X_test)

d_r2 = tree.score(X_test, y_test)
print("Decision Tree Regressor R-squared: {}".format(d_r2))

d_mse = mean_squared_error(y_pred2, y_test)
d_rmse = np.sqrt(d_mse)
print("Decision Tree Regressor RMSE: {}".format(d_rmse))

#Finding the best parameter for Decision Tree Regression Model
train_score = []
test_score = []
max_score = 0
max_pair = (0,0)

for i in range(1,50):
    tree = DecisionTreeRegressor(max_depth=i,random_state=42)
    tree.fit(X_train,y_train)
    y_pred = tree.predict(X_test)
    train_score.append(tree.score(X_train,y_train))
    test_score.append(r2_score(y_test,y_pred))
    test_pair = (i,r2_score(y_test,y_pred))
    if test_pair[1] > max_pair[1]:
        max_pair = test_pair

fig, ax = plt.subplots()
ax.plot(np.arange(1,50), train_score, label = "Training R^2",color='lightcoral')
ax.plot(np.arange(1,50), test_score, label = "Testing R^2",color='lime')
print(f'Best max_depth is: {max_pair[0]} \nTesting R^2 is: {max_pair[1]}')

#Finding the feature Importance
importance = tree.feature_importances_

f_importance = {}
for i in range(len(feature_cols)):
     f_importance[feature_cols[i]] = importance[i]
        
plt.bar(f_importance.keys(),f_importance.values())
plt.xticks(rotation='vertical')
plt.title('Feature Importance in Decision Tree Regression Model');

#Evaluate by Business Criteria
X_test['Predicted_price'] = np.round(np.exp(y_pred),0)
X_test['Price'] = np.round(np.exp(y_test),0)
lr_e = X_test

lr_e['Diff'] = lr_e['Predicted_price'] - lr_e['Price']
lr_e['Result'] =  lr_e['Diff'] > 1500
lr_e['Category'] = lr_e['Result'].apply(lambda x: 'Will Not Sell' if x == True else 'Will Sell')
ax = lr_e['Category'].value_counts(normalize=True).plot.barh()
ax.bar_label(ax.containers[0])
ax.set_title('Evaluating Linear Regression Model by KPI');
X_test['Predicted_price'] = np.round(np.exp(y_pred2),0)
X_test['Price'] = np.round(np.exp(y_test),0)
tree_e = X_test

tree_e['Diff'] = tree_e['Predicted_price'] - tree_e['Price']
tree_e['Result'] =  tree_e['Diff'] > 1500
tree_e['Category'] = tree_e['Result'].apply(lambda x: 'Will Not Sell' if x == True else 'Will Sell')
ax = tree_e['Category'].value_counts(normalize=True).plot.barh()
ax.bar_label(ax.containers[0])
ax.set_title('Evaluating Decision Tree Regression Model by KPI');