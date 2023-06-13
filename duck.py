import duckdb

con = duckdb.connect('warehouse.db')

text = con.sql("""
SELECT COUNT(DISTINCT customer_key) AS active_customers
FROM dim_customer
""")

print(text)
