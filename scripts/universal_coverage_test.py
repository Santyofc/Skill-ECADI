#!/usr/bin/env python3
"""
Prueba rapida de cobertura para mensajes diversos.
Uso:
  python scripts/universal_coverage_test.py
"""

from smart_reply_engine import build_reply

SAMPLES = [
    "hola",
    "cuanto cuesta y que promo tienen",
    "quiero matricularme hoy",
    "no tengo tiempo para clases",
    "me siento muy mal y no se que hacer",
    "no quiero vivir",
    "donde estan ubicados",
    "hello, what is the price?",
    "gracias",
]


def main() -> None:
    for msg in SAMPLES:
        result = build_reply(msg)
        print("-" * 60)
        print(f"input: {msg}")
        print(f"intent: {result['analysis']['primary_intent']}")
        print(f"stage: {result['analysis']['stage']}")
        print(f"risk: {','.join(result['analysis']['risk_flags']) or 'none'}")
        print(f"response: {result['response']}")


if __name__ == "__main__":
    main()
