import holidays
from datetime import date, timedelta

# Año actual
anio = date.today().year

# Feriados oficiales de Argentina (solo este año)
ar = holidays.AR(years=[anio])

# Puentes turísticos oficiales conocidos (solo los del año actual)
PUENTES_TURISTICOS = {
    2025: ["2025-05-02", "2025-08-15", "2025-10-10", "2025-11-21"],
    2026: ["2026-03-13", "2026-05-29", "2026-07-17", "2026-10-09", "2026-12-04"],
    # Cuando salga decreto 2027+, se agregan aquí
}

def escribir_evento(f, dtstart, dtend, summary):
    f.write("BEGIN:VEVENT\n")
    f.write(f"UID:{dtstart}@feriados-argentina\n")
    f.write(f"DTSTART;VALUE=DATE:{dtstart}\n")
    f.write(f"DTEND;VALUE=DATE:{dtend}\n")
    f.write(f"SUMMARY:{summary}\n")
    f.write("TRANSP:TRANSPARENT\n")
    f.write("END:VEVENT\n")

# Siempre el mismo nombre de archivo
filename = "feriados_argentina_actual.ics"

with open(filename, "w", encoding="utf-8") as f:
    f.write("BEGIN:VCALENDAR\n")
    f.write("VERSION:2.0\n")
    f.write("PRODID:-//Feriados Argentina Actual//ES\n")
    f.write("METHOD:PUBLISH\n")
    f.write(f"X-WR-CALNAME:Feriados Argentina {anio} 🇦🇷\n")
    f.write("X-WR-TIMEZONE:America/Argentina/Buenos_Aires\n")
    f.write("REFRESH-INTERVAL;VALUE=DURATION:PT12H\n")  # Google actualiza cada 12h
    f.write("X-PUBLISHED-TTL:PT12H\n")

    # Feriados nacionales + religiosos + trasladables
    for fecha, nombre in ar.items():
        dtstart = fecha.strftime("%Y%m%d")
        dtend = (fecha + timedelta(days=1)).strftime("%Y%m%d")
        if "trasladable" in nombre.lower():
            nombre = nombre + " (trasladado) Argentina"
        else:
            nombre = nombre + " Argentina"
        escribir_evento(f, dtstart, dtend, nombre)

    # Puentes turísticos del año actual
    for puente in PUENTES_TURISTICOS.get(anio, []):
        p = date.fromisoformat(puente)
        dtstart = p.strftime("%Y%m%d")
        dtend = (p + timedelta(days=1)).strftime("%Y%m%d")
        escribir_evento(f, dtstart, dtend, "Puente turístico Beach")

    # Todos los sábados y domingos del año
    actual = date(anio, 1, 1)
    while actual.year == anio:
        if actual.weekday() >= 5:  # sábado o domingo
            dtstart = actual.strftime("%Y%m%d")
            dtend = (actual + timedelta(days=1)).strftime("%Y%m%d")
            escribir_evento(f, dtstart, dtend, "Fin de semana")
        actual += timedelta(days=1)

    f.write("END:VCALENDAR\n")

print(f"¡Listo! feriados_argentina_actual.ics generado para el año {anio}")
print("   → El 1 de enero de 2026 se actualizará automáticamente a 2026")
