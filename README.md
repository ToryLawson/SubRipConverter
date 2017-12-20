# SubRipConverter
Converts a set of SubRip subtitle files (.srt files) into formatted output. Intended to allow downloading Udacity lecture subtitle sets for offline reading as text.

## Quick start
1. Clone the repo
2. Open the SubRipConverter directory at the command line
3. Type `pip install -r requirements.txt` and hit `enter`
4. Type `python main.py` and hit `enter` to see a list of options and their defaults

## Options

`-d <working directory>` Indicates the directory where SubRipConverter should look for .srt files. The default is the current directory. 

`-f [txt|html|pdf]` Sets the output format to plaintext, HTML, or PDF, respectively. The default is txt. 

`-o <filename>` Sets the file name for the resulting output. This will be placed into the working directory. The default is "output." 

## Tested courses

This has been tested on and is known to work for these courses:

* CS6250 (CN, Computer Networking) 
* CS7646 (ML4T, Machine Learning for Trading)
* CS8803-3 (IOS, Introduction to Operating Systems)
* CS8803-8 (?, Compilers)

If you verify it for other courses, please let me know so I can add to the list.

## Bugs, problems

Please log any issues to the issues board, and especially let me know if the conversion doesn't work properly for a given course.
