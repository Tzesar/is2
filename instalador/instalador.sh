#! /bin/bash

#Definimos las variables del programa
#Establecemos la ruta de instalacion del programa
rutainstalacion="/home/ZAR/is2_git/is2_git"

#Establecemos al usuario Administrador para la Base de Datos
usuario='admin'
password='admin'

#Definimos la ruta del instalador
rutainstalador=`pwd`

#Localizacion del codigo fuente del proyecto
#fuente="https://github.com/Tzesar/is2/archive/master.zip"

#echo "Bienvenido a la Instalación del Programa ZAR Project Manager. Favor ingrese la versión que desea descargar"
#if read -t 10 -p "Version:" var1; then
#	if [ $var1 = "1" ]; then
#		echo "Usted ha seleccionado la versión 1.0"
#		fuente="https://github.com/Tzesar/is2/archive/Iteracion_1.zip"
#	elif [ $var1 = "2" ]; then
#		echo "Usted ha seleccionado la versión 2.0"
#		fuente="https://github.com/Tzesar/is2/archive/Iteracion_2.zip"
#	elif [ $var1 = "3" ]; then
#		echo "Usted ha seleccionado la versión 3.0"
#		fuente="https://github.com/Tzesar/is2/archive/Iteracion_3.zip"
#	elif [ $var1 = "4" ]; then
#		echo "Usted ha seleccionado la versión 4.0"
#		fuente="https://github.com/Tzesar/is2/archive/master.zip"
#	else
#		echo "Lo sentimos la versión que ha especificado no existe o ha sido declarada obsoleta"
#		echo "Favor introduzca una versión disponible. Las versions disponibles son: [1.0; 2.0; 3.0; 4.0; 5.0]"
#		echo "Disculpe las molestias"
#	fi
#else
#	echo "Tiempo de espera superado se instalará la versión más reciente del programa" 
#	fuente="https://github.com/Tzesar/is2/archive/Iteracion_4.zip"
#fi

clear
while true
    echo "Bienvenido a la Instalación del Programa ZAR Project Manager."
    echo "Favor ingrese la versión que desea descargar."

    do
    PS3='Favor introzca la versión que desea descargar: '
    options=(   "Versión 1.0" 
                "Versión 2.0" 
                "Versión 3.0" 
                "Versión 4.0" 
                "Versión 5.0" 
                "Salir"  )

    select opt in "${options[@]}" 
    do
        case $opt in
            "Versión 1.0")
                echo "Usted ha seleccionado la versión 1.0"
                archivo="is2-Iteracion_1"
                fuente="https://github.com/Tzesar/is2/archive/Iteracion_1.zip"
                break
                ;;
            "Versión 2.0")
                echo "Usted ha seleccionado la versión 2.0"
                archivo="is2-Iteracion_2"
                fuente="https://github.com/Tzesar/is2/archive/Iteracion_2.zip"
                break
                ;;
            "Versión 3.0")
                echo "Usted ha seleccionado la versión 3.0"
                archivo="is2-Iteracion_3"
                fuente="https://github.com/Tzesar/is2/archive/Iteracion_3.zip"
                break
                ;;
            "Versión 4.0")
                echo "Usted ha seleccionado la versión 4.0"
                archivo="is2-Iteracion_4"
                fuente="https://github.com/Tzesar/is2/archive/Iteracion_4.zip"
                break
                ;;
            "Versión 5.0")
                echo "Usted ha seleccionado la versión 5.0"
                archivo="is2-Iteracion_4"
                fuente="https://github.com/Tzesar/is2/archive/Iteracion_5.zip"
                break
                ;;
            "Salir")
                echo "Saliendo del Instalador"
                sleep 1                 
                exit
                ;;
            *) echo "Lo sentimos la versión que ha especificado no existe."
               echo "Favor introduzca una versión disponible. Disculpe las molestias";;
        esac
    done
    break
done
clear

#Verificamos los paquetes instalados actualmente en el sistema
sudo apt-get install apt-show-versions
apt-show-versions > instalados.txt

if [ ! -d "$rutainstalacion" ];
	then
	echo "###### LA RUTA DE INSTALACION NO EXISTE, SE CREARA EL EL DIRECTORIO EN LA RUTA ESPECIFICADA ######"
	mkdir -p "$rutainstalacion"
fi

echo "###### INICIANDO LA INSTALACION DEL SISTEMA ZAR project manager (ZARpm) ######"
# Para este proceso verificamos la existencia de los paquetes en el sistema para instalarlos si es necesario
# Instalamos python 2.7.4
instalado=`grep python2.7 instalados.txt`
if [ -n "$instalado" ];
	then
	echo "python2.7 ya esta instalado"
