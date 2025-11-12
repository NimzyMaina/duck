# Duck Ingestion

## System Requirements

- You need python 3.9+
- uv (python package manager)

### Setup Logfire

Logfire is used for monitoring ingestion activity. 
You can view logs from the "live" dashboard.

This tool provides a centralized view the following from your pipelines and your APIs.
- Logs
- Metrics
- Alerts

Below is an example screenshot of validation checks done during the ingestion process.

![Logfire Dashboard](screenshots/img.png)

You can also configure Dashboards to monitor the health of your infrastructure. 

Signup here to get an **API TOKEN** - [Logfire Sign Up](https://pydantic.dev/logfire) and set **LOGFIRE_API_TOKEN** in your **.env** file

```dotenv
LOGFIRE_API_TOKEN=pylf_v1_eu_...
```

# How to Run the Project

### Setup project

Install dependencies from root directory
```terminal
$ uv sync 
```

## Running Excel Ingestion Pipeline

Running ingestion will use **pydantic**  to validate the data in the Excel dump. 
These validation rules can be customized according to business needs.
```terminal
$ uv run ingest.py 
```

Rows of data which don't pass the validation check are exported to the error directory.

In a production environment, you can log metrics to track a stores data accuracy, a simple percentage can be used.

# Data Architecture

I would go with the [**Medallion Architecture**](https://www.databricks.com/glossary/medallion-architecture) which allows data to flow through multiple layers, improving in **quality, structure,** and **usability** at each step.

For example, I would imagine that data from QuickMark & Carrefour have different formats so at their individual formats, that would fall under **Bronze** layer. 
The data can then be Augmented into a uniform schema at the **Silver** layer before finally "massaging" it into the **Gold** layer for business analytics.

![Medallion Architecture](https://www.databricks.com/sites/default/files/inline-images/building-data-pipelines-with-delta-lake-120823.png)


# FastAPI

How to run the api

```terminaloutput
$  uv run uvicorn api:app --reload
```

## API Endpoints

Data Quality Endpoint does a simple percentage check of how many records uploaded actually pass the validation check.

```shell
    curl http://127.0.0.1:8000/api/v1/quality
```

Example Response
```json
{
    "success": true,
    "message": "Success",
    "data": [
        {
            "store_name": "BURUBURU",
            "quality_percentage": 99.82
        },
        {
            "store_name": "CHAKA RD",
            "quality_percentage": 99.54
        }
    ]
}
```


## Finding Outliers

For finding outliers in the data, one can use a simple z-score to identify out of ordinary values

```python
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
```