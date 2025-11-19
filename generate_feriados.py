import holidays
from datetime import date, timedelta

# Librería oficial que calcula feriados AR para cualquier año
ar = holidays.AR()

# Puentes turísticos oficiales (hardcodeados del decreto 2025-2026)
PUENTES = {
    2025: [date(2025, 5, 2), date(2025, 8, 15), date(2025, 10, 10), date(2025, 11, 21)],
    2026: [date(2026, 3, 13), date(2026, 5, 29), date(2026, 7, 17), date(2026, 10, 9), date(2026, 12, 4)],
    # Se agregan más cuando salgan decretos
}

def escribir_evento(f, dtstart: str, dtend: str, summary: str):
    f.write("BEGIN:VEVENT\n")
    f.write(f"UID:{dtstart}@feriados-ar\n")
    f.write(f"DTSTART;VALUE=DATE:{dtstart}\n")
    f.write(f"DTEND;VALUE=DATE:{dtend}\n")
    f.write(f"SUMMARY:{summary}\n")
    f.write("TRANSP:TRANSPARENT\n")
    f.write("CLASS:PUBLIC\n")
    f.write("END:VEVENT\n")

def generar_ics(anio: int):
    filename = f"feriados_argentina_{anio}_oficial_completo.ics"
    
    # Feriados de holidays.AR (nacionales + trasladables + religiosos)
    feriados_anio = ar.get_list(year=anio)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("VERSION:2.0\n")
        f.write("PRODID:-//Feriados Argentina Completo//holidays//ES\n")
        f.write("METHOD:PUBLISH\n")
        f.write(f"X-WR-CALNAME:Feriados AR {anio} (nacionales + puentes + religiosos + fines semana)\n")
        f.write("X-WR-TIMEZONE:America/Argentina/Buenos_Aires\n")

        # Feriados oficiales
        for fecha in feriados_anio:
            dtstart = fecha.strftime("%Y%m%d")
            dtend = (fecha + timedelta(days=1)).strftime("%Y%m%d")
            nombre = ar[fecha]  # Ej: "Año Nuevo"
            if "trasladable" in nombre.lower():
                nombre += " (trasladado) 🇦🇷"
            else:
                nombre += " 🇦🇷"
            escribir_evento(f, dtstart, dtend, nombre)

        # Puentes turísticos (si existen para este año)
        for puente in PUENTES.get(anio, []):
            dtstart = puente.strftime("%Y%m%d")
            dtend = (puente + timedelta(days=1)).strftime("%Y%m%d")
            escribir_evento(f, dtstart, dtend, "Puente turístico 🏖️")

        # Fines de semana
        inicio = date(anio, 1, 1)
        actual = inicio
        while actual.year == anio:
            if actual.weekday() >= 5:
                dtstart = actual.strftime("%Y%m%d")
                dtend = (actual + timedelta(days=1)).strftime("%Y%m%d")
                escribir_evento(f, dtstart, dtend, "Fin de semana")
            actual += timedelta(days=1)

        f.write("END:VCALENDAR\n")

    print(f"✓ {filename} generado ({len(feriados_anio)} feriados + puentes + fines de semana)")

if __name__ == "__main__":
    año_actual = date.today().year
    for año in range(año_actual, año_actual + 6):
        generar_ics(año)
