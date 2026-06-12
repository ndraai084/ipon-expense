from pathlib import Path

file = Path("templates/base.html")

text = file.read_text(encoding="utf-8")

viewport_tag = """
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">
"""

if "name=\"viewport\"" not in text:

    text = text.replace(
        "<head>",
        f"<head>\n\n    {viewport_tag}"
    )

    file.write_text(
        text,
        encoding="utf-8"
    )

    print("Viewport meta tag added.")

else:

    print("Viewport tag already exists.")