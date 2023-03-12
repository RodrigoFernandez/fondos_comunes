"""
diferencias_fondos.py
"""

from pathlib import Path
# https://realpython.com/python-toml/
import tomli

from diferenciador.diferenciadores import Diferenciador


if __name__ == '__main__':
    configuracion = tomli.loads(Path(".fondos_comunes.toml").read_text(encoding='utf-8'))

    diferenciador = Diferenciador(configuracion["diferenciador"]["fondos"],
                                  configuracion["diferenciador"]["salida"])
    diferenciador.ejecutar()
