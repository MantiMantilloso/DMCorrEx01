from pyspark.sql.functions import col, avg

# Asumimos que la sesión de Spark (spark) y las credenciales (db_url, db_user, etc.) ya están definidas.

# 1. Cargar la dimensión de fechas usando la estructura JDBC solicitada
df_dates = spark.read.format("jdbc") \
    .option("url", db_url) \
    .option("dbtable", "dim_date") \
    .option("user", db_user) \
    .option("password", db_password) \
    .option("driver", jdbc_driver) \
    .load()

# 2. Cargar la tabla de hechos usando la estructura JDBC solicitada
df_facts = spark.read.format("jdbc") \
    .option("url", db_url) \
    .option("dbtable", "fact_user_usage") \
    .option("user", db_user) \
    .option("password", db_password) \
    .option("driver", jdbc_driver) \
    .load()

# 3. Filtrar la dimensión de fecha explícitamente para el año 2025
df_dates_2025 = df_dates.filter(col("year") == 2025)

# 4. Unir (Join) la tabla de hechos con las fechas filtradas
# Spark optimizará esto al ignorar automáticamente los datos de 2015-2024 en la tabla de hechos
df_joined = df_facts.join(df_dates_2025, on="date_id", how="inner")

# 5. Calcular el ingreso promedio agrupando por el nombre del plan
df_avg_revenue = df_joined.groupBy("plan_name") \
    .agg(avg("total_revenue").alias("ingreso_promedio_2025"))

# Mostrar el resultado final para la Gerencia
df_avg_revenue.show()