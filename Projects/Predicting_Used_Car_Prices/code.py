# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
import seaborn as sns
import numpy as np

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
 