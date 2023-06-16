# springbricks

Purpose:\

The purpose of the springbricks initiative is threefold \

i) Expedite the time and level of effort for migrating pipelines built on dbt + snowflake to dbt + databricks. This is done by transpiling snowflake functions that are not natively available in spark sql to compatible spark sql functions that take in the same input(s) and render the same outputs. This is all done via DBT macros (feel free to reference the macros directory).  \

ii) Be a centralized source of truth for Snowflake functions mapping to Databricks functions. Also surface instances where certain functions can not be automated and manual intervention is required. You can find further information in the read.me in the tests directory.  \

iii) Surface best practices around unit tests to instill confidence that the macros are robust and reliable (feel free to reference the tests directory). \

'Hello World' CUJ:  \

To get a quick sense of what this module offers, you can reference and run the models in the models directory. Here are the relevant steps:  \

i) Insert the relevant values into the profiles.yml based on your snowflake and databricks credentials.

ii) Build the snowflake models by executing dbt run --target snow --select dev

iii) Build the databricks models by executing dbt run --target dbx --select dbx

iv) Observe that when when the models build on databricks they transpile the snowflake functions that invoke macros (wrapped in curly braces). Also observe that while syntax is slightly different in each system the end results are still the same. Also note that manually 'migrating' these two models from scratch should take no longer than 5 mins-- it is just a matter of wrapping the relevant function in braces and wrapping the input parameters in single quotes. 

Next Steps: \

i) Build a parsing script that will leverage regex to create a clone model directory that will wrap the relevant snowflake functions in curly braces (and the input params in single quotes) to trigger function invocation and transpilation to ensure that the tables can build in databricks in an automated fashion.  

ii) Deploy this logic as a package in the dbt hub so it is simpler to interface with

Note that we gladly welcome contributions from the partners and from the community-- if intersted please submit a pull request!! We can particularly use support with building the regex parsing script and increasing our surface area of supported functions. When submitting a PR please include a unit test for each new macro added. If you have a request so support a particular function please do let us know in the comments and happy building!!
