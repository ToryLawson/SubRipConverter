import datetime
import os
import sys
import pdfkit

from Enums import OutputFormats
from SubRipSpec import *


class SubRipConverter:

    def __init__(self):
        self.working_directory = './'
        self.output_format = OutputFormats.PLAINTEXT
        self.sentences_per_paragraph = 5
        self.output_file_name = 'output'
        self.language = None

    def get_file_list(self):
        files = os.listdir(self.working_directory)
        if self.language is not None:
            filtered_list = [f for f in files if f.endswith('.srt') and 'lang_' + self.language in f]
        else:
            filtered_list = [f for f in files if f.endswith('.srt')]
        return filtered_list

    @staticmethod
    def sort_if_possible(collection):
        potential_delimiters = ['-', ' ']
        for delimiter in potential_delimiters:
            if collection is None or len(collection) == 0:
                print "No files found in specified location, exiting"
                exit(1)
            test = collection[0].split(delimiter)[0]
            if test.strip().isdigit():
                collection.sort(key=lambda fn: int(fn.split(delimiter)[0]))
                break
        return collection

    @staticmethod
    def get_title_from_file_name(input_string):
        title = input_string.split('.srt')[0]
        title = title.lstrip('0123456789- ')
        lang_suffix = re.compile('(\.[a-z]_[A-Z]$)|( - lang_.*$)')
        title = re.sub(lang_suffix, '', title)
        title = title.replace('_ ', ': ')
        if title.endswith('_'):
            title = title[:-1] + '?'
        return '\0' + title

    def get_all_lines(self, file_names):
        content_lines = []
        for file_name in file_names:
            content_lines.append(self.get_title_from_file_name(file_name))
            curr_file = open(self.working_directory + file_name)
            for line in curr_file:
                if is_text(line):
                    content_lines.append(line.strip().decode('utf-8'))
        return content_lines

    @staticmethod
    def process_text(line_list, paragraph_size):
        result = ''
        sentence_count = 1
        is_first = True
        current_sentence = ''

        for line in line_list:

            line = line.strip()

            if line.startswith('\0'):
                result += os.linesep + os.linesep
                sentence_count = 0
                is_first = True
                current_sentence = ''
                result += line[1:]
                result += os.linesep + '-----------------' + os.linesep
                continue

            if line.startswith('>>'):
                result += current_sentence
                current_sentence += os.linesep + ">> " + line[2:].strip()[0].upper() + line[2:].strip()[1:]
                sentence_count = 1
                if line.endswith(tuple(['.', '!', '?'])):
                    result += current_sentence
                    current_sentence = ''
                    sentence_count += 1
                    is_first = True
                else:
                    is_first = False
                continue

            if is_first:
                line = line[0].upper() + line[1:]
                is_first = False

            current_sentence += ' ' + line

            if sentence_count >= paragraph_size and not current_sentence.strip().startswith('And'):
                sentence_count = 0
                result += os.linesep + os.linesep

            if line.endswith(tuple(['.', '!', '?'])):
                result += current_sentence
                current_sentence = ''
                sentence_count += 1
                is_first = True
        return result

    def store_content(self, content):
        if self.output_format == OutputFormats.PLAINTEXT:
            if not self.output_file_name.endswith('.txt'):
                self.output_file_name += '.txt'

        if self.output_format == OutputFormats.HTML:
            if not self.output_file_name.endswith('.html'):
                self.output_file_name += '.html'

        if self.output_format == OutputFormats.PDF:
            if not self.output_file_name.endswith('.pdf'):
                self.output_file_name += '.pdf'

            try:
                pdfkit.from_string(content, output_path=self.working_directory + self.output_file_name)
            except IOError:
                print "Error creating PDF. Make sure you have wkhtmltopdf installed:" + \
                      " (https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf)"
                sys.exit(2)
        else:
            output_file = open(self.working_directory + self.output_file_name, 'a+')
            output_file.seek(0)
            output_file.truncate()
            for line in content:
                output_file.write(line)
            output_file.close()

    def main(self, *args):
        start_time = datetime.datetime.now()
        import getopt
        options, values = getopt.getopt(args, 'd:f:o:l:')
        options_flag = 0

        for opt, val in options:
            if opt == '-d':
                if not val.endswith(os.sep):
                    val += os.sep
                self.working_directory = val
                options_flag += 1
            elif opt == '-f':
                self.output_format = OutputFormats.from_string(val)
                options_flag += 2
            elif opt == '-o':
                self.output_file_name = val
                options_flag += 4
            elif opt == '-l':
                self.language = val
                options_flag += 8

        if not options_flag & 1:
            print "Missing working directory option (-d <working directory>);"
            print "  defaulting to current directory"
        if not options_flag & 2:
            print "Missing format option (-f [txt|html|pdf]);"
            print "  defaulting to plaintext format"
        if not options_flag & 4:
            print "Missing output file name option (-o <name>);"
            print "  defaulting to 'output'"
        if not options_flag & 8:
            print "No language specified. If your output contains multiple languages," \
                  " add a language filter (-l [en|fr|es|etc.])"

        file_list = self.get_file_list()
        file_list = self.sort_if_possible(file_list)
        content = self.get_all_lines(file_list)
        if self.output_format == OutputFormats.PLAINTEXT:
            content = self.process_text(content, self.sentences_per_paragraph)
        elif self.output_format in [OutputFormats.HTML, OutputFormats.PDF]:
            content = process_html(content, self.sentences_per_paragraph)
        elif self.output_format is None:
            print "No valid output format specified, exiting"
            sys.exit(1)

        self.store_content(content)
        end_time = datetime.datetime.now()

        print 'Processed {0} files in {1}ms{2}Output written to {3}'\
            .format(len(file_list), (end_time - start_time).microseconds/1000,
                    os.linesep, self.working_directory + self.output_file_name)


def process_html(line_list, paragraph_size):
    header = '<!doctype html>' + os.linesep + '<html><head></head><body>'
    footer = '</body></html>'
    body = ''
    sentence_count = 1
    is_first = True
    current_sentence = ''

    for line in line_list:

        if line.startswith('\0'):
            if not body.strip().endswith('</p>') and len(body) > 0:
                body += '</p>' + os.linesep
            body += os.linesep + os.linesep
            sentence_count = 0
            is_first = True
            current_sentence = ''
            body += '<h3>' + line[1:] + '</h3>' + os.linesep
            body += '<p>' + os.linesep
            continue

        line = line.strip()

        if line.startswith('>>'):
            body += current_sentence
            current_sentence += "<br \>" + "&gt;&gt; " + line[2:].strip()[0].upper() + line[2:].strip()[1:]
            sentence_count = 1
            if line.endswith(tuple(['.', '!', '?'])):
                body += current_sentence
                current_sentence = ''
                sentence_count += 1
                is_first = True
            else:
                is_first = False
            continue

        if is_first:
            line = line[0].upper() + line[1:]
            is_first = False

        current_sentence += ' ' + line

        if sentence_count >= paragraph_size and not current_sentence.strip().startswith('And'):
            sentence_count = 0
            body += '</p>' + os.linesep + '<p>'

        if line.endswith(tuple(['.', '!', '?'])):
            body += current_sentence
            current_sentence = ''
            sentence_count += 1
            is_first = True

    if not body.strip().endswith('</p>'):
        body += '</p>' + os.linesep
    return header + body + footer


if __name__ == "__main__":
    SubRipConverter().main(*sys.argv[1:])
