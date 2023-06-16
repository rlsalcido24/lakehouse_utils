# springbricks

Purpose:\

The purpose of the springbricks initiative is threefold \

i) Expedite the time and level of effort for migrating pipelines built on dbt + snowflake to dbt + databricks. This is done by transpiling snowflake functions that are not natively available in spark sql to compatible spark sql functions that take in the same input(s) and render the same outputs. This is all done via DBT macros (feel free to reference the macros directory).  \

ii) Be a centralized source of truth for Snowflake functions mapping to Databricks functions. You can find further information in the read.me in the tests directory.  \

iii) Surface best practices around unit tests to instill confidence that the macros are robust and reliable (feel free to reference the tests directory). \

'Hello World' CUJ:  \

To get a quick sense of what this module offers, you can reference and run the models in the models directory. Here are the relevant steps:  \

i) Prep the yml files...

ii) Build the snowflake models by executing dbt run --target snow --select snow

iii) Build the databricks models by executing dbt run --target dbx --select dbx

iv) Observe that when when the models build on databricks they transpile the snowflake functions that invoke macros (wrapped in curly braces). Also observe that while syntax is slightly different in each system the end results are still the same. 

Next Steps: \

i) Build parser

ii) deploy dbt hub

iii) welcome contributions from partners/community \ 

