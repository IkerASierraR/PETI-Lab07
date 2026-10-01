"""PE06 · Paso E — Validar y corregir — DICOSUR (Taller 07, SI-886).

Ejecuta las tres comprobaciones del taller y termina con código 1 si alguna falla:
  1. Cada factor de la EFI y la EFE viene de una sección del diagnóstico, citada
     (y cada factor PESTEL tiene fuente con año y decisión que obliga).
  2. Los pesos de las matrices suman uno y las calificaciones están fundamentadas
     (en la EFE, la justificación debe describir la RESPUESTA de la organización).
  3. Cada estrategia cruzada nombra los códigos que cruza y no es una frase general.

Uso (desde la raíz del repositorio):
    python 03_diagnostico/PE06_valida.py
"""
import re
import sys
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
pestel = pd.read_csv(BASE / "PE01_pestel.csv")
efi = pd.read_csv(BASE / "PE02_matriz_efi.csv")
efe = pd.read_csv(BASE / "PE02_matriz_efe.csv")
foda = pd.read_csv(BASE / "PE03_foda_cruzado.csv")
traz = pd.read_csv(BASE / "PE05_trazabilidad.csv")

# Frases que describen la respuesta de la organización, según la escala de la EFE
RESPUESTA = {1: "Respuesta deficiente", 2: "Por debajo del promedio", 3: "Por encima del promedio", 4: "Respuesta superior"}
DIMENSIONES = {"Político", "Económico", "Social", "Tecnológico", "Ecológico/Ético", "Legal"}

fallas = []


def registra(ok, mensaje):
    print(f"  [{'OK' if ok else 'FALLA'}] {mensaje}")
    if not ok:
        fallas.append(mensaje)


def vacio(v):
    return pd.isna(v) or str(v).strip() == ""


print("=" * 72)
print("PE06 · VALIDACIÓN DEL TALLER 07 · DICOSUR")
print("=" * 72)

# ---------------------------------------------------------------- 1
print("\nComprobación 1 · Cada factor viene de una sección del diagnóstico, citada")
for nombre, df in (("EFI", efi), ("EFE", efe)):
    sin = [r.id for r in df.itertuples() if vacio(r.origen) or not str(r.origen).startswith("Sección")]
    registra(not sin, f"{nombre}: {len(df) - len(sin)}/{len(df)} factores con sección de origen" + (f" · sin origen: {', '.join(sin)}" if sin else ""))
dims = set(pestel["Dimensión"])
registra(DIMENSIONES <= dims, f"PESTEL: {len(DIMENSIONES & dims)}/6 dimensiones con al menos un factor")
sin_fuente = [r[0] for r in pestel.itertuples(index=False) if not re.search(r"(19|20)\d\d", str(r[4]))]
registra(not sin_fuente, f"PESTEL: {len(pestel) - len(sin_fuente)}/{len(pestel)} factores con fuente institucional y año")
sin_dec = pestel[pestel["Decisión que obliga"].apply(vacio)].id.tolist()
registra(not sin_dec, f"PESTEL: {len(sin_dec)} factores sin «decisión que obliga»")
pestel_efe = [r for r in efe.origen if str(r).startswith("Sección 3.3")]
no_existe = [r for r in pestel_efe if r.split()[-1] not in set(pestel.id)]
registra(not no_existe, "EFE: las citas a la Sección 3.3 apuntan a factores PESTEL existentes")

# ---------------------------------------------------------------- 2
print("\nComprobación 2 · Pesos que suman uno y calificaciones fundamentadas")
for nombre, df in (("EFI", efi), ("EFE", efe)):
    s = round(df.peso.sum(), 4)
    registra(abs(s - 1) < 1e-6, f"{nombre}: suma de pesos = {s:.2f}")
    fuera = df[~df.calificacion.between(1, 4)].id.tolist()
    registra(not fuera, f"{nombre}: calificaciones dentro de la escala 1-4")
    sin_j = df[df.justificacion_peso.apply(vacio) | df.justificacion_calificacion.apply(vacio)].id.tolist()
    registra(not sin_j, f"{nombre}: cada peso y cada calificación tienen justificación")
efi_mal = [r.id for r in efi.itertuples() if (r.id.startswith("F") and r.calificacion < 3) or (r.id.startswith("D") and r.calificacion > 2)]
registra(not efi_mal, "EFI: fortalezas calificadas 3-4 y debilidades 1-2" + (f" · revisar {', '.join(efi_mal)}" if efi_mal else ""))
efe_mal = [f"{r.id} (calif. {r.calificacion}: «{str(r.justificacion_calificacion)[:40]}…»)"
           for r in efe.itertuples() if not str(r.justificacion_calificacion).startswith(RESPUESTA[int(r.calificacion)])]
registra(not efe_mal, "EFE: cada calificación mide la respuesta de la organización, no la gravedad"
         + (f" · revisar {'; '.join(efe_mal)}" if efe_mal else ""))

# ---------------------------------------------------------------- 3
print("\nComprobación 3 · Cada estrategia nombra los códigos que cruza")
validos = set(efi.id) | set(efe.id)
conteo = foda.Tipo.value_counts()
registra(len(foda) >= 12 and all(conteo.get(t, 0) >= 3 for t in ("FO", "FA", "DO", "DA")),
         f"FODA cruzado: {len(foda)} estrategias · " + " · ".join(f"{t} {conteo.get(t, 0)}" for t in ("FO", "FA", "DO", "DA")))
for r in foda.itertuples(index=False):
    cods = [c.strip() for c in r[2].replace("+", " ").split()]
    problemas = []
    desconocidos = [c for c in cods if c not in validos]
    if desconocidos:
        problemas.append(f"códigos inexistentes {', '.join(desconocidos)}")
    letras = {c[0] for c in cods}
    if letras != set(r[1]):
        problemas.append(f"el tipo {r[1]} no coincide con los códigos {', '.join(cods)}")
    no_citados = [c for c in cods if f"({c})" not in r[3]]
    if no_citados:
        problemas.append(f"el texto no cita {', '.join(no_citados)}: frase general")
    if vacio(r[5]):
        problemas.append("sin proyecto candidato")
    registra(not problemas, f"{r[0]} ({r[1]}, {r[2]})" + (" · " + "; ".join(problemas) if problemas else ""))

print("\nTrazabilidad")
cods_traz = {c.strip() for v in traz["Factor F/D/O/A"] for c in str(v).split("·")}
registra(len(traz) >= 12, f"PE05_trazabilidad.csv: {len(traz)} filas (mínimo 12)")
registra(cods_traz <= validos, "PE05_trazabilidad.csv: todos los factores existen en la EFI o la EFE")
ests = {e.strip() for v in traz.Estrategia for e in str(v).split(",")}
registra(ests == set(foda.id), f"PE05_trazabilidad.csv: cubre {len(ests & set(foda.id))}/{len(foda)} estrategias")

print("\n" + "=" * 72)
if fallas:
    print(f"RESULTADO: {len(fallas)} comprobaciones fallidas. Corregir antes de cerrar la sesión.")
    sys.exit(1)
print("RESULTADO: todas las comprobaciones pasaron.")
