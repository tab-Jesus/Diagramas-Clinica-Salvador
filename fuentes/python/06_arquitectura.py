from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(9.6, 7.4))
ax.set_xlim(0, 96); ax.set_ylim(0, 72); ax.axis("off")

LX, LW = 2, 62          # x y ancho de las capas
H = 10.6                # alto de cada capa
GAP = 3.2
tops = [70 - i*(H+GAP) for i in range(5)]

capas = [
    ("CAPA DE PRESENTACIÓN", "Aplicación web SPA (React + TypeScript)\nFormulario de cita · Búsqueda de paciente\nCalendario de disponibilidad", "#FFFFFF"),
    ("CAPA DE API", "Controladores REST (Spring Web) · DTOs\nValidación de entrada · Documentación OpenAPI", "#F2F2F2"),
    ("CAPA DE APLICACIÓN / DOMINIO", "PacienteService · AgendaService\nCitaService · NotificacionService\nReglas de negocio de agendamiento", "#E6E6E6"),
    ("CAPA DE PERSISTENCIA", "Repositorios (Spring Data JPA)\nTransacciones y bloqueo de franjas", "#F2F2F2"),
    ("CAPA DE DATOS", "PostgreSQL — pacientes, médicos, horarios, citas, usuarios", "#FFFFFF"),
]

for (titulo, detalle, color), top in zip(capas, tops):
    box = FancyBboxPatch((LX, top-H), LW, H, boxstyle="round,pad=0.2,rounding_size=1.2",
                         linewidth=1.6, edgecolor="black", facecolor=color)
    ax.add_patch(box)
    ax.text(LX+LW/2, top-2.6, titulo, ha="center", va="center", fontsize=11.5, fontweight="bold")
    ax.text(LX+LW/2, top-6.9, detalle, ha="center", va="center", fontsize=9.6, linespacing=1.45)

# Flechas entre capas
etiquetas = ["HTTPS / JSON", "invoca servicios", "usa repositorios", "JDBC"]
for i in range(4):
    y1 = tops[i]-H-0.2; y2 = tops[i+1]+0.2
    ax.add_patch(FancyArrowPatch((LX+LW/2, y1), (LX+LW/2, y2), arrowstyle="-|>",
                                 mutation_scale=16, linewidth=1.5, color="black"))
    ax.text(LX+LW/2+1.8, (y1+y2)/2, etiquetas[i], fontsize=8.8, va="center", style="italic")

# Bloque de aspectos transversales (capas 2 a 4)
tx_top = tops[1]; tx_bot = tops[3]-H
TXx, TXw = 70, 24
tx = FancyBboxPatch((TXx, tx_bot), TXw, tx_top-tx_bot, boxstyle="round,pad=0.2,rounding_size=1.2",
                    linewidth=1.6, edgecolor="black", facecolor="#FAFAFA", linestyle=(0,(5,3)))
ax.add_patch(tx)
ax.text(TXx+TXw/2, tx_top-3, "ASPECTOS\nTRANSVERSALES", ha="center", va="center", fontsize=11, fontweight="bold")
items = ["Seguridad\n(JWT + roles)", "Auditoría", "Registro de eventos\n(logging)", "Manejo de errores", "Validaciones"]
yy = tx_top-9.5
for it in items:
    n = it.count("\n")+1
    h = 3.4 + 1.9*(n-1)
    ax.add_patch(FancyBboxPatch((TXx+2, yy-h), TXw-4, h, boxstyle="round,pad=0.1,rounding_size=0.8",
                                linewidth=1.1, edgecolor="black", facecolor="white"))
    ax.text(TXx+TXw/2, yy-h/2, it, ha="center", va="center", fontsize=8.8, linespacing=1.3)
    yy -= h + 1.5

# Conectores punteados capas 2-4 -> transversales
for i in (1, 2, 3):
    ym = tops[i]-H/2
    ax.add_patch(FancyArrowPatch((LX+LW+0.3, ym), (TXx-0.3, ym), arrowstyle="-", linewidth=1.1,
                                 linestyle=(0,(3,3)), color="black"))

salida = Path(__file__).resolve().parents[2] / "diagramas" / "06_arquitectura.png"
salida.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(salida, dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.15)
print(salida)
