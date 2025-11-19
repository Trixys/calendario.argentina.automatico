import requests
from datetime import date, timedelta

BASE_URL = "https://api.argentinadatos.com/v1/feriados"

def escribir_evento(f, dtstart: str, dtend: str, summary: str):
    f.write("BEGIN:VEVENT\n")
    f.write(f"UID:{dtstart}@argentinadatos-ar\n")
    f.write(f"DTSTART;VALUE=DATE:{dtstart}\n")
    f.write(f"DTEND;VALUE=DATE:{dtend}\n")
    f.write(f"SUMMARY:{summary}\n")
    f.write("TRANSP:TRANSPARENT\n")
    f.write("CLASS:PUBLIC\n")
    f.write("END:VEVENT\n")

def generar_ics(anio: int):
    params = {"año": anio}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        feriados = response.json()
    except Exception as e:
        print(f"Error bajando datos para {anio}: {e}")
        return

    filename = f"feriados_argentina_{anio}_oficial_completo.ics"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("VERSION:2.0\n")
        f.write("PRODID:-//Feriados Argentina Oficial//argentinadatos//ES\n")
        f.write("METHOD:PUBLISH\n")
        f.write(f"X-WR-CALNAME:Feriados AR {anio} (nacionales + puentes + religiosos + fines semana)\n")
        f.write("X-WR-TIMEZONE:America/Argentina/Buenos_Aires\n")

        # Feriados oficiales
        for feriado in feriados:
            fecha_str = feriado["fecha"].replace("-", "")
            fecha_date = date.fromisoformat(feriado["fecha"])
            dtend = (fecha_date + timedelta(days=1)).strftime("%Y%m%d")
            
            summary = feriado["nombre"]
            tipo = feriado["tipo"].lower()
            if "puente" in tipo:
                summary += " 🏖️"
            elif "trasladable" in tipo:
                summary += " (trasladado) 🇦🇷"
            else:
                summary += " 🇦🇷"  # Por defecto nacional/religioso

            escribir_evento(f, fecha_str, dtend, summary)

        # Fines de semana
        inicio = date(anio, 1, 1)
        actual = inicio
        while actual.year == anio:
            if actual.weekday() >= 5:  # Sábado/domingo
                dtstart = actual.strftime("%Y%m%d")
                dtend = (actual + timedelta(days=1)).strftime("%Y%m%d")
                escribir_evento(f, dtstart, dtend, "Fin de semana")
            actual += timedelta(days=1)

        f.write("END:VCALENDAR\n")

    print(f"✓ {filename} generado ({len(feriados)} feriados + fines de semana)")

if __name__ == "__main__":
    año_actual = date.today().year
    for año in range(año_actual, año_actual + 6):
        generar_ics(año)
