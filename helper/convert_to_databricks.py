"""

Author: Cody Austin Davis
Date:  12/6/2023

Description: Local Model converter from Redshift / Snowflake models to Databricks

Main Command Example: 
Standalone Mode: 
python3 ./convert_to_databricks.py redshift --subdir_path "redshift/" --parse_mode 'all' --parse_first 'syntax'


Package Mode:
python3 ./dbt_packages/lakehouse_utils/helper/convert_to_databricks.py redshift \
--subdir_path 'example/' \
--parse_mode 'all' \
--run_mode 'package'

TO DO:
1. Add rule to not replace anything in between 2 sets of double brackets - DONE - Cody Davis
2. Add parameter to choose which parse mode goes first - syntax or functions - DONE - Cody Davis
3. Add ability to not use macros at all, just replace the code with the databricks code - ensure parameters are in correct order for target system
4. Add ability to add dynamic exclusionary rules (i.e. do not parse when text is in between double curly braces)
5. Add ability to pass in list of file extensions you want to parse (i.e. sql,yml, etc.)

"""


import os
import re
import json
import argparse
from pathlib import Path
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

def findargs (contentstring, sourcepatterninit):
  # this function takes in content and sourcestring and uses a recursive function to isolate the args associated with each function invocation match
  content = contentstring
  source_patterninit = sourcepatterninit
  initlistraw = []
  initlistgold = []
  findfunction = re.findall(source_patterninit, content, flags= re.IGNORECASE)
  funlength = len(findfunction)
  if funlength > 0:
    for i in range(funlength):
      leftparen = findfunction[i].count("(")
      rightparen = findfunction[i].count(")")
      init = 1
      initfunc = findfunction[i]
      if leftparen != rightparen:
        while leftparen != rightparen:
          sourceappend = "[^)]*?)"
          if init == 1:
            updatedregex = initfunc + sourceappend
          else:  
            updatedregex = findfunction[0] + sourceappend
          udpatedregexescapepre = updatedregex.replace("\\", "\\\\")   
          udpatedregexescapeuno = udpatedregexescapepre.replace("(", "\(")
          udpatedregexescapedos = udpatedregexescapeuno.replace(")", "\)")
          udpatedregexescapedos = udpatedregexescapedos.replace("[", "\[")
          udpatedregexescapedos = udpatedregexescapedos.replace("]", "\]")
          udpatedregexescapedos = udpatedregexescapedos.replace("\[^\)\]*?\)", "[^\)]*?\)")
          findfunction = re.findall(udpatedregexescapedos, content)
          if len(findfunction) == 0:
            if tmplogs == 'true':
              print(f"localregex: {udpatedregexescapedos}")
              print(f"localfindfunc: {findfunction}")
          leftparen = findfunction[0].count("(")
          rightparen = findfunction[0].count(")")
          latestdict = {"leftparen": leftparen, "rightparen": rightparen, "funcstring": findfunction[0]}
          initlistraw.append(latestdict)
          if len(findfunction) == 0:
            break
          init = 0
      else: 
        latestdict = {"leftparen": 0, "rightparen": 0, "funcstring": initfunc}
        initlistraw.append(latestdict)  

      listlength = len(initlistraw)
      lastelement = initlistraw[listlength - 1]
      lastleftparen = lastelement['leftparen'] 
      lastrightparen = lastelement['rightparen']
      lastfuncstring = lastelement['funcstring']
      parendiff = leftparen - rightparen
      parenappend = parendiff * (")") 
      funcstring = lastfuncstring + parenappend
      uniquekey = i
      args = []
      funcdict = {"funcstring": funcstring, "uniquekey": uniquekey}
      #print(funcdict)
      initlistgold.append(funcdict)
      #print(initlistgold)
      findfunction = re.findall(source_patterninit, content, flags= re.IGNORECASE)
  return initlistgold  

def parsestrings(fullargs):
  # this function parses the args and replaces commas in strings with a tmp placeholder. this ensures that our tuple logic can delimit individual args
  ## todo--make dynamic to support when double args are first
  initlistgold = fullargs
  initlistsilver = []
  for gold in initlistgold:
    findfirstparen = gold["funcstring"].find("(")
    strlength = len(gold["funcstring"])
    extractarg = gold["funcstring"][findfirstparen + 1:strlength - 1]
    stringargregex = "'[^']*?'"
    findstringargs = re.findall(stringargregex, extractarg)
    #print(findstringargs)
    localsilverlist = []
    #print(findstringargs)
    for stringarg in findstringargs:
      commaph = "#tmpcommaplaceholder"
      stringargreplace = stringarg.replace(",", "#tmpcommaplaceholder")
      escapedq = stringargreplace.replace("\"", "\\\"")
      removecomma = extractarg.replace(stringarg, escapedq)
      extractarg = removecomma
      localsilverlist.append(removecomma)
    llave = gold["uniquekey"]  
    listlengthsilver = len(localsilverlist)
    if listlengthsilver > 0: 
      lastelementsilver = localsilverlist[listlengthsilver - 1]
      silverdict = {"target_string": lastelementsilver, "uniquekey": llave }
      initlistsilver.append(silverdict)
    else:
      silverdict = {"target_string": extractarg, "uniquekey": llave }
      initlistsilver.append(silverdict)
  return initlistsilver

def parseparens(parsedstrings):
  # this function parses the args and replaces commas in nested function invocations with a tmp placeholder. this ensures that our tuple logic can delimit individual args
  initlistsilver = parsedstrings
  initlistplatiunum = []
  for silver in initlistsilver:
    
    findleftparen = silver["target_string"].find("(", 0)
    findleftparenlist = []
    findrightparen = silver["target_string"].find(")", 0)
    findrightparenlist = []
    startindexlist = []
    indexdflist = []
    silverstring = silver["target_string"]
    while findleftparen != -1:
      findleftparenlist.append(findleftparen)
      findleftparen = silver["target_string"].find("(", findleftparen + 1) 
    while findrightparen != -1:
      findrightparenlist.append(findrightparen)
      findrightparen = silver["target_string"].find(")", findrightparen + 1)
    for rightparen in findrightparenlist:
        lenleftparen = len(findleftparenlist)
        if lenleftparen > 0:
          lowervals= [i for i in findleftparenlist if i < rightparen]
          lowervalsort = lowervals.sort(reverse=True)
          toplowerval = lowervals[0]
          startindexlist.append(toplowerval)
          findleftparenlist.remove(toplowerval)
    indexdict = {"startindex": startindexlist, "endindex": findrightparenlist }
    indexdf = pd.DataFrame(indexdict)
    for start, end in zip(indexdf["startindex"], indexdf["endindex"]):
      substring = silverstring[start:end + 1]
      indexdflist.append(substring)
    llave = silver["uniquekey"]  
    listlengthindex = len(indexdflist)
    if listlengthindex > 0: 
      stringarg = indexdflist[listlengthindex - 1]
      substringargreplace = stringarg.replace(",", "#tmpcommaplaceholder")
      removecomma = silverstring.replace(stringarg, substringargreplace)
      platinumdict = {"target_string": removecomma, "uniquekey": llave }
      initlistplatiunum.append(platinumdict)
    else:
      platinumdict = {"target_string": silverstring, "uniquekey": llave }
      initlistplatiunum.append(platinumdict)
  return initlistplatiunum 
    
