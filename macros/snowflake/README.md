#### For the most up to date list of supported functions, refrence the functionlist.csv in the seed directory.

#### V1 supported string functions: 

md5_binary <br>
inputs: msg <br>
desc: Returns a 16-byte BINARY value containing the 128-bit MD5 message digest. <br>
outputs: Returns a 16-byte BINARY value containing the MD5 message digest. <br>

json_extract_path_text <br>
inputs: column, identifier <br>
desc: Parses the first argument as a JSON string and returns the value of the element pointed to by the path in the second argument. This is equivalent to TO_VARCHAR(GET_PATH(PARSE_JSON(JSON), PATH)) <br>
outputs: The data type of the returned value is VARCHAR. <br>

base64_encode <br>
inputs: input, max_line_length(optional), alphabet(optional) <br>
desc:Encodes the input (string or binary) using Base64 encoding. <br>
outputs: Returns a string (regardless of whether the input was a string or BINARY). <br>

zeroifnull <br> 
inputs: expr <br> 
desc: Returns 0 if its argument is null; otherwise, returns its argument. <br> 
outputs: zero or the original arg <br> 


seq4 <br>
inputs: (01) optional <br>
desc: Returns a sequence of monotonically increasing integers, with wrap-around. Wrap-around occurs after the largest representable integer of the integer width (1, 2, 4, or 8 byte). <br>
outputs: If the optional sign argument is 0, the sequence continues at 0 after wrap-around. If the optional sign argument is 1, the sequence continues at the smallest representable number based on the given integer width. The default sign argument is 0.
<br>

strok_to_array <br>
inputs: string, delimiter (optional) <br>
desc: Tokenizes the given string using the given set of delimiters and returns the tokens as an array. If either parameter is a NULL, a NULL is returned. An empty array is returned if tokenization produces no tokens. <br>
outputs: The data type of the returned value is ARRAY. <br>

to_number <br> 
inputs: expr (reqd), format (optional), precision (optional), scale (optional) <br> 
desc: The function returns NUMBER(p,s), where p is the precision and s is the scale. If the precision is not specified, then it defaults to 38. If the scale is not specified, then it defaults to 0. <br> 
outputs: number(precision, scale) <br> 

array_size <br> 
inputs: expr <br> 
desc: Returns the size of the input array. A variation of ARRAY_SIZE takes a VARIANT value as input. If the VARIANT value contains an array, the size of the array is returned; otherwise, NULL is returned if the value is not an array. <br> 
outputs: INT articulating size <br> 

#### V1 supported timestamp functions: 

dateadd <br> 
inout: date_or_time_part, value, date_or_time_expr <br> 
desc: Adds the specified value for the specified date or time part to a date, time, or timestamp. <br> 
output: time/timestamp/date depending on the input <br> 

dayname <br>
inputs: date_or_timestamp_expr <br>
desc: Extracts the three-letter day-of-week name from the specified date or timestamp. <br>
outputs: Extracts the three-letter day-of-week name from the specified date or timestamp. <br>

timestampadd <br>
inputs: date_or_time_part, time_value, date_or_time_expr <br>
desc: Adds the specified value for the specified date or time part to a date, time, or timestamp. <br>
outputs: If date_or_time_expr is a time: The return data type is a time. If date_or_time_expr is a timestamp: The return data type is a timestamp. If date_or_time_expr is a date: If date_or_time_part is day or larger (e.g. month, year), the function returns a DATE value. If date_or_time_part is smaller than a day (e.g. hour, minute, second), the function returns a TIMESTAMP_NTZ value, with 00:00:00.000 as the starting time for the date. <br>

week <br>
inputs: date_or_timestamp_expr <br>
desc: Extracts the corresponding date part from a date or timestamp. <br>
outputs: Extracts the corresponding date part from a date or timestamp. <br>

timediff <br>
inputs: date_or_time_part, date_or_time_expr1, date_or_time_expr2  <br>
desc: Calculates the difference between two date, time, or timestamp expressions based on the specified date or time part. The function returns the result of subtracting the second argument from the third argument. <br>
outputs: Returns an integer representing the number of units (seconds, days, etc.) difference between date_or_time_expr2 and date_or_time_expr1. <br>

date_from_parts <br>
inputs: year, month, day <br>
desc: Creates a date from individual numeric components that represent the year, month, and day of the month. <br>
outputs: DATE_FROM_PARTS is typically used to handle values in “normal” ranges (e.g. months 1-12, days 1-31), but it also handles values from outside these ranges. This allows, for example, choosing the N-th day in a year, which can be used to simplify some computations.
Year, month, and day values can be negative (e.g. to calculate a date N months prior to a specific date). The behavior of negative numbers is not entirely intuitive; see the Examples section for details. <br>

