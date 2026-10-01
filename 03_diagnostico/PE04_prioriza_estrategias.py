"""PE04 · Priorización preliminar de estrategias — DICOSUR (Taller 07, SI-886).

Puntaje = suma de los pesos (EFI/EFE) de los factores que cruza la estrategia
          × bono por tipo (supervivencia primero: DA > FA > DO > FO).

Uso (desde la raíz del repositorio):
    python 03_diagnostico/PE04_prioriza_estrategias.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parent
SALIDAS = BASE.parent / "docs" / "evidencias" / "S07" / "salidas"
SALIDAS.mkdir(parents=True, exist_ok=True)

e = pd.read_csv(BASE / "PE03_foda_cruzado.csv")
efi = pd.read_csv(BASE / "PE02_matriz_efi.csv").set_index("id")
efe = pd.read_csv(BASE / "PE02_matriz_efe.csv").set_index("id")
pesos = pd.concat([efi.peso, efe.peso])


def codigos(fs):
    return [f.strip() for f in fs.replace("+", " ").split()]


def peso_estrategia(fs):
    return round(sum(pesos.get(f, 0) for f in codigos(fs)), 3)


desconocidos = sorted({c for fs in e["Factores cruzados"] for c in codigos(fs) if c not in pesos.index})
if desconocidos:
    print(f"[ALERTA] Códigos que no existen en la EFI ni en la EFE (pesan 0): {', '.join(desconocidos)}\n")

e["peso_factores"] = e["Factores cruzados"].apply(peso_estrategia)
BONO = {"DA": 1.35, "FA": 1.20, "DO": 1.10, "FO": 1.00}   # supervivencia primero
e["puntaje"] = (e.peso_factores * e.Tipo.map(BONO)).round(3)
e = e.sort_values("puntaje", ascending=False)
e.insert(0, "orden", range(1, len(e) + 1))
e.to_csv(BASE / "PE04_estrategias_priorizadas.csv", index=False)

print(e[["orden", "id", "Tipo", "peso_factores", "puntaje", "Proyecto candidato"]].to_string(index=False))
print("\nDistribución por tipo:\n", e.Tipo.value_counts().sort_index().to_string())
print("\nPuntaje medio por tipo:\n", e.groupby("Tipo").puntaje.mean().round(3).sort_values(ascending=False).to_string())
top = e.head(5)
print("\nCinco primeras estrategias por tipo:", ", ".join(f"{i} ({t})" for i, t in zip(top.id, top.Tipo)))
if (top.Tipo == "DA").sum() + (top.Tipo == "FA").sum() >= 3:
    print("\n→ Predominan DA y FA en la parte alta: la organización está en posición defensiva;")
    print("  el PETI debe priorizar continuidad y cumplimiento antes que transformación.")
else:
    print("\n→ Predominan FO y DO en la parte alta: la organización puede priorizar crecimiento.")

colores = {"DA": "#C0392B", "FA": "#E67E22", "DO": "#2E86C1", "FO": "#27AE60"}
fig, ax = plt.subplots(figsize=(10, 5.5))
orden = e.iloc[::-1]
ax.barh([f"{i} · {p[:42]}" for i, p in zip(orden.id, orden["Proyecto candidato"])], orden.puntaje,
        color=[colores[t] for t in orden.Tipo])
for y, v in enumerate(orden.puntaje):
    ax.text(v + 0.004, y, f"{v:.3f}", va="center", fontsize=8)
ax.set_xlabel("Puntaje = Σ pesos de los factores cruzados × bono por tipo")
ax.set_title("DICOSUR · priorización preliminar de estrategias", fontweight="bold")
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for c in colores.values()], labels=list(colores.keys()),
          loc="lower right")
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(SALIDAS / "PE04_priorizacion.png", dpi=160)
plt.close(fig)
print("\nArchivos generados:\n  03_diagnostico/PE04_estrategias_priorizadas.csv\n  docs/evidencias/S07/salidas/PE04_priorizacion.png")