def splitargs(finalparsedstrings):
  ## todo this function is not used, perhaps deprecate in future
  initlistplatinum = finalparsedstrings
  secondlistsilver = []
  for platinum in initlistplatinum:
    splitstringlist = platinum["target_string"].split(",")
    returnofcomma = [i.replace("#tmpcommaplaceholder", ",") for i in splitstringlist]
    llavesplatinum = platinum["uniquekey"]
    secondsilverdict = {"args": returnofcomma, "uniquekey": llavesplatinum}
    secondlistsilver.append(secondsilverdict)

  golddf = pd.DataFrame(initlistgold)
  silverdf = pd.DataFrame(secondlistsilver)
  finaldf = pd.merge(silverdf, golddf, on="uniquekey")
  return(finaldf)

def splitargstuple(finalparsedstrings, goldenargs, flag, sourcepattern):
  # this function takes the function invocation and creates a tuple based on comma delimter. this allows us to iterate through individual args when creating the replacement strings
  initlistplatinum = finalparsedstrings
  platinumreplace = ''
  secondlistsilver = []
  initlistgold = goldenargs
  initpattern = sourcepattern
  for platinum in initlistplatinum:
    initsq = platinum["target_string"].find("'")
    initdq = platinum["target_string"].find('"')
    commacounter = platinum["target_string"].count(',')
    if initsq == -1 and initdq == -1 :
      if flag == 'syntax':
        platinumparens = "'" + platinum["target_string"] + "'"
      else:
        platinumparens = "'" + platinum["target_string"] + "'"  
      platinumreplace = platinumparens.replace(",", "','")
      if commacounter < 1:
        platinumreplace = platinumreplace + ","
    elif initsq != -1 and initdq == -1:
      if flag == 'syntax':
        platinumparens = '"' + platinum["target_string"] + '"'
      else: 
        platinumparens = '"' + platinum["target_string"] + '"'
      platinumreplace = platinumparens.replace(",", '","')
      if commacounter < 1:
        platinumreplace = platinumreplace + ","
    elif initsq != -1 and initdq != -1 and initsq < initdq:
      if flag == 'syntax':
        platinumparens = '"' + platinum["target_string"] + '"'
      else:
        platinumparens = '"' + platinum["target_string"] + '"'  
      platinumreplace = platinumparens.replace(",", '","')
      if commacounter < 1:
        platinumreplace = platinumreplace + "," 
    elif initdq != -1 and initsq == -1:
      if flag == 'syntax':
        platinumparens = "'" + platinum["target_string"] + "'"
      else:
        platinumparens = "'" + platinum["target_string"] + "'"  
      platinumreplace = platinumparens.replace(",", "','")
      if commacounter < 1:
        platinumreplace = platinumreplace + ","
    elif initdq != -1 and initsq != -1 and initdq < initsq:
      if flag == 'syntax':     
        platinumparens = "'" + platinum["target_string"] + "'"
      else:
        platinumparens = "'" + platinum["target_string"] + "'"  
      platinumreplace = platinumparens.replace(",", "','")
      if commacounter < 1:
        platinumreplace = platinumreplace + ","
    else:
      print('how did we arrive here? red alert!')
    #print(platinumreplace)
    if flag == 'syntax':
      if initpattern == "date_part\\([^)]*?\\)":
        firstcomma = platinumreplace.find(",")
        timearg = platinumreplace[0:firstcomma]
        #print(f" Tiempo is equal to {timearg}")
        timeargquoteflag = timearg.find("'")
        timeargquoteflagdq = timearg.find('"')
        if timeargquoteflag == -1:
          timeargslice = timearg[1:firstcomma - 1]
          timeargquotes = "'" + timeargslice + "'"
          platinumreplace = platinumreplace.replace(timeargslice, timeargquotes)
        elif timeargquoteflagdq == -1:
          timeargslice = timearg[1:firstcomma - 1]
          timeargquotes = '"' + timeargslice + '"'
          platinumreplace = platinumreplace.replace(timeargslice, timeargquotes)
      elif initpattern == "dateadd\\([^)]*?\\)":
        firstcomma = platinumreplace.find(",")
        timeargslice = platinumreplace[0:firstcomma]
        timeargnoquotes = platinumreplace[1:firstcomma-1]
        #platinumreplace = platinumreplace.replace(timeargslice, timeargnoquotes)
      if platinumreplace.find("xmlget") > -1:
        platinumreplace = '"xmlgetplaceholder"'
      platinumreplace = platinumreplace.replace("\n", "")
      platinumreplace = platinumreplace.replace(" ", "")    
      platinumtuple = eval(platinumreplace)
      llavesplatinum = platinum["uniquekey"]
      secondsilverdict = {"args": platinumtuple, "uniquekey": llavesplatinum}
      secondlistsilver.append(secondsilverdict)
    elif flag == 'function':
      ## todo add datapartlogic like above
      llavesplatinum = platinum["uniquekey"]
      secondsilverdict = {"args": platinumreplace, "uniquekey": llavesplatinum}
      secondlistsilver.append(secondsilverdict)
    else:
      print('how did we arrive here? red alert!')    

  golddf = pd.DataFrame(initlistgold)
  silverdf = pd.DataFrame(secondlistsilver)
  finaldf = pd.merge(silverdf, golddf, on="uniquekey")
  return(finaldf)

