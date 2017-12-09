import datetime
import os
import sys
import pdfkit

from Enums import OutputFormats
from SubRipSpec import *


class SubRipConverter:

    def __init__(self):
        self.working_directory = './resources/'
        self.output_format = OutputFormats.PLAINTEXT
        self.sentences_per_paragraph = 5
        self.output_file_name = 'result'

    def get_file_list(self):
        files = os.listdir(self.working_directory)
        filtered_list = [f for f in files if f.endswith('.srt')]
        return filtered_list

    @staticmethod
    def sort_if_possible(collection):
        potential_delimiters = ['-', ' ']
        for delimiter in potential_delimiters:
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
                    content_lines.append(line.strip())
        return content_lines

    @staticmethod
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

            if is_first:
                line = line.capitalize()
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

    @staticmethod
    def process_text(line_list, paragraph_size):
        result = ''
        sentence_count = 1
        is_first = True
        current_sentence = ''

        for line in line_list:

            if line.startswith('\0'):
                result += os.linesep + os.linesep
                sentence_count = 0
                is_first = True
                current_sentence = ''
                result += line[1:]
                result += os.linesep + '-----------------' + os.linesep
                continue

            line = line.strip()

            if is_first:
                line = line.capitalize()
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
        if self.output_format == OutputFormats.HTML:
            if not self.output_file_name.endswith('.html'):
                self.output_file_name += '.html'
        if self.output_format == OutputFormats.PDF:
            if not self.output_file_name.endswith('.pdf'):
                self.output_file_name += '.pdf'

            try:
                pdfkit.from_string(content, output_path=self.output_file_name)
            except IOError:
                print "Error creating PDF. Make sure you have wkhtmltopdf installed:" + \
                      " (https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf)"
            sys.exit(2)

        output_file = os.open(self.working_directory + self.output_file_name, os.O_CREAT | os.O_WRONLY)
        for line in content:
            os.write(output_file, line)
        os.close(output_file)

    def main(self, *args):
        start_time = datetime.datetime.now()
        import getopt
        options, values = getopt.getopt(args, 'd:f:o:')
        for opt, val in options:
            if opt == '-d':
                if not val.endswith('/'):
                    val += '/'
                self.working_directory = val
            elif opt == '-f':
                self.output_format = OutputFormats.from_string(val)
            elif opt == '-o':
                self.output_file_name = val

        file_list = self.get_file_list()
        file_list = self.sort_if_possible(file_list)
        content = self.get_all_lines(file_list)
        if self.output_format == OutputFormats.PLAINTEXT:
            content = self.process_text(content, self.sentences_per_paragraph)
        elif self.output_format in [OutputFormats.HTML, OutputFormats.PDF]:
            content = self.process_html(content, self.sentences_per_paragraph)
        elif self.output_format is None:
            print "No valid output format specified, exiting"
            sys.exit(1)

        self.store_content(content)
        end_time = datetime.datetime.now()

        print 'Processed {0} files in {1}ms{2}Output written to {3}'\
            .format(len(file_list), (end_time - start_time).microseconds/1000, os.linesep, self.output_file_name)


if __name__ == "__main__":
    SubRipConverter().main(*sys.argv[1:])
