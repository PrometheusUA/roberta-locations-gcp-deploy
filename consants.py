import re
import string

# patterns of the regexps
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251" 
    "]+"
)
STREET_PATTERN = re.compile("в?ул(?:\.|иц[я|ю|і|а|е])?|просп(?:\.|ект[у|і|а]?)?")
CITY_VILLAGE_PATTERN = re.compile("сел(?:о|a|і|ом|ищ(?:а|е|у|ем)?(?: міського типу)?)?|смт\.?|міст(?:а|у|і|ом|о)?|пгт\.?|посел(?:ок|ка|ку|ком|ке)?(?: городского типа)?|город(?:а|у|е|ом)?")
DELIMETERS = ['\u200b', '\xa0', ' ', '\n'] # Symbols that are used to separate words
PUNCTUATION = '…»«' + string.punctuation # Punctiation symbols

NAME_WORDS = ['@', 't.me', 'надіслат', "запропонуват", "писат", "підписатис", "чита", "надсилай", 'новин', 'прям']