from dotenv import load_dotenv
from scipy import stats
import pandas as pd

load_dotenv()

file_path = './data/Test_Data.xlsx'
df = pd.read_excel(file_path)
# Normalize column names (remove spaces, make snake_case)
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace('-', '_')
)
df = df[df['quantity'] > 0].dropna(subset=['quantity', 'total_sales', 'rrp'])

# Step 1: Compute the effective unit price
df['unit_price'] = df['total_sales'] / df['quantity']
# Step 2: Compute the difference from RRP
df['price_diff'] = df['unit_price'] - df['rrp']
# Step 3: Compute the Z-score of that difference
df['z_score'] = stats.zscore(df['price_diff'])
# Step 4: Identify outliers (e.g., abs(z_score) > 3) this can be fine-tuned based on the data at hand
df['is_outlier'] = df['z_score'].abs() > 3
# Step 5: Output outliers to csv file
df = df[df['is_outlier'] == True]
df.to_csv('outliers.csv', index=False)