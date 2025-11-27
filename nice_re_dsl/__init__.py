from .app import Elem, Group, CharSet, ProcessedElem
from .app import WordBoundary, NonWordBoundary
from .app import Op
from .app import Regexp
from .app import CSRange

ANY_CHAR = ProcessedElem('.')
NEWLINE = ProcessedElem(r'\n')
TAB = ProcessedElem(r'\t')
SPACE = ProcessedElem(r'\s')
NON_SPACE = ProcessedElem(r'\S')
LETTER_NUM_UNDERLINE = ProcessedElem(r'\w')
NON_LETTER_NUM_UNDERLINE = ProcessedElem(r'\W')
NUMBER = ProcessedElem(r'\d')
NON_NUMBER = ProcessedElem(r'\D')

a2z = CSRange('a', 'z')
A2Z = CSRange('A', 'Z')
zero2nine = CSRange('0', '9')
a2z_A2Z_029 = CSRange('A', 'Z') + CSRange('a', 'z') + CSRange('0', '9')
a2z_A2Z = CSRange('A', 'Z') + CSRange('a', 'z')
