#!/usr/bin/env python3
"""
Analiza mensajes libres y produce senales conversacionales para Skill ECADI.
Uso:
  python scripts/smart_message_analyzer.py --text "quiero matricularme hoy"
"""

import argparse
import json
import re
import unicodedata

INTENT_KEYWORDS = {
    "saludo": ["hola", "buenas", "buen dia", "buenas tardes", "hey", "hello", "hi"],
    "despedida": ["adios", "chao", "nos vemos", "gracias igual"],
    "agradecimiento": ["gracias", "muchas gracias", "agradezco", "thanks", "thank you"],
    "small-talk": ["como estas", "que tal", "todo bien", "como va", "how are you"],
    "info-general": ["informacion", "como funciona", "ecadi", "educacion abierta"],
    "programas": ["programa", "tercer ciclo", "bachillerato", "madurez", "edad"],
    "requisitos": ["requisito", "edad", "titulo", "documento", "requirement", "requirements"],
    "fechas-convocatoria": ["fecha", "convocatoria", "cuando", "inicio", "calendario", "date", "schedule"],
    "costos-promociones": ["precio", "costo", "promo", "oferta", "matricula gratis", "cuanto", "price", "cost"],
    "formas-de-pago": ["pago", "sinpe", "transferencia", "cuotas", "fraccionado"],
    "modalidad-sincronica": ["sincronico", "en vivo", "clase en vivo"],
    "modalidad-asincronica": ["asincronico", "grabado", "a mi ritmo"],
    "matricula": ["matricula", "inscribirme", "inscripcion", "empezar", "iniciar", "enroll", "enrollment"],
    "demo": ["demo", "muestra", "probar"],
    "ubicacion-contacto": ["direccion", "donde", "ubicacion", "telefono", "contacto", "horario", "where", "location", "phone"],
    "objecion-costo": ["caro", "muy caro", "no me alcanza", "dinero"],
    "objecion-tiempo": ["no tengo tiempo", "ocupado", "trabajo todo el dia", "sin tiempo"],
    "objecion-confianza": ["no se si puedo", "me da miedo", "no estoy seguro", "dudo"],
    "emotional-support": [
        "me siento mal",
        "ansioso",
        "abrumado",
        "estresado",
        "deprimido",
        "no se que hacer",
        "me siento perdido",
    ],
    "seguimiento": ["retomar", "seguimiento", "aun", "todavia", "sigo pensando"],
    "reactivacion": ["volvi", "retome", "de nuevo", "continuar"],
    "reclamo": ["queja", "reclamo", "molesto", "decepcionado", "mala atencion"],
    "consulta-legal": ["legal", "abogado", "demanda", "contrato"],
    "posible-spam": ["bitcoin", "casino", "inversion rapida", "ganancias faciles"],
}

INTENT_PRIORITY = [
    "matricula",
    "costos-promociones",
    "formas-de-pago",
    "requisitos",
    "fechas-convocatoria",
    "modalidad-sincronica",
    "modalidad-asincronica",
    "programas",
    "demo",
    "ubicacion-contacto",
    "objecion-costo",
    "objecion-tiempo",
    "objecion-confianza",
    "emotional-support",
    "seguimiento",
    "reactivacion",
    "reclamo",
    "consulta-legal",
    "posible-spam",
    "info-general",
    "small-talk",
    "agradecimiento",
    "saludo",
    "despedida",
]

POSITIVE_WORDS = ["bien", "genial", "excelente", "perfecto", "gracias", "listo"]
NEGATIVE_WORDS = ["mal", "molesto", "enojado", "caro", "no puedo", "decepcionado", "abrumado"]
URGENT_WORDS = ["hoy", "ya", "urgente", "ahora", "inmediato", "esta semana"]
CRISIS_WORDS = [
    "suicidio",
    "matarme",
    "autolesion",
    "violencia",
    "no quiero vivir",
    "quiero morir",
]
AGGRESSIVE_WORDS = ["idiota", "estafa", "basura", "mierda", "inutil"]

VIGENCIA_INTENTS = {
    "fechas-convocatoria",
    "costos-promociones",
    "formas-de-pago",
    "ubicacion-contacto",
    "requisitos",
}

