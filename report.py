import csv
import html
import sys
from collections import defaultdict
from pathlib import Path


def build_report(source, destination):
    with open(source, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    totals = defaultdict(float)
    for row in rows:
        totals[row["category"]] += float(row["amount"])
    cards = "".join(f"<li><strong>{html.escape(key)}</strong>: ${value:,.2f}</li>"
                    for key, value in sorted(totals.items()))
    table = "".join("<tr>" + "".join(f"<td>{html.escape(str(row[field]))}</td>"
                                      for field in ("date", "product", "category", "amount")) + "</tr>"
                    for row in rows)
    page = f"""<!doctype html><meta charset='utf-8'><title>Reporte de ventas</title>
<style>body{{font:16px system-ui;max-width:900px;margin:40px auto}} table{{border-collapse:collapse;width:100%}}td,th{{padding:8px;border:1px solid #ddd;text-align:left}}</style>
<h1>Reporte de ventas</h1><p>Registros: {len(rows)}</p><ul>{cards}</ul>
<table><thead><tr><th>Fecha</th><th>Producto</th><th>Categoría</th><th>Importe</th></tr></thead><tbody>{table}</tbody></table>"""
    Path(destination).write_text(page, encoding="utf-8")
    print(f"Reporte generado: {destination}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python report.py ventas.csv reporte.html")
    build_report(sys.argv[1], sys.argv[2])
