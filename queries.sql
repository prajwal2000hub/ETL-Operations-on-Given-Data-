-- a) Count the total number of records
SELECT COUNT(*) FROM sales_data;

-- b) Find the total sales amount by region
SELECT region, SUM(total_sales) AS total_sales
FROM sales_data
GROUP BY region;

-- c) Find the average sales amount per transaction
SELECT AVG(total_sales) AS avg_sales
FROM sales_data;

-- d) Ensure no duplicate OrderId values
SELECT OrderId, COUNT(*)
FROM sales_data
GROUP BY OrderId
HAVING COUNT(*) > 1;