def finalcountdown(finaldf, contentstring, targetstring):
  # this function iterates through function invocation and their individual args to generate dynamic replacement strings. transpiled strings get outputted.
  updated_content = contentstring
  targetstringlist = []
  for sourcesting, args in zip(finaldf["funcstring"], finaldf["args"]):
    if targetstring == "CASE WHEN lower(#arg0) IN ('year', 'years','y', 'yr', 'yrs') THEN date_trunc('year', #arg1::timestamp)::timestamp WHEN lower(#arg0) IN ('month', 'months', 'mon', 'mons') THEN date_trunc('month', #arg1::timestamp)::timestamp WHEN lower(#arg0) IN ('week', 'weeks', 'w') THEN date_trunc('week', #arg1::timestamp)::timestamp WHEN lower(#arg0) IN ('day', 'days', 'd') THEN date_trunc('day', #arg1::timestamp)::timestamp ELSE NULL END":
      tiempounit = args[0]
      mappingdict = {"quarter": "date_trunc('quarter', #arg1::timestamp)", "quarters": "date_trunc('quarter', #arg1::timestamp)","qtr": "date_trunc('quarter', #arg1::timestamp)", "qtrs": "date_trunc('quarter', #arg1::timestamp)","year": "date_trunc('year', #arg1::timestamp)", "years": "date_trunc('year', #arg1::timestamp)", "y": "date_trunc('year', #arg1::timestamp)", "yr": "date_trunc('year', #arg1::timestamp)", "yrs": "date_trunc('year', #arg1::timestamp)", "month": "date_trunc('month', #arg1::timestamp)", "months": "date_trunc('month', #arg1::timestamp)", "mon": "date_trunc('month', #arg1::timestamp)", "mons": "date_trunc('month', #arg1::timestamp)", "week": "date_trunc('week', #arg1::timestamp)", "weeks": "date_trunc('week', #arg1::timestamp)", "w": "date_trunc('week', #arg1::timestamp)", "day": "date_trunc('day', #arg1::timestamp)", "days": "date_trunc('day', #arg1::timestamp)", "d": "date_trunc('day', #arg1::timestamp)", "hour": "date_trunc('hour', #arg1::timestamp)", "hours": "date_trunc('hour', #arg1::timestamp)", "hr": "date_trunc('hour', #arg1::timestamp)", "hrs": "date_trunc('hour', #arg1::timestamp)", "h": "date_trunc('hour', #arg1::timestamp)", "minute": "date_trunc('minute', #arg1::timestamp)", "minutes": "date_trunc('minute', #arg1::timestamp)", "mins": "date_trunc('minute', #arg1::timestamp)", "min": "date_trunc('minute', #arg1::timestamp)", "m": "date_trunc('minute', #arg1::timestamp)", "second": "date_trunc('second', #arg1::timestamp)", "seconds": "date_trunc('second', #arg1::timestamp)", "secs": "date_trunc('second', #arg1::timestamp)", "sec": "date_trunc('second', #arg1::timestamp)", "s": "date_trunc('second', #arg1::timestamp)", "millisecond": "date_trunc('millisecond', #arg1::timestamp)", "milliseconds": "date_trunc('millisecond', #arg1::timestamp)", "msec": "date_trunc('millisecond', #arg1::timestamp)", "msecs": "date_trunc('millisecond', #arg1::timestamp)", "ms": "date_trunc('millisecond', #arg1::timestamp)" }
      tiempunitnosq = tiempounit.replace("'", "") 
      tiempunitnodq = tiempunitnosq.replace('"','')
      cwval = mappingdict[tiempunitnodq.lower()]
      lastarget = cwval.replace('#arg1', args[1])
      updated_content = updated_content.replace(sourcesting, lastarget)
    elif targetstring == "CASE WHEN lower( '#arg0') IN ('year', 'years','y', 'yr', 'yrs') THEN FLOOR(timestampdiff(YEAR, #arg1::timestamp, #arg2::timestamp) / 1) WHEN lower( '#arg0') IN ('month', 'months', 'mon', 'mons') THEN timestampdiff(MONTH, #arg1::timestamp, #arg2::timestamp)  WHEN lower( '#arg0') IN ('week', 'weeks', 'w') THEN timestampdiff(WEEK, #arg1::timestamp, #arg2::timestamp)   WHEN lower( '#arg0') IN ('day', 'days', 'd') THEN timestampdiff(DAY, #arg1::timestamp, #arg2::timestamp) ELSE NULL END":
      tiempounit = args[0]
      mappingdict = {"quarter": "FLOOR(timestampdiff(quarter, #arg1::timestamp, #arg2::timestamp) / 1)", "quarters": "FLOOR(timestampdiff(quarter, #arg1::timestamp, #arg2::timestamp) / 1)", "qtr": "FLOOR(timestampdiff(quarter, #arg1::timestamp, #arg2::timestamp) / 1)", "qtrs": "FLOOR(timestampdiff(quarter, #arg1::timestamp, #arg2::timestamp) / 1)","year": "FLOOR(timestampdiff(YEAR, #arg1::timestamp, #arg2::timestamp) / 1)", "years": "FLOOR(timestampdiff(YEAR, #arg1::timestamp, #arg2::timestamp) / 1)", "y": "FLOOR(timestampdiff(YEAR, #arg1::timestamp, #arg2::timestamp) / 1)", "yr": "FLOOR(timestampdiff(YEAR, #arg1::timestamp, #arg2::timestamp) / 1)", "yrs": "FLOOR(timestampdiff(YEAR, #arg1::timestamp, #arg2::timestamp) / 1)", "month": "timestampdiff(MONTH, #arg1::timestamp, #arg2::timestamp)", "months": "timestampdiff(MONTH, #arg1::timestamp, #arg2::timestamp)", "mon": "timestampdiff(MONTH, #arg1::timestamp, #arg2::timestamp)", "mons": "timestampdiff(MONTH, #arg1::timestamp, #arg2::timestamp)", "week": "timestampdiff(WEEK, #arg1::timestamp, #arg2::timestamp)", "weeks": "timestampdiff(WEEK, #arg1::timestamp, #arg2::timestamp)", "w": "timestampdiff(WEEK, #arg1::timestamp, #arg2::timestamp)", "day": "timestampdiff(DAY, #arg1::timestamp, #arg2::timestamp)", "days": "timestampdiff(DAY, #arg1::timestamp, #arg2::timestamp)", "d": "timestampdiff(DAY, #arg1::timestamp, #arg2::timestamp)", "hour": "timestampdiff(hour, #arg1::timestamp, #arg2::timestamp)", "hours": "timestampdiff(hour, #arg1::timestamp, #arg2::timestamp)", "hr": "timestampdiff(hour, #arg1::timestamp, #arg2::timestamp)", "hrs": "timestampdiff(hour, #arg1::timestamp, #arg2::timestamp)", "h": "timestampdiff(hour, #arg1::timestamp, #arg2::timestamp)", "minutes": "timestampdiff(minute, #arg1::timestamp, #arg2::timestamp)", "minute": "timestampdiff(minute, #arg1::timestamp, #arg2::timestamp)", "mins": "timestampdiff(minute, #arg1::timestamp, #arg2::timestamp)", "min": "timestampdiff(minute, #arg1::timestamp, #arg2::timestamp)", "m": "timestampdiff(minute, #arg1::timestamp, #arg2::timestamp)", "seconds": "timestampdiff(second, #arg1::timestamp, #arg2::timestamp)", "second": "timestampdiff(second, #arg1::timestamp, #arg2::timestamp)", "secs": "timestampdiff(second, #arg1::timestamp, #arg2::timestamp)", "sec": "timestampdiff(second, #arg1::timestamp, #arg2::timestamp)", "s": "timestampdiff(second, #arg1::timestamp, #arg2::timestamp)", "milliseconds": "timestampdiff(millisecond, #arg1::timestamp, #arg2::timestamp)", "millisecond": "timestampdiff(millisecond, #arg1::timestamp, #arg2::timestamp)", "msecs": "timestampdiff(millisecond, #arg1::timestamp, #arg2::timestamp)", "msec": "timestampdiff(millisecond, #arg1::timestamp, #arg2::timestamp)", "ms": "timestampdiff(millisecond, #arg1::timestamp, #arg2::timestamp)" }
      tiempunitnosq = tiempounit.replace("'", "") 
      tiempunitnodq = tiempunitnosq.replace('"','')
      cwval = mappingdict[tiempunitnodq.lower()]
      putarget = cwval.replace('#arg1', args[1])
      lastarget = putarget.replace('#arg2', args[2])
      updated_content = updated_content.replace(sourcesting, lastarget)
    elif sourcesting.find("xmlget") > -1:
      xmlfunc = "true"
    elif targetstring == "get_json_object(#arg0, #arg1)":
      firstarg = args[0]
      restarg = args[1:]
      newarray = list(restarg)
      jsonpatharg = '.'.join(newarray)
      jsonpathnq = jsonpatharg.replace("'","")
      jsonpathfinal = "$."+ jsonpathnq
      firstargenrich = firstarg.replace('#tmpcommaplaceholder', ",")
      getjsonddl = "get_json_object({}, '{}')".format(firstargenrich, jsonpathfinal)
      updated_content = updated_content.replace(sourcesting, getjsonddl)
    else:    
      targetstringlocal = targetstring
      counter = 0
      for arg in args:
        counterstring = str(counter)
        fullcounter = "#arg"+counterstring
        targetstringlocal = targetstringlocal.replace(fullcounter, arg.replace("#tmpcommaplaceholder", ","))
        counter = counter + 1
        targetstringlist.append(targetstringlocal)
      targetstringlength = len(targetstringlist)
      lastarget = targetstringlist[targetstringlength - 1] 
      updated_content = updated_content.replace(sourcesting, lastarget)
  return(updated_content)    

