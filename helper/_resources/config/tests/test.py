import re


# Example usage
content = """

select 
    sysdate() AS sys_date_col_test,
    SYSDATE() AS sys_date_caps_col_test,
    dlog10(c_acctbal) as actbalbaseten,
    c_mktsegment,
    c_comment,
    getdate() as hoy,
    GETDATE AS get_date_caps_test,
    ISNULL(test, test_is_null) AS null_test_col_caps,
    isnull(test, 'test_is_null') AS null_test_col,

from
    redshift_sample_data.tpch_rs1.customer


"""

# Define the regex pattern
#pattern = r"(first_value\()([\s\S]*?)(ignore nulls)([\s\S]*?)(\)\s+over\s*\()"

# Define the regex pattern
#pattern = "(first_value\()(.*?)(ignore nulls\s*\)\s*over\s*\()"

# Define the replacement pattern
#replacement = "\1\2) ignore nulls over \3"

function_names = ["dlog10", "sysdate", "getdate", "isnull"]

for function_name in function_names:


    # Define the regex pattern
    pattern = r'({})(\()([^)]*)\)'.format(function_name.lower()) #Look for functions of the format name(input1,input2)
    replacement_doubleQuotes = r'{{{{lakehouse_utils.{}("\3")}}}}'.format(function_name) #Surround the expression with double curly braces, and quotes on either end

    check_preventDoubleReplace_pattern = r'({{lakehouse_utils.{}\()([^)]*)\)'.format(function_name)
    check_preventInnerReplace_pattern = r'(\w{}\()([^)]*)\)'.format(function_name)

    # If the function hasn't already been replaced with a macro AND isn't a subpart of another function name, then continue
    if (re.search(check_preventDoubleReplace_pattern,content, flags=re.IGNORECASE) is None) & (re.search(check_preventInnerReplace_pattern,content, flags=re.IGNORECASE) is None):
        try:
            number_of_matches = len(re.findall(pattern, content, flags=re.IGNORECASE))
        except:
            number_of_matches = 0

    content = re.sub(pattern, replacement_doubleQuotes, content, flags=re.IGNORECASE | re.DOTALL)



    #print(updated_content)

    matched_patterns = re.findall(pattern,content, flags=re.IGNORECASE) 

    #print(matched_patterns)

    for i in matched_patterns:
      
      # Substitute quotes around inner commas

      commas = r','
      quoted_commas = r'","'
      updated_match = re.sub(commas,quoted_commas,i[1], flags=re.IGNORECASE)
      content = content.replace(i[1], updated_match)

    # If we inadvertently surrounded a double-quoted string with more double-quotes, change these to be single quotes to prevent compatibility issues!

    double_doubleQuotes_pattern = r'""([^"]*)""'
    single_doubleQuotes_pattern = r"""'"\1"'"""
    
    content = re.sub(double_doubleQuotes_pattern,single_doubleQuotes_pattern,content, flags=re.IGNORECASE)

    # If we inadvertently added double-quotes to an empty input macro, remove these!

    accidental_doubleQuotes_pattern = r'({{lakehouse_utils.{}\()""\)'.format(function_name)
    fixed_noQuotes_pattern = r'\1)'
    
    content = re.sub(accidental_doubleQuotes_pattern,fixed_noQuotes_pattern,content, flags=re.IGNORECASE)

    print(content)