else
	echo "Instalamos python2.7..."
	cd paquetes
	tar -Jxf Python-2.7.4.tar.xz
	cd Python-2.7.4
	./configure
	make
	make install
	cd ..
	rm -rf Python-2.7.4
	cd ..
fi

#python-setuptools
instalado=`grep python-setuptools instalados.txt`
if [ -n "$instalado" ];
	then
	echo "la libreria python-setuptools ya esta instalada"
else
	echo "Instalamos la libreria python-setuptools"
	apt-get -y install python-setuptools
fi

#python-dev
instalado=`grep python-dev instalados.txt`
if [ -n "$instalado" ];
	then
	echo "la libreria python-dev ya esta instalada"
else
	echo "Instalamos la libreria python-dev"
	apt-get install -y python-dev
fi


#Django
if [ -d /usr/local/lib/python2.7/dist-packages/django ];
	then
	echo "Django ya esta instalado"
else
	#Instalamos el framework Django
	echo "Instalamos el framework Django"
	cd paquetes
	tar xzvf Django-1.6.2.tar.gz
	cd Django-1.6.2
	python setup.py install
	cd ..
	rm -rf Django-1.6.2
	cd ..
fi

#Django - sphinx-rtd-theme
if [ -d /usr/local/lib/python2.7/dist-packages/sphinx_rtd_theme ];
	then
	echo "sphinx-rtd-theme ya esta instalado"
else
	#Instalamos el framework Django
	echo "Instalamos el sphinx-rtd-theme"
	sudo pip intall sphinx-rtd-theme
fi

#Django - floppyforms
if [ -d /usr/local/lib/python2.7/dist-packages/floppyforms ];
	then
	echo "sphinx-rtd-theme ya esta instalado"
else
	#Instalamos el framework Django
	echo "Instalamos el Django-floppyforms"
	pip install django-floppyforms
fi

#Django - filter
if [ -d /usr/local/lib/python2.7/dist-packages/django_filters ];
	then
	echo "sphinx-rtd-theme ya esta instalado"
else
	#Instalamos el framework Django
	echo "Instalamos el Django-floppyforms"
	pip install django-filter
fi

#Django - Tables2
if [ -d /usr/local/lib/python2.7/dist-packages/django_tables2 ];
	then
	echo "sphinx-rtd-theme ya esta instalado"
else
	#Instalamos el framework Django
	echo "Instalamos el django-tables2"
	sudo pip intall django-tables2
fi


#Django - Guardian
if [ -d /usr/local/lib/python2.7/dist-packages/guardian ];
	then
	echo "sphinx-rtd-theme ya esta instalado"
else
	#Instalamos el framework Django
	echo "Instalamos Django-guardian"
	sudo pip install django-guardian
fi

#Django - Reversion
if [ -d /usr/local/lib/python2.7/dist-packages/reversion ];
	then
	echo "Django-reversion ya esta instalado"
else
	#Instalamos el framework Django-revision
	echo "Instalamos la aplicacion Django-reversion"
	apt-get -y install django-reversion
fi


#Python - PyDot
instalado=`grep pydot instalados.txt`
if [ -n "$instalado" ];
	then
	echo "Python - PyDot ya esta instalado"
else
	echo "Instalamos Python-PyDot"
	apt-get -y install Python-Pydot
fi


#Apache2
instalado=`grep apache2 instalados.txt`
if [ -n "$instalado" ];
	then
	echo "apache2 ya esta instalado"
else
	echo "Instalamos apache2"
	apt-get -y install apache2
fi


#libapache2
instalado=`grep libapache2 instalados.txt`
if [ -n "$instalado" ];
	then
	echo "la libreria libapache2 ya esta instalada"
else
	echo "Instalamos la libreria libapache2"
	apt-get -y install libapache2-mod-wsgi
fi



# intalamos html5lib-0.90
if [ -d /usr/local/lib/python2.7/dist-packages/html5lib-0.90-py2.7.egg ];
	then
	echo "html5lib-0.90 ya esta instalado"
else
	echo "Instalamos html5lib-0.90..."
	cd paquetes
	tar xzvf html5lib-0.90.tar.gz
	cd html5lib-0.90
	python setup.py install
	cd ..
	rm -rf html5lib-0.90
	cd ..
fi

# instalamos reportlab
instalado=`grep reportlab instalados.txt`
if [ -n "$instalado" ];
	then
	echo "la libreria reportlab ya esta instalada"
