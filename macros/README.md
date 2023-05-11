to_varchar <br> 
inputs: expr (reqd), format (optional) <br> 
desc: Converts the input expression to a string. For NULL input, the output is NULL.
outputs: For VARIANT, ARRAY, or OBJECT inputs, the output is the string containing a JSON document or JSON elementary value (unless VARIANT or OBJECT contains an XML tag, in which case the output is a string containing an XML document):A string stored in VARIANT is preserved as is (i.e. it is not converted to a JSON string).
A JSON null value is converted to a string containing the word “null”. <br> 

dateadds
inout: date_or_time_part, value, date_or_time_expr
desc: Adds the specified value for the specified date or time part to a date, time, or timestamp.
output: time/timestamp/date depending on the input

contains
input: expr1, expr2
desc: Returns true if expr1 contains expr2. Both expressions must be text or binary expressions.
output: Returns a BOOLEAN. The value is True if expr2 is found inside expr1. Returns NULL if either input expression is NULL. Otherwise, returns False.

convert_timezone
inputs: source_tz, target_tz, source_tiemstamp_ntz or target_tz, source_timestamp
desc: For the 3-argument version:
The “wallclock” time in the result represents the same moment in time as the input “wallclock” in the input time zone, but in the destination time zone.
The return value is always of type TIMESTAMP_NTZ.
For the 2-argument version:
The source_timestamp argument is considered to include the time zone. If the value is of type TIMESTAMP_TZ, the time zone is taken from its value. Otherwise, the current session time zone is used.
The return value is always of type TIMESTAMP_TZ.
For source_tz and target_tz, you can specify a time zone name or a link name from release 2021a of the IANA Time Zone Database (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.).
output: returns either timestamp_ntz (three args) or timestamp_tz (two args)

listagg
inputs: expr1, delimiter, expr2, orderby_clause
desc: Returns the concatenated input values, separated by the delimiter string.
outputs: Returns a string that includes all of the non-NULL input values, separated by the delimiter. (Note that this does not return a “list” (e.g. it does not return an ARRAY; it returns a single string that contains all of the non-NULL input values.)

to_binary
inputs: string_expr, format(optional)
desc:Converts the input expression to a binary value. For NULL input, the output is NULL.
outputs: binary

equal_null
inputs: expr1, expr2
desc: Compares whether two expressions are equal. The function is NULL-safe, meaning it treats NULLs as known values for comparing equality. Note that this is different from the EQUAL comparison operator (=), which treats NULLs as unknown values.
outputs: true/false boolean

get_date
inputs:
desc:
outputs:

to_array
inputs: expr
desc:Converts the input expression to an ARRAY:
If the input is an ARRAY, or VARIANT containing an array value, the result is unchanged.
For NULL or a JSON null input, returns NULL.
For any other value, the result is a single-element array containing this value.
outputs: array

to_timestamp_ntz (later)
to_timestamp_tz (later)


to_char 
inputs: expr (reqd), format (optional)
desc: Converts the input expression to a string. For NULL input, the output is NULL.
outputs: For VARIANT, ARRAY, or OBJECT inputs, the output is the string containing a JSON document or JSON elementary value (unless VARIANT or OBJECT contains an XML tag, in which case the output is a string containing an XML document):A string stored in VARIANT is preserved as is (i.e. it is not converted to a JSON string).
A JSON null value is converted to a string containing the word “null”.

startswith
inputs: expr, expr2
desc: Returns true if expr1 starts with expr2. Both expressions must be text or binary expressions.
outputs: boolean

try_cast
inputs: source_string_expr, target_data_type
desc: A special version of CAST , :: that is available for a subset of data type conversions. It performs the same operation (i.e. converts a value of one data type into another data type), but returns a NULL value instead of raising an error when the conversion can not be performed.
outputs: returns the casted val, or null if it ca't be casted

to_number
inputs: expr (reqd), format (optional), precision (optional), scale (optional)
desc: The function returns NUMBER(p,s), where p is the precision and s is the scale. If the precision is not specified, then it defaults to 38. If the scale is not specified, then it defaults to 0.
outputs: number(precision, scale)

array_size
inputs: expr
desc: Returns the size of the input array. A variation of ARRAY_SIZE takes a VARIANT value as input. If the VARIANT value contains an array, the size of the array is returned; otherwise, NULL is returned if the value is not an array.
outputs: INT articulating size

array_construct
inputs: kwarg expressions
desc: Returns an array constructed from zero, one, or more inputs.
outputs: array

array_agg
inputs: expr1, expr2, orderby_clause(optional)
desc: Returns the input values, pivoted into an ARRAY. If the input is empty, an empty ARRAY is returned.
outputs: an array

split_part
inputs: string, delimiter, partnumber
desc: Splits a given string at a specified character and returns the requested part.
outputs: split up string

to_time
inputs: expr, format(optaional)
desc: Converts an input expression into a time. If input is NULL, returns NULL.
outputs: time

to_boolean
inputs: expr
desc: Coverts the input text or numeric expression to a Boolean value. For NULL input, the output is NULL.
outputs: boolean

timeadd
inputs: date_or_time_part, value, date_or_time_expr
desc: Adds the specified value for the specified date or time part to a date, time, or timestamp.
outputs: date, time, or timestamp depending on the date_or_time_expr

zeroifnull
inputs: expr
desc: Returns 0 if its argument is null; otherwise, returns its argument.
outputs: zero or the original arg

object_construct
inputs: kwargs
desc: Returns an OBJECT constructed from the arguments.
outputs: instantiated object

timestampdiff
inputs: date_or_time_part, date_or_time_expr1, date_or_time_expr2
desc: Calculates the difference between two date, time, or timestamp expressions based on the specified date or time part. The function returns the result of subtracting the second argument from the third argument.
outputs: Returns an integer representing the number of units (seconds, days, etc.) difference between date_or_time_expr2 and date_or_time_expr1.

is_null_value
inputs: variant
desc: Returns true if its VARIANT argument is a JSON null value.
outputs: boolean 

array_compact
inputs: array1
desc: Returns a compacted array with missing and null values removed, effectively converting sparse arrays into dense arrays. 
outputs: dense array



