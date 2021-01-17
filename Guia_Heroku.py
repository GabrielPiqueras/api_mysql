DESPLEGAR UNA APP EN HEROKU

# Una forma es hacerlo a través del CLI de heroku, lo descargo e instalo de aquí:
https://devcenter.heroku.com/

# Inicio sesión:
heroku login

# Al apretar cualquier tecla se abrirá en una ventana del navegador, una vez logueado voy al package.json

package.json
----------------------------------------------------------------------------------------------------------
    "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    # Añado este script tal cual:
        "start": "node ."
    },

    "devDependencies": {
    "nodemon": "^2.0.7"
    },
    # También debo asegurarme que las dependencias formen parte de la APP, no solo para su desarrollo
    "dependencies": {
    "express": "^4.17.1",
    "mysql": "^2.18.1"
    }
----------------------------------------------------------------------------------------------------------

# Creamos la aplicación de Heroku (Si no especifico un nombre Heroku le pondrá uno propio)
heroku create nombreApp

# Nos dirá el nombre junto a la url de nuestra App en heroku

# Para cambiar el nombre de la App:
heroku apps:rename nuevoNombre --app nombreActual

DESPLEGAR LA APP

# Hacemos
git remote -v
# Con esto podremos comprobar nuestros repositorios y si nos fijamos habrá uno para Heroku donde podremos hacer push
# De esta forma subiremos nuestro código de la APP actualizado

# Lo subimos, en heroku despliego mi rama master
git push heroku master

# Ahora si vuelvo a la url de mi App me dará un error, para ello puedo ejecutar los logs (debo estar logueado):
heroku logs --tail


PREPARAR LA APP DE HEROKU QUE SE ENCARGARÁ DE LA BASE DE DATOS:

La base por defecto en Heroku es PostgreSQL, NO MySql.
Asi que crearemos un Addon para nuestra base de datos, usaremos ignite

# Desde la consola de GitBash:
heroku addons:create cleardb:ignite

(Nececesito tener una tarjeta de crédito vinculada a Heroku, aun así, esta APP será gratis)

# Una vez correcto todo hago:
heroku config

# Me devolverá la siguiente url de conexion, que será la que utilizaré en mi App, por ejemplo:
mysql://b3d1aed80d7ff3:db5ce683@us-cdbr-east-03.cleardb.com/heroku_b4585f3fb3fd27f?reconnect=true

# Con eso claro, pasamos esa url al siguiente comando:
heroku config:set DATABASE_URL='miUrlDeConexion'

Con esto hemos asignado la url de conexión a la variable DATABASE_URL

# La url tiene varias partes:
mysql://usuario:contraseña@host?nombreBaseDeDatos

# Esto sería
Usuario: b3d1aed80d7ff3
Contraseña: db5ce683
host: us-cdbr-east-03.cleardb.com
Nombre Base de Datos: heroku_b4585f3fb3fd27f

Extra: ?reconnect=true (para conectarla, supongo)

# Vamos a nuestra app y ponemos estos valores en la configuración de la conexión SQL

const conexion = mysql.createConnection({
    host     : 'us-cdbr-east-03.cleardb.com',
    user     : 'b3d1aed80d7ff3',
    password : 'db5ce683',
    database : 'heroku_b4585f3fb3fd27f'
});

# Ahora tenemos una base de datos creada en una instancia (Addon) de Heroku pero no tenemos una tabla, así que deberemos crearla

Si voy a http://heroku.com > Mi App > Overview

En Installed add-ons entro en el ClearDB MySQL Ignite > How to Use

Me dirá que debo connectarlo con Workbench por ejemplo.

CONEXION REMOTA CON Workbench

Mini-guia: https://desarrollowebtutorial.com/mysql-workbench-configurar-conexion-remota/

1) En el administrador de conexiones creo una nueva.
2) En Connection Method elijo 'Standart TCP/IP'
3) Pongo los datos de configuración como el host, usuario y contraseña.
4) Testeo la conexión y entro en ella.











