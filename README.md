is2
===

Proyecto de IS2

Para crear la base de datos se debe usar el script 'createDB.sh'.
Para agregar permisos de acceso a la BD al usuario 'zar' agregar la siguiente línea al archivo /etc/postgresql/9.1/main/pg_hba.conf:

  local    zarbd    zar        md5