monthname <br>
inputs: date_or_timestamp_expr <br>
desc: Extracts the three-letter month name from the specified date or timestamp. <br>
outputs: Extracts the three-letter month name from the specified date or timestamp. <br>

timestampdiff <br> 
inputs: date_or_time_part, date_or_time_expr1, date_or_time_expr2 <br> 
desc: Calculates the difference between two date, time, or timestamp expressions based on the specified date or time part. The function returns the result of subtracting the second argument from the third argument. <br> 
outputs: Returns an integer representing the number of units (seconds, days, etc.) difference between date_or_time_expr2 and date_or_time_expr1. <br>

to_time <br> 
inputs: expr, format(optaional) <br> 
desc: Converts an input expression into a time. If input is NULL, returns NULL. <br> 
outputs: time <br> 

timeadd <br> 
inputs: date_or_time_part, value, date_or_time_expr <br> 
desc: Adds the specified value for the specified date or time part to a date, time, or timestamp. <br> 
outputs: date, time, or timestamp depending on the date_or_time_expr <br> 


#### V1 supported numeric functions: 

try_to_number <br> 
inputs: string, format (optional), precision (optional), scale (optional) <br> 
desc: <br> A special version of TO_DECIMAL , TO_NUMBER , TO_NUMERIC that performs the same operation (i.e. converts an input expression to a fixed-point number), but with error-handling support (i.e. if the conversion cannot be performed, it returns a NULL value instead of raising an error). 
outputs: <br> The function returns NUMBER(p,s), where p is the precision and s is the scale. If the precision is not specified, then it defaults to 38. If the scale is not specified, then it defaults to 0.

try_to_numeric <br> 
inputs: string, format (optional), precision (optional), scale (optional) <br> 
desc: <br> A special version of TO_DECIMAL , TO_NUMBER , TO_NUMERIC that performs the same operation (i.e. converts an input expression to a fixed-point number), but with error-handling support (i.e. if the conversion cannot be performed, it returns a NULL value instead of raising an error). 
outputs: <br> The function returns NUMBER(p,s), where p is the precision and s is the scale. If the precision is not specified, then it defaults to 38. If the scale is not specified, then it defaults to 0.

to_decimal <br>
inputs: expr (reqd), format (optional), precision (optional), scale (optional) <br>
desc: The function returns NUMBER(p,s), where p is the precision and s is the scale. If the precision is not specified, then it defaults to 38. If the scale is not specified, then it defaults to 0. <br>
outputs: number(precision, scale) <br>

to_numeric <br>
inputs: expr (reqd), format (optional), precision (optional), scale (optional) <br>
desc: The function returns NUMBER(p,s), where p is the precision and s is the scale. If the precision is not specified, then it defaults to 38. If the scale is not specified, then it defaults to 0. <br>
outputs: number(precision, scale) <br>

try_to_decimal <br> 
inputs: string, format (optional), precision (optional), scale (optional) <br> 
desc: <br> A special version of TO_DECIMAL , TO_NUMBER , TO_NUMERIC that performs the same operation (i.e. converts an input expression to a fixed-point number), but with error-handling support (i.e. if the conversion cannot be performed, it returns a NULL value instead of raising an error). 
outputs: <br> The function returns NUMBER(p,s), where p is the precision and s is the scale. If the precision is not specified, then it defaults to 38. If the scale is not specified, then it defaults to 0.

#### V1 supported boolean functions: 

to_boolean <br> 
inputs: expr <br> 
desc: Coverts the input text or numeric expression to a Boolean value. For NULL input, the output is NULL. <br> 
outputs: boolean <br> 

#### V1 supported complex functions: 

to_array <br> 
inputs: expr <br> 
desc:Converts the input expression to an ARRAY: <br> 
If the input is an ARRAY, or VARIANT containing an array value, the result is unchanged.
For NULL or a JSON null input, returns NULL.
For any other value, the result is a single-element array containing this value.
outputs: array

