# Detección de cajas con yolov3

En este proyecto se entreno un modelo para reconocer cajas y se desplegó en Google cloud platform.

## Uso
**- Por web:**
 - Ingresar a la url: https://yoloapp.ue.r.appspot.com/
 ![index_image](https://github.com/HeimerR/obj_detect/blob/main/imagenes_github/1.png)
 - Cargar imagen dando click en seleccionar archivo
 - Verificar si la imagen tiene cajas dando click en el boton analyze
 - Visualizar resultados
 ![detection_image](https://github.com/HeimerR/obj_detect/blob/main/imagenes_github/2.png)


**- Petición json:**
 - Hacer petición POST
 - En los Headers usar Content-Type con application/json
 - En el Body usar el formato raw
 - Enviar un JSON con la key = image y en el value la direccion de la imagen a analizar, como se ve en el ejemplo.
```json
{
	"image": "https://image.freepik.com/psd-gratis/mockup-cajas-envio-diferentes-tamanos_23-2147861796.jpg"
}
```
 - Recibira un JSON con la url de la imagen analizada como se ve en el ejemplo.
```json
{
    "output": "https://storage.googleapis.com/yolo_data/mockup-cajas-envio-diferentes-tamanos_23-2147861796.jpg.analized.jpg"
}
```

## Etiquetado
Se probaron diferentes forma de realizarlo:
- Manualmente con programa de etiquetado
- Descargar dataset previamente etiquetado desde Roboflow y Open Images Dataset V6 (se adapto el formato en el que se encontraba el etiquetado)
- Con libreria flip: Se crearon imagenes sinteticas y se guardo la posición de los objetos en el formato de etiquetado requerido.

Se usaron diferentes datasets:
**- Roboflow:**
 - Train:
 - Valid:

**- Open Images Dataset V6 :**
 - Train:
 - Valid:

**- Libreria Flip:**
1. Dataset
 - Train:
 - Valid:
 
2. Dataset
 - Train:
 - Valid:

## Entrenamiento
Se arranco con un modelo preentrenado de yolov3 suministrado por Roboflow. El entrenameinto se dividio en dos etapas:
- Solo se entrenaron las 2 ulitmas capas
 - epochs: 500
 - batch: 32

 
- Se entrenaron todas las capas
 - epochs: 50
 - batch: 8 (por limitaciones de memoria)

## Despliegue
Se realizó en Google cloud platform - app engine y se uso Google cloud storage para el almacenamiento de los datos.
https://yoloapp.ue.r.appspot.com/

## Retos
- Etiquetar los datos en poco tiempo, tener un dataset lo suficientemente grande que permita generalizar y mejorar la detección. Se uso datos sintenticos para automatizar el etiquetado y también se probo con datasets pre-etiquetados
- Los entrenamiento toman mucho tiempo por lo cual no se realizaron tantas pruebas.
- Desconocimiento previo del uso de Google cloud platform.
- Unificar todo el proceso bajo los mismos requerimientos de Software (versiones de programas y librerias usadas)

## Futuras mejoras
- Incrementar el dataset
- Mejorar el tiempo de carga a la hora de cargar la aplicación.
