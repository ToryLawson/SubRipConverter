# SubRipConverter
Converts a set of SubRip subtitle files (.srt files) into formatted output. Intended to allow downloading Udacity lecture subtitle sets for offline reading as text.

## Requirements

* Python 2.7 (sorry, I'll fix it up for Python 3 over break)
* [Wkhtmltopdf](https://wkhtmltopdf.org) for PDF generation
* [PDFKit](https://pypi.python.org/pypi/pdfkit) for PDF generation
* Some SRT files to convert

## Quick start
1. Clone the repo
2. Open the SubRipConverter directory at the command line
3. Type `pip install -r requirements.txt` and hit `enter`
4. Type `python main.py` and hit `enter` to see a list of options and their defaults

## Options

`-d <working directory>` Indicates the directory where SubRipConverter should look for .srt files. The default is the current directory.

`-f [txt|html|pdf]` Sets the output format to plaintext, HTML, or PDF, respectively. The default is txt.

`-o <filename>` Sets the file name for the resulting output. This will be placed into the working directory. The default is "output."

`-l <language code>` Sets a value to use in the language filter. Requires that the files contain the string `lang_xx` where `xx` is the language code. Think en, es, ru, etc.

## Tested Udacity courses

This has been tested on / is known to work for these courses:

* CS6250 (CN, Computer Networking)
* CS7641 (ML, Machine Learning)
* CS7646 (ML4T, Machine Learning for Trading)
* CS8803-3 (IOS, Introduction to Operating Systems)
* CS8803-8 (?, Compilers)

If you verify it for other courses, please let me know so I can add to the list.

## Bugs, problems

Please log any issues to the issues board, and especially let me know if the conversion doesn't work properly for a given course.
