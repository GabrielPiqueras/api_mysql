const express = require('express');
const mysql = require('mysql');

// El puerto será el de nuestro hosting, y si no el que queramos en local: 3050
const PUERTO = process.env.PUERTO || 3050;

// Creo una instancia de express
const app = express();

// Le decimos que use express.json(), que está basado e bodyParser, de esta forma podemos enviar información en JSON si lo necesitamos.
// Nota: Para enviar JSON desde Postman activar la pestaña 'Body' > raw > Y cambiar a JSON en la derecha
app.use(express.json());

// MySql - Configuro la conexión
const conexion = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'api_mysql'
});

// Ruta para probar a renderizar algo
app.get('/', (req, res) => {
    res.send('Bienvenido a mi API!')
})

// Obtener todos los usuarios
app.get('/usuarios', (req, res) => {

    // Creo mi consulta
    const sql = "SELECT * FROM usuarios"

    // La ejecuto
    conexion.query(sql, (error, results) => {
        // Si hay un error, lo muestro
        if (error) { throw error }

        // Si hay más de un registro, los devuelvo en formato json
        if (results.length > 0) {
            res.json(results)
        } else {
            res.send('No se obtuvo ningún resultado')
        }
    })
});

app.get('/usuarios/:id', (req, res) => {
    // Extraigo mi parámetro id del objeto params
    const { id } = req.params

    // Creo mi consulta, la ejecuto y manejo errores
    const sql = `SELECT * FROM usuarios WHERE id=${id}`
    
    conexion.query(sql, (error, result) => {
        if (error) { throw error }

        if (result.length > 0) {
            res.json(result)
        } else {
            res.send('No se obtuvo ningún resultado')
        }
    })
});

// Añadir un usuario
app.post('/add', (req, res) => {
    // Pongo SET ? en vez de VALUES() 
    const sql = `INSERT INTO usuarios SET ?`

    // Esto es para obtener la fecha y hora actual
    const fechaHora = { toSqlString: function() { return 'CURRENT_TIMESTAMP()'; } };

    // Porque eso me permitirá pasar este objeto a la query
    // Las claves deben llamarse como los nombres de las columnas en la BDD
    // El método json() de express me permite en la petición recibir información extra que yo quiera en formato JSON con estas claves:
    const objUsuario = {
        nombre: req.body.nombre,
        edad: req.body.edad,
        alta: fechaHora
    }

    // Ejecuto pasando el objeto con los datos que completarán la consulta 
    conexion.query(sql, objUsuario, error => {
        if (error) {
            throw error
        } else {
            res.send('Usuario añadido correctamente.')
        }
    })
});

// Editar un usuario
app.put('/editar/:id', (req, res) => {

    const { id } = req.params

    // Nombres de las claves del JSON pasado en la petición, gracias al express.json() de arriba las puedo obtener
    const { nombre, edad } = req.body

    // En este caso, las variables que se usan el set deben ir entre comillas simples.
    const sql = `UPDATE usuarios SET nombre = '${nombre}', edad = '${edad}' WHERE id = ${id}`

    conexion.query(sql, (error) => {
        if (error) {
            throw error
        } else {
            res.send('El usuario se editó correctamente.')
        }
    })
});

// Borrar un usuario
app.delete('/borrar/:id', (req, res) => {
    
    const { id } = req.params
    sql = `DELETE FROM usuarios WHERE id = ${id}`

    conexion.query(sql, (error, result) => {
        if (error) {
            throw error
        } else {
            res.send('Usuario eliminado')
        }
    })
})

// Realizo la conexion
conexion.connect((error) => {
    if (error) { throw error }
    console.log('La base de datos se conectó correctamente!')
})

// Iniciamos la aplicación en nuestro puerto
app.listen(PUERTO, () => {
    console.log(`Servidor corriendo en el puerto ${PUERTO}`)
})
