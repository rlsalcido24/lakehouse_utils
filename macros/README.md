to_varchar 
inputs: expr (reqd), format (optional)
desc: Converts the input expression to a string. For NULL input, the output is NULL.
outputs: For VARIANT, ARRAY, or OBJECT inputs, the output is the string containing a JSON document or JSON elementary value (unless VARIANT or OBJECT contains an XML tag, in which case the output is a string containing an XML document):A string stored in VARIANT is preserved as is (i.e. it is not converted to a JSON string).
A JSON null value is converted to a string containing the word “null”.

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

to_char

startswith
