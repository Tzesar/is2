#!/bin/bash

# Recolectar todos los archivos estaticos
cd ../
ls
echo "Collecting static files"
django-admin.py collectstatic --noinput --pythonpath='is2/' --settings=is2.settings_produccion

# Borrar los archivos anteriores
echo -e "\nBorrando archivos antiguos"
rm -r /var/www/zarPm/
echo -e "Archivos borrados\n"

# Copiar los archivos al directorio servido por apache2
echo "Copiando archivos"
cp -r ./is2/ /var/www/zarPm/
echo -e "Archivos copiados\n"

echo -e "Configurando Apache"
mv /var/www/zarPm/conf/*.conf /etc/apache2/sites-available/
rm -r /var/www/zarPm/conf
echo -e "Activando los sitios [zarPm] en Apache"
a2ensite zarPm.conf
a2ensite staticZarPm.conf

echo -e "Recargando Apache"
service apache2 reload

echo -e "Fix[sin DNS]: Agrega el nombre y direccion de la pagina a los hosts conocidos de la maquina."
echo "127.0.0.1 zarpm.org" >> /etc/hosts
echo "127.0.0.1 static-zarpm.org" >> /etc/hosts

echo "--Fin--"
