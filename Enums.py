class OutputFormats:
    PLAINTEXT = 1
    HTML = 2
    PDF = 3
    LATEX = 4

    @staticmethod
    def from_string(string):
        if string.lower() in ['text', 'plaintext', 'txt']:
            return OutputFormats.PLAINTEXT
        elif string.lower() == 'html':
            return OutputFormats.HTML
        elif string.lower() == 'pdf':
            return OutputFormats.PDF
        elif string.lower() in ['tex', 'latex']:
            print 'LaTeX format not yet supported, switching to HTML instead.'
            return None
        else:
            print 'Output format not recognized, switching to plaintext.'
            return None
