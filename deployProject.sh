#!/bin/bash

# Recolectar todos los archivos estaticos
cd ../
echo "----Recolectando archivos del sistema----"
django-admin.py collectstatic --noinput --pythonpath='is2/' --settings=is2.settings_produccion
if [ "$?" -ne 0 ]
then
    echo -e "ERROR: No se pudo recolectar los archivos estaticos"
    exit 1
fi

# Borrar los archivos anteriores
echo -e "\nBorrando archivos antiguos"
rm -r /var/www/zarPm/
if [ "$?" -ne 0 ]
then
    echo -e "ERROR: No se pudieron borrar los archivos del directorio /var/www/zarPm/"
    exit 1
fi
echo -e "Archivos borrados\n"

# TODO: Eliminar al desinstalar la aplicacion
# Copiar los archivos al directorio servido por apache2
echo "Copiando archivos"
cp -r ./is2/ /var/www/zarPm/
if [ "$?" -ne 0 ]
then
    echo -e "ERROR: No se pudo copiar el directorio is2/ a /var/www/zarPm"
    exit 1
fi
chown -R www-data /var/www
if [ "$?" -ne 0 ]
then
    echo -e "ERROR: No se pudo cambiar el duenho del directorio /var/www/zarPm"
    exit 1
fi
chgrp -R www-data /var/www
if [ "$?" -ne 0 ]
then
    echo -e "ERROR: No se pudo cambiar el grupo del directorio /var/www/zarPm"
    exit 1
fi
echo -e "Archivos copiados\n"

# TODO: Eliminar al desinstalar la aplicacion
echo -e "----Configurando Apache----"
mv /var/www/zarPm/conf/*.conf /etc/apache2/sites-available/
if [ "$?" -ne 0 ]
then
    echo -e "ERROR: No se mover los archivos de configuracion desde /var/www/zarPm/conf/ a /etc/apache2/sites-available"
    exit 1
fi
rm -r /var/www/zarPm/conf
if [ "$?" -ne 0 ]
then
    echo -e "ERROR: No se pudo borrar el directorio /var/www/zarPm/conf/"
    exit 1
fi
echo -e "Activando los sitios [zarPm] en Apache"
a2ensite zarPm.conf
if [ "$?" -ne 0 ]
then
    echo -e "ERROR: No se pudo activar el sitio zarPm.conf"
    exit 1
fi
a2ensite staticZarPm.conf
if [ "$?" -ne 0 ]
then
    echo -e "ERROR: No se pudo activar el sitio staticZarPm.conf"
    exit 1
fi

echo -e "Recargando Apache"
service apache2 reload
if [ "$?" -ne 0 ]
then
    echo -e "ERROR: No se pudo recargar el servicio apache2"
    exit 1
fi

# TODO: Verificar si estos datos en /etc/hosts antes de agregarlos, actualmente se agregan cada vez que se ejecuta el archivo
# TODO: Eliminar al desinstalar la aplicacion
echo -e "----Fix[sin DNS]: Agrega el nombre y direccion de la pagina a los hosts conocidos de la maquina.----"
echo "127.0.0.1 zarpm.org" >> /etc/hosts
echo "127.0.0.1 static-zarpm.org" >> /etc/hosts

echo "----Fin----"
exit 0