def finalcountdowndbt(finaldf, contentstring, targetmacroname):

  updated_content = contentstring
  enrichedargs = 'zzzplaceholderzzz'
  for sourcesting, args in zip(finaldf["funcstring"], finaldf["args"]):
    alreadyenriched = updated_content.find(enrichedargs)
    if alreadyenriched == -1: 
      substring = targetmacroname + "("
      lowersubstring = substring.lower()
      lowerargs = args.lower()
      enrichedargs = "{{lakehouse_utils." + lowersubstring + lowerargs + ")}}"
      lenarg = len(lowerargs)
      lastcomma = lowerargs.rfind(",")
      if lowerargs == "'',":
        enrichedargs = "{{lakehouse_utils." + lowersubstring + ")}}"
      elif lenarg == lastcomma + 1:
        nocommarg = lowerargs[0:lenarg - 1]
        enrichedargs = "{{lakehouse_utils." + lowersubstring + nocommarg + ")}}"  
      updated_content = updated_content.replace(sourcesting, enrichedargs)
  return(updated_content)    

## Function to find all sql files within a given directory
def find_files(directory:str, file_type: str, except_list: [str] = []):
    # Convert the input to a Path object
    path = Path(directory)
    if noisylogs == 'true':
      print(f"Path to glob: {path}")

    # Check if the provided path is a directory
    if not path.is_dir():
        raise NotADirectoryError(f"{directory} is not a directory.")

    # List to store all .sql file paths
    files = []

    # Use glob to find all .sql files recursively
    for file in path.rglob('*.{}'.format(file_type)):
        if noisylogs == 'true':
          print(f"File to glob: {file}")
        tmpfilestring = str(file)
        filetypedot = ".{}".format(file_type)
        sourceregex = "\w*\{}".format(filetypedot)
        lenel = len(except_list)
        if len(except_list) > 1:  
          filepath = re.findall(sourceregex, tmpfilestring)
          filepathinit = filepath[0]
          filepathreplace = filepathinit.replace("/", "") 
          if except_list.count(filepathreplace) == 0: 

            if "to_databricks" not in str(file):
              files.append(str(file))
        else:
          if "to_databricks" not in str(file):
            files.append(str(file))    

    ## TEST
    if noisylogs == 'true':
      print(files)

    return files


## Function to convert Snowflake/Redshift functions to dbt macros


def function_to_macroprod(content: str, function_name: dict[str, str]):
  #todo deprecate this function with simpler function_to_marco function

  raw_function_name = function_name.get("source_name")
  target_macro_name = function_name.get("macro_name")

  

  ## Pattern to exclude replacing things inside existing curly braces / macros
  pattern = r'({}\()([^)]*)\)'.format(raw_function_name) #Look for functions of the format name(input1,input2)
  replacement_doubleQuotes = r'{{{{lakehouse_utils.{}("\2")}}}} '.format(target_macro_name) #Surround the expression with double curly braces, and quotes on either end
  
  ## Pattern to exclude replacing things inside existing curly braces / macros
  exclude_curlys_pattern = r'(?<!\{{\{{)\s\S*?({}\()([^)]*)\)\s\S*?(?!\}}\}})'.format(raw_function_name)

  check_preventDoubleReplace_pattern = r'({{lakehouse_utils\.{}\()([^)]*)\)'.format(raw_function_name)
  check_preventInnerReplace_pattern = r'(\w{}\()([^)]*)\)'.format(raw_function_name)

  number_of_matches = len(re.findall(pattern, content, flags=re.IGNORECASE))

  ## TO DO: This assumes there is only 1 function per script - not a good assumption
  # If the function hasn't already been replaced with a macro AND isn't a subpart of another function name, then continue
  if (((re.search(check_preventDoubleReplace_pattern,content, flags=re.IGNORECASE) is None) 
      & (re.search(check_preventInnerReplace_pattern,content, flags=re.IGNORECASE) is None)) 
      | (re.search(exclude_curlys_pattern,content, flags=re.IGNORECASE) is not None)
  ):
    try:

      if (re.search(pattern,content, flags=re.IGNORECASE) is not None):
        
        number_of_matches = len(re.findall(pattern, content, flags=re.IGNORECASE))
      
      else:

        number_of_matches = len(re.findall(pattern, content, flags=re.IGNORECASE))

    except Exception as e:
      number_of_matches = 0

    if (re.search(pattern,content, flags=re.IGNORECASE) is not None):

      updated_content = re.sub(pattern, replacement_doubleQuotes, content, flags=re.IGNORECASE)
    
    else:

      updated_content = re.sub(pattern, replacement_doubleQuotes, content, flags=re.IGNORECASE)
    #print(updated_content)

    matched_patterns = re.findall(pattern,updated_content, flags=re.IGNORECASE) 

    for i in matched_patterns:
      
      # Substitute quotes around inner commas

      commas = r','
      quoted_commas = r'","'
      updated_match = re.sub(commas,quoted_commas,i[1], flags=re.IGNORECASE)
      updated_content = updated_content.replace(i[1], updated_match)

    # If we inadvertently surrounded a double-quoted string with more double-quotes, change these to be single quotes to prevent compatibility issues!

    double_doubleQuotes_pattern = r'""([^"]*)""'
    single_doubleQuotes_pattern = r"""'"\1"'"""
    
    updated_content = re.sub(double_doubleQuotes_pattern,single_doubleQuotes_pattern,updated_content, flags=re.IGNORECASE)

    # If we inadvertently added double-quotes to an empty input macro, remove these!

    accidental_doubleQuotes_pattern = r'({{lakehouse_utils.{}\()""\)'.format(target_macro_name)
    fixed_noQuotes_pattern = r'\1)'
    
    updated_content = re.sub(accidental_doubleQuotes_pattern,fixed_noQuotes_pattern,updated_content, flags=re.IGNORECASE)

    ## If we have multiple instances of the same function, the quotes get strange - '" - fix this

    bad_quotes_pattern_1 = r'(\(\'\"\))'
    bad_quotes_pattern_2 = r'(\(\"\'\))'

    updated_content = re.sub(bad_quotes_pattern_1,r'()',updated_content, flags=re.IGNORECASE)
    updated_content = re.sub(bad_quotes_pattern_2,r'()',updated_content, flags=re.IGNORECASE)

  # If the previous check failed, continue unchanged
  else:
    updated_content = content
    number_of_matches = 0

  return (updated_content, number_of_matches)


