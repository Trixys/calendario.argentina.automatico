import requests
from datetime import date
import json

API_URL = "https://apis.datos.gob.ar/feriados"

def generar_ics(anio: int):
    filename = f"feriados_argentina_{anio}_oficial_completo.ics"
    
    # Bajamos los datos oficiales del gobierno
    response = requests.get(API_URL, params={"anio": anio})
    if response.status_code != 200:
        print(f"Error descargando datos del año {anio}")
        return
    
    feriados = response.json()

    with open(filename, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("VERSION:2.0\n")
        f.write("PRODID:-//Feriados Argentina OFICIAL (datos.gob.ar)//ES\n")
        f.write("METHOD:PUBLISH\n")
        f.write("X-WR-CALNAME:Feriados Argentina Oficial + Puentes + Religiosos\n")
        f.write("X-WR-TIMEZONE:America/Argentina/Buenos_Aires\n")

        for feriado in feriados:
            # Fecha observada = la que realmente es feriado (ya incluye traslados y puentes)
            fecha = f"{feriado['anio']}-{feriado['mes']:02d}-{feriado['dia']:02d}"
            fecha_date = date(feriado['anio'], feriado['mes'], feriado['dia'])
            dtstart = fecha.replace("-", "")
            dtend = (fecha_date + timedelta(days=1)).strftime("%Y%m%d")
            
            motivo = feriado["motivo"]
            tipo = feriado["tipo"]
            if "turismo" in tipo.lower():
                motivo = f"{motivo} (Puente turístico) 🏖️"
            elif "trasladable" in tipo.lower():
                motivo = f"{motivo} (trasladado) 🇦🇷"

            f.write("BEGIN:VEVENT\n")
            f.write(f"UID:{dtstart}@datos-gob-ar\n")
            f.write(f"DTSTART;VALUE=DATE:{dtstart}\n")
            f.write(f"DTEND;VALUE=DATE:{dtend}\n")
            f.write(f"SUMMARY:{motivo}\n")
            f.write("TRANSP:TRANSPARENT\n")
            f.write("END:VEVENT\n")

        # Opcional: agregar fines de semana (como antes)
        inicio = date(anio, 1, 1)
        fin = date(anio, 12, 31)
        actual = inicio
        while actual <= fin:
            if actual.weekday() >= 5:
                dtstart = actual.strftime("%Y%m%d")
                dtend = (actual + timedelta(days=1)).strftime("%Y%m%d")
                f.write("BEGIN:VEVENT\n")
                f.write(f"UID:{dtstart}-weekend@feriados\n")
                f.write(f"DTSTART;VALUE=DATE:{dtstart}\n")
                f.write(f"DTEND;VALUE=DATE:{dtend}\n")
                f.write("SUMMARY:Fin de semana\n")
                f.write("TRANSP:TRANSPARENT\n")
                f.write("END:VEVENT\n")
            actual += timedelta(days=1)

        f.write("END:VCALENDAR\n")
    
    print(f"Generado {filename} con datos 100% oficiales del gobierno")

if __name__ == "__main__":
    from datetime import timedelta
    año_actual = date.today().year
    for año in range(año_actual, año_actual + 6):  # 6 años adelante
        generar_ics(año)
