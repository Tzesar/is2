#encoding:utf-8
#!/usr/bin/env python
"""
*Es el código que permite interactuar con el proyecto Django.*

*Contiene la especificación de la dirección del archivo de configuración del Proyecto ZARpm*
"""


import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "is2.settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