def function_to_macrodev(content: str, function_name: dict[str, str]):
  num_matches = 0
  raw_function_name = function_name.get("source_name")
  target_macro_name = function_name.get("macro_name")
  spappend = "\\([^)]*?\\)"
  source_pattern = raw_function_name + spappend

  initargs = findargs(content, source_pattern)
  ## todo add logic to eliminate matches prepended by lakehouseutils 
  num_matches = len(initargs)
  if len(initargs) > 0: 
    stringdelim = parsestrings(initargs)
    parendelim = parseparens(stringdelim)
    gentuple = splitargstuple(parendelim, initargs, "function", source_pattern)
    finalcontent = finalcountdowndbt(gentuple, content, target_macro_name)
    updated_content = finalcontent
  else:
    updated_content = content
  
  return (updated_content, num_matches)

def discovery_parser(content: str, function_name: [str]):
  num_matches = 0
  spappend = "\\([^)]*?\\)"
  source_pattern = function_name + spappend

  initargs = findargs(content, source_pattern)
  ## todo add logic to eliminate matches prepended by lakehouseutils 
  num_matches = len(initargs)
  updated_content = content
  
  return (updated_content, num_matches)  

## Function to convert Snowflake/Redshift functions to dbt macros
def convert_syntax_expressions(content: str, source_pattern: str, target_pattern: str):
  
  ## '(?<!\{{\{{)\s\S*?({}\()([^)]*)\)\s\S*?(?!\}}\}})'
  #exclude_curlys_pattern = r'(?<!lakehouse_utils\.)({})\s*?(?!\}}\}})'.format(source_pattern)

  source_pattern = source_pattern
  target_pattern = target_pattern
  num_matches = 0

  #print(f"SOURCE PATTERN: {source_pattern}")
  #print(f"TARGET PATTERN: {target_pattern}")

  if target_pattern == "\\1 \\2 \\3 NULLS FIRST": 
  
    source_patternng = "ORDER BY[\\w\\s,]+\\bDESC(?=\\s*$|\\s*\\n*)"

    updated_contenttmp = re.sub(source_pattern, target_pattern, content, flags= re.DOTALL | re.IGNORECASE)
    findall = re.findall(source_patternng, updated_contenttmp, flags=re.IGNORECASE)
    num_matches = len(findall)
    updated_content = updated_contenttmp

    for i in findall:
      commas = ","
      commareplace = " NULLS FIRST,"
      updated_match = re.sub(commas,commareplace, i, flags=re.IGNORECASE)
      updated_content = updated_content.replace(i, updated_match)

  elif target_pattern == "\\1 \\2 \\3 NULLS LAST":
    
    source_patternng = "ORDER BY[\\w\\s,]+\\bASC(?=\\s*$|\\s*\\n*)"

    updated_contenttmp = re.sub(source_pattern, target_pattern, content, flags= re.DOTALL | re.IGNORECASE)
    findall = re.findall(source_patternng, updated_contenttmp, flags=re.IGNORECASE)
    num_matches = len(findall)
    updated_content = updated_contenttmp

    for i in findall:
      commas = ","
      commareplace = " NULLS LAST,"
      updated_match = re.sub(commas,commareplace, i, flags=re.IGNORECASE)
      updated_content = updated_content.replace(i, updated_match)
  
  elif target_pattern == "jsonextractpathplaceholderzzz":
    # todo eliminate some of this custom logic
    source_patternuno = "json_extract_path_text\([^)]*\)"
    inputsearchinit = re.findall(source_patternuno, content, flags= re.DOTALL | re.IGNORECASE)
    num_matches = len(inputsearchinit)
    updated_content = content
    for i in inputsearchinit:
      source_patterndos = "(json_extract_path_text\()([^)]*)(\))"
      inputsearchloop = re.search(source_patterndos, i, flags= re.DOTALL | re.IGNORECASE)
      inputargs = inputsearchloop.group(2)
      source_patterninitarg = "([^(]*?)(?=,[\W]*')"
      findinitarg = re.search(source_patterninitarg, inputargs, flags= re.DOTALL | re.IGNORECASE)
      source_patternotherargs = "'[^')]*'|\)"
      findallargs = re.findall(source_patternotherargs, inputargs, flags= re.DOTALL | re.IGNORECASE)
      initarg = findallargs[0]
      initargmatch = findinitarg.group(1)
      if initargmatch == initarg:
        removeinit = findallargs.pop(0)
      jsonpatharg = '.'.join(findallargs)
      jsonpathnq = jsonpatharg.replace("'","")
      jsonpathfinal = "$."+ jsonpathnq
      getjsonddl = "get_json_object({}, '{}')".format(findinitarg.group(1), jsonpathfinal)
      updated_content = updated_content.replace(i, getjsonddl)

  elif source_pattern == 'getdate\\s':
    encontrar = re.findall(source_pattern, content, flags= re.DOTALL | re.IGNORECASE)
    num_matches = len(encontrar)
    updated_content = re.sub(source_pattern, target_pattern, content, flags= re.DOTALL | re.IGNORECASE) 

  elif source_pattern == 'isnull':
    encontrar = re.findall(source_pattern, content, flags= re.DOTALL | re.IGNORECASE)
    num_matches = len(encontrar)
    updated_content = re.sub(source_pattern, target_pattern, content, flags= re.DOTALL | re.IGNORECASE) 

  elif source_pattern == 'getdate\\(\\)':
    encontrar = re.findall(source_pattern, content, flags= re.DOTALL | re.IGNORECASE)
    num_matches = len(encontrar)
    updated_content = re.sub(source_pattern, target_pattern, content, flags= re.DOTALL | re.IGNORECASE) 

  elif source_pattern == "sysdate\\(\\)":
    encontrar = re.findall(source_pattern, content, flags= re.DOTALL | re.IGNORECASE)
    num_matches = len(encontrar)
    updated_content = re.sub(source_pattern, target_pattern, content, flags= re.DOTALL | re.IGNORECASE)

  elif target_pattern == "\\1\\2\\4 \\3 \\5":
    encontrar = re.findall(source_pattern, content, flags= re.DOTALL | re.IGNORECASE)
    num_matches = len(encontrar)
    updated_content = re.sub(source_pattern, target_pattern, content, flags= re.DOTALL | re.IGNORECASE)

  elif target_pattern == "rlike":
    encontrar = re.findall(source_pattern, content, flags= re.DOTALL | re.IGNORECASE)
    num_matches = len(encontrar)
    updated_content = re.sub(source_pattern, target_pattern, content, flags= re.DOTALL | re.IGNORECASE)

  elif target_pattern == "not rlike":
    encontrar = re.findall(source_pattern, content, flags= re.DOTALL | re.IGNORECASE)
    num_matches = len(encontrar)
    updated_content = re.sub(source_pattern, target_pattern, content, flags= re.DOTALL | re.IGNORECASE)

  elif target_pattern == "yyyy-":
    encontrar = re.findall(source_pattern, content)
    num_matches = len(encontrar)
    updated_content = re.sub(source_pattern, target_pattern, content)                 
    
  else:
      initargs = findargs(content, source_pattern)
      num_matches = len(initargs)
      if len(initargs) > 0: 
        stringdelim = parsestrings(initargs)
        #print(silver)
        parendelim = parseparens(stringdelim)
        gentuple = splitargstuple(parendelim, initargs, "syntax", source_pattern)
        finalcontent = finalcountdown(gentuple, content, target_pattern)
        updated_content = finalcontent
      else:
        updated_content = content
    
  return (updated_content, num_matches)



