# Taller 07 · Matrices EFI, EFE, PESTEL y FODA cruzado — Caso DICOSUR

**SI-886 · Planeamiento Estratégico de TI** · Semana 07 · Universidad Privada de Tacna

Organización analizada: **Distribuidora Comercial del Sur S.A.C. (DICOSUR)**, empresa de distribución y logística comercial de Tacna (48 colaboradores, 8 400 clientes minoristas).

> Documento clasificado **Confidencial**. Las debilidades de seguridad se describen sin detalle técnico explotable y los factores derivados de entrevistas se registran por cargo.

## Contenido

```
.
├── 03_diagnostico/
│   ├── PE01_pestel.csv                    # Paso A · PESTEL con evidencia y decisión que obliga
│   ├── PE02_matriz_efi.csv                # Paso B · factores internos, pesos y calificaciones
│   ├── PE02_matriz_efe.csv                # Paso B · factores externos, pesos y calificaciones
│   ├── PE02_matrices.py                   # Paso B · cálculo de EFI, EFE y posición IE
│   ├── PE03_foda_cruzado.csv              # Paso C · 12 estrategias FO, FA, DO y DA
│   ├── PE04_prioriza_estrategias.py       # Paso C · priorización de estrategias
│   ├── PE04_estrategias_priorizadas.csv   # Paso C · salida de la priorización
│   ├── PE05_trazabilidad.csv              # Paso D · evidencia → factor → estrategia → objetivo → proyecto
│   ├── PE06_valida.py                     # Paso E · las tres comprobaciones
│   ├── PE07_genera_anexos.py              # Anexos A–F y figuras
│   ├── PE08_capturas.py                   # Capturas de las salidas de consola
│   ├── 3.3_pestel.md                      # Sección 3.3 del PETI
│   ├── 3.4_foda.md                        # Sección 3.4 del PETI
│   └── 3.5_estrategias.md                 # Sección 3.5 del PETI
├── docs/evidencias/S07/
│   ├── salidas/                           # salidas de consola (.txt), CSV y gráficos
│   ├── capturas/                          # capturas de las salidas de consola
│   └── anexo_A … anexo_F                  # anexos del informe
└── informe/                               # informe del taller en PDF
```

## Cómo se reproduce

```bash
python -m pip install pandas matplotlib openpyxl python-docx
python 03_diagnostico/PE02_matrices.py
python 03_diagnostico/PE04_prioriza_estrategias.py
python 03_diagnostico/PE06_valida.py
python 03_diagnostico/PE07_genera_anexos.py
python 03_diagnostico/PE08_capturas.py
```

Los scripts se ejecutan desde la raíz del repositorio. Las rutas se resuelven respecto de cada script, así que también funcionan desde `03_diagnostico/`.

## Etiquetas

| Etiqueta | Qué marca |
|---|---|
| `v0.7` | PETI v0.7 — diagnóstico estratégico con estrategias derivadas (secciones 3.3 a 3.5) |
| `taller-07` | Commit entregado del Taller 07 |
