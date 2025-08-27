import csv
import os
import json
from datetime import datetime
from pyzabbix import ZabbixAPI

class ZabbixConnect:
    def __init__(self, config_file='config.json', grupo_impresoras='Impresoras', csv_file='Contadores_historicos.csv'):
        self.config_file = config_file
        self.grupo_impresoras = grupo_impresoras
        self.csv_file = csv_file
        self.server, self.api_token = self._leer_configuracion()  # Datos sensibles reemplazados en config.json
        self.zapi = ZabbixAPI(self.server)
        self._crear_csv_si_no_existe()
    
    def _leer_configuracion(self):
        with open(self.config_file, 'r') as file:
            config = json.load(file)
            return config['zabbix_server'], config['api_token']

    def obtener_mensaje(self):
        # Conectarse al servidor Zabbix
        self.zapi.login(api_token=self.api_token)

        # Verificar la conexión obteniendo la versión del servidor Zabbix
        version = self.zapi.api_version()
        print(f'Conectado a Zabbix API versión {version}')

        # Obtener el ID del grupo de impresoras
        grupo = self.zapi.hostgroup.get(filter={"name": self.grupo_impresoras})
        if not grupo:
            print(f'No se encontró el grupo {self.grupo_impresoras}')
            return

        grupo_id = grupo[0]["groupid"]

        # Construir la cadena de salida
        output_string = "Buenas tardes.\n\nLe dejo el contador actual de las impresoras:\n"

        # Obtener información sobre los hosts (impresoras) en el grupo de impresoras
        impresoras = self.zapi.host.get(groupids=grupo_id, output='extend')
        datos_csv = []
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        fuera_de_rango = []
        for impresora in impresoras:
            items = self.zapi.item.get(hostids=impresora["hostid"], search={"name": "Распечатано страниц"}, output='extend')
            for item in items:
                valor_actual = int(item["lastvalue"])
                nombre_impresora = impresora["name"]
                valor_mes_anterior = self._obtener_valor_mes_anterior(nombre_impresora)

                if valor_mes_anterior is not None:
                    if not (0.8 * valor_mes_anterior <= valor_actual <= 1.2 * valor_mes_anterior):
                        fuera_de_rango.append({
                            "nombre": nombre_impresora,
                            "actual": valor_actual,
                            "anterior": valor_mes_anterior
                        })

                output_string += f'-- {nombre_impresora} = {valor_actual}\n'
                datos_csv.append([fecha_actual, nombre_impresora, valor_actual])

        self._guardar_datos_csv(datos_csv)

        return output_string, fuera_de_rango

        # Guardar los datos en el archivo CSV
        self._guardar_datos_csv(datos_csv)

        return output_string

    def _crear_csv_si_no_existe(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Fecha', 'Nombre Impresora', 'Распечатано страниц'])

    def _guardar_datos_csv(self, datos):
        with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(datos)

    def _obtener_valor_mes_anterior(self, nombre_impresora):
        if not os.path.exists(self.csv_file):
            return None

        with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera
            for row in reversed(list(reader)):
                fecha, nombre, valor = row
                if nombre == nombre_impresora:
                    fecha_datetime = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
                    if fecha_datetime.month == (datetime.now().month - 1):
                        return int(valor)
        return None