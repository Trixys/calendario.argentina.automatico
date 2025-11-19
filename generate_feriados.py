import holidays
from datetime import date, timedelta

# Feriados oficiales Argentina (incluye nacionales, trasladables y religiosos)
ar_holidays = holidays.AR(years=range(date.today().year, date.today().year + 6))

# Puentes turísticos oficiales 2025-2026 (decreto vigente)
PUENTES_TURISTICOS = {
    2025: ["2025-05-02", "2025-08-15", "2025-10-10", "2025-11-21"],
    2026: ["2026-03-13", "2026-05-29", "2026-07-17", "2026-10-09", "2026-12-04"],
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
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("VERSION:2.0\n")
        f.write("PRODID:-//Feriados Argentina Oficial//ES\n")
        f.write("METHOD:PUBLISH\n")
        f.write(f"X-WR-CALNAME:Feriados AR {anio} (oficial + puentes + fines semana)\n")
        f.write("X-WR-TIMEZONE:America/Argentina/Buenos_Aires\n")

        # === Feriados oficiales (nacionales + religiosos + trasladables) ===
        for fecha_str, nombre in ar_holidays.items():
            if fecha_str.year != anio:
                continue
            dtstart = fecha_str.strftime("%Y%m%d")
            dtend = (fecha_str + timedelta(days=1)).strftime("%Y%m%d")
            if "trasladable" in nombre.lower():
                nombre += " (trasladado) Argentina"
            else:
                nombre += " Argentina"
            escribir_evento(f, dtstart, dtend, nombre)

        # === Puentes turísticos ===
        for puente_str in PUENTES_TURISTICOS.get(anio, []):
            puente = date.fromisoformat(puente_str)
            dtstart = puente.strftime("%Y%m%d")
            dtend = (puente + timedelta(days=1)).strftime("%Y%m%d")
            escribir_evento(f, dtstart, dtend, "Puente turístico Beach")

        # === Fines de semana ===
        inicio = date(anio, 1, 1)
        actual = inicio
        while actual.year == anio:
            if actual.weekday() >= 5:  # sábado o domingo
                dtstart = actual.strftime("%Y%m%d")
                dtend = (actual + timedelta(days=1)).strftime("%Y%m%d")
                escribir_evento(f, dtstart, dtend, "Fin de semana")
            actual += timedelta(days=1)

        f.write("END:VCALENDAR\n")

    print(f"Generated {filename} → Año Nuevo 1/1/{anio}, Carnaval, puentes, fines de semana, TODO")

if __name__ == "__main__":
    for año in range(date.today().year, date.today().year + 6):
        generar_ics(año)
