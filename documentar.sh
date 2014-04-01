#!/bin/bash

# Crear archivos .rst sobre los modulos
echo "Creando .rst"
sphinx-apidoc -f -o docs/ .

# Cambiar el titulo del archivo modules.rst
cd docs/
echo "Arreglando 'modules.rst'."
sed -i.bak s/^'\.'$/Packages/ modules.rst
sed -i.bak s/^=$/========/ modules.rst


# Crear los archivos html
echo "Creando archivos html"
make html
