import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("Libraries imported successfully!")

df = pd.read_csv('DATA/superstore.csv.csv', encoding='latin1')

print("Dataset loaded successfully!")
print(f"Total Rows: {df.shape[0]}")
print(f"Total Columns: {df.shape[1]}")
print(df.head())
print(df.columns.tolist())

print(df.dtypes)
print(df.isnull().sum())
print(df.describe())

df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed')
df['Order Month'] = df['Order Date'].dt.month
df['Order Year'] = df['Order Date'].dt.year

print("Data cleaned successfully!")
print(df[['Order Date', 'Order Month', 'Order Year']].head())

plt.figure(figsize=(10,5))
category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
sns.barplot(x=category_sales.index, y=category_sales.values, palette='Blues_d')
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.savefig('outputs/sales_by_category.png')
plt.show()
print("Chart 1 saved!")

plt.figure(figsize=(10,5))
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
sns.barplot(x=region_sales.index, y=region_sales.values, palette='Greens_d')
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.savefig('outputs/sales_by_region.png')
plt.show()
print("Chart 2 saved!")

plt.figure(figsize=(12,5))
monthly_sales = df.groupby(['Order Year', 'Order Month'])['Sales'].sum().reset_index()
monthly_sales['Month-Year'] = monthly_sales['Order Month'].astype(str) + '-' + monthly_sales['Order Year'].astype(str)
sns.lineplot(data=monthly_sales, x=monthly_sales.index, y='Sales', marker='o', color='steelblue')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.savefig('outputs/monthly_sales_trend.png')
plt.show()
print("Chart 3 saved!")

plt.figure(figsize=(12,6))
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
sns.barplot(x=top_products.values, y=top_products.index, palette='Oranges_d')
plt.title('Top 10 Products by Sales')
plt.xlabel('Total Sales')
plt.ylabel('Product Name')
plt.tight_layout()
plt.savefig('outputs/top_10_products.png')
plt.show()
print("Chart 4 saved!")

plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='Sales', y='Profit', hue='Category', alpha=0.6)
plt.title('Profit vs Sales by Category')
plt.xlabel('Sales')
plt.ylabel('Profit')
plt.tight_layout()
plt.savefig('outputs/profit_vs_sales.png')
plt.show()
print("Chart 5 saved!")

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder

df_model = df.copy()
df_model['Profit_Margin'] = df_model['Profit'] / df_model['Sales']
df_model = df_model[df_model['Profit_Margin'].between(-1, 1)]

le = LabelEncoder()
df_model['Category_enc'] = le.fit_transform(df_model['Category'])
df_model['Region_enc'] = le.fit_transform(df_model['Region'])
df_model['Segment_enc'] = le.fit_transform(df_model['Segment'])
df_model['SubCategory_enc'] = le.fit_transform(df_model['Sub-Category'])
df_model['Discount_sq'] = df_model['Discount'] ** 2

X = df_model[['Discount', 'Quantity', 'Category_enc', 'Region_enc', 'Segment_enc', 'SubCategory_enc', 'Discount_sq']]
y = df_model['Profit_Margin']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"R2 Score: {r2:.2f}")
print(f"Mean Absolute Error: {mae:.2f}")
print("Model trained successfully!")

plt.figure(figsize=(12,6))
monthly_forecast = df.groupby(['Order Year', 'Order Month'])['Sales'].sum().reset_index()
monthly_forecast['Month_Number'] = range(1, len(monthly_forecast) + 1)

plt.plot(monthly_forecast['Month_Number'], monthly_forecast['Sales'], 
         marker='o', color='steelblue', label='Actual Sales')

from sklearn.linear_model import LinearRegression
forecast_model = LinearRegression()
X_forecast = monthly_forecast[['Month_Number']]
y_forecast = monthly_forecast['Sales']
forecast_model.fit(X_forecast, y_forecast)

future_months = pd.DataFrame({'Month_Number': range(1, len(monthly_forecast) + 5)})
forecast_values = forecast_model.predict(future_months)

plt.plot(future_months['Month_Number'], forecast_values, 
         color='red', linestyle='--', label='Forecast Trend')

plt.title('Sales Forecast Trend')
plt.xlabel('Month Number')
plt.ylabel('Total Sales')
plt.legend()
plt.tight_layout()
plt.savefig('outputs/sales_forecast.png')
plt.show()
print("Forecast chart saved!")