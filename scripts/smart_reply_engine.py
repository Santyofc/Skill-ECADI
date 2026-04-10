#!/usr/bin/env python3
"""
Genera respuestas inteligentes para mensajes libres usando analisis heuristico.
Uso:
  python scripts/smart_reply_engine.py --text "hola, cuanto cuesta y como me matriculo"
"""

import argparse
import json

from smart_message_analyzer import analyze_message

OPENING_BY_SENTIMENT_ES = {
    "positive": "Excelente, con gusto te ayudo.",
    "neutral": "Con gusto te ayudo.",
    "negative": "Entiendo tu inquietud, vamos a resolverlo con claridad.",
}

PRIMARY_RESPONSE_ES = {
    "saludo": "Estoy aqui para ayudarte con todo lo relacionado a ECADI.",
    "despedida": "Gracias por escribir. Cuando quieras retomar, te acompano.",
    "agradecimiento": "Con mucho gusto.",
    "small-talk": "Todo bien, gracias. Si quieres, avanzamos con tu objetivo academico.",
    "info-general": "ECADI te prepara para las pruebas de Educacion Abierta del MEP con ruta clara, material y acompanamiento.",
    "programas": "Te puedo orientar en tercer ciclo, bachillerato por madurez o por edad segun tu caso.",
    "requisitos": "Te explico los requisitos puntuales para tu programa objetivo.",
    "fechas-convocatoria": "Te comparto las fechas de referencia y te ayudo a confirmar vigencia actual.",
    "costos-promociones": "Te comparto un resumen de costos y promociones para que tomes una decision clara.",
    "formas-de-pago": "Te indico las opciones de pago disponibles y como elegir la mas conveniente.",
    "modalidad-sincronica": "La modalidad sincronica es ideal si buscas estructura y acompanamiento en vivo.",
    "modalidad-asincronica": "La modalidad asincronica funciona bien si necesitas estudiar a tu ritmo.",
    "matricula": "Perfecto, te guio paso a paso para iniciar matricula.",
    "demo": "Claro, te explico como acceder a una muestra para que conozcas la metodologia.",
    "ubicacion-contacto": "Te comparto canales oficiales de contacto y ubicacion de referencia.",
    "objecion-costo": "Es totalmente valido cuidar el presupuesto; busquemos la ruta con mejor equilibrio valor-inversion.",
    "objecion-tiempo": "Te entiendo; podemos ajustar la modalidad a tu disponibilidad real para que avances sin friccion.",
    "objecion-confianza": "Es normal sentir eso al inicio; lo importante es avanzar con una ruta guiada y acompanamiento.",
    "emotional-support": "Gracias por confiar en contarlo. No estas solo, podemos ir paso a paso para que tengas claridad y apoyo.",
    "seguimiento": "Retomemos desde donde lo dejamos para facilitar tu siguiente paso.",
    "reactivacion": "Que bueno que retomaste, avancemos con la opcion mas conveniente para tu caso.",
    "reclamo": "Lamento la experiencia. Quiero ayudarte a resolverlo de forma correcta.",
    "consulta-legal": "Para ese punto necesitas validacion formal con asesor responsable.",
    "posible-spam": "Puedo ayudarte especificamente con informacion de ECADI y proceso academico.",
}

CTA_BY_STAGE_ES = {
    "frio": "Si quieres, te ayudo a identificar la mejor modalidad para vos.",
    "tibio": "Si te parece, te dejo una recomendacion personalizada y el siguiente paso.",
    "caliente": "Si ya estas listo, iniciamos matricula ahora mismo.",
}


def build_reply(text: str, name: str = "") -> dict:
    analysis = analyze_message(text)

    if "crisis-personal" in analysis["risk_flags"]:
        response = (
            "Lamento que estes pasando por esto. Para ayudarte de forma segura, "
            "te voy a conectar con apoyo humano inmediato."
        )
        return {"analysis": analysis, "response": response}

    opening = OPENING_BY_SENTIMENT_ES.get(analysis["sentiment"], OPENING_BY_SENTIMENT_ES["neutral"])
    body = PRIMARY_RESPONSE_ES.get(analysis["primary_intent"], PRIMARY_RESPONSE_ES["info-general"])

    parts = [opening, body]

    if analysis["language"] == "en":
        parts.append("If you prefer, I can continue in English or Spanish.")

    if analysis["needs_vigencia_note"]:
        parts.append(
            "Estos datos pueden cambiar por convocatoria; si quieres, te confirmo la version vigente ahora mismo."
        )

    if analysis["needs_human_escalation"]:
        parts.append(
            "Para darte precision total en este punto, te conecto de inmediato con un asesor de ECADI."
        )
    else:
        parts.append(CTA_BY_STAGE_ES.get(analysis["stage"], CTA_BY_STAGE_ES["frio"]))

    response = " ".join(parts)
    if name:
        response = f"{name}, {response}"

    return {"analysis": analysis, "response": response}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generador inteligente de respuestas ECADI")
    parser.add_argument("--text", required=True)
    parser.add_argument("--name", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_reply(args.text, args.name)
    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        print(result["response"])


if __name__ == "__main__":
    main()
