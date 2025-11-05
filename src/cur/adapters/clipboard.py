import pyperclip


def copy(text: str):
    pyperclip.copy(text)


def paste() -> str:
    return pyperclip.paste()
