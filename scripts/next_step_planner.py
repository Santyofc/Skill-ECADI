#!/usr/bin/env python3
"""
Planner de respuesta siguiente segun intencion, etapa y barrera.
Uso:
  python scripts/next_step_planner.py --intent costos-promociones --stage tibio --barrier costo
"""

import argparse


def plan(intent: str, stage: str, barrier: str) -> str:
    if stage == "caliente":
        return "CTA: iniciar matricula ahora + confirmar vigencia de datos criticos."

    if barrier == "costo":
        return "Accion: validar objecion de costo + mostrar valor + CTA de ruta personalizada."
    if barrier == "tiempo":
        return "Accion: recomendar modalidad flexible + plan de avance realista."
    if barrier == "confianza":
        return "Accion: reforzar acompanamiento + proponer demo o paso pequeno."

    if intent in {"requisitos", "fechas-convocatoria"}:
        return "Accion: responder puntual + nota de vigencia + CTA unica."
    if intent == "matricula":
        return "Accion: paso a paso de inicio inmediato."

    return "Accion: orientar, calificar y cerrar con CTA contextual."


def main() -> None:
    parser = argparse.ArgumentParser(description="Planifica siguiente accion conversacional")
    parser.add_argument("--intent", default="info-general")
    parser.add_argument("--stage", default="frio")
    parser.add_argument("--barrier", default="ninguna")
    args = parser.parse_args()

    print(plan(args.intent, args.stage, args.barrier))


if __name__ == "__main__":
    main()
