#!/usr/bin/env python3
"""
Selector de seguimiento por dias sin respuesta.
Uso:
  python scripts/followup_picker.py --days 3
"""

import argparse


def pick(days: int) -> str:
    if days <= 1:
        return "Seguimiento suave: retomar con ayuda breve y CTA simple."
    if days <= 3:
        return "Seguimiento medio: resumen de valor + ruta recomendada."
    if days <= 7:
        return "Seguimiento final: invitacion respetuosa a retomar sin presion."
    return "Cierre temporal: dejar puerta abierta para reactivacion futura."


def main() -> None:
    parser = argparse.ArgumentParser(description="Selecciona tipo de follow-up")
    parser.add_argument("--days", type=int, default=1)
    args = parser.parse_args()
    print(pick(args.days))


if __name__ == "__main__":
    main()
