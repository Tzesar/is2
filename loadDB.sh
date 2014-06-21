#!/bin/bash

# CODIGOS DE ERROR:
#   1 : ERROR AL BORRAR LA BD DE POSTGRESQL
#   2 : ERROR AL CREAR LA BD EN POSTGRESQL
#   3 : ERROR AL RESTAURAR LOS DATOS DESDE EL ARCHIVO CON LA HERRAMIENTA LOADDATA DE DJANGO

echo -e "Base de datos zarbd [RESTAURANDO]"
echo -e "Borrando la base de datos zarbd antigua"
echo -e "Ingrese la contrasenha del usuario zar"
dropdb -U zar zarbd
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo borrar la base de datos zarbd, verifique que nadie la este usando"
    exit 1
fi
echo -e "Se ha borrado zarbd antigua"

echo -e "Creando la base de datos zarbd"
echo -e "Ingrese la contrasenha del usuario zar"
createdb -U zar zarbd
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo crear la base de datos zarbd"
    exit 2
fi
echo -e "Se ha creado zarbd"

echo -e "Restaurando los datos desde el archivo backupBD.dump"
psql -U zar -d zarbd  -f backupDB.sql

if [ "$?" -ne 0 ]
then
    echo -e "Ocurrio un problema con al cargar los datos a la BD"
    exit 3
fi
echo -e "Base de datos zarbd [RESTAURADA]"

exit 0