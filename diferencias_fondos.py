"""
diferencias_fondos.py
"""

import argparse

from diferenciador.diferenciadores import Diferenciador


def get_parser():
    parser = argparse.ArgumentParser(description="Diferencias fondos csv")
    parser.add_argument('fondos', help='archivo csv con las cotizaciones de los fondos')
    parser.add_argument('--salida', help='Nombre csv con la salida',
                        required=False, default='diferencias_fondos_comunes.csv')
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()

    diferenciador = Diferenciador(args.fondos, args.salida)
    diferenciador.ejecutar()
