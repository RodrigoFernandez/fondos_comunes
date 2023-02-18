"""
actualizadores.py
"""

import xlrd
import os
import datetime
import pandas as pd  # Para manipular los datos


class Actualizador(object):
    def __init__(self, ruta_csv, ruta_tenencia):
        self.ruta_csv = ruta_csv
        self.ruta_tenencia = ruta_tenencia
        self.dia_anterior = self.get_dia_anterior(self.ruta_tenencia)

    def get_dia_anterior(self, nombre_archivo):
        aux = nombre_archivo.split(".")
        sin_extension = aux[0] if len(aux) > 1 else nombre_archivo
        partes = sin_extension.split("_")
        partes.reverse()
        if len(partes) >= 3:
            fecha = datetime.date(int(partes[2]), int(partes[1]), int(partes[0]))
            delta = datetime.timedelta(days=1)
            dia_anterior = fecha - delta
            return dia_anterior.strftime('%Y-%m-%d')
        return ""

    def getHoja(self, ruta):
        planilla = xlrd.open_workbook(ruta)
        hoja = planilla.sheet_by_index(0)
        lector = [hoja.row_values(nro_fila) for nro_fila in range(0, hoja.nrows)]
        return lector

    def corregir_formato_monto(self, monto):
        return monto.replace('.', '').replace(',', '.')

    def es_fila_con_fondo(self, fila):
        textos_buscados = ['Total', 'Tipo', 'Cuenta títulos',
                           'Intervinientes', 'Fondos en pesos', 'Fondos en dólares']
        return len(fila) > 3 and (fila[1] not in textos_buscados) and sum([len(x.strip()) for x in fila]) > 0

    def limpiar_info(self, fila):
        for indice in range(1, len(fila)):
            fila[indice] = fila[indice].replace('.', '').replace(
                ',', '.').replace('$', '').replace('us', '').strip()

    def get_fondos(self, lector, fecha_cotizacion):
        rta = []

        for fila in lector:
            fila = fila[:len(fila)-1]

            if self.es_fila_con_fondo(fila):
                fila = fila[2:]

                es_en_dolares = 'u$s' in fila[2]

                self.limpiar_info(fila)

                un_fondo = {}
                un_fondo['fecha'] = fecha_cotizacion
                un_fondo['nombre'] = fila[0]
                un_fondo['moneda'] = 'u$s' if es_en_dolares else '$'
                un_fondo['cotizacion'] = fila[2]
                un_fondo['cuotapartes'] = fila[1]
                rta.append(un_fondo)
        return rta

    def get_lista_tenencias(self, tenencias):
        todos = []
        for tenencia in tenencias:
            actual = self.getHoja(tenencia[0])
            fondo_actual = self.get_fondos(actual, tenencia[1])
            todos = todos + fondo_actual
        return todos

    def get_columnas(self, nombre_campo, fondos):
        return [fondo[nombre_campo] for fondo in fondos]

    def get_preplanilla(self, fondos):
        preplanilla = {}
        preplanilla['fechas'] = self.get_columnas('fecha', fondos)
        preplanilla['nombres'] = self.get_columnas('nombre', fondos)
        preplanilla['monedas'] = self.get_columnas('moneda', fondos)
        preplanilla['cotizaciones'] = self.get_columnas('cotizacion', fondos)
        preplanilla['cuotapartes'] = self.get_columnas('cuotapartes', fondos)
        return preplanilla

    def es_nueva_planilla(self, ruta_planilla_csv):
        if os.path.isfile(ruta_planilla_csv):
            if os.stat(ruta_planilla_csv).st_size == 0:
                return True
        else:
            return True
        return False

    def actualizar_csv_fondos(self, ruta_planilla_csv, ruta_tenencia, dia_anterior):
        nuevas_tenencias = self.get_lista_tenencias([(ruta_tenencia, dia_anterior)])
        preplanilla_nueva = self.get_preplanilla(nuevas_tenencias)
        planilla_nueva = pd.DataFrame(preplanilla_nueva, columns=preplanilla_nueva.keys())
        planilla_nueva.replace(to_replace="-", value=1.0, inplace=True)

        if self.es_nueva_planilla(ruta_planilla_csv):
            planilla_nueva.to_csv(ruta_planilla_csv)
        else:
            planilla_vieja = pd.read_csv(ruta_planilla_csv, index_col=0)
            planilla_actualizada = pd.concat([planilla_vieja, planilla_nueva], ignore_index=True)
            planilla_actualizada.to_csv(ruta_planilla_csv)

    def ejecutar(self):
        self.actualizar_csv_fondos(self.ruta_csv, self.ruta_tenencia, self.dia_anterior)
