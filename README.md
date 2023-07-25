# springbricks

Purpose:\

The purpose of the springbricks initiative is threefold \

i) Expedite the time and level of effort for migrating pipelines built on dbt + snowflake to dbt + databricks. This is done by transpiling snowflake functions that are not natively available in spark sql to compatible spark sql functions that take in the same input(s) and render the same outputs. This is all done via DBT macros (feel free to reference the macros directory).  \

ii) Be a centralized source of truth for Snowflake functions mapping to Databricks functions. Also surface instances where certain functions can not be automated and manual intervention is required. You can find further information in the read.me in the macros directory.  \

iii) Surface best practices around unit tests to instill confidence that the macros are robust and reliable (feel free to reference the tests directory). \

Manual 'Hello World' CUJ:  \

To get a quick sense of what this module offers, you can reference and run the models in the models directory. Here are the relevant steps:  \

i) Insert the relevant values into the profiles.yml based on your snowflake and databricks credentials.

ii) Build the snowflake models by executing dbt run --target snow 

iii) Build the databricks models by temporarily updating the models_path key in profiles.yml to be tmp and executing dbt run --target dbx

iv) Observe that when when the models build on databricks they transpile the snowflake functions that invoke macros (wrapped in curly braces). Also observe that while syntax is slightly different in each system the end results are still the same. Also note that manually 'migrating' these two models from scratch should take no longer than 5 mins-- it is just a matter of wrapping the relevant function in braces and wrapping the input parameters in quotes. 

Automated 'to the moon' CUJ \

i) Create a seperate dev branch of your dbt project. Copy the helper directory and the macros directory into your project. Run the helper function_to_macro.py file on Databricks or locally. Obvserve that all your snowflake models have now been automatically refactored to reference relevant macros, therefore making it possible to build these models in databricks.

ii) dbt run.

iii) Execute unit tests to ensure that the models built in Databricks match the models built on Snowflake.

iv) Once you have sufficient confidence copy the directory from the models directory of the dev branch to the models directory of the main branch and name the directory something different to differentiate it from the snowflake models (ie snow and databricks) 

v) Build models in both systems until sufficient confidence is instilled to run the models solely on one system.


Next Steps: \

i) Deploy this logic as a package in the dbt hub so it is simpler to interface with (ci/cd, docs, contributor guide, issue/request guide, sqlfluff)

Note that we gladly welcome contributions from the partners and from the community-- if intersted please submit a pull request!! We can particularly use support with increasing our surface area of supported functions. When submitting a PR please include a unit test for each new macro added-- as long as any new unit tests pass, and existing tests continue to pass, we should be able to GTM (example pr template in .github directory). If you have a request so support a particular function please do log it as a feature requests in issues and happy building!!
