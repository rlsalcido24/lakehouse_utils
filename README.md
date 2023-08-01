### lakehouse_utils:

The purpose of the lakehouse utils package is threefold 

I) Expedite the time and level of effort for migrating pipelines from cloud data warehouses to the Lakehouse  (ie dbt + databricks). This is done by transpiling functions that are not natively available in spark sql to compatible spark sql functions that take in the same input(s) and render the same outputs. This is all done via DBT macros (feel free to reference the macros directory).  

II) Be a centralized source of truth for warehouse function mapping to Databricks function mapping. Also surface instances where certain functions can not be automated and manual intervention is required. You can find the full list of supported functions in the functionlist.csv in the seed directory; you can also find further information in the read.me in the macros directory.  

III) Surface best practices around unit tests to instill confidence that the macros are robust and reliable (feel free to reference the tests directory). 

### Installation instructions:

I) Include this package in your packages.yml — check [here](https://github.com/rlsalcido24/lakehouse_utils/releases/tag/v0.1.1) for the latest version number.

II) Run dbt deps

III) Execute dbt seed -- this project includes a CSV that must be seeded for automated transpilation.

### Database support:

This package has been tested on Snowflake and Databricks.

### Manual 'Hello World' CUJ:  

To get a quick sense of what this module offers, you can reference and run the models in the models directory. Here are the relevant steps:  

I) Insert the relevant values into the profiles.yml based on your warehouse and lakehouse credentials.

II) Build the Snowflake models by executing dbt run --target snow 

III) Build the Databricks models by temporarily updating the models_path key in profiles.yml to be tmp and executing dbt run --target databricks.

IV) Observe that when when the models build on Databricks they transpile the Snowflake functions that invoke macros (wrapped in curly braces). Also observe that while syntax is slightly different in each system the end results are still the same. Also note that manually 'migrating' these two models from scratch should take no longer than 5 mins-- it is just a matter of wrapping the relevant function in braces and wrapping the input parameters in quotes. 

### Automated 'to the moon' CUJ 

I) Create a seperate dev branch of your dbt project. Execute dbt seed (if you haven't already). Run the helper function_to_macro.py file on Databricks. Obvserve that all your Snowflake models have now been automatically refactored to reference relevant macros, therefore making it possible to build these models in Databricks.

II) dbt run.

III) Execute unit tests to ensure that the models built in Databricks match the models built on Snowflake.

IV) Once you have sufficient confidence copy the directory from the models directory of the dev branch to the models directory of the main branch and name the directory something different to differentiate it from the Snowflake models (ie Snow and Databricks) 

V) Build models in both systems until sufficient confidence is instilled to run the models solely on one system.

## Macros:

### zeroifnull (source)

This macro takes in a column input and leverages the nvl function to return 0 if the input is null.
```
    {% macro zeroifnull(column_name) %}
    nvl({{column_name}}, 0)
    {% endmacro %}
```

Arguments:

a) Column name


### Next Steps: 

I) Deploy this logic as a package in the dbt hub so it is simpler to interface with.

Note that we gladly welcome contributions from the partners and from the community-- if intersted please submit a pull request! We can particularly use support with increasing our surface area of supported functions. When submitting a PR please include a unit test for each new macro added-- as long as any new unit tests pass, and existing tests continue to pass, we should be able to GTM (example pr template in .github directory). If you have a request to support a particular function please do log it as an enhancement in issues and happy building!!
