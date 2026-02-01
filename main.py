import flet as ft

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]

def check_winner(board: list[str]) -> str | None:
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def main(page: ft.Page):
    page.title = "Flet360 — Jogo da Velha"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    board = [""] * 9
    current = "X"
    game_over = False

    status = ft.Text("Vez do X", size=18, weight=ft.FontWeight.BOLD)

    # Em vez de trocar "text" do botão, trocamos o value do Text dentro dele
    cell_labels: list[ft.Text] = []
    buttons: list[ft.ElevatedButton] = []

    def refresh():
        nonlocal game_over
        winner = check_winner(board)

        if winner:
            status.value = f"{winner} venceu! ✅"
            game_over = True
        elif all(cell != "" for cell in board):
            status.value = "Empate! 🤝"
            game_over = True
        else:
            status.value = f"Vez do {current}"

        page.update()

    def on_click(i: int):
        nonlocal current, game_over
        if game_over or board[i] != "":
            return

        board[i] = current
        cell_labels[i].value = current  # atualiza o Text interno do botão
        current = "O" if current == "X" else "X"
        refresh()

    def reset(e):
        nonlocal board, current, game_over
        board = [""] * 9
        current = "X"
        game_over = False

        for t in cell_labels:
            t.value = ""

        refresh()

    grid_rows = []
    idx = 0
    for _r in range(3):
        row = []
        for _c in range(3):
            label = ft.Text("", size=26, weight=ft.FontWeight.BOLD)
            cell_labels.append(label)

            b = ft.ElevatedButton(
                content=label,              # ✅ agora é "content", não "text"
                width=90,
                height=90,
                on_click=lambda e, i=idx: on_click(i),
            )
            buttons.append(b)
            row.append(b)
            idx += 1

        grid_rows.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER))

    page.add(
        ft.Text("Jogo da Velha", size=24, weight=ft.FontWeight.BOLD),
        status,
        ft.Container(height=10),
        ft.Column(grid_rows, spacing=8),
        ft.Container(height=10),
        ft.OutlinedButton(content="Reiniciar", on_click=reset),  # ✅ content aqui também
    )

    refresh()

ft.run(main)
