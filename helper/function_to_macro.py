# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## What is this doing?
# MAGIC
# MAGIC
# MAGIC - Verify it is running in a dbt repo, e.g. search for a `dbt_project.yml`
# MAGIC - For all .sql files in the Models folder, search for the existence of the fixed list of Snowflake functions
# MAGIC - For each function:
# MAGIC   - Verify it hasn't already been converted into a macro, e.g. ensure it isn't already preceded by `{{`
# MAGIC   - Verify the function we are replacing isn't actually a substring of another function, e.g. `xmlget()` not `get()`
# MAGIC   - Replace the pattern `function_name(var1,var2,...)` with `{{function_name("var1","var2",...)}}`

# COMMAND ----------

import os
import re

dbutils.widgets.text("repo_path", "<user-name>/<repo-path>")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Helper functions

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
  replacement = r'{{\1"\2")}}' #Surround the expression with double curly braces, and quotes on either end
  
  check_preventDoubleReplace_pattern = r'({{{}\()([^)]+)\)'.format(function_name)
  check_preventInnerReplace_pattern = r'(\w{}\()([^)]+)\)'.format(function_name)

  # If the function hasn't already been replaced with a macro AND isn't a subpart of another function name, then continue
  if (re.search(check_preventDoubleReplace_pattern,content) is None) & (re.search(check_preventInnerReplace_pattern,content) is None):
    try:
      number_of_matches = len(re.findall(pattern, content))
    except:
      number_of_matches = 0
    updated_content = re.sub(pattern, replacement, content)
    matched_patterns = re.findall(pattern,updated_content) 

    for i in matched_patterns:
      commas = r','
      quoted_commas = r'","'
      updated_match = re.sub(commas,quoted_commas,i[1])
      updated_content = updated_content.replace(i[1], updated_match)

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
            print(f"Processed: {data}")
        else:
            print(f"Nothing to change: {data}")

  except:
      print("Not a valid dbt project")

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

  return ({full_path}, f'Converted functions: {converted_functions}') ## Return list of functions that converted

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## List of valid Snowflake functions to replace

# COMMAND ----------

input_functions = ["array_agg","any_value"
,"approx_top_k"
,"approximate_count_distinct"
,"approximate_jaccard_index"
,"approximate_similarity"
,"array_append"
,"array_cat"
,"array_compact"
,"array_construct"
,"array_construct_compact"
,"array_insert"
,"array_intersection"
,"array_size"
,"array_slice"
,"array_to_string"
,"arrayagg"
,"as_char"
,"as_date"
,"as_integer"
,"as_number"
,"as_varchar"
,"base64_decode_binary"
,"base64_decode_string"
,"base64_encode"
,"bitand"
,"booland_agg"
,"boolor_agg"
,"boolxor_agg"
,"charindex"
,"check_json"
,"compress"
,"contains"
,"control.harmonize_compact"
,"convert_timezone"
,"date_from_parts"
,"dateadd"
,"dayname"
,"dayofweekiso"
,"decrypt"
,"div0"
,"editdistance"
,"encrypt"
,"endswith"
,"enrich_placement_ad_type"
,"equal_null"
,"xmlget"
,"get_ddl"
,"get_path"
,"getdate"
,"hash_agg"
,"hex_decode_binary"
,"hex_decode_string"
,"hll"
,"hll_estimate"
,"hll_export"
,"hll_import"
,"iff"
,"ilike"
,"insert"
,"is_boolean"
,"is_date"
,"is_integer"
,"is_null_value"
,"is_real"
,"is_role_in_session"
,"json_extract_path_text"
,"last_query_id"
,"last_transaction"
,"len"
,"listagg"
,"md5_binary"
,"md5_hex"
,"md5_number_lower64"
,"md5_number_upper64"
,"median"
,"minhash"
,"minhash_combine"
,"mode"
,"monthname"
,"nullifzero"
,"object_agg"
,"object_construct"
,"object_delete"
,"object_insert"
,"object_keys"
,"objectagg"
,"parse_json"
,"parse_xml"
,"percentile_cont"
,"percentile_disc"
,"previous_day"
,"randstr"
,"ratio_to_report"
,"regexp"
,"regexp_count"
,"regexp_instr"
,"regexp_like"
,"regexp_substr"
,"seq1"
,"seq2"
,"seq4"
,"seq8"
,"sha1_hex"
,"sha2_binary"
,"sha2_hex"
,"split_part"
,"square"
,"st_intersects"
,"standardize"
,"startswith"
,"strtok"
,"strtok_to_array"
,"sysdate"
,"systimestamp"
,"time_slice"
,"timeadd"
,"timediff"
,"timestamp_from_parts"
,"timestamp_ntz_from_parts"
,"timestampadd"
,"timestampdiff"
,"to_array"
,"to_binary"
,"to_boolean"
,"to_char"
,"to_number"
,"to_double"
,"to_geography"
,"to_decimal"
,"to_numeric"
,"to_object"
,"to_time"
,"to_timestamp_ltz"
,"to_timestamp_ntz"
,"to_timestamp_tz"
,"to_varchar"
,"to_variant"
,"truncate"
,"try_base64_decode_string"
,"try_cast"
,"try_parse_json"
,"try_to_binary"
,"try_to_boolean"
,"try_to_date"
,"try_to_decimal"
,"try_to_number"
,"try_to_numeric"
,"try_to_time"
,"try_to_timestamp"
,"try_to_timestamp_ntz"
,"try_to_timestamp_tz"
,"unicode"
,"uniform"
,"uuid_string"
,"variance_samp"
,"weekiso"
,"yearofweek"
,"yearofweekiso"
,"zeroifnull"
,"get"
,"week"
,"time"
]

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Run the converter
# MAGIC
# MAGIC Enter your repo path as shown in the Databricks UI. e.g. `<user-name>/<repo-folder>`

# COMMAND ----------

repo_path = dbutils.widgets.get("repo_path")

dbt_project_functions_to_macros(repo_path)
