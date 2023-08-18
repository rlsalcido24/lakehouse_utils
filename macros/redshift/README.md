#### For the most up to date list of supported functions, refrence the functionlist.csv in the seed directory.

#### V1 supported math functions:

dexp <br>
inputs: number <br>
desc: Returns the exponential value in scientific notation for a double precision number. <br>
outputs: Returns the exponential value in double precision format. <br>

#### V1 supported data type formatting functions

text_to_int_alt <br>
inputs: expression, format <br>
desc: Converts a character string to an integer usign Teradata-style formatting. <br>
outputs: Returns an integer value where the fractional portion of the cast result is truncated. <br>

text_to_numeric_alt <br>
inputs: expression, format, precision, scale <br>
desc: Performs a Teradata-style cast operation to convert a character string to a numeric data format based on the expression, format, precision, and scale provided. <br>
outputs: Returns a decimal number. <br>