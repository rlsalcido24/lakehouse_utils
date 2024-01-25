import os
os.chdir("lakehouse_utils/integration_tests")
syntaxakpath = 'syntaxak.sql' 
#functionakpath = 'functionak.sql' 
pyakpath = 'tresak.py' 
lookerakpath = 'unoak.lkml'

with open(syntaxakpath, 'r+') as file:
    syntaxak = file.read()

#with open(functionakpath, 'r+') as file:
#    functionak = file.read()

with open(lookerakpath, 'r+') as file:
    lookerak = file.read()

with open(pyakpath, 'r+') as file:
    pyak = file.read()

os.chdir("lakehouse_utils/models/redshift_to_databricks") 
syntaxgenpath = 'customerrs.sql'

with open(syntaxgenpath, 'r+') as file:
    syntaxgen = file.read()

os.chdir("lakehouse_utils/beyondsqltest")
pygenpath = "testpyfiles_to_databricks/tres.py"
lookergenpath = "testlookmlfiles_to_databricks/uno.lkml"   

with open(pygenpath, 'r+') as file:
    pygen = file.read()

with open(lookergenpath, 'r+') as file:
    lookergen = file.read()


assert syntaxak == syntaxgen
assert pyak == pygen
assert lookerak == lookergen

print('wooho, test passed!!')