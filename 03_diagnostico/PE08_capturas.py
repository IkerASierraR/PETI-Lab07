"""PE08 · Capturas de las salidas de consola — DICOSUR (Taller 07, SI-886).

Convierte cada salida registrada en docs/evidencias/S07/salidas/*.txt en una
imagen PNG con estilo de terminal (docs/evidencias/S07/capturas/), para que el
informe muestre la ejecución y enlace el archivo de texto original en GitHub.

Uso (desde la raíz del repositorio):
    python 03_diagnostico/PE08_capturas.py
"""
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parent
S07 = BASE.parent / "docs" / "evidencias" / "S07"
SALIDAS = S07 / "salidas"
CAPTURAS = S07 / "capturas"
CAPTURAS.mkdir(parents=True, exist_ok=True)

PROMPT = "PS C:\\Taller07_SierraIker> "
CAPTURAS_A_GENERAR = [
    ("salida_PE02_matrices.txt", "python 03_diagnostico/PE02_matrices.py", "captura_PE02_matrices.png"),
    ("salida_PE04_prioriza.txt", "python 03_diagnostico/PE04_prioriza_estrategias.py", "captura_PE04_prioriza.png"),
    ("salida_PE06_validacion_inicial.txt", "python 03_diagnostico/PE06_valida.py   # primera ejecución", "captura_PE06_validacion_inicial.png"),
    ("salida_PE06_validacion.txt", "python 03_diagnostico/PE06_valida.py   # después de corregir", "captura_PE06_validacion.png"),
    ("salida_git_log.txt", "git log --oneline --decorate", "captura_git_log.png"),
]


def color(linea):
    if "[FALLA]" in linea or "[ALERTA]" in linea:
        return "#FF6B6B"
    if "[OK]" in linea or "todas las comprobaciones pasaron" in linea:
        return "#7CD67C"
    if linea.startswith("=") or linea.isupper():
        return "#6CB6FF"
    if "->" in linea or "→" in linea:
        return "#F5D76E"
    return "#D4D4D4"


def captura(txt, comando, png):
    lineas = (SALIDAS / txt).read_text(encoding="utf-8").rstrip().splitlines()
    lineas = [PROMPT + comando] + lineas
    ancho = max(len(l) for l in lineas)
    alto = len(lineas)
    fig = plt.figure(figsize=(max(8, ancho * 0.075), 0.6 + alto * 0.165))
    fig.patch.set_facecolor("#1E1E1E")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#1E1E1E")
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, alto + 2)
    ax.add_patch(plt.Rectangle((0, alto + 1), 1, 1, color="#333333"))
    for k, c in enumerate(("#FF5F56", "#FFBD2E", "#27C93F")):
        ax.text(0.012 + k * 0.014, alto + 1.5, "●", ha="center", va="center", color=c, fontsize=10)
    ax.text(0.5, alto + 1.5, "Windows PowerShell · " + txt, ha="center", va="center", color="#BBBBBB", fontsize=8,
            family="monospace")
    for n, l in enumerate(lineas):
        ax.text(0.01, alto - n + 0.3, l, ha="left", va="center", fontsize=8.2, family="monospace",
                color="#4EC9B0" if n == 0 else color(l))
    fig.savefig(CAPTURAS / png, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  docs/evidencias/S07/capturas/{png}")


def vista_previa(xlsx, hoja, columnas, anchos, png, titulo, filas=None):
    """Imagen de la hoja de un anexo .xlsx, para insertarla en el informe."""
    df = pd.read_excel(S07 / xlsx, sheet_name=hoja, header=3)[columnas].dropna(how="all")
    if filas:
        df = df.head(filas)
    celdas = [[textwrap.fill(str(v), max(int(a * 0.8), 3)) for v, a in zip(fila, anchos)] for fila in df.itertuples(index=False)]
    alto = sum(max(c.count("\n") + 1 for c in fila) for fila in celdas)
    fig = plt.figure(figsize=(10, 1.0 + alto * 0.21))
    ax = fig.add_axes([0.01, 0.01, 0.98, 0.9])
    ax.axis("off")
    fig.suptitle(titulo, fontsize=12, fontweight="bold", color="#1F2D5C", x=0.01, ha="left")
    t = ax.table(cellText=celdas, colLabels=[textwrap.shorten(c, a + 2, placeholder="…") for c, a in zip(columnas, anchos)],
                 loc="upper left", cellLoc="left",
                 colWidths=[a / sum(anchos) for a in anchos])
    t.auto_set_font_size(False)
    t.set_fontsize(8)
    for (r, c), cel in t.get_celld().items():
        n = 1 if r == 0 else max(v.count("\n") + 1 for v in celdas[r - 1])
        cel.set_height(0.95 / (alto + 1) * max(n, 1))
        if r == 0:
            cel.set_facecolor("#1F2D5C")
            cel.get_text().set_color("white")
            cel.get_text().set_fontweight("bold")
    fig.savefig(CAPTURAS / png, dpi=150)
    plt.close(fig)
    print(f"  docs/evidencias/S07/capturas/{png}")


def vista_previa_pdf(pdf, png):
    try:
        import pymupdf
    except ImportError:
        print("  [AVISO] pymupdf no instalado: sin vista previa del anexo F")
        return
    doc = pymupdf.open(S07 / pdf)
    doc[0].get_pixmap(dpi=110).save(CAPTURAS / png)
    print(f"  docs/evidencias/S07/capturas/{png}")


if __name__ == "__main__":
    print("PE08 · Capturas generadas:")
    for txt, comando, png in CAPTURAS_A_GENERAR:
        if (SALIDAS / txt).exists():
            captura(txt, comando, png)
        else:
            print(f"  [AVISO] falta {txt}")
    print("PE08 · Vistas previas de los anexos:")
    vista_previa("anexo_A_pestel.xlsx", "PESTEL", ["id", "Dimensión", "Factor", "Evidencia con cifra", "Tipo (O/A)", "Intensidad (1–5)", "Decisión que obliga"],
                 [6, 12, 26, 46, 8, 9, 34], "preview_anexo_A.png", "Anexo A · anexo_A_pestel.xlsx (vista previa)")
    vista_previa("anexo_B_matrices_efi_efe.xlsx", "EFE", ["id", "factor", "origen", "peso", "calificacion", "justificacion_calificacion"],
                 [4, 34, 24, 6, 8, 54], "preview_anexo_B.png", "Anexo B · anexo_B_matrices_efi_efe.xlsx · hoja EFE (vista previa)", 12)
    vista_previa("anexo_D_estrategias_priorizadas.xlsx", "Priorización", ["orden", "id", "Tipo", "Factores cruzados", "puntaje", "Prioridad preliminar", "Proyecto candidato"],
                 [5, 6, 5, 14, 7, 10, 52], "preview_anexo_D.png", "Anexo D · anexo_D_estrategias_priorizadas.xlsx (vista previa)")
    vista_previa("anexo_E_trazabilidad.xlsx", "Trazabilidad", ["Evidencia del diagnóstico", "Sección de origen", "Factor F/D/O/A", "Estrategia", "Proyecto (Sección 7.1)"],
                 [46, 26, 10, 10, 40], "preview_anexo_E.png", "Anexo E · anexo_E_trazabilidad.xlsx (vista previa)")
    vista_previa_pdf("anexo_F_secciones_3_3_a_3_5.pdf", "preview_anexo_F.png")
