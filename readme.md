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

**4- Aplicar el file 03-ingress.yaml**
```
kubectl apply 03-ingress.yaml -n utn-k8s-desafio
```


**Verificaciones**
* Verificar que esta todo corriendo en el namespace
```
darioc@cod-fac-devops:~$ kubectl get all -n utn-k8s-desafio
NAME                                      READY   STATUS    RESTARTS   AGE
pod/app-desafio-utn-k8s-7f7dd897f-btm6b   1/1     Running   0          59m
pod/app-desafio-utn-k8s-7f7dd897f-gv8hf   1/1     Running   0          59m
pod/app-desafio-utn-k8s-7f7dd897f-rsdpv   1/1     Running   0          59m

NAME                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/app-desafio-utn-k8s   ClusterIP   10.43.233.117   <none>        5000/TCP   59m

NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/app-desafio-utn-k8s   3/3     3            3           59m

NAME                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/app-desafio-utn-k8s-7f7dd897f   3         3         3       59m
```

* Verificar ingress
```
darioc@cod-fac-devops:~$ kubectl get ingress -n utn-k8s-desafio
NAME                        CLASS    HOSTS                   ADDRESS         PORTS     AGE
utn-k8s.chicho.com.ar       <none>   utn-k8s.chicho.com.ar   192.168.52.31   80, 443   108s
cm-acme-http-solver-szk9v   <none>   utn-k8s.chicho.com.ar   192.168.52.31   80        106s
```

* Verificar certificado TLS
```
darioc@cod-fac-devops:~$ kubectl get certificate -n utn-k8s-desafio 
NAME                  READY   SECRET                AGE
letsencrypt-utn-k8s   False   letsencrypt-utn-k8s   34s
```


**Acceso a la apliacion**
* Para los dns se utilizo Cloudflare
* Se utlizo nginx-ingress-controller para exponer la app y cert-manager para los certs TLS

URL: https://utn-k8s.chicho.com.ar/tareas


**Extra: Monitoreo y Observabilidad**

Se instalo kube-prom-stack y loki-stack con helm. Con lo cual podemos visualizar con grafana las metricas de salud del Cluster que nos provee prometheus. Y tambien Loki para los logs de las applicaciones que corren dentro del Cluster.
Para almacenamiento persistente de las configuraciones de grafana, metricas y logs se utilizo Longhorn que es una herramienta de almacenamiento distribuido y un proyecto de la CNCF.

URL: https://grafana.chicho.com.ar/

Se agrego un dashboard Node Exporter llamado con el que podemos ver visualizar CPU, memoria, E/S de disco, red, temperatura y otras métricas de monitoreo.

URL: https://grafana.chicho.com.ar/d/W5KDrdKnz/6e86b6fe-1eab-5293-a881-2592e2eb6445?orgId=1&from=1732884630455&to=1732888230455

