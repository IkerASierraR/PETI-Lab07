"""PE02 · Matrices EFI y EFE — DICOSUR (Taller 07, SI-886).

Lee PE02_matriz_efi.csv y PE02_matriz_efe.csv, comprueba pesos y escalas,
calcula los totales ponderados, los interpreta frente al promedio de 2.5
y ubica a la organización en la matriz interna-externa (IE).

Uso (desde la raíz del repositorio):
    python 03_diagnostico/PE02_matrices.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parent
SALIDAS = BASE.parent / "docs" / "evidencias" / "S07" / "salidas"
SALIDAS.mkdir(parents=True, exist_ok=True)

PROMEDIO = 2.5


def cargar(nombre):
    df = pd.read_csv(BASE / nombre)
    df["ponderado"] = (df.peso * df.calificacion).round(3)
    return df


def revisar(df, nombre):
    ok = True
    suma = round(df.peso.sum(), 4)
    if abs(suma - 1) > 1e-6:
        print(f"  [ALERTA] {nombre}: los pesos suman {suma:.2f}, deben sumar 1.00")
        ok = False
    else:
        print(f"  [OK] {nombre}: los pesos suman {suma:.2f}")
    fuera = df[~df.calificacion.between(1, 4)]
    if len(fuera):
        print(f"  [ALERTA] {nombre}: calificaciones fuera de la escala 1-4 en {', '.join(fuera.id)}")
        ok = False
    sin_origen = df[df.origen.isna() | (df.origen.astype(str).str.strip() == "")]
    if len(sin_origen):
        print(f"  [ALERTA] {nombre}: factores sin sección de origen citada: {', '.join(sin_origen.id)}")
        ok = False
    return ok


def tabla(df):
    t = df[["id", "factor", "peso", "calificacion", "ponderado"]].copy()
    t["factor"] = t.factor.str.slice(0, 52)
    return t.to_string(index=False)


def interpretar(total, matriz):
    if matriz == "EFI":
        if total >= 3.0:
            return "posición interna fuerte"
        if total >= PROMEDIO:
            return "posición interna promedio, con fortalezas que compensan las debilidades"
        return "posición interna débil: las debilidades pesan más que las fortalezas"
    if total >= 3.0:
        return "respuesta superior al entorno"
    if total >= PROMEDIO:
        return "respuesta promedio al entorno"
    return "respuesta deficiente: la organización no aprovecha las oportunidades ni se defiende de las amenazas"


def celda_ie(efi, efe):
    col = 0 if efi >= 3 else (1 if efi >= 2 else 2)
    fila = 0 if efe >= 3 else (1 if efe >= 2 else 2)
    celdas = [["I", "II", "III"], ["IV", "V", "VI"], ["VII", "VIII", "IX"]]
    c = celdas[fila][col]
    if c in ("I", "II", "IV"):
        estrategia = "crecer y construir"
    elif c in ("III", "V", "VII"):
        estrategia = "conservar y mantener"
    else:
        estrategia = "cosechar o desinvertir (posición defensiva)"
    return c, estrategia


def graficos(efi, efe, t_efi, t_efe):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    for ax, df, titulo, total in ((axes[0], efi, "Matriz EFI", t_efi), (axes[1], efe, "Matriz EFE", t_efe)):
        colores = ["#1F6FB2" if i[0] in "FO" else "#C0392B" for i in df.id]
        ax.barh(df.id[::-1], df.ponderado[::-1], color=colores[::-1])
        for y, v in enumerate(df.ponderado[::-1]):
            ax.text(v + 0.005, y, f"{v:.2f}", va="center", fontsize=8)
        ax.set_title(f"{titulo} · total ponderado {total:.2f}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Peso × calificación")
        ax.grid(axis="x", alpha=0.3)
    axes[0].text(0.98, 0.02, "azul: fortaleza · rojo: debilidad", transform=axes[0].transAxes, ha="right", fontsize=8)
    axes[1].text(0.98, 0.02, "azul: oportunidad · rojo: amenaza", transform=axes[1].transAxes, ha="right", fontsize=8)
    fig.suptitle("DICOSUR · valores ponderados por factor", fontsize=12)
    fig.tight_layout()
    fig.savefig(SALIDAS / "PE02_matrices_efi_efe.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.2, 6))
    nombres = [["I", "II", "III"], ["IV", "V", "VI"], ["VII", "VIII", "IX"]]
    tonos = {"I": "#D5E8D4", "II": "#D5E8D4", "IV": "#D5E8D4", "III": "#FFF2CC", "V": "#FFF2CC",
             "VII": "#FFF2CC", "VI": "#F8CECC", "VIII": "#F8CECC", "IX": "#F8CECC"}
    for f in range(3):
        for c in range(3):
            x0, y0 = 4 - c, 4 - f
            ax.add_patch(plt.Rectangle((x0 - 1, y0 - 1), 1, 1, facecolor=tonos[nombres[f][c]], edgecolor="#555"))
            ax.text(x0 - 0.5, y0 - 0.5, nombres[f][c], ha="center", va="center", fontsize=14, color="#555")
    ax.plot(t_efi, t_efe, "o", color="#16285C", markersize=12)
    ax.annotate(f"DICOSUR\nEFI {t_efi:.2f} · EFE {t_efe:.2f}", (t_efi, t_efe), xytext=(t_efi + 0.35, t_efe + 0.45),
                arrowprops=dict(arrowstyle="->"), fontsize=9, fontweight="bold")
    ax.set_xlim(4, 1)
    ax.set_ylim(1, 4)
    ax.set_xticks([4, 3, 2, 1])
    ax.set_yticks([1, 2, 3, 4])
    ax.set_xlabel("Total ponderado EFI (fuerte → débil)")
    ax.set_ylabel("Total ponderado EFE (bajo → alto)")
    ax.set_title("Matriz interna-externa (IE)", fontweight="bold")
    fig.tight_layout()
    fig.savefig(SALIDAS / "PE02_matriz_ie.png", dpi=160)
    plt.close(fig)


def main():
    efi = cargar("PE02_matriz_efi.csv")
    efe = cargar("PE02_matriz_efe.csv")

    print("=" * 72)
    print("PE02 · MATRICES EFI Y EFE · DICOSUR")
    print("=" * 72)
    print("\n1. Comprobación de pesos, escalas y origen")
    ok = revisar(efi, "EFI") & revisar(efe, "EFE")

    t_efi = round(efi.ponderado.sum(), 2)
    t_efe = round(efe.ponderado.sum(), 2)

    print("\n2. Matriz EFI (calificación 1-4: intensidad del factor interno)")
    print(tabla(efi))
    f = efi[efi.id.str.startswith("F")].ponderado.sum()
    d = efi[efi.id.str.startswith("D")].ponderado.sum()
    print(f"\n  Fortalezas: {f:.2f} · Debilidades: {d:.2f} · TOTAL EFI = {t_efi:.2f}")
    print(f"  -> {interpretar(t_efi, 'EFI')} (promedio de referencia {PROMEDIO})")

    print("\n3. Matriz EFE (calificación 1-4: qué tan bien RESPONDE la organización)")
    print(tabla(efe))
    o = efe[efe.id.str.startswith("O")].ponderado.sum()
    a = efe[efe.id.str.startswith("A")].ponderado.sum()
    print(f"\n  Oportunidades: {o:.2f} · Amenazas: {a:.2f} · TOTAL EFE = {t_efe:.2f}")
    print(f"  -> {interpretar(t_efe, 'EFE')} (promedio de referencia {PROMEDIO})")

    celda, estrategia = celda_ie(t_efi, t_efe)
    print("\n4. Posición en la matriz interna-externa (IE)")
    print(f"  EFI {t_efi:.2f} · EFE {t_efe:.2f} -> celda {celda}: {estrategia}")

    resumen = pd.DataFrame([
        {"matriz": "EFI", "total": t_efi, "positivo": round(f, 2), "negativo": round(d, 2), "interpretacion": interpretar(t_efi, "EFI")},
        {"matriz": "EFE", "total": t_efe, "positivo": round(o, 2), "negativo": round(a, 2), "interpretacion": interpretar(t_efe, "EFE")},
    ])
    resumen.to_csv(SALIDAS / "PE02_resumen_matrices.csv", index=False)
    pd.concat([efi.assign(matriz="EFI"), efe.assign(matriz="EFE")]).to_csv(SALIDAS / "PE02_matrices_calculadas.csv", index=False)
    graficos(efi, efe, t_efi, t_efe)
    print("\n5. Archivos generados")
    for n in ("PE02_resumen_matrices.csv", "PE02_matrices_calculadas.csv", "PE02_matrices_efi_efe.png", "PE02_matriz_ie.png"):
        print(f"  docs/evidencias/S07/salidas/{n}")
    print("\n" + ("[OK] Matrices consistentes." if ok else "[ALERTA] Revise los avisos antes de usar los totales."))


if __name__ == "__main__":
    main()