HOT_HINTS = ["quiero iniciar", "quiero matricularme", "como me matriculo", "inscribirme hoy", "empezar hoy"]
WARM_HINTS = ["precio", "costo", "modalidad", "como funciona", "requisitos", "horario"]

ENGLISH_HINTS = ["hello", "price", "cost", "enroll", "schedule", "where", "thanks"]
SPANISH_HINTS = ["hola", "precio", "matricula", "horario", "gracias", "donde"]


def normalize(text: str) -> str:
    low = text.lower().strip()
    no_tilde = "".join(
        c for c in unicodedata.normalize("NFD", low) if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"\s+", " ", no_tilde)


def detect_language(text: str) -> str:
    english_score = sum(1 for w in ENGLISH_HINTS if w in text)
    spanish_score = sum(1 for w in SPANISH_HINTS if w in text)
    return "en" if english_score > spanish_score else "es"


def score_intents(text: str) -> dict:
    scores = {intent: 0 for intent in INTENT_KEYWORDS}
    for intent, words in INTENT_KEYWORDS.items():
        for word in words:
            if word in text:
                scores[intent] += 1
    return scores


def choose_primary_intent(scores: dict) -> str:
    max_score = max(scores.values())
    if max_score <= 0:
        return "info-general"

    candidates = {intent for intent, value in scores.items() if value == max_score}
    for intent in INTENT_PRIORITY:
        if intent in candidates:
            return intent
    return sorted(candidates)[0]


def top_secondary_intents(scores: dict, primary_intent: str) -> list:
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    secondary = []
    for intent, value in ranked:
        if intent == primary_intent or value <= 0:
            continue
        secondary.append(intent)
        if len(secondary) == 2:
            break
    return secondary


def detect_sentiment(text: str) -> str:
    positive = sum(1 for w in POSITIVE_WORDS if w in text)
    negative = sum(1 for w in NEGATIVE_WORDS if w in text)
    if negative > positive:
        return "negative"
    if positive > negative:
        return "positive"
    return "neutral"


def detect_urgency(text: str) -> str:
    return "high" if any(w in text for w in URGENT_WORDS) else "normal"


def detect_stage(text: str) -> str:
    if any(h in text for h in HOT_HINTS):
        return "caliente"
    if any(h in text for h in WARM_HINTS):
        return "tibio"
    return "frio"


def detect_risks(text: str, primary_intent: str) -> list:
    risks = []
    if any(w in text for w in CRISIS_WORDS):
        risks.append("crisis-personal")
    if any(w in text for w in AGGRESSIVE_WORDS):
        risks.append("lenguaje-agresivo")
    if primary_intent in {"consulta-legal", "reclamo", "posible-spam"}:
        risks.append(primary_intent)
    if primary_intent == "emotional-support":
        risks.append("emotional-distress")
    return sorted(set(risks))


def analyze_message(raw_text: str) -> dict:
    normalized = normalize(raw_text)
    scores = score_intents(normalized)

    primary_intent = choose_primary_intent(scores)
    secondary_intents = top_secondary_intents(scores, primary_intent)

    sentiment = detect_sentiment(normalized)
    urgency = detect_urgency(normalized)
    stage = detect_stage(normalized)
    language = detect_language(normalized)
    risk_flags = detect_risks(normalized, primary_intent)

    needs_vigencia_note = primary_intent in VIGENCIA_INTENTS or any(
        i in VIGENCIA_INTENTS for i in secondary_intents
    )
    needs_human_escalation = any(
        flag in {"crisis-personal", "consulta-legal", "reclamo", "lenguaje-agresivo"}
        for flag in risk_flags
    )

    top_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "normalized_text": normalized,
        "language": language,
        "primary_intent": primary_intent,
        "secondary_intents": secondary_intents,
        "sentiment": sentiment,
        "urgency": urgency,
        "stage": stage,
        "risk_flags": risk_flags,
        "needs_vigencia_note": needs_vigencia_note,
        "needs_human_escalation": needs_human_escalation,
        "intent_scores": scores,
        "top_intents": top_intents,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analiza mensajes para Skill ECADI")
    parser.add_argument("--text", required=True)
    args = parser.parse_args()

    result = analyze_message(args.text)
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
