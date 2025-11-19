import json
from datetime import date, timedelta

try:
    import requests
except ImportError:
    print("requests no está instalado")
    exit(1)

API_URL = "https://apis.datos.gob.ar/feriados"

def generar_ics(anio: int):
    filename = f"feriados_argentina_{anio}_oficial_completo.ics"
    
    try:
        response = requests.get(API_URL, params={"anio": anio}, timeout=10)
        response.raise_for_status()
        feriados = response.json()
    except Exception as e:
        print(f"No se pudieron bajar los feriados del año {anio}: {e}")
        return

    with open(filename, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("VERSION:2.0\n")
        f.write("PRODID:-//Feriados Argentina OFICIAL via datos.gob.ar//ES\n")
        f.write("METHOD:PUBLISH\n")
        f.write("X-WR-CALNAME:Feriados Argentina Oficial + Puentes + Fines de semana\n")
        f.write("X-WR-TIMEZONE:America/Argentina/Buenos_Aires\n")

        # Feriados oficiales (ya vienen con traslados y puentes turísticos incluidos)
        for feriado in feriados:
            fecha = date(feriado["anio"], feriado["mes"], feriado["dia"])
            dtstart = fecha.strftime("%Y%m%d")
            dtend = (fecha + timedelta(days=1)).strftime("%Y%m%d")
            
            motivo = feriado["motivo"]
            if "turismo" in feriado["tipo"].lower():
                motivo += " (Puente turístico) 🏖️"

            f.write("BEGIN:VEVENT\n")
            f.write(f"UID:{dtstart}@datos-gob-ar\n")
            f.write(f"DTSTART;VALUE=DATE:{dtstart}\n")
            f.write(f"DTEND;VALUE=DATE:{dtend}\n")
            f.write(f"SUMMARY:{motivo}\n")
            f.write("TRANSP:TRANSPARENT\n")
            f.write("END:VEVENT\n")

        # Fines de semana
        actual = date(anio, 1, 1)
        fin = date(anio, 12, 31)
        while actual <= fin:
            if actual.weekday() >= 5:  # sábado o domingo
                dtstart = actual.strftime("%Y%m%d")
                dtend = (actual + timedelta(days=1)).strftime("%Y%m%d")
                f.write("BEGIN:VEVENT\n")
                f.write(f"UID:{dtstart}-weekend\n")
                f.write(f"DTSTART;VALUE=DATE:{dtstart}\n")
                f.write(f"DTEND;VALUE=DATE:{dtend}\n")
                f.write("SUMMARY:Fin de semana\n")
                f.write("TRANSP:TRANSPARENT\n")
                f.write("END:VEVENT\n")
            actual += timedelta(days=1)

        f.write("END:VCALENDAR\n")
    
    print(f"Generado {filename} con {len(feriados)} feriados oficiales + fines de semana")

if __name__ == "__main__":
    año_actual = date.today().year
    for año in range(año_actual, año_actual + 6):
        generar_ics(año)
