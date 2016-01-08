# Voting Information Project Exploration #

## Merging addresses and polling location files ##
This is done by the merge.py script.

Notes - Some rows in the files provided were malformed, I assume this was intentional to replicate real world scenarios. I chose to handle this by kicking out these lines with a warning to fix. A better solution most likely exists. Taking a look at the generation of these input files (if under your control) or a sanitation script/step before running this script may be a smarter option. I created a hardcoded lookup table for precinct/polling ids. This may not be realistic in a real world example, however it seemed like this most straight forward approach here. 

This script absolutely can be improved. Automated testing and error handling is weak or non existant.  

## Generating VIP files from merged file ##
Find generated precinct.txt, polling_location.txt, and precinct_polling_location.txt in root directory of this repo.

This is handled by the gen_VIP_files.py script.

Feeding the resulting file from the merge script into a generate VIP file script we can produce the  resulting precinct.txt, polling_location.txt, and precinct_polling_location.txt. Some assumptions were made as all information wasn't present. Those assumptions are commented in the gen_VIP_files.py script.

This script absolutely can be improved. Automated testing and error handling is weak or non existant.  

## Merging larger address and polling location files##

Merging two tables of the same format with larger input files still would work with the provided merge.py script, up to a point. A file a few hundred thousand lines runs through no problem. As file sizes continued to increase an alternative approach may be needed. (For the sake of this experiment I ran a few million line address file through the script and on my old MBP things finished in a handful of seconds, which was good enough for me for the time being). Splitting up the work on different processes may one option. Another option would be to move from purely flat files to a database or hybrid approach. Since much of this information is relatable, a relational database seems like the right direction, being smart about indexing on proper ids, etc. An important step would be to document and think hard about the structure of tables and connections between them, before they get huge. Since the precinct polling data will be read many times an in-memory database e.g. Redis may be an option worth looking into. Another positive of a database approach would be querying the data to answer specific questions may become more approachable. Sorry, no cave painting this time around, maybe next.


