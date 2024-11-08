# Actividad integradora de Docker
Api en Python con Flask para visualizar, cargar y borrar una lista de tareas.

Eleji esta tecnologia por que la he usado para scripting y para realizar pequeñas apps sencillas, tiene muchas integraciones  y una comunidad muy grande a la hora de hacer consultas o pedir ayuda.

* Primero se prueba la aplicacion en un entorno local para verificar su funcionamiento.
* Despues se creo el Dockerfile para generar una imagen local.
* Se sube la imagen a dockerhub
* Se creo un archivo docker-compose con la aplicacion
* Se corre la aplicacion en docker y se verifica su funcionamiento.
* Crear el repositorio en GitHub

### Pasos para correr la aplicacion
Se realizaron pruebas en  Ubuntu 22.04.5 LTS

**1- Clonar el repositorio**
```
git clone https://github.com/chichocoria/api_python.git
```

**2- Correr el file docker-compose**
```
cd api_python/
docker-compose up -d
```

**3- Acceder a la URL para verificar el funcionamiento de la aplicacion**

Se puede acceder como localhost dentro del host o tambien por la IP privada del host

```
http://127.0.0.1:5000/tareas
http://IP:5000/tareas
```

Enviar solicitud POST para agregar una tarea
```
curl -X POST http://127.0.0.1:5000/tareas -H "Content-Type: application/json" -d '{"titulo": "Test de la aplicacion","completado": false}'
```

Resultado esperado
```
{
  "completado": false,
  "id": 3,
  "titulo": "Test de la aplicacion"
}
```

Enviar una solicitud DELETE para eliminar una tarea
```
curl -X DELETE http://127.0.0.1:5000/tareas/1
```

Resultado Esperado
```
{
  "mensaje": "Tarea eliminada"
}
```