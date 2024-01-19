# Databricks notebook source
# MAGIC %sh
# MAGIC pwd

# COMMAND ----------

# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "redshift" --dir_path "redshift/" --parse_mode 'syntax' --parse_first 'syntax' --except_list ["uno.py", "dos.py"]

# COMMAND ----------

# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "redshift" --dir_path "/Workspace/Repos/roberto.salcido@databricks.com/lakehouse_utils/testpyfiles" --parse_mode 'syntax' --parse_first 'syntax' --dir_mode 'nondbt' --file_type 'py' --except_list 'uno.py','dos.py'

# COMMAND ----------

# MAGIC %sh
# MAGIC python3 ./convert_to_databricks.py --sourcedb "redshift" --dir_path "/Workspace/Repos/roberto.salcido@databricks.com/lakehouse_utils/testlookmlfiles" --parse_mode 'syntax' --parse_first 'syntax' --dir_mode 'lookml' --file_type 'lkml' --except_list 'dos.lkml','tres.lkml'

# COMMAND ----------


