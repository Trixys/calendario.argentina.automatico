import holidays
from datetime import date, timedelta

def escribir_evento(f, fecha: date, nombre: str):
    dtstart = fecha.strftime("%Y%m%d")
    dtend = (fecha + timedelta(days=1)).strftime("%Y%m%d")
    f.write("BEGIN:VEVENT\n")
    f.write(f"UID:{dtstart}@feriados-argentina\n")
    f.write(f"DTSTART;VALUE=DATE:{dtstart}\n")
    f.write(f"DTEND;VALUE=DATE:{dtend}\n")
    f.write(f"SUMMARY:{nombre}\n")
    f.write("TRANSP:TRANSPARENT\n")
    f.write("CLASS:PUBLIC\n")
    f.write("STATUS:CONFIRMED\n")
    f.write("END:VEVENT\n")

def generar_ics(anio: int):
    filename = f"feriados_argentina_{anio}_completo.ics"
    ar = holidays.AR(years=anio)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("VERSION:2.0\n")
        f.write("PRODID:-//Feriados Argentina Completo//ES\n")
        f.write("METHOD:PUBLISH\n")
        f.write("X-WR-CALNAME:Feriados Argentina + Puentes + Religiosos + Fines de semana\n")
        f.write("X-WR-TIMEZONE:America/Argentina/Buenos_Aires\n")

        # 1. Feriados oficiales (incluye trasladables en ambas fechas)
        for fecha, nombre in sorted(ar.items()):
            escribir_evento(f, fecha, f"{nombre} 🇦🇷")

        # 2. Puentes turísticos oficiales 2025-2029 (actualizados al decreto más reciente)
        puentes = {
            2025: ["2025-03-21", "2025-05-23", "2025-12-05"],
            2026: ["2026-03-27", "2026-05-22", "2026-12-04"],
            2027: ["2027-04-23", "2027-06-18", "2027-12-06"],
            2028: ["2028-04-14", "2028-05-26", "2028-12-08"],
            2029: ["2029-04-06", "2029-06-22", "2029-12-07"],
        }
        for fecha_str in puentes.get(anio, []):
            fecha = date.fromisoformat(fecha_str.replace("-",
