# Funciones extras de la aplicacion users

import random
import string

# Genera un codigo aleatorio
def generar_codigo(size=6, chars=string.ascii_uppercase + string.digits):

    return ''.join(random.choice(chars) for _ in range(size))