listagg <br> 
inputs: expr1, delimiter, expr2, orderby_clause <br> 
desc: Returns the concatenated input values, separated by the delimiter string. <br> 
outputs: Returns a string that includes all of the non-NULL input values, separated by the delimiter. (Note that this does not return a “list” (e.g. it does not return an ARRAY; it returns a single string that contains all of the non-NULL input values.) <br> 

#### Recently supported native functions: 

to_binary <br> 
inputs: string_expr, format(optional) <br> 
desc:Converts the input expression to a binary value. For NULL input, the output is NULL. <br> 
outputs: binary <br> 

array_compact <br> 
inputs: array1 <br> 
desc: Returns a compacted array with missing and null values removed, effectively converting sparse arrays into dense arrays.  <br> 
outputs: dense array <br> 

len <br>
inputs: expr <br>
desc: Returns the length of an input string or binary value. For strings, the length is the number of characters, and UTF-8 characters are counted as a single character. For binary, the length is the number of bytes. <br>
outputs: The returned data type is INTEGER (more precisely, NUMBER(18, 0)). <br>

equal_null <br> 
inputs: expr1, expr2 <br> 
desc: Compares whether two expressions are equal. The function is NULL-safe, meaning it treats NULLs as known values for comparing equality. Note that this is different from the EQUAL comparison operator (=), which treats NULLs as unknown values. <br> 
outputs: true/false boolean <br> 

to_timestamp_ntz <br>
inputs: expr1, format, scale <br> 
desc: Converts an input expression into the corresponding timestamp <br> 
outputs: The data type of the returned value is one of the TIMESTAMP data types. By default, the data type is TIMESTAMP_NTZ. You can change this by setting the session parameter TIMESTAMP_TYPE_MAPPING. <br> 

contains <br> 
input: expr1, expr2 <br> 
desc: Returns true if expr1 contains expr2. Both expressions must be text or binary expressions. <br> 
output: Returns a BOOLEAN. The value is True if expr2 is found inside expr1. Returns NULL if either input expression is NULL. Otherwise, returns False. <br> 

startswith <br> 
inputs: expr, expr2 <br> 
desc: Returns true if expr1 starts with expr2. Both expressions must be text or binary expressions. <br> 
outputs: boolean <br> 

try_cast <br> 
inputs: source_string_expr, target_data_type <br> 
desc: A special version of CAST , :: that is available for a subset of data type conversions. It performs the same operation (i.e. converts a value of one data type into another data type), but returns a NULL value instead of raising an error when the conversion can not be performed.
outputs: returns the casted val, or null if it ca't be casted <br> 

current_schema <br>
inputs: n/a <br>
desc: Returns the name of the schema in use by the current session. <br>
outputs: current schema <br>

ends_with <br>
inputs: exp1, expr2 <br>
desc: Returns TRUE if the first expression ends with second expression. Both expressions must be text or binary expressions. <br>
outputs: Returns a BOOLEAN. The value is True if expr1 ends with expr2. Returns NULL if either input expression is NULL. Otherwise, returns False. <br>

charindex <br>
inputs: expr1, expr2, start_pos (optional)<br>
desc: Searches for the first occurrence of the first argument in the second argument and, if successful, returns the position (1-based) of the first argument in the second argument. <br>
outputs: If any arguments are NULL, the function returns NULL.If the string or binary value is not found, the function returns 0. If the specified optional start_pos is beyond the end of the second argument (the string to search), the function returns 0. If the first argument is empty (e.g. an empty string), the function returns 1. The data types of the first two arguments should be the same; either both should be strings or both should be binary values. <br>

array_agg <br> 
inputs: expr1, expr2, orderby_clause(optional) <br> 
desc: Returns the input values, pivoted into an ARRAY. If the input is empty, an empty ARRAY is returned. <br> 
outputs: an array <br> 

split_part <br> 
inputs: string, delimiter, partnumber <br> 
desc: Splits a given string at a specified character and returns the requested part. <br> 
outputs: split up string <br> 

[regexp_like, regexp_substr, iff, median, regexp_instr, percentile_disc, regexp_count, percentile_cont, any_value]


#### Not yet supported functions:

to_varchar <br> 
inputs: expr (reqd), format (optional) <br> 
desc: Converts the input expression to a string. For NULL input, the output is NULL.
outputs: For VARIANT, ARRAY, or OBJECT inputs, the output is the string containing a JSON document or JSON elementary value (unless VARIANT or OBJECT contains an XML tag, in which case the output is a string containing an XML document):A string stored in VARIANT is preserved as is (i.e. it is not converted to a JSON string).
A JSON null value is converted to a string containing the word “null”. <br> 

convert_timezone <br> 
inputs: source_tz, target_tz, source_tiemstamp_ntz or target_tz, source_timestamp <br> 
desc: For the 3-argument version: <br> 
The “wallclock” time in the result represents the same moment in time as the input “wallclock” in the input time zone, but in the destination time zone.
The return value is always of type TIMESTAMP_NTZ.
For the 2-argument version:
The source_timestamp argument is considered to include the time zone. If the value is of type TIMESTAMP_TZ, the time zone is taken from its value. Otherwise, the current session time zone is used.
The return value is always of type TIMESTAMP_TZ.
For source_tz and target_tz, you can specify a time zone name or a link name from release 2021a of the IANA Time Zone Database (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.).
output: returns either timestamp_ntz (three args) or timestamp_tz (two args) <br> 


to_char  <br> 
inputs: expr (reqd), format (optional) <br> 
desc: Converts the input expression to a string. For NULL input, the output is NULL. <br> 
outputs: For VARIANT, ARRAY, or OBJECT inputs, the output is the string containing a JSON document or JSON elementary value (unless VARIANT or OBJECT contains an XML tag, in which case the output is a string containing an XML document):A string stored in VARIANT is preserved as is (i.e. it is not converted to a JSON string). 
A JSON null value is converted to a string containing the word “null”. <br> 

array_construct <br> 
inputs: kwarg expressions <br> 
desc: Returns an array constructed from zero, one, or more inputs. <br> 
outputs: array <br> 


object_construct <br> 
inputs: kwargs <br> 
desc: Returns an OBJECT constructed from the arguments. <br> 
outputs: instantiated object <br>  

is_null_value <br> 
inputs: variant <br> 
desc: Returns true if its VARIANT argument is a JSON null value. <br> 
outputs: boolean  <br> 

array_to_string <br> 
inputs: array, seperator_string <br> 
desc: Returns an input array converted to a string by casting all values to strings (using TO_VARCHAR) and concatenating them (using the string from the second argument to separate the elements). <br> 
outputs: The data type of the returned value is VARCHAR. <br> 

to_timestamp_tz
inputs: varchar <br> 
desc: Interprets an input string as a JSON document, producing a VARIANT value. <br> 
outputs: The returned value is of type VARIANT and contains a JSON document. <br> 
blocker: we support timestamp for ntz... <br>

parse_json
inputs: varchar <br> 
desc: Interprets an input string as a JSON document, producing a VARIANT value. <br> 
outputs: The returned value is of type VARIANT and contains a JSON document. <br> 
blocker: databricks does not support variant type <br>

last_query_id
inputs: num <br> 
desc: Returns the ID of a specified query in the current session. If no query is specified, the most recently-executed query is returned. <br> 
outputs: Return the ID for the most recently-executed query: <br> 
blocker: no comparable databricks DQL <br>

current_transaction
inputs: none <br> 
desc: Returns the transaction id of an open transaction in the current session. <br> 
outputs: This shows the transaction ID of the current transaction: <br> 
blocker: no comparable databricks DQL <br>

object_insert
inputs: object, key, value <br> 
desc: Returns an object consisting of the input object with a new key-value pair inserted (or an existing key updated with a new value). <br> 
outputs: Insert a third key-value pair into an object containing two key-value pairs: <br> 
blocker: TBD <br>

check_json
inputs: string/variant <br> 
desc: Checks the validity of a JSON document. If the input string is a valid JSON document or a NULL, the output is NULL (i.e. no error). If the input cannot be translated to a valid JSON value, the output string contains the error message. <br> 
outputs: Use the CHECK_JSON function to check the validity of potential JSON-compatible strings in a VARIANT column: <br> 
blocker: TBD <br>

hll_export
inputs: binaryexpr <br> 
desc: Converts input in BINARY format to OBJECT format. <br> 
outputs: Converts input in BINARY format to OBJECT format. <br> 
blocker: TBD <br>

decrpt
TBD

get
inputs: internalstage <br> 
desc: Downloads data files from one of the following Snowflake stages to a local directory/folder on a client machine:. <br> 
outputs: N/A <br> 
blocker: we dont have stages, we work directly against cloud storage. in databricks you can use dbutils copy for this use case. <br>

current_region
inputs: na <br> 
desc: Returns the name of the region for the account where the current user is logged in. <br> 
outputs: Returns the name of the region for the account where the current user is logged in. <br> 
blocker: no comparable DQL in databricks <br>

get_ddl
inputs: objecttype, objectname <br> 
desc: Returns a DDL statement that can be used to recreate the specified object. For databases and schemas, GET_DDL is recursive (i.e. it returns the DDL statements for recreating all supported objects within the specified database/schema). <br> 
outputs: Returns a string (VARCHAR) containing the text of the DDL statement that created the object. <br> 
blocker: we have show create table but wouldnt support the other objecttypes <br>

try_parse_json
inputs: varchar <br> 
desc: A special version of PARSE_JSON that returns a NULL value if an error occurs during parsing. <br> 
outputs: The returned value is of type VARIANT and contains a JSON document. <br> 
blocker: databricks does not support variant type <br>

to_geography
inputs: varchar <br> 
desc: Parses an input and returns a value of type GEOGRAPHY. <br> 
outputs: The function returns a value of type GEOGRAPHY. <br> 
blocker: databricks does not support geography type <br>

parse_xml

object_delete

standardize

hll_estimate

get_path

st_intersects







