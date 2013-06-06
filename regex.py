import re

regex = {}

regex['trim'] = re.compile(r"(//|').*$")
regex['directive'] = re.compile(r"^\s*(#\w*)\s*(\w*)")
regex['backslash'] = re.compile(r"(?P<backslash>\\)")
regex['typedot'] = re.compile(r"(\D)(?P<dot>\.)(\D)")
regex['comment_start'] = re.compile(r"(?P<comment_start>/\*)")
regex['comment_end'] = re.compile(r"(?P<comment_end>\*/)")


