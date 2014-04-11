#!/bin/bash

echo "El password debe ser 'zar' sin las comillas simples. Se pedira dos veces"
echo "Cuando pida una tercera contrasenha se refiere a la del usuario postgres"

createuser -d -l -P -r -S zar -U postgres

if [ $? -ne 0 ]; then
    echo -e "\nSi ocurrio un error del tipo"
    echo -e "\t\t'la autentificaci?n password fall? para el usuario <<postgres>>'"
    echo -e "Recurrir al archivo 'ProblemasConPostgre.txt'"
    exit
fi

echo -e "\n\nUsuario creado con exito."
echo "Ahora se creara la BD con el usuario 'postgres'"
psql -U postgres postgres -f createDB.sql

if [ $? -ne 0 ]; then
    echo "Ha ocurrido un error."
    echo "Si luego de varios intentos no puede arreglarlo consulte a Agu"
    echo "No moleste a Agu si no ha intentado varias soluciones"
fi

exit