else
	echo "Instalamos reportlab..."
	cd paquetes
	tar xzvf reportlab-3.1.8.tar.gz
	cd reportlab-3.1.8
	python setup.py install
	cd ..
	rm -rf reportlab-3.1.8
	cd ..
fi


#unipath
if [ -d /usr/local/lib/python2.7/dist-packages/unipath ];
	then
	echo "unipath ya esta instalado"
else
	#instalamos el framework Django
	echo "Instalamos la libreria unipath"
	cd paquetes
	tar xzvf Unipath-1.0.tar.gz
	cd Unipath-1.0
	python setup.py install
	cd ..
	rm -rf Unipath-1.0
fi


# instalamos PIL
if [ -d /usr/local/lib/python2.7/dist-packages/PIL ];
	then
	echo "PIL ya esta instalado"
else
	echo "Instalamos PIL..."
	cd paquetes
	tar xzvf Imaging-1.1.7.tar.gz
	cd Imaging-1.1.7
	python setup.py install
	cd ..
	rm -rf Imaging-1.1.7
	cd ..
fi

# instalamos pyPdf
if [ -d /usr/local/lib/python2.7/dist-packages/pyPdf ];
	then
	echo "pyPdf ya esta instalado"
else
	echo "Instalamos pyPdf..."
	cd paquetes
	tar xzvf pyPdf-1.10.tar.gz
	cd pyPdf-1.10
	python setup.py install
	cd ..
	rm -rf pyPdf-1.10
	cd ..
fi

# finalmente instalamos pisa
if [ -d /usr/local/lib/python2.7/dist-packages/pisa-3.0.33-py2.7.egg ];
	then
	echo "pisa ya esta instalado"
else
	echo "Instalamos pisa..."
	cd paquetes
	tar xzvf pisa-3.0.33.tar.gz
	cd pisa-3.0.33
	python setup.py install
	cd ..
	rm -rf pisa-3.0.33
	cd ..
fi


#Instalamos el proyecto
if [ -d "$rutainstalacion/ZAR" ];
	then
	echo "El proyecto ya se encuentra instalado"
else 
	if [ ! -d proyecto ];
		then
		wget "$fuente" -P proyecto
	fi
	cd proyecto
	unzip $archivo
	cd archivo
	#unzip master.zip
	#cd is2-master
	mv * "$rutainstalacion"
	cd "$rutainstalacion"
	chown zar zar README.md
	chmod -R 777 zar
	chmod -R 777 is2
#	cd ..
#	cd is2/static
#	chmod -R a+w archivos
#	chmod -R a+w grafos
	cd "$rutainstalador"
	rm -rf proyecto
	wsgi_conf="yes"
fi


#postgresql
instalado=`grep postgresql instalados.txt`
if [ -n "$instalado" ];
	then
	echo "postgresql ya esta instalado"
else
	echo "Instalamos postgresql..."
	apt-get -y install postgresql postgresql-client postgresql-contrib

	#python-psycopg2
	instalado=`grep python-psycopg2 instalados.txt`
	if [ -n "$instalado" ];
		then
		echo "python-psycopg2 ya esta instalado"
	else
		echo "Instalamos python-psycopg2..."
		apt-get -y install python-psycopg2
	fi
fi

	echo "Operaciones sobre la Base de Datos"
	echo "Favor introduza la contraseña del usuario postgres"
	echo "ALTER USER postgres WITH PASSWORD 'postgres';" > comandos.sql
	echo "\q" >> comandos.sql
	sudo -u postgres psql postgres -a -f comandos.sql
	sudo -u postgres createuser --superuser admin
	echo "Contraseña establecida 'postgres' para el usuario 'postgres'"
	echo "Favor introduza la contraseña del usuario postgres para establecer una nueva contraseña para el Super Usuario"
	echo "ALTER USER "$usuario" WITH PASSWORD '"$password"';" > comandos.sql
	echo "\q" >> comandos.sql
	sudo -u postgres psql -a -f comandos.sql
	sudo -u postgres createuser -d -a zar
	echo "Favor introduza la contraseña del usuario postgres par establecer una nueva contraseña para el zar"
	echo "ALTER USER zar WITH PASSWORD 'zar';" > comandos.sql
	echo "\q" >> comandos.sql
	sudo -u postgres psql -a -f comandos.sql
	sudo -u postgres createdb zarbd -O zar
	#Insertar aqui el script que carga la base de datos
	echo "Fin de las Operaciones sobre la Base de Datos"
	rm comandos.sql
	python syncdb.py	

rm instalados.txt

echo "###### INSTALACION FINALIZADA ######"