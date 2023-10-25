# Databricks notebook source
import os
import re

dbutils.widgets.text("repo_path", "<user-name>/<repo-path>")
dbutils.widgets.text("targetdb", "snowflake")

#Catalog and schema targets from your dbt project profile
dbutils.widgets.text("catalog", "catalog")
dbutils.widgets.text("schema", "schema")

debugmode = dbutils.widgets.get("debugmode")


# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Helper Functions

# COMMAND ----------

## Function to discover sql files in a given Repo cloned to Databricks
## Add a check for whether in Databricks or external

def get_dir_content(ls_path):
  dir_paths = dbutils.fs.ls(ls_path)
  subdir_paths = [get_dir_content(p.path) for p in dir_paths if p.isDir() and p.path != ls_path]
  flat_subdir_paths = [p for subdir in subdir_paths for p in subdir]
  return list(map(lambda p: p.path, dir_paths)) + flat_subdir_paths

## Function to convert Snowflake functions to dbt macros

def function_to_macro(content, function_name):

  pattern = r'({}\()([^)]+)\)'.format(function_name) #Look for functions of the format name(input1,input2)
  replacement_doubleQuotes = r'{{lakehouse_utils.\1"\2")}}' #Surround the expression with double curly braces, and quotes on either end
  
  check_preventDoubleReplace_pattern = r'({{lakehouse_utils.{}\()([^)]+)\)'.format(function_name)
  check_preventInnerReplace_pattern = r'(\w{}\()([^)]+)\)'.format(function_name)

  # If the function hasn't already been replaced with a macro AND isn't a subpart of another function name, then continue
  if (re.search(check_preventDoubleReplace_pattern,content) is None) & (re.search(check_preventInnerReplace_pattern,content) is None):
    try:
      number_of_matches = len(re.findall(pattern, content))
    except:
      number_of_matches = 0

    updated_content = re.sub(pattern, replacement_doubleQuotes, content)

    #print(updated_content)

    matched_patterns = re.findall(pattern,updated_content) 

    #print(matched_patterns)

    for i in matched_patterns:
      
      # Substitute quotes around inner commas

      commas = r','
      quoted_commas = r'","'
      updated_match = re.sub(commas,quoted_commas,i[1])
      updated_content = updated_content.replace(i[1], updated_match)

    # If we inadvertently surrounded a double-quoted string with more double-quotes, change these to be single quotes to prevent compatibility issues!

    double_doubleQuotes_pattern = r'""([^"]*)""'
    single_doubleQuotes_pattern = r"""'"\1"'"""
    
    updated_content = re.sub(double_doubleQuotes_pattern,single_doubleQuotes_pattern,updated_content)

  # If the previous check failed, continue unchanged
  else:
    updated_content = content
    number_of_matches = 0

  return (updated_content, number_of_matches)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Define function for all .sql files in the dbt repo

# COMMAND ----------

from concurrent.futures import ThreadPoolExecutor, as_completed, wait

## Function to asynchronously kick off: open each file, loop through every function, write results

def process_file(full_path, functions_list):

  converted_functions = dict()
  with open(full_path, 'r+') as file:
    content = file.read()
    for function_name in functions_list:
      content, no_matches = function_to_macro(content, function_name)

      if no_matches > 0:
        converted_functions[function_name] = no_matches

    file.seek(0)
    file.write(content)
    file.truncate()

  return (full_path, converted_functions) ## Return list of functions that converted

def dbt_project_functions_to_macros(repo_path):
  # Verify we are running in a dbt project
  try:
    dbutils.fs.ls(f'file:/Workspace/Repos/{repo_path}/dbt_project.yml')

    print("Valid dbt project!")
    print("Converting .sql files in the Models folder...")

    # List all sql files to be checked in a folder
    paths = get_dir_content(f'file:/Workspace/Repos/{repo_path}/models')
    sql_files = [i[5:] for i in paths if '.sql' in i]

    with ThreadPoolExecutor() as executor:
      futures_sql = {executor.submit(process_file, p, input_functions): p for p in sql_files}
      for future in as_completed(futures_sql):
        data = future.result()
        if data:
            print(f"Processed: {data[0]} Converted Functions: {data[1]}")
           
        else:
            print(f"Nothing to change: {data}")
        
        if debugmode == 'true':
          if targetdb == 'redshift':
            if data[0] == "/Workspace/Repos/roberto.salcido@databricks.com/lakehouse_utils/models/redshift/customerrs.sql":
              assert len(data[1]) == 2
              print('testpass, woohoo')
          elif targetdb == 'snowflake':   
            if data[0] == "/Workspace/Repos/roberto.salcido@databricks.com/lakehouse_utils/models/snow/lineitem.sql":
              assert len(data[1]) == 3  
              print('testpass, woohoo')
            if data[0] == "/Workspace/Repos/roberto.salcido@databricks.com/lakehouse_utils/models/snow/customer.sql":
              assert len(data[1]) == 2
              print('testpass, woohoo')    
            

  except:
      print("Not a valid dbt project")  

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## List of valid Snowflake functions to replace

# COMMAND ----------

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
targetdb = dbutils.widgets.get("targetdb")

if targetdb == 'snowflake':
  input_functionsql = sql('select * from {}.{}.functionlist'.format(catalog, schema))
elif targetdb == 'redshift': 
  input_functionsql = sql('select * from {}.{}.functionlistrs'.format(catalog, schema))
else:
  input_functionsql = sql('select 1')

input_functionspd = input_functionsql.toPandas()
input_functions = input_functionspd["function_name"]
