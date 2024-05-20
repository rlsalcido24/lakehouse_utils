# Databricks notebook source
# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "redshift" --dir_path "redshift/" --parse_mode 'functions' --parse_first 'functions' --customdp 'true' --onlypublishagg "true"

# COMMAND ----------

# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "snowflake" --dir_path "snowflake/" --parse_mode 'all' --parse_first 'functions' --onlypublishagg "true"

# COMMAND ----------

# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "redshift" --dir_path "redshift/" --parse_mode 'syntax' --parse_first 'syntax'

# COMMAND ----------

# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "snowflake" --dir_path "snowflake/" --parse_mode 'syntax' --parse_first 'syntax' --onlypublishagg "true"

# COMMAND ----------

# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "redshift" --dir_path "redshift/" --parse_mode 'syntax' --parse_first 'syntax' --customdp "true" --onlypublishagg "true"

# COMMAND ----------

# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "redshift" --dir_path "redshift/" --parse_mode 'discovery' --parse_first 'syntax' --customdp "true"

# COMMAND ----------

# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "snowflake" --dir_path "snowflake/" --parse_mode 'discovery' --onlypublishagg 'true'

# COMMAND ----------

# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "redshift" --dir_path "/Workspace/Repos/roberto.salcido@databricks.com/lakehouse_utils/tmp/beyondsqltest/testpyfiles" --parse_mode 'syntax' --parse_first 'syntax' --dir_mode 'nondbt' --file_type 'py' --except_list 'uno.py','dos.py'

# COMMAND ----------

# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "redshift" --dir_path "/Workspace/Repos/roberto.salcido@databricks.com/lakehouse_utils/tmp/beyondsqltest/testlookmlfiles" --parse_mode 'syntax' --parse_first 'syntax' --dir_mode 'lookml' --file_type 'lkml' --except_list 'dos.lkml','tres.lkml'

# COMMAND ----------

from pathlib import Path

dirpath = "/Workspace/Repos/roberto.salcido@databricks.com/lakehouse_utils/models"
path = Path(dirpath)
print(f"Path to glob: {path}")
globs = path.rglob('*.sql')
for file in globs:
  print(file)

# COMMAND ----------


