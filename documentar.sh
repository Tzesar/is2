#!/bin/bash

# Verifica si existe la configuracion del sphinx
if [ ! -f docs/conf.py ]; then
    echo "Configure Sphinx con Pycharm siguiendo los pasos del archivo Sphinx.txt"
    exit
fi

# Crear archivos .rst sobre los modulos
echo "Creando .rst"
sphinx-apidoc  -o docs/ .

# Cambiar el titulo del archivo modules.rst
cd docs/
echo -e "\nArreglando 'modules.rst'."
sed -i.bak s/^'\.'$/Modulos/ modules.rst
sed -i.bak s/^=$/========/ modules.rst

# Crear los archivos html
echo -e "Creando archivos html\n"
make html

echo "Mostramos la documentacion actual"
cd ..
firefox docs/_build/html/index.html &
if [ $? -ne 0 ]; then
    firefox docs/_build/html/index.html &
fi