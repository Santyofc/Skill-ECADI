#!/usr/bin/env python3
"""
Clasificador simple de intencion para Skill ECADI (basado en palabras clave).
Uso:
  python scripts/intent_classifier.py --text "quiero saber requisitos y costos"
"""

import argparse

INTENT_KEYWORDS = {
    "info-general": ["informacion", "como funciona", "educacion abierta", "ecadi"],
    "requisitos": ["requisito", "edad", "titulo", "documento"],
    "fechas-convocatoria": ["fecha", "convocatoria", "cuando", "inicio"],
    "costos-promociones": ["precio", "costo", "promo", "matricula gratis", "pago"],
    "modalidad": ["sincronico", "asincronico", "en vivo", "grabado", "modalidad"],
    "matricula": ["matricula", "inscribirme", "inscripcion", "iniciar"],
    "demo": ["demo", "muestra", "probar"],
    "seguimiento": ["retomar", "seguimiento", "aun", "pensando"],
}


def classify(text: str) -> str:
    lowered = text.lower()
    scores = {intent: 0 for intent in INTENT_KEYWORDS}
    for intent, words in INTENT_KEYWORDS.items():
        for w in words:
            if w in lowered:
                scores[intent] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "info-general"


def main() -> None:
    parser = argparse.ArgumentParser(description="Clasifica intencion de mensaje")
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    print(classify(args.text))


if __name__ == "__main__":
    main()
