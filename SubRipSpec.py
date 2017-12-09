import re

id_num = re.compile('^\d+$')
time_range = re.compile('^[\-\d\s,:>]+$')


def is_id(input_string):
    return id_num.match(input_string.strip()) is not None


def is_time_range(input_string):
    return time_range.match(input_string.strip()) is not None


def is_text(input_string):
    return not is_id(input_string) \
           and not is_time_range(input_string) \
           and not len(input_string.strip()) == 0
