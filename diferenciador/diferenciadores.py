"""
diferenciadores.py
"""

import pandas as pd  # Para manipular los datos


class Diferenciador(object):
    def __init__(self, csv_fondos, csv_salida):
        self.csv_fondos = csv_fondos
        self.csv_salida = csv_salida

    def get_planilla_agrupada(self, fondos, agrupacion=['nombres', 'monedas']):
        planilla_aux = pd.read_csv(fondos, index_col=0)
        agrupados = planilla_aux.groupby(agrupacion)
        return agrupados

    def get_dataframe_diferencias_vacio(self):
        return pd.DataFrame(columns=['fondos',
                                     'monedas',
                                     'periodos',
                                     'cotizacion_nueva',
                                     'cotizacion_vieja',
                                     'cuotapartes',
                                     'diferencia_cuotapartes',
                                     'total',
                                     'resultado_total'])

    def get_fila_df_diferencia(self, nombre_fondo, moneda, periodo_ante_ultimo,
                               periodo_ultimo, cotizacion_ante_ultimo, cotizacion_ultimo,
                               cuotapartes_ante_ultimo, cuotapartes_ultimo,
                               cuotapartes_diferencia, total_ante_ultimo, total_ultimo,
                               resultado_total):
        return [
            nombre_fondo,
            moneda,
            periodo_ante_ultimo + " | " + periodo_ultimo,  # periodos
            str(cotizacion_ante_ultimo),  # cotizacion_vieja
            str(cotizacion_ultimo),  # cotizacion_nueva
            str(cuotapartes_ante_ultimo) + " - " + str(cuotapartes_ultimo),  # cuotapartes
            str(cuotapartes_diferencia),  # diferencia_cuotapartes
            str(total_ante_ultimo) + " - " + str(total_ultimo),  # total
            str(resultado_total)  # resultado_total
        ]

    def get_dataframe_diferencias(self, agrupados):
        rta = self.get_dataframe_diferencias_vacio()

        indice = 0

        for clave, grupo in agrupados:
            grupo_ordenado = grupo.sort_values(['fechas'], ascending=False)
            seccion = grupo_ordenado.head(n=2)
            # print(seccion)
            fila = self.get_fila_df_diferencia(clave[0], clave[1],
                                               seccion.iloc[0]["fechas"],
                                               seccion.iloc[1]["fechas"],
                                               seccion.iloc[0]["cotizaciones"],
                                               seccion.iloc[1]["cotizaciones"],
                                               seccion.iloc[0]["cuotapartes"],
                                               seccion.iloc[1]["cuotapartes"],
                                               # cuotapartes_diferencia,
                                               seccion.iloc[0]["cuotapartes"] - \
                                               seccion.iloc[1]["cuotapartes"],
                                               # total_ante_ultimo,
                                               seccion.iloc[0]["cuotapartes"] * \
                                               seccion.iloc[0]["cotizaciones"],
                                               seccion.iloc[1]["cuotapartes"] * \
                                               seccion.iloc[1]["cotizaciones"],  # total_ultimo,
                                               (seccion.iloc[0]["cuotapartes"] * seccion.iloc[0]["cotizaciones"]) - (seccion.iloc[1]["cuotapartes"] * seccion.iloc[1]["cotizaciones"]))  # resultado_total)
            rta.loc[indice] = fila
            indice = indice + 1

        return rta

    def ejecutar(self):
        df = self.get_planilla_agrupada(self.csv_fondos)
        print("Grupos generados: " + str(len(df.groups.keys())))

        df_dif = self.get_dataframe_diferencias(df)
        rta = df_dif.sort_values(['monedas', 'fondos'])
        rta.to_csv(self.csv_salida, sep=';', encoding='utf-8')
        print("Se genero el archivo: " + self.csv_salida)
