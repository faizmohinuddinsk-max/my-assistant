"""
theme.py — shared colors for the assistant's app (app.py).
Palette: black / cyan / grey, based on the earlier OceanPulse-style layout.
"""

import flet as ft

BLACK = "#0A0A0C"
BLACK_DEEP = "#000000"
CYAN = "#22D3EE"
CYAN_DIM = "#0E7490"
GREY_BG = "#F1F2F4"
CARD = "#FFFFFF"
INK = "#111114"
INK_SOFT = "#6B7280"
LINE = "#E2E4E8"

# status accents (kept semantic, not part of brand palette)
AMBER = "#E2A23D"
CORAL = "#E2664F"
GREEN_OK = "#2FA35A"

RADIUS_LG = 20
RADIUS_MD = 14
RADIUS_SM = 10


def header_gradient():
    return ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=[BLACK, BLACK_DEEP],
    )


def card_container(content, padding=16):
    return ft.Container(
        content=content,
        bgcolor=CARD,
        border_radius=RADIUS_LG,
        padding=padding,
        shadow=ft.BoxShadow(blur_radius=18, color="#0A0A0C14", offset=ft.Offset(0, 6)),
    )
