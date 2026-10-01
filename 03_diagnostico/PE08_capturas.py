"""PE08 · Capturas de las salidas de consola — DICOSUR (Taller 07, SI-886).

Convierte cada salida registrada en docs/evidencias/S07/salidas/*.txt en una
imagen PNG con estilo de terminal (docs/evidencias/S07/capturas/), para que el
informe muestre la ejecución y enlace el archivo de texto original en GitHub.

Uso (desde la raíz del repositorio):
    python 03_diagnostico/PE08_capturas.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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


if __name__ == "__main__":
    print("PE08 · Capturas generadas:")
    for txt, comando, png in CAPTURAS_A_GENERAR:
        if (SALIDAS / txt).exists():
            captura(txt, comando, png)
        else:
            print(f"  [AVISO] falta {txt}")
