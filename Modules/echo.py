# echo.py
"""
Moduł echo działający w czystym Pythonie.
Dodano:
- kolorowy output (ANSI)
- obsługę błędów
"""

# Kolory ANSI
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


def run(args=None):
    """
    Główna funkcja modułu.
    System wywołuje ją automatycznie.
    """
    try:
        if not args:
            print(f"{YELLOW}Użycie: e echo <tekst>{RESET}")
            return

        text = " ".join(args)
        print(f"{GREEN}{text}{RESET}")

    except Exception as e:
        print(f"{RED}Wystąpił błąd: {e}{RESET}")


def echo(text: str) -> str:
    """
    Funkcja pomocnicza — zwraca tekst.
    """
    return text