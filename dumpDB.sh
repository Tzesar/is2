#!/bin/bash

echo -e "Creando el archivo backupDB.sql"
pg_dump -U zar zarbd -f backupDB.sql
#django-admin.py dumpdata auth contenttypes messages staticfiles admin django_tables2 floppyforms guardian zar autenticacion administrarUsuarios administrarProyectos administrarFases --pythonpath='./' --settings=is2.settings > backupBD.json

if [ "$?" -ne 0 ]
then
    echo -e "Ocurrio un error al crear la copia de respaldo de la base de datos"
    exit 1
fi
echo -e "Exito, el archivo backupDB.sql fue creado satisfactoriamente"

exit 0