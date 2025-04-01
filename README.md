# ETL-Operations-on-Given-Data-
Provided two files containing sales data from two different regions. create a Python script that:
1. Extracts data from these above files.
2. Transforms the data according to the specified business rules.
3. Loads the transformed data into a database of your choice (SQLite preferred).
4. Writes SQL queries to validate the data in database.

## Running the Script:
1. Clone the repository.
2. Ensure you have pandas installed: pip install pandas.
3. Place order_region_a.csv and order_region_b.csv in the same directory.
4. Run the script: python main.py.
5. The data will be loaded into: sales_data.db.
6. Use SQLite browser or run the provided queries.sql file to validate the data.

## Explanation of Steps:
### Extract Phase: 
1. Reads two CSV files into Pandas DataFrames.
2. Adds a region column (A and B) to differentiate the regions.

### Transform Phase:
1. Combines both regions into a single table.
2. Adds:

        total_sales = QuantityOrdered × ItemPrice

        net_sales = total_sales - PromotionDiscount
3. Removes duplicate OrderId.
4. Excludes rows where net_sales <= 0.

### Load Phase:
1. Creates an SQLite database..
2. Loads the transformed data into the sales_data table.

### Validation:
1. SQL queries:

               a.Count total records.

               b.Aggregate sales by region.

               c.Calculate average sales per transaction.

               d.Detect duplicate OrderId entries.

## Assumptions & Decisions:
1. The database used is SQLite.
2. Duplicate OrderId records are removed.
3. Invalid sales (net_sales <= 0) are excluded.
4. Total sales and net sales calculations use INR currency.

## Snap Shots:
### Output:
![image](https://github.com/user-attachments/assets/db0c2d7e-b09c-4f31-ac15-bf15d2651ac9)

### Strcture of Sales_data Table:
![image](https://github.com/user-attachments/assets/7414d59b-9817-4e94-8824-2ed4749f8c5c)

## Execute SQL:
### a) Count the total number of records:
![image](https://github.com/user-attachments/assets/fdf2dc67-d2bf-4183-88ff-c33e3c6a8cb8)

### b) Find the total sales amount by region:
![image](https://github.com/user-attachments/assets/fd948623-711b-443a-b3d2-48a8d8ae8cf4)

### c) Find the average sales amount per transaction:
![image](https://github.com/user-attachments/assets/1d8d91f6-694f-4963-8c86-77ec2ae1335a)

### d) Ensure no duplicate OrderId values:
![image](https://github.com/user-attachments/assets/6521e973-37f0-4667-a992-2ac642529cc3)


 
