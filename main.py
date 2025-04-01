{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "46c974ad",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Data extracted successfully.\n",
      "Data transformed successfully.\n",
      "Data loaded into the database successfully.\n",
      "\n",
      "--- Data Validation Results ---\n",
      "\n",
      "Total Records: 41052\n",
      "\n",
      "Total Sales by Region:\n",
      "Region A: INR 34570984.52\n",
      "\n",
      "Average Sales per Transaction: INR 842.1266812822753\n",
      "\n",
      "No Duplicate OrderId Found\n",
      "\n",
      "ETL process and validation completed successfully.\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import sqlite3\n",
    "\n",
    "# --- Step 1: Extract Data ---\n",
    "def extract_data(file_a, file_b):\n",
    "    \"\"\"Extract data from CSV files into Pandas DataFrames\"\"\"\n",
    "    try:\n",
    "        df_a = pd.read_csv(file_a)\n",
    "        df_b = pd.read_csv(file_b)\n",
    "\n",
    "        # Add region identifiers\n",
    "        df_a['region'] = 'A'\n",
    "        df_b['region'] = 'B'\n",
    "\n",
    "        print(\"Data extracted successfully.\")\n",
    "        return df_a, df_b\n",
    "\n",
    "    except Exception as e:\n",
    "        print(f\"Error extracting data: {e}\")\n",
    "        return None, None\n",
    "\n",
    "\n",
    "# --- Step 2: Transform Data ---\n",
    "def transform_data(df_a, df_b):\n",
    "    \"\"\"Apply business rules and transform the data\"\"\"\n",
    "    \n",
    "    # Combine data\n",
    "    df = pd.concat([df_a, df_b], ignore_index=True)\n",
    "\n",
    "    # Convert numerical columns to float type\n",
    "    num_cols = ['QuantityOrdered', 'ItemPrice', 'PromotionDiscount']\n",
    "\n",
    "    for col in num_cols:\n",
    "        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)\n",
    "\n",
    "    # Calculate total_sales\n",
    "    df['total_sales'] = df['QuantityOrdered'] * df['ItemPrice']\n",
    "\n",
    "    # Calculate net_sales with type-safe operations\n",
    "    df['net_sales'] = df['total_sales'] - df['PromotionDiscount']\n",
    "\n",
    "    # Remove duplicates based on OrderId\n",
    "    df = df.drop_duplicates(subset=['OrderId'])\n",
    "\n",
    "    # Exclude orders with negative or zero net_sales\n",
    "    df = df[df['net_sales'] > 0]\n",
    "\n",
    "    print(\"Data transformed successfully.\")\n",
    "    return df\n",
    "\n",
    "\n",
    "# --- Step 3: Load Data into SQLite ---\n",
    "def load_data(df, db_name='sales_data.db'):\n",
    "    \"\"\"Load transformed data into SQLite database\"\"\"\n",
    "    try:\n",
    "        conn = sqlite3.connect(db_name)\n",
    "        cursor = conn.cursor()\n",
    "\n",
    "        # Create the table\n",
    "        cursor.execute('''\n",
    "        CREATE TABLE IF NOT EXISTS sales_data (\n",
    "            OrderId INTEGER PRIMARY KEY,\n",
    "            OrderItemId INTEGER,\n",
    "            QuantityOrdered INTEGER,\n",
    "            ItemPrice REAL,\n",
    "            PromotionDiscount REAL,\n",
    "            total_sales REAL,\n",
    "            net_sales REAL,\n",
    "            region TEXT\n",
    "        )\n",
    "        ''')\n",
    "\n",
    "        # Load data into the table\n",
    "        df.to_sql('sales_data', conn, if_exists='replace', index=False)\n",
    "\n",
    "        conn.commit()\n",
    "        conn.close()\n",
    "\n",
    "        print(\"Data loaded into the database successfully.\")\n",
    "    \n",
    "    except Exception as e:\n",
    "        print(f\"Error loading data: {e}\")\n",
    "\n",
    "\n",
    "# --- Step 4: SQL Validation Queries ---\n",
    "def validate_data(db_name='sales_data.db'):\n",
    "    \"\"\"Run SQL validation queries and print the results\"\"\"\n",
    "    conn = sqlite3.connect(db_name)\n",
    "    cursor = conn.cursor()\n",
    "\n",
    "    print(\"\\n--- Data Validation Results ---\\n\")\n",
    "\n",
    "    # a) Count total records\n",
    "    cursor.execute(\"SELECT COUNT(*) FROM sales_data\")\n",
    "    print(f\"Total Records: {cursor.fetchone()[0]}\")\n",
    "\n",
    "    # b) Total sales by region\n",
    "    cursor.execute(\"SELECT region, SUM(total_sales) FROM sales_data GROUP BY region\")\n",
    "    print(\"\\nTotal Sales by Region:\")\n",
    "    for row in cursor.fetchall():\n",
    "        print(f\"Region {row[0]}: INR {row[1]:.2f}\")\n",
    "\n",
    "    # c) Average sales amount per transaction\n",
    "    cursor.execute(\"SELECT AVG(total_sales) FROM sales_data\")\n",
    "    print(\"\\nAverage Sales per Transaction: INR\", cursor.fetchone()[0])\n",
    "\n",
    "    # d) Ensure no duplicate OrderId values\n",
    "    cursor.execute(\"\"\"\n",
    "    SELECT OrderId, COUNT(*)\n",
    "    FROM sales_data\n",
    "    GROUP BY OrderId\n",
    "    HAVING COUNT(*) > 1\n",
    "    \"\"\")\n",
    "    duplicates = cursor.fetchall()\n",
    "\n",
    "    if duplicates:\n",
    "        print(\"\\nDuplicate OrderId Found:\")\n",
    "        for row in duplicates:\n",
    "            print(row)\n",
    "    else:\n",
    "        print(\"\\nNo Duplicate OrderId Found\")\n",
    "\n",
    "    conn.close()\n",
    "\n",
    "\n",
    "# --- Main Execution ---\n",
    "if __name__ == '__main__':\n",
    "    # File paths\n",
    "    file_a = 'order_region_a.csv'\n",
    "    file_b = 'order_region_b.csv'\n",
    "\n",
    "    # ETL Process\n",
    "    df_a, df_b = extract_data(file_a, file_b)\n",
    "\n",
    "    if df_a is not None and df_b is not None:\n",
    "        transformed_df = transform_data(df_a, df_b)\n",
    "        load_data(transformed_df)\n",
    "\n",
    "        # Validate the data\n",
    "        validate_data()\n",
    "\n",
    "    print(\"\\nETL process and validation completed successfully.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "be0a58b3",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