## Function to asynchronously kick off: open each file, loop through every function, write results
## Make new directory for new results
def process_file(discovery_map, full_path: str, function_map: dict[str, dict[str, str]], parse_mode:str = 'functions', syntax_map : {str, str} = {}, parse_first='functions'):

  ## Steps 
  ## 1. If function mode or all mode - process the function conversions first
  ## 2. If syntax or all mode - process the syntax conversions next
  ## 3. If 'all' mode - go back through to find functions after fixing syntax - this is specifically for strange thing like function calls with no parentheses like GETDATE

  converted_functions = dict()
  converted_syntax = dict()
  parsed_discovery = dict()

  #assert (parse_mode in ['functions', 'syntax', 'discovery', 'all'])

  print(f"Converting SQL File: {full_path}")

  ## private Function to convert functions
  def functions_chunk(function_map, content, results_dict = {}):

    ## v2.0.1 - make functions_list a json dict of soure and target names to allow for namespace resolution errors
    functions_list = function_map.keys()

    for function_name in functions_list:

      current_function_map = function_map.get(function_name)

      content, num_matches = function_to_macrodev(content, current_function_map)
      #print(f"NUM MATCHES FOR: {function_name} = {no_matches}")
      if function_name in results_dict:
        results_dict[function_name] += num_matches
      else: 
        results_dict[function_name] = num_matches
        results_dict['full_path'] = full_path

    return content, results_dict
  
  def discovery_chunk(discovery_map, content, results_dict = {}):

    ## v2.0.1 - make functions_list a json dict of soure and target names to allow for namespace resolution errors
    discovery_functions = discovery_map['function_name']

    for func in discovery_functions:

      content, num_matches = discovery_parser(content, func)
      #print(f"NUM MATCHES FOR: {function_name} = {no_matches}")
      if func in results_dict:
        results_dict[func] += num_matches
      else: 
        results_dict[func] = num_matches
        results_dict['full_path'] = full_path

    return content, results_dict    
  ## private Function to convert syntax
  def syntax_chunk(syntax_map, content, results_dict = {}):
    if len(syntax_map.keys()) > 0:
        
        for key, value in syntax_map.items():
            
            #print(f"Parsing syntax mapping: {key}")
            source_pattern = value.get("source_pattern")
            target_pattern = value.get("target_pattern")

            content, num_matches = convert_syntax_expressions(content= content, source_pattern= source_pattern, target_pattern= target_pattern)

            if key in results_dict:
              results_dict[key] += num_matches
            else: 
              results_dict[key] = num_matches
              results_dict['full_path'] = full_path
  
    else:
        print(f"No syntax values to parse: {syntax_map}. Skipping. ")
    
    return content, results_dict 

  def dtchunkuno(content, dtdict):
   for key, value in dtdict.items():
      content = dtconvertuno(content, value.get("source_name"), value.get("target_name"))
   return content   


  def dtchunkdos(content, dtdict):
    for key, value in dtdict.items():
      content = dtconvertdos(content, value.get("source_name"), value.get("target_name"))
    return content 

  def dtconvertuno(content, dtinput, dtoutput):
    cast_pattern = r'(CAST\(\s*[^)]+\s+AS\s+){}(\s*\))'.format(dtinput)
    replacement_pattern = r'\1{}\2'.format(dtoutput)
    updated_content = re.sub(cast_pattern, replacement_pattern, content, flags= re.DOTALL | re.IGNORECASE)  
    return updated_content

  def dtconvertdos(content, dtinput, dtoutput):
    cast_pattern = r'::{}'.format(dtinput)
    replacement_pattern = r'::{}'.format(dtoutput)
    updated_content = re.sub(cast_pattern, replacement_pattern, content, flags= re.DOTALL | re.IGNORECASE)  
    return updated_content     
  
  with open(full_path, 'r+') as file:
    content = file.read()

    if parse_mode in ['functions']:
       content, converted_functions = functions_chunk(function_map=function_map, content=content, results_dict=converted_functions)
    ## Parse and convert syntax nuances with source and target regex expressions from sourcedb/syntax_mappings.json
    elif parse_mode in ['syntax']:
       content, converted_syntax = syntax_chunk(syntax_map=syntax_map, content=content, results_dict=converted_syntax)

    elif parse_mode in ['discovery']:
       content, parsed_discovery = discovery_chunk(discovery_map=discovery_map, content=content, results_dict=parsed_discovery)   
      
    ## If the syntax map changes functions that are recognized, then we need to go back through and check for functions as well
    if parse_mode == 'all':
       
       if parse_first == 'functions':
          content, converted_functions = functions_chunk(function_map=function_map, content=content, results_dict=converted_functions)
          content, converted_syntax = syntax_chunk(syntax_map=syntax_map, content=content, results_dict=converted_syntax)
          content, converted_functions = functions_chunk(function_map=function_map, content=content, results_dict=converted_functions)

       elif parse_first == 'syntax':
          content, converted_syntax = syntax_chunk(syntax_map=syntax_map, content=content, results_dict=converted_syntax)
          content, converted_functions = functions_chunk(function_map=function_map, content=content, results_dict=converted_functions)
       else:
          raise(NotImplementedError(f"Incorrect Parse First Parameter Provided {parse_first}. Shoudl be syntax or functions"))
    
    current_script = Path(__file__).resolve()
    parent_directory = current_script.parent
    file_path = parent_directory / '_resources' / 'config' / sourcedb / 'dt_mappings.json'
    with open(file_path, 'r') as file:
      dtmap = json.load(file)
    contentuno = dtchunkuno(content, dtmap)
    contentdos = dtchunkdos(contentuno, dtmap)
    ## Instead of writing data in place, lets write it to a new model subfolder ./databricks/
    # Write content to the new file

    # Create a Path object from the full path
    if parse_mode == 'discovery':
      #print(parsed_discovery)
      cow = 'moo'

    # Ensure the new directory exists
      #os.makedirs(new_dir, exist_ok=True)

    else: 
      original_path = Path(full_path)

    # Determine the new directory's path
      new_dir = original_path.parent.parent / (original_path.parent.name + "_to_databricks")

    # Ensure the new directory exists
      os.makedirs(new_dir, exist_ok=True)

    # Define the new file path
      new_file_path = new_dir / original_path.name
      with open(new_file_path, 'w') as file:
        file.write(contentdos)

  return (full_path, converted_functions, converted_syntax, parsed_discovery) ## Return list of functions that converted

   

