#!/usr/bin/env python3
"""
Generador simple de respuestas base para Skill ECADI.
Uso:
  python scripts/response_builder.py --intent info-general --stage frio --name "Andrea"
"""

import argparse

BASE_BY_INTENT = {
    "info-general": "ECADI te ayuda a prepararte para las pruebas de Educacion Abierta del MEP con una ruta clara.",
    "requisitos": "Te explico los requisitos puntuales y luego confirmamos vigencia para tu convocatoria.",
    "costos-promociones": "Te comparto el resumen de inversion y beneficios vigentes para que tomes una decision clara.",
    "modalidad": "Podemos elegir entre modalidad sincronica o asincronica segun tu disponibilidad.",
    "matricula": "Te guio paso a paso para iniciar matricula de inmediato.",
    "seguimiento": "Retomo tu proceso para ayudarte a avanzar con el siguiente paso mas conveniente."
}

CTA_BY_STAGE = {
    "frio": "Si quieres, te recomiendo la modalidad ideal para tu caso.",
    "tibio": "Si te parece, te comparto la ruta personalizada para avanzar hoy.",
    "caliente": "Si ya estas listo, iniciamos matricula ahora mismo."
}


def build_response(intent: str, stage: str, name: str | None) -> str:
    base = BASE_BY_INTENT.get(intent, BASE_BY_INTENT["info-general"])
    cta = CTA_BY_STAGE.get(stage, CTA_BY_STAGE["frio"])

    if name:
        return f"{name}, {base} {cta}"
    return f"{base} {cta}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Construye respuestas base para ECADI")
    parser.add_argument("--intent", default="info-general")
    parser.add_argument("--stage", default="frio")
    parser.add_argument("--name", default=None)
    args = parser.parse_args()

    if args.stage not in CTA_BY_STAGE:
        args.stage = "frio"

    print(build_response(args.intent, args.stage, args.name))


if __name__ == "__main__":
    main()
