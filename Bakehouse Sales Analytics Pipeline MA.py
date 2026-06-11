# Databricks notebook source
# MAGIC %md
# MAGIC 1- bronze table

# COMMAND ----------

# MAGIC
# MAGIC %sql
# MAGIC -- BRONZE TABLE FOR SALES_CUSTOMER
# MAGIC
# MAGIC SELECT * FROM samples.bakehouse.sales_customers
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE bronze_sales_customers
# MAGIC AS SELECT * FROM samples.bakehouse.sales_customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bronze_sales_customers

# COMMAND ----------

# MAGIC %sql
# MAGIC --BRONZE TABLE FOR SALES_FRANCHISE
# MAGIC
# MAGIC SELECT*FROM samples.bakehouse.sales_franchises
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE bronze_sales_franchises
# MAGIC AS SELECT * FROM samples.bakehouse.sales_franchises
# MAGIC     
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bronze_sales_franchises

# COMMAND ----------

# MAGIC %sql
# MAGIC --BRONZE TABLE FOR SALES_SUPPLIERS
# MAGIC
# MAGIC SELECT * FROM samples.bakehouse.sales_suppliers
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE bronze_sales_suppliers
# MAGIC AS SELECT * FROM samples.bakehouse.sales_suppliers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bronze_sales_suppliers

# COMMAND ----------

# MAGIC %sql
# MAGIC -- BRONZE TABLE FOR SALES_TRANSACTION
# MAGIC SELECT * FROM samples.bakehouse.sales_transactions
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE bronze_sales_transactions
# MAGIC AS
# MAGIC SELECT * FROM samples.bakehouse.sales_transactions
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bronze_sales_transactions

# COMMAND ----------

# MAGIC %sql
# MAGIC -- SILVER TABLE FOR BRONZE_SALES_CUSTOMER
# MAGIC
# MAGIC CREATE OR REPLACE TABLE silver_sales_customers AS
# MAGIC SELECT 
# MAGIC   customerID,
# MAGIC   email_address,
# MAGIC   phone_number,
# MAGIC   TRIM (address) AS address,
# MAGIC   UPPER (city) AS city,
# MAGIC   UPPER (state) AS state,
# MAGIC   UPPER (country) AS country,
# MAGIC   UPPER (continent) AS continent,
# MAGIC   UPPER (gender) AS gender
# MAGIC   
# MAGIC
# MAGIC   FROM bronze_sales_customers
# MAGIC   ORDER BY customerID ASC
# MAGIC     
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver_sales_customers

# COMMAND ----------

# MAGIC %sql
# MAGIC -- SILVER TABLE FOR SALES_FRANCHISE
# MAGIC
# MAGIC CREATE OR REPLACE TABLE silver_sales_franchise AS
# MAGIC SELECT
# MAGIC  franchiseID,
# MAGIC  UPPER (city) AS frachise_city,
# MAGIC  UPPER (district) AS franchise_district,
# MAGIC  UPPER (country) AS franchise_country,
# MAGIC  size,
# MAGIC  TRIM (longitude) AS longitude,
# MAGIC  TRIM (latitude) AS latitude,
# MAGIC  supplierID
# MAGIC
# MAGIC  FROM bronze_sales_franchises
# MAGIC ORDER BY franchiseID ASC
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver_sales_franchise

# COMMAND ----------

# MAGIC %sql
# MAGIC -- SILVER TABLE FOR SALES_SUPPLIER
# MAGIC CREATE OR REPLACE TABLE silver_sales_suppliers AS
# MAGIC SELECT 
# MAGIC  supplierID,
# MAGIC  UPPER (ingredient) AS ingredient,
# MAGIC  
# MAGIC  size
# MAGIC  FROM bronze_sales_suppliers
# MAGIC ORDER BY supplierID ASC
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver_sales_suppliers

# COMMAND ----------

# MAGIC %sql
# MAGIC -- SILVER TABLE FOR SALES_TRANSACTION 
# MAGIC CREATE OR REPLACE TABLE silver_sales_transactions AS
# MAGIC SELECT DISTINCT
# MAGIC  transactionID,
# MAGIC  customerID,
# MAGIC  franchiseID,
# MAGIC  TO_DATE(dateTime) AS transaction_date,
# MAGIC  DATE_FORMAT (dateTime, 'HH:mm:ss') AS transaction_time,
# MAGIC  UPPER (product) AS product,
# MAGIC  quantity,
# MAGIC  unitPrice,
# MAGIC  totalPrice,
# MAGIC  UPPER (paymentMethod) AS paymentMethod
# MAGIC  FROM bronze_sales_transactions
# MAGIC ORDER BY transactionID ASC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver_sales_transactions

# COMMAND ----------

# MAGIC %sql
# MAGIC -- CREATE GOLD TABLE 
# MAGIC CREATE OR REPLACE TABLE bakehouse_sales_analytics AS
# MAGIC SELECT 
# MAGIC   c.country,
# MAGIC   t.franchiseID,
# MAGIC   t.product,
# MAGIC  
# MAGIC
# MAGIC   COUNT (t.transactionID) AS total_transactions,
# MAGIC   SUM (t.quantity) AS total_quantity,
# MAGIC   SUM (t.totalPrice) AS total_revenue
# MAGIC FROM silver_sales_transactions t
# MAGIC LEFT JOIN silver_sales_customers c ON t.customerID = c.customerID
# MAGIC GROUP BY 1,2,3;
# MAGIC
# MAGIC
# MAGIC
# MAGIC   
# MAGIC   

# COMMAND ----------

# MAGIC %md
# MAGIC FINAL GOLD TABLE FOR BAKEHOUSE SALES ANALYTICS

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bakehouse_sales_analytics

# COMMAND ----------

# MAGIC %sql
# MAGIC -- COUNTRY WITH HIGHEST TOTAL REVENUE
# MAGIC SELECT
# MAGIC country,
# MAGIC SUM (total_revenue) AS grand_total
# MAGIC FROM bakehouse_sales_analytics
# MAGIC GROUP BY country
# MAGIC ORDER BY grand_total DESC
# MAGIC LIMIT 3