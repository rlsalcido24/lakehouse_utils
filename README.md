# springbricks

springbricks is an initiative to automate dbt + snowflake model builds to dbt + databricks with minimal refactoring. This is done through dbt macros. The relevant macros are in the macros folder. Assuming dbt is intalled locally, execute dbt run and witness the comilation that is done under the hood! The sample model leverages 3 of the example macros but feel free to test with any of the ~60 that are currently available!

If you want to contribute to unit tests pull the repo, insert a token, and then run dbt seed and dbt test. if all the tests pass submit a PR and LGTM!!

Next steps

i) Complete coverage for ~80 most common used snowflake functions (all v1 in todo/test failure, dont worry about NA/yes/blocked)

ii) Stress test with tpc-di

iii) develop regression testing framework 

iv) Add comments in macros read.me to clarrify inputs/outputs for each macro

iv) release package– track how often it is used for migrations, iterate over time based on most requested functions

v) use dashboards/metrics to determine ARR impact of the package
