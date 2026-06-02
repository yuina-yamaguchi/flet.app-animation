import random
from math import pi

import flet as ft


def main(page: ft.Page):
    size = 40
    gap = 5
    duration = 2000

    RED = ft.Colors.RED_800
    BLACK = "#1a1a1a"

    all_colors = [
        ft.Colors.AMBER_400,
        ft.Colors.AMBER_ACCENT_400,
        ft.Colors.BLUE_400,
        ft.Colors.BROWN_400,
        ft.Colors.CYAN_700,
        ft.Colors.DEEP_ORANGE_500,
        ft.Colors.CYAN_500,
        ft.Colors.INDIGO_600,
        ft.Colors.ORANGE_ACCENT_100,
        ft.Colors.PINK,
        ft.Colors.RED_600,
        ft.Colors.GREEN_400,
        ft.Colors.GREEN_ACCENT_200,
        ft.Colors.TEAL_ACCENT_200,
        ft.Colors.LIGHT_BLUE_500,
    ]

    # Grid: 10 cols x 9 rows
    #
    # Top half (rows 0-3): N (cols 0-3) and C (cols 5-9) — both RED
    #
    # N shape (cols 0-3, rows 0-3):
    #   col0: full (rows 0-3)
    #   col1: row1
    #   col2: row2
    #   col3: full (rows 0-3)
    #
    # C shape (cols 5-9, rows 0-3):
    #   row0: cols 5-9
    #   col5: rows 0-3
    #   row3: cols 5-9
    #
    # Bottom half (rows 4-8): U shape — BLACK
    #   col0: rows 4-7
    #   col9: rows 4-7
    #   row8: cols 0-9  (bottom arc — wide)
    #   cols 1-8 row 7: part of arc curve
    #
    # U is wide: spans full 10 cols

    parts = []

    # --- N (RED, cols 0-3, rows 0-3) ---
    for row in range(4):
        parts.append((0, row, RED))   # left stroke
    parts.append((1, 1, RED))         # diagonal top
    parts.append((2, 2, RED))         # diagonal bottom
    for row in range(4):
        parts.append((3, row, RED))   # right stroke

    # --- C (RED, cols 5,6,7,8 rows 0-3) --- (旧7→6, 8→7, 9→8)
    for col in [5, 6, 7, 8]:
        parts.append((col, 0, RED))   # top bar
    for row in range(1, 4):
        parts.append((5, row, RED))   # left stroke
    for col in [5, 6, 7, 8]:
        parts.append((col, 3, RED))   # bottom bar

    # --- U (BLACK, cols 0-8, rows 4-8) --- (旧col9→8)
    # Left stroke (cols 0-3)
    for row in range(4, 8):
        parts.append((0, row, BLACK))
    for col in range(1, 4):
        for row in range(4, 7):
            parts.append((col, row, BLACK))
    # Right stroke (旧col9→8)
    for row in range(4, 8):
        parts.append((8, row, BLACK))
    # Bottom arc (row 7 inner + row 8)
    for col in range(1, 8):
        parts.append((col, 7, BLACK))
    for col in range(2, 7):
        parts.append((col, 8, BLACK))

    COLS = 9
    ROWS = 9
    width = COLS * (size + gap)
    height = ROWS * (size + gap)

    canvas = ft.Stack(
        width=width,
        height=height,
        animate_scale=duration,
        animate_opacity=duration,
    )

    for _ in range(len(parts)):
        canvas.controls.append(
            ft.Container(
                animate=duration,
                animate_position=duration,
                animate_rotation=duration,
            )
        )

    def randomize(e):
        random.seed()
        for i in range(len(parts)):
            c = canvas.controls[i]
            part_size = random.randrange(int(size / 2), int(size * 3))
            c.left = random.randrange(0, width)
            c.top = random.randrange(0, height)
            c.bgcolor = all_colors[random.randrange(0, len(all_colors))]
            c.width = part_size
            c.height = part_size
            c.border_radius = random.randrange(0, int(size / 2))
            c.rotate = random.randrange(0, 90) * 2 * pi / 360
        canvas.scale = 5
        canvas.opacity = 0.3
        go_button.visible = True
        again_button.visible = False
        page.update()

    def assemble(e):
        for i, (col, row, bgcolor) in enumerate(parts):
            c = canvas.controls[i]
            c.left = col * (size + gap)
            c.top = row * (size + gap)
            c.bgcolor = bgcolor
            c.width = size
            c.height = size
            c.border_radius = 5
            c.rotate = 0
        canvas.scale = 1
        canvas.opacity = 1
        go_button.visible = False
        again_button.visible = True
        page.update()

    go_button = ft.Button("Go!", on_click=assemble)
    again_button = ft.Button("Again!", on_click=randomize)

    randomize(None)

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.spacing = 30
    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[canvas, go_button, again_button],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
