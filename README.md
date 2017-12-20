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
