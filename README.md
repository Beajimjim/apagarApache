# Monitor de Red y Control de Apache

## Descripción

Este proyecto proporciona una herramienta para monitorear el uso de red en tiempo real y detener Apache automáticamente si se detectan anomalías en el tráfico de subida o descarga. Está diseñado para ejecutarse en sistemas Windows y utiliza **Python** junto con **Tkinter** para la interfaz gráfica.

## Características

- Monitoreo continuo del tráfico de red con valores de referencia ajustables.
- Detección de anomalías en la velocidad de subida y descarga.
- Apagado automático de Apache (`httpd.exe`) si se detectan irregularidades.
- Interfaz gráfica amigable basada en **Tkinter**.

## Instalación y Requisitos

### Requisitos

- **Sistema operativo:** Windows
- **Python 3.x** instalado
- **Librerías necesarias:**
  
  ```bash
  pip install psutil
  ```

### Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/usuario/monitor-apache.git
   cd monitor-apache
   ```
2. Instalar dependencias:
   ```bash
   pip install psutil
   ```
3. Ejecutar el script:
   ```bash
   python apagarApache.py
   ```

## Uso

1. **Ejecutar el script** `apagarApache.py`.
2. En la interfaz, hacer clic en **"Iniciar Monitoreo"** para comenzar el análisis del tráfico de red.
3. Si se detecta una anomalía, Apache se detendrá automáticamente.
4. Para detener el monitoreo manualmente, hacer clic en **"Detener Monitoreo"**.

## Funcionamiento Interno

1. **Monitoreo de Red:** Se calculan valores normales de velocidad de subida y descarga.
2. **Detección de Anomalías:** Si la velocidad excede 5 veces el valor normal, se considera una anomalía.
3. **Detención de Apache:** Se ejecuta el comando `taskkill` para cerrar `httpd.exe`.
4. **Registro en la Interfaz:** Se muestran logs en tiempo real con la actividad del monitoreo.

