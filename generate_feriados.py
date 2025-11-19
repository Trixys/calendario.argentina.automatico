import holidays
from datetime import datetime, timedelta

def generar_ics(anio):
    ar = holidays.AR(years=anio)
    filename = f"feriados_argentina_{anio}.ics"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCALENDAR
")
        f.write("VERSION:2.0
")
        f.write("PRODID:-//FeriadosAR//Calendario Automático//ES\n")

        for fecha, nombre in ar.items():
            f.write("BEGIN:VEVENT
")
            f.write(f"DTSTART;VALUE=DATE:{fecha.strftime('%Y%m%d')}\n")
            f.write(f"DTEND;VALUE=DATE:{(fecha + timedelta(days=1)).strftime('%Y%m%d')}\n")
            f.write(f"SUMMARY:{nombre}\n")
            f.write("END:VEVENT\n")

        f.write("END:VCALENDAR\n")

    print(f"Generado: {filename}")

if __name__ == "__main__":
    year = datetime.now().year
    generar_ics(year)
    generar_ics(year + 1)
    generar_ics(year + 2)
