from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import json
import random
import ctypes

_libso = ctypes.CDLL('/var/www/sampleapp/sampleapp/_foo.so')


@dajaxice_register
def execeuteCAjax(request):
    dajax = Dajax()
    c_value = _libso.foo()
    dajax.assign('#result', 'value', str(c_value))
    return dajax.json()