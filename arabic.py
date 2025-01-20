from bidi.algorithm import get_display
from arabic_reshaper import reshape
def convert(txt):
    text=reshape(txt)
    arabic_text=get_display(text)
    return arabic_text