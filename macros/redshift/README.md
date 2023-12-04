#### For the most up to date list of supported functions, refrence the functionlist.csv in the seed directory.

#### V1 supported functions: 

convert <br>
inputs: type, expression <br>
desc: Like the CAST function, the CONVERT function converts one data type to another compatible data type. For instance, you can convert a string to a date, or a numeric type to a string. CONVERT performs a runtime conversion, which means that the conversion doesn't change a value's data type in a source table. It's changed only in the context of the query. <br>
outputs: CONVERT returns the data type specified by the type argument. <br>

TEXT_TO_NUMERIC_ALT <br>
inputs: expresssion, format, precision, scale <br>
desc: Amazon Redshift casts the input expression string to the numeric type with the highest precision that you specify for that type in the precision option. If the length of the numeric value exceeds the value that you specify for precision, Amazon Redshift rounds the numeric value according to the following rules:. <br>

HLL_COMBINE_SKETCHES <br>
inputs: expr1, expr2 <br>
desc: The HLL_COMBINE_SKETCHES is a scalar function that takes as input two HLLSKETCH values and combines them into a single HLLSKETCH.
The combination of two or more HyperLogLog sketches is a new HLLSKETCH that encapsulates information about the union of the distinct values that each input sketch represents. <br>
outputs: HLL sketch type <br>

HLL_COMBINE <br>
inputs: expr <br>
desc: The combination of two or more HyperLogLog sketches is a new HLLSKETCH that encapsulates information about the union of the distinct values that each input sketch represents. After combining sketches, Amazon Redshift extracts the cardinality of the union of two or more datasets. <br>
outputs: HLL sketch type <br>

HLL_CREATE_SKETCH <br>
inputs: expr1 <br>
desc: The HLL_CREATE_SKETCH function returns an HLLSKETCH data type that encapsulates the input expression values. The HLL_CREATE_SKETCH function works with any data type and ignores NULL values. When there are no rows in a table or all rows are NULL, the resulting sketch has no index-value pairs such as {"version":1,"logm":15,"sparse":{"indices":[],"values":[]}}. <br>
outputs: The HLL_CREATE_SKETCH function returns an HLLSKETCH value. <br>

HLL_CARDINALITY <br>
inputs: expr <br>
desc: The HLL_CARDINALITY function returns the cardinality of the input HLLSKETCH data type. <br>
outputs: BigInt. <br>

DEXP <br>
inputs: number <br>
desc: The DEXP function returns the exponential value in scientific notation for a double precision number. The only difference between the DEXP and EXP functions is that the parameter for DEXP must be a double precision. <br>
outputs: Double Precision number <br>

DLOG10 <br>
inputs: number <br>
desc: The DLOG10 returns the base 10 logarithm of the input parameter. <br>
outputs: double precision <br>

DLOG1 <br>
inputs: expression <br>
desc: Returns the natural logarithm of the input parameter. Synonym of the DLOG1 function. <br>
outputs: The LN function returns the same type as the expression. <br>

isnull <br>
inputs: value, value_is_null <br>
desc: ISNULL in Redshift is just like a single COALESCE. This translates to COALESCE(value, value_is_null) <br>
outputs: The LN function returns the same type as the expression. <br>

getdate <br>
inputs: none <br>
desc: GETDATE returns the current date and time in the current session time zone (UTC by default). It returns the start date or time of the current statement, even when it is within a transaction block. <br>
outputs: The LN function returns the same type as the expression. <br>

sysdate <br>
inputs: none <br>
desc: SYSDATE returns the current date and time in the current session time zone (UTC by default).
outputs: The LN function returns the same type as the expression. <br>

#### V1 un-supported functions: 

HLL <br>
inputs: aggregate_expression <br>
desc: The HLL function returns the HyperLogLog cardinality of the input expression values. The HLL function works with any data types except the HLLSKETCH data type. The HLL function ignores NULL values. When there are no rows in a table or all rows are NULL, the resulting cardinality is 0. <br>
outputs: BigInt <br>
why no support: HLL can take in any expression whereas cardinality only takes in array/map expressions

TEXT_TO_INT_ALT <br>
inputs: expression, format <br>
desc: TEXT_TO_INT_ALT converts a character string to an integer using Teradata-style formatting. Fraction digits in the result are truncated. <br>
outputs: TEXT_TO_INT_ALT returns an INTEGER value. <br>
why no support: incompatible formatting

