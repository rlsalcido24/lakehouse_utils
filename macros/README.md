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
