import html
import re
import unicodedata


def sanitize_text(text: str) -> str:

    if not text:
        return ""

    text = unicodedata.normalize(
        "NFKC",
        text
    )

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2022": "-",
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )

    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def parse_semicolon_terms(
    terms: str
) -> list[str]:

    return [
        item.strip()
        for item in terms.split(";")
        if item.strip()

    ]


def text_to_html(
    text: str
) -> str:

    safe_text = html.escape(
        sanitize_text(text)
    )

    blocks = []

    for block in safe_text.split("\n\n"):

        lines = block.split("\n")

        content = "<br>".join(
            lines
        )

        blocks.append(
            f"<p>{content}</p>"
        )

    return "\n".join(blocks)