def dbt_project_functions_to_macros(discovery_map, base_project_path: str, input_functions: [str], dir_mode: str, file_type: str, dbtmodelroot : str, except_list: [str] = [], subdirpath: str = '', parse_mode:str = None, syntax_map : {str, str} = {}, parse_first:str=None):
  # Verify we are running in a dbt project

  ### LOCAL VERSION - 2 options - running as a parent project, or running as a package in another project. 
  ## Checks for a parent project first under the following directory assumption: /project_folder/dbt_project.yml.
  ## The package version assumes the utility helper lives under /project_folder/packages/lakehouse_utils/helper/. So it looks 3 levels up for a dbt_project file and uses that as the base directory
  
  if dir_mode == 'dbt':
  
    try:

      dbt_file = base_project_path / 'dbt_project.yml'
      if dbt_file.is_file():
          print("Valid dbt project!")
          print("Converting .sql files in the Models folder...")
      else:
        raise(FileNotFoundError("Cannot find DBT project file. Please check the project structure and run in the correct mode (standalone vs packages.)"))

      paths = []
      if len(except_list) > 0:
        files = find_files(f'{base_project_path}/{dbtmodelroot}/{subdirpath}', "sql", except_list)
      else:
        files = find_files(f'{base_project_path}/{dbtmodelroot}/{subdirpath}', "sql")   
    
    except Exception as e:
      raise(e)    

  else: 
    if len(except_list) > 0:
      files = find_files(subdirpath, file_type, except_list)
    else:
      files = find_files(subdirpath, file_type)  

    
    # List all sql files to be checked in a folder
    ## TBD: Do not parse macros until we can dynamically handle the package/or standalone structure. We dont want to edit and parse the macros that this utility relies on
    #if parsemacro == 'true':  
    #  paths.extend(find_sql_files(f'{base_project_path}/macros'))
  function_array = []
  syntax_array = []
  discovery_array = []
  with ThreadPoolExecutor() as executor:
    futures_sql = {executor.submit(process_file, discovery_map, p, input_functions, parse_mode, syntax_map, parse_first): p for p in files}
    for future in as_completed(futures_sql):
      data = future.result()
      if data:
        if onlypublishagg != 'true':
          print(f"Processed: {data[0]} \n Converted Functions: {data[1]} \n Converted Syntax Mappings: {data[2]}")
        discovery_array.append(data[3])
        function_array.append(data[1])
        syntax_array.append(data[2])
           
      else:
          print(f"Nothing to change: {data}")

  if parse_mode == 'discovery':
    final_disco = discovery_array
    discoverydf = pd.DataFrame(discovery_array)
    print(discoverydf.columns)
    meltdf = discoverydf.melt(id_vars = ['full_path'])
    sumseries = meltdf["value"].sum()
    totaleffort = sumseries / 2
    print(f"Approximate Total effort: {totaleffort} hours")
    current_script = Path(__file__).resolve()
    parent_directory = current_script.parent
    file_path = parent_directory / '_resources' / 'config' / 'snowflake' / 'discoveryparser.csv'
    meltdf.to_csv(file_path, index=False) 

  
  if parse_mode == 'syntax':
    final_syntax = syntax_array
    syntaxdf = pd.DataFrame(syntax_array)
    syntaxmeltdf = syntaxdf.melt(id_vars = ['full_path'])
    current_script = Path(__file__).resolve()
    parent_directory = current_script.parent
    file_path = parent_directory / '_resources' / 'config' / sourcedb / 'syntaxparser.csv'
    syntaxmeltdf.to_csv(file_path, index=False)
  elif parse_mode == 'functions':
    final_syntax = function_array
    functiondf = pd.DataFrame(function_array)
    functionmeltdf = functiondf.melt(id_vars = ['full_path'])
    current_script = Path(__file__).resolve()
    parent_directory = current_script.parent
    file_path = parent_directory / '_resources' / 'config' / sourcedb / 'functionparser.csv'
    functionmeltdf.to_csv(file_path, index=False)
  elif parse_mode == 'all':
    final_syntax = syntax_array
    syntaxdf = pd.DataFrame(syntax_array)
    syntaxmeltdf = syntaxdf.melt(id_vars = ['full_path'])
    current_script = Path(__file__).resolve()
    parent_directory = current_script.parent
    file_path = parent_directory / '_resources' / 'config' / sourcedb / 'syntaxparser.csv'
    syntaxmeltdf.to_csv(file_path, index=False)
    final_syntax = function_array
    functiondf = pd.DataFrame(function_array)
    functionmeltdf = functiondf.melt(id_vars = ['full_path'])
    current_script = Path(__file__).resolve()
    parent_directory = current_script.parent
    file_path = parent_directory / '_resources' / 'config' / sourcedb / 'functionparser.csv'
    functionmeltdf.to_csv(file_path, index=False)              
            

def find_dbt_project_file(start_path: str, run_mode: str = "standalone"):

    """
    This local version has 2 methods of running, it can run as a standalone or as a DBT package in another existing project. 
    1. Package Version - If running as a package, it will traverse the directory and look for the dbt_project.yml file. 
    The package version assumes the utility helper lives under /project_folder/packages/lakehouse_utils/helper/. So it looks 3 levels up for a dbt_project file and uses that as the base directory

    2. Standalone Version - This is more flexible, and simply traverses up the directory from its current point until it finds a dbt_project. This will work if you just add this folder "helper" directly next to your DBT project. 
    """

    assert (run_mode in ["standalone", "package"])

    if run_mode == "standalone":
       
        path = Path(start_path).resolve()

        # Traverse up the directory tree
        while path != path.parent:
            dbt_file = path / 'dbt_project.yml'
            if dbt_file.is_file():
                return path
        
            path = path.parent

        return None
    
    elif run_mode == "package":
       
       try:
            # Create a Path object for the current script and resolve to an absolute path
            current_path = Path(__file__).resolve()
            # Navigate three levels up from ./parent/dbt_packages/lakehouse_utils/helper/convert_to_databricks.py
            three_levels_up = current_path.parents[3]

            # Path of the 'dbt_project.yml' file three levels up
            dbt_project_file = three_levels_up / 'dbt_project.yml'

            # Check if the file exists
            if dbt_project_file.is_file():
                print(f"PROJECT STRUCTURE CHECK: SUCCESS: 'dbt_project.yml' exists at {dbt_project_file}")
                return three_levels_up
            
            else:
                print(f"PROJECT STRUCTURE CHECK: FAIL: 'dbt_project.yml' does not exist at {dbt_project_file}")

            return None
       
       except Exception as e:
        print(f"WARNING: Unable to resolve dbt_project file in parent directory for package mode. Trying to find the dbt_project file anywhere. ")  
        path = Path(start_path).resolve()

        # Traverse up the directory tree
        while path != path.parent:
            dbt_file = path / 'dbt_project.yml'
            if dbt_file.is_file():
                return path

            path = path.parent

        return None
          
          
def find_helper_directory(start_path):

    path = Path(start_path).resolve()

    # Traverse up the directory tree
    while path != path.parent:
        helper_dir = path / 'helper'
        if helper_dir.is_dir():
            # Return the path of the 'helper' directory where the migration package is
            return helper_dir
        path = path.parent

    return None


## Function to load supported functions to convert from config folder
def get_function_map(sourcedb):

    current_script = Path(__file__).resolve()

    parent_directory = current_script.parent

    file_path = parent_directory / '_resources/config' / sourcedb / 'function_mappings.json'
    # Check if the file exists
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as file:
      input_functions_dict = json.load(file)

      return input_functions_dict


