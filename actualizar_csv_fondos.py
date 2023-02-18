"""
actualizar_csv_fondos.py
"""

import argparse

from pathlib import Path
# https://realpython.com/python-toml/
import tomli
import glob

from actualizador.actualizadores import Actualizador


def get_parser():
    parser = argparse.ArgumentParser(description="Actualizador de csv fondos")
    parser.add_argument('csv', help='ruta csv fondos')
    return parser


def actualizar(csv, directorio_tenencias):
    for una_tenencia in sorted(glob.glob(directorio_tenencias + r'/TenenciaFondosComunes*')):
        actualizador = Actualizador(csv, una_tenencia)
        actualizador.ejecutar()


if __name__ == '__main__':
    configuracion = tomli.loads(Path(".fondos_comunes.toml").read_text(encoding='utf-8'))
    args = get_parser().parse_args()

    actualizar(args.csv, configuracion["actualizador"]["directorio"])
