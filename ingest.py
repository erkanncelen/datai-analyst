import duckdb

con = duckdb.connect('warehouse.db')

dim_city_ing = duckdb.read_csv('data/dim_city.csv', sample_size = 10000, normalize_names=True)
dim_customer_ing = duckdb.read_csv('data/dim_customer.csv', sample_size = 10000, normalize_names=True)
dim_date_ing = duckdb.read_csv('data/dim_date.csv', sample_size = 10000, normalize_names=True)
dim_employee_ing = duckdb.read_csv('data/dim_employee.csv', sample_size = 10000, normalize_names=True)
dim_stock_item_ing = duckdb.read_csv('data/dim_stock_item.csv', sample_size = 10000, normalize_names=True)
fact_sales_ing = duckdb.read_csv('data/fact_sales.csv', sample_size = -1, normalize_names=True)

con.execute('CREATE OR REPLACE TABLE dim_city AS SELECT * FROM dim_city_ing')
con.execute('CREATE OR REPLACE TABLE dim_customer AS SELECT * FROM dim_customer_ing')
con.execute('CREATE OR REPLACE TABLE dim_date AS SELECT * FROM dim_date_ing')
con.execute('CREATE OR REPLACE TABLE dim_employee AS SELECT * FROM dim_employee_ing')
con.execute('CREATE OR REPLACE TABLE dim_stock_item AS SELECT * FROM dim_stock_item_ing')
con.execute('CREATE OR REPLACE TABLE fact_sales AS SELECT * FROM fact_sales_ing')
