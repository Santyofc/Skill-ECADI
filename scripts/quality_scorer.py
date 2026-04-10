#!/usr/bin/env python3
"""
Score rapido de calidad de respuesta (heuristico) segun rubrica ECADI.
Uso:
  python scripts/quality_scorer.py --response "..."
"""

import argparse


def score(response: str) -> tuple[int, dict[str, int]]:
    text = response.lower()

    clarity = 2 if len(response) <= 450 else 1
    precision = 2 if ("vigencia" in text or "puede cambiar" in text or "confirmar" in text) else 1
    utility = 2 if any(k in text for k in ["te ayudo", "te comparto", "te recomiendo", "ruta"]) else 1
    advance = 2 if any(k in text for k in ["si quieres", "iniciar", "matricula", "siguiente paso"]) else 1
    tone = 2 if any(k in text for k in ["con gusto", "te ayudo", "si quieres", "perfecto"]) else 1

    subs = {
        "clarity": clarity,
        "precision": precision,
        "utility": utility,
        "advance": advance,
        "tone": tone,
    }
    return sum(subs.values()), subs


def main() -> None:
    parser = argparse.ArgumentParser(description="Puntua respuesta ECADI")
    parser.add_argument("--response", required=True)
    args = parser.parse_args()

    total, subs = score(args.response)
    print(f"total={total}/10")
    for k, v in subs.items():
        print(f"{k}={v}")


if __name__ == "__main__":
    main()
