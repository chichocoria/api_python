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


---

# Trabajo integrador de Kubernetes

Para realizar las pruebas de la aplicacion que se contenerizo se va a utilizar un ambiente de laboratorio con un cluster k8s on-premise con RKE1 que consta de 1 control plane y 2 workers, en un ambiente real lo llevariamos a la cloud con al menos 2 nodos workers con autoescalado horizontal automatico en caso de que si se llega a un umbral de recursos altos, se generen mas workers para soportal la carga.

Si bien este es un ejemplo de deploy de una API, se le podria agregar una base de datos por fuera del cluster para que los datos sean persistentes.

Se utiliza un ingress para exponer la aplicacion hacia afuera.

### Pasos para correr la aplicacion
En esta prueba se supone que ya tenemos acceso al cluster para poder realizar el deploy de la app. 

Se va a crear un namespace llamado utn-k8s-desafio para agrupar los objetos.

```
kubectl create ns utn-k8s-desafio
```

**1- Clonar el repositorio**
```
git clone https://github.com/chichocoria/api_python.git
```

**1- Dirigirse a la carpeta /k8s**
```
cd api_python/k8s/
```

**2- Aplicar el file 01-deployment.yaml**
```
kubectl apply 01-deployment.yaml -n utn-k8s-desafio
```

**3- Aplicar el file 02-services.yml**
```
kubectl apply 02-services.yml -n utn-k8s-desafio
```

* Se podria relizar un port-forward para verificar que la app funciona antes de generar el ingress.
```
kubectl port-forward svc/app-desafio-utn-k8s 8090:5000 -n utn-k8s-desafio
 ```

 ```
darioc@cod-fac-devops:~/api_python/k8s$ curl localhost:8090/tareas
[
  {
    "completado": false,
    "id": 1,
    "titulo": "Aprender Flask"
  },
  {
    "completado": false,
    "id": 2,
    "titulo": "Hacer una API"
  }
]
 ```

**4- Aplicar el file 003-ingress.yaml**
```
kubectl apply 03-ingress.yaml -n utn-k8s-desafio
```

* Para los dns se utilizo Cloudflare

URL: https://utn-k8s.chicho.com.ar/tareas