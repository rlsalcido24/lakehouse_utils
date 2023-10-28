# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Instructions
# MAGIC
# MAGIC 0. Pre-requisites: 
# MAGIC   * Clone the target dbt project repo into Databricks and create a new branch
# MAGIC   * Run `dbt seed` in your IDE / dbt Cloud to ensure the list of functions to be replaced is populated
# MAGIC
# MAGIC 1. Attach a single-user UC cluster to the notebook (this will avoid compatibility issues when we can leverage the Helper Functions)
# MAGIC
# MAGIC 2. Populate the widgets with: 
# MAGIC
# MAGIC   - **Repo path:** Enter the path of the cloned repo here: e.g. `<user-name>/<repo-path>`
# MAGIC   - **Targetdb:** Whether we are replacing snowflake or redshift functions
# MAGIC   - **Catalog:** The catalog you configured in your target dbt project. The `dbt seed` command will generate a list of functions to replace in this catalog
# MAGIC   - **Schema:** The schema you configured in your target dbt project. The `dbt seed` command will generate a list of functions to replace in this schema
# MAGIC
# MAGIC 3. Hit *Run all* in the top right of the notebook
# MAGIC
# MAGIC 4. Confirm
# MAGIC
# MAGIC ## What is this doing?
# MAGIC
# MAGIC
# MAGIC - Verify the target is a valid dbt repo, e.g. search for a `dbt_project.yml`
# MAGIC - For all .sql files in the Models folder, search for the existence of the fixed list of Snowflake / Redshift functions
# MAGIC - For each function:
# MAGIC   - Verify it hasn't already been converted into a macro, e.g. ensure it isn't already preceded by `{{lakehouse_utils.`
# MAGIC   - Verify the function we are replacing isn't actually a substring of another function, e.g. `xmlget()` not `get()`
# MAGIC   - Replace the pattern `function_name(var1,var2,...)` with `{{lakehouse_utils.function_name("var1","var2",...)}}`

# COMMAND ----------

dbutils.widgets.text("repo_path", "<user-name>/<repo-path>")
dbutils.widgets.dropdown("targetdb", "snowflake", ["snowflake", "redshift"])

#Catalog and schema targets from your dbt project profile
dbutils.widgets.text("catalog", "catalog")
dbutils.widgets.text("schema", "schema")
dbutils.widgets.dropdown("debugmode", "false", ["true", "false"])
dbutils.widgets.dropdown("parsemacro", "false", ["true", "false"])
dbutils.widgets.dropdown("subdir", "false", ["true", "false"])
dbutils.widgets.text("subdirpath", "redshift")


# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Setup the discovery function

# COMMAND ----------

# MAGIC %run ./_resources/01-discovery $targetdb=$targetdb $catalog=$catalog $schema=$schema $debugmode=$debugmode $parsemacro=$parsemacro $subdir=$subdir $subdirpath=$subdirpath

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Run the converter
# MAGIC
# MAGIC Enter your repo path as shown in the Databricks UI. e.g. `<user-name>/<repo-folder>`

# COMMAND ----------

repo_path = dbutils.widgets.get("repo_path")

listofdicts = dbt_project_functions_to_macros(repo_path)

# COMMAND ----------

###convert to df, pivot df, sum pivotcol, multipl *.5, 
import pandas as pd
df= pd.DataFrame(listofdicts)
meltdf = df.melt()
sumseries = meltdf["value"].sum()
totaleffort = sumseries / 2
print(f"Approximate Total effort: {totaleffort} hours")

# COMMAND ----------

if debugmode == 'true':
  if targetdb == 'snowflake':
    if subdir == 'true' and subdirpath == "snow":
      assert totaleffort == 2.0
      print('testpass, woohoo')
    elif subdir == 'false' and parsemacro == 'false':   
      assert totaleffort == 2.0  
      print('testpass, woohoo')
    else:
      cow = 'moo'
      print('no tests validate this time around!')    
