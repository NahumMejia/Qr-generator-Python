import os
import base64
import qrcode
from io import BytesIO
import flet as ft


def main(page: ft.Page):
    page.title = "QR Code Generator"
    page.padding = 12
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    colors = {
        "black": "#000000",
        "white": "#FFFFFF",
        "red": "#FF0000",
        "green": "#008000",
        "blue": "#0000FF",
        "yellow": "#FFFF00",
        "orange": "#FFA500",
        "purple": "#800080",
        "pink": "#FFC0CB",
        "brown": "#A52A2A",
        "gray": "#808080",
        "cyan": "#00FFFF",
        "magenta": "#FF00FF",
        "lime": "#00FF00",
        "navy": "#000080",
        "teal": "#008080",
        "maroon": "#800000",
        "olive": "#808000",
        "silver": "#C0C0C0",
        "gold": "#FFD700",
    }

    current_qr_base64 = None

    def show_snackbar(message):
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()

    title = ft.Text("QR Code Generator", size=22, weight=ft.FontWeight.BOLD)

    url_input = ft.TextField(
        label="URL",
        width=300,
        hint_text="https://example.com",
    )

    dropdown_options = [ft.dropdown.Option(k, k.capitalize()) for k in colors]

    bg_color = ft.Dropdown(
        label="Background",
        width=140,
        value="white",
        options=dropdown_options,
    )

    code_color = ft.Dropdown(
        label="Code color",
        width=140,
        value="black",
        options=dropdown_options,
    )

    border = ft.Dropdown(
        label="Border",
        width=120,
        value="4",
        options=[ft.dropdown.Option(str(i)) for i in [1, 2, 3, 4, 5, 6, 8]],
    )

    preview_box = ft.Container(
        width=180,
        height=180,
        border=ft.border.all(2, ft.Colors.GREY_400),
        bgcolor=ft.Colors.GREY_100,
        content=ft.Text("Generate QR", color=ft.Colors.GREY_600),
    )

    def generate_qr(e):
        nonlocal current_qr_base64

        if not url_input.value:
            show_snackbar("Please enter a URL")
            return

        if bg_color.value == code_color.value:
            show_snackbar("Colors must be different")
            return

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=int(border.value),
        )

        qr.add_data(url_input.value)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=colors[code_color.value],
            back_color=colors[bg_color.value],
        )

        buffer = BytesIO()
        img.save(buffer, format="PNG")

        current_qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        preview_box.content = ft.Image(
            src=f"data:image/png;base64,{current_qr_base64}"
        )

        page.update()

    async def open_qr_page(e):
        if not current_qr_base64:
            show_snackbar("Generate the QR first")
            return

        await page.launch_url(
            f"data:image/png;base64,{current_qr_base64}"
        )

    page.add(
        ft.Column(
            [
                title,
                url_input,
                ft.Row(
                    [bg_color, code_color, border],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("GENERATE", on_click=generate_qr),
                        ft.ElevatedButton("OPEN / DOWNLOAD", on_click=open_qr_page),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [preview_box],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        )
    )


ft.app(
    target=main,
    view=ft.WEB_BROWSER,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
)