## Function to load supported syntax maps to convert from config folder
def get_syntax_map(sourcedb, customdp):

    current_script = Path(__file__).resolve()

    parent_directory = current_script.parent

    file_path = parent_directory / '_resources/config' / sourcedb / 'syntax_mappings.json'
    # Check if the file exists
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as file:
        syntax_map = json.load(file, strict=False)
        if sourcedb == 'redshift':
          if customdp == 'true':
            syntax_map.pop("datepart_to_casewhen")
            syntax_map.pop("datetrunc_to_casewhen")
            syntax_map.pop("datediff_to_casewhen")
            syntax_map.pop("getdate_to_df")
          else:
            syntax_map.pop("customdatepart")
            syntax_map.pop("customdatetrunc")
            syntax_map.pop("customdateadd")
        return syntax_map


#### Main runner
def get_discovery_map(sourcedb):

    current_script = Path(__file__).resolve()

    parent_directory = current_script.parent

    file_path = parent_directory / '_resources' / 'config' / 'snowflake' / 'blockedfunctionlist.csv'
    discovery_map = pd.read_csv(file_path)
    # Check if the file exists
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")


    return discovery_map
    
if __name__ == '__main__':

    def list_of_strings(arg):
      return arg.split(',')

    # Create the parser 
    parser = argparse.ArgumentParser(description='Local DBT to Databricks SQL Tranpiler')

    parser.add_argument("--dir_mode", type=str, default = 'dbt', help='Binary-- select dbt if you are parsing a dbt project, otherwise state anything else such as nondbt')
    parser.add_argument("--sourcedb", type=str, help='The database in which we are converting from - snowflake or redshift')
    parser.add_argument("--dir_path", type=str, default = "", help="If dbt mode, a sub-path under the models folder if you have multiple model folders and only want to convert one. Leave blank if you want all models parsed. If non-dbt mode, include root path that contains all the files you want to be parsed. To indicate files you dont want to be parsed, leverage except list var.")
    parser.add_argument("--parse_mode", type=str, default = 'functions', help = "Flag stating whether to parse for functions, syntax, or all or discovery mode.")
    parser.add_argument("--run_mode", type=str, default = 'standalone', help = "'package' or 'standalone' mode. package mode is running within another DBT project as an import package. standalone is running in a DBT project directly. ")
    parser.add_argument("--output_folder", type=str, default = 'databricks', help = "Name of output directory of converted functions. 'databricks' by default under the models folder. Takes name of source folder and name of target foler to create output folder for each folder.")
    parser.add_argument("--parse_first", type=str, default = 'syntax', help = "parse mode to run first if mode is 'all")
    parser.add_argument("--file_type", type=str, default = 'sql', help = "indicate file type that you want to parse. defaul is sql")
    parser.add_argument("--except_list", type=list_of_strings, default = [str], help = "list of files of file_type under dir_path that you want to exclude from parsing")
    parser.add_argument("--customdp", type=str, default = 'false', help = "set this to true to leverage custom date part target pattern logic")
    parser.add_argument("--noisylogs", type=str, default = 'false', help = "set this to true to output additional logs for debugging")
    parser.add_argument("--tmplogs", type=str, default = 'false', help = "set this to true to output additional tmp logs for debugging")
    parser.add_argument("--dbtmodelroot", type=str, default = 'models', help = "modify this config if dbt model root is not models/ directory")
    parser.add_argument("--onlypublishagg", type=str, default = 'false', help = "modify this config if you want to skip per file print outs and just receive agg summary")

    
    ### Script Arguments
    # Parse arguments
    args = parser.parse_args()

    ## Source Database
    if str(args.sourcedb).lower() not in ["snowflake", "redshift"]:
      raise(Exception("sourcedb must be either snowflake or Redshift"))
    else: 
      sourcedb = str(args.sourcedb).lower()

    ## Sub Model Path (or None)
    if len(args.dir_path) > 1:
      subdirpath = str(args.dir_path)
    else: 
      subdirpath = ""
    
    ## Parse Mode
    if str(args.parse_mode).lower() not in ["functions", "syntax", "all", "discovery"]:
      raise(Exception("ERROR: Parse mode must be 'functions', 'syntax' or 'all' or 'discovery'"))
    else: 
      parse_mode = str(args.parse_mode).lower()
      #print(parse_mode)

    ## Which parse mode to run first
    if str(args.parse_first).lower() not in ["functions", "syntax"]:
      raise(Exception("ERROR: Parse first must be 'functions' or 'syntax'"))
    else: 
      parse_first = str(args.parse_first).lower()

    ## Run as package mode or standalone
    run_mode = args.run_mode
    dir_mode = args.dir_mode
    file_type = args.file_type
    except_list = args.except_list
    customdp = args.customdp
    noisylogs = args.noisylogs
    tmplogs = args.tmplogs
    dbtmodelroot = args.dbtmodelroot
    onlypublishagg = args.onlypublishagg


    if dir_mode == "dbt":
      print(f"\nDBT TRANSPILER: Transpiling to Databricks Macros from {sourcedb} functions... with run mode {run_mode}.\n")
      if len(subdirpath) > 1:
        print(f"Processing only the following model subdirectory {subdirpath}. \n")
      else:
        print(f"Processing all models under models folder. \n")


    # Start from the current script's directory
      project_base_directory = find_dbt_project_file(__file__, run_mode = run_mode)
      if project_base_directory:
        print(f"Found 'dbt_project.yml' in: {project_base_directory}")
        # You can now use base_directory as your base path for further navigation
      else:
        raise("dbt_project.yml not found in any parent directories. Something is wrong with this project setup.")
    else:
       project_base_directory = '' 

    ## Load location of helper directory for library configs
    migration_utility_base_directory = find_helper_directory(__file__)

    if migration_utility_base_directory:
        print(f"Found Migration Utility Folder {migration_utility_base_directory}")
        # You can now use base_directory as your base path for further navigation
    else:
        raise("Migration utility not found in any parent directories. Something is wrong with this project setup.")


    ## Load input functions from lakehouse utils file
    input_functions = get_function_map(sourcedb = sourcedb)
    if noisylogs == 'true':
      print(f"\nConverting the following functions from {sourcedb} to Databricks Dialect: \n {input_functions}")

    discovery_map = get_discovery_map(sourcedb = sourcedb)
    if noisylogs == 'true':
      print(f"\nScanning the files for unsupported snowflake function invocations \n {discovery_map}")  

    ## Load syntax regex mappings
    syntax_map = get_syntax_map(sourcedb= sourcedb, customdp = customdp)
    if noisylogs == 'true':
      print(f"\nConverting the following syntax rules from {sourcedb} to Databricks Dialect: \n {syntax_map}")

    ## Now do project conversion
    dbt_project_functions_to_macros(discovery_map = discovery_map,base_project_path= project_base_directory, 
                                    input_functions= input_functions,
                                    subdirpath= subdirpath, 
                                    parse_mode= parse_mode,
                                    syntax_map= syntax_map,
                                    parse_first= parse_first,
                                    dir_mode = dir_mode,
                                    file_type = file_type,
                                    except_list = except_list,
                                    dbtmodelroot = dbtmodelroot )

