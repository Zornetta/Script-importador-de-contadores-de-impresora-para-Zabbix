# ContadoresImpresoras

Este proyecto permite consultar y visualizar los contadores de páginas impresas de impresoras gestionadas por Zabbix, mostrando los resultados en una interfaz gráfica sencilla.

## Características principales
- Conexión a la API de Zabbix usando credenciales configuradas en `config.json`.
- Obtención automática de los contadores actuales de todas las impresoras de un grupo específico.
- Comparación de los valores actuales con los del mes anterior y alerta si algún contador está fuera de rango.
- Interfaz gráfica (Tkinter) para visualizar los resultados y copiar el mensaje al portapapeles.
- Registro histórico de los contadores en un archivo CSV.

## Estructura del proyecto
- `main.py`: Interfaz gráfica principal. Permite consultar y copiar los contadores.
- `zabbix_connect.py`: Lógica de conexión y consulta a la API de Zabbix, manejo de CSV y comparación de valores.
- `config.json`: Archivo de configuración con la URL del servidor Zabbix y el API token (rellenados con fillers para seguridad).
- `Contadores_historicos.csv`: Archivo generado automáticamente para guardar el historial de contadores.

## Requisitos
- Python 3.8+
- Paquetes: `pyzabbix`, `tkinter`, `pyperclip`

Instalación de dependencias:
```powershell
pip install pyzabbix pyperclip
```
Tkinter suele estar incluido en la instalación estándar de Python.

## Uso
1. Configura el archivo `config.json` con los datos de tu servidor Zabbix y tu API token.
2. Ejecuta `main.py`:
```powershell
python main.py
```
3. Usa la interfaz para consultar los contadores y copiar el mensaje generado.

## Seguridad
Los datos sensibles en `config.json` han sido reemplazados por fillers. Asegúrate de usar tus propios datos para producción.

## Autor
Desarrollado por Anzor.
