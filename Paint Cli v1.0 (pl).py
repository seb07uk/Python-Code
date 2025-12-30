import os
import sys
import msvcrt
import glob
from datetime import datetime

class Colors:
    RESET = '\033[0m'
    HOME = '\033[H'
    WHITE = '\033[97m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BG_CYAN = '\033[46m'
    BLACK = '\033[30m'
    CLEAR_LINE = '\033[K'
    
    PALETTE = {
        '1': ('#', GREEN, "Zielony"),
        '2': ('#', RED, "Czerwony"),
        '3': ('#', BLUE, "Niebieski"),
        '4': ('#', YELLOW, "Zolty"),
        '5': ('#', MAGENTA, "Magenta")
    }

def get_paint_dir():
    # Folder zgodnie z instrukcją: %userprofile%\.polsoft\Paint\
    folder = os.path.join(os.environ['USERPROFILE'], '.polsoft', 'Paint')
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    return folder

def show_about():
    os.system('cls')
    print(f"""
{Colors.BG_CYAN}{Colors.BLACK}           INFORMACJE O AUTORZE           {Colors.RESET}

Autor:   **Sebastian Januchowski**
Email:   **polsoft.its@fastservice.com**
GitHub:  **https://github.com/seb07uk**

-------------------------------------------
Folder zapisu: %userprofile%\\.polsoft\\Paint\\
-------------------------------------------

STEROWANIE:
- WASD: Poruszanie kursorem (@)
- 1-5:  Wybór koloru z palety
- R:    Rysuj punkt (#)
- E:    Zmaż punkt (.)
- P:    Zapisz rysunek
- O:    Otwórz menu plików
- C:    Wyczyść planszę
- N:    iNfO (ten ekran)
- Q:    Wyjście

Naciśnij dowolny klawisz, aby wrócić...""")
    msvcrt.getch()
    os.system('cls')

def open_file_menu(width, height):
    folder = get_paint_dir()
    files = glob.glob(os.path.join(folder, "*.txt"))
    files.sort(key=os.path.getctime, reverse=True)
    if not files:
        os.system('cls')
        print("Brak zapisanych plików. Naciśnij dowolny klawisz...")
        msvcrt.getch()
        return None, "Brak plików."
    
    selected_idx = 0
    while True:
        os.system('cls')
        print(f"{Colors.BG_CYAN}{Colors.BLACK}   WYBIERZ PLIK (W/S: Ruch, O: Otwórz, Q: Powrót)   {Colors.RESET}\n")
        for i, fpath in enumerate(files):
            marker = "--> " if i == selected_idx else "    "
            print(f"{marker}{os.path.basename(fpath)}")
        
        k = msvcrt.getch().lower()
        if k == b'q': return None, "Anulowano."
        elif k == b'w' and selected_idx > 0: selected_idx -= 1
        elif k == b's' and selected_idx < len(files) - 1: selected_idx += 1
        elif k == b'o':
            new_board = [[(".", Colors.WHITE) for _ in range(width)] for _ in range(height)]
            with open(files[selected_idx], 'r', encoding='utf-8') as f:
                for r, line in enumerate(f.readlines()[:height]):
                    for c, char in enumerate(line.strip()[:width]):
                        if char == '#': new_board[r][c] = ('#', Colors.GREEN)
            return new_board, f"Wczytano: {os.path.basename(files[selected_idx])}"

def main():
    os.system('') # Inicjalizacja kolorów ANSI na Windows
    sys.stdout.write('\033[?25l') # Ukrycie kursora systemowego
    
    WIDTH, HEIGHT = 80, 20
    board = [[(".", Colors.WHITE) for _ in range(WIDTH)] for _ in range(HEIGHT)]
    x, y, active_color_key, status_msg = 0, 0, '1', ""
    
    os.system('cls')

    try:
        while True:
            sys.stdout.write(Colors.HOME)
            
            output = [f"{Colors.CYAN}--- PAINT CLI | Sebastian Januchowski ---{Colors.RESET}{Colors.CLEAR_LINE}"]
            
            for r in range(HEIGHT):
                row_str = ""
                for c in range(WIDTH):
                    if r == y and c == x:
                        row_str += f"{Colors.YELLOW}@{Colors.RESET}"
                    else:
                        char, col = board[r][c]
                        row_str += f"{col}{char}{Colors.RESET}"
                
                # Logika panelu bocznego
                sidebar = "  "
                row_idx = r - 1
                key_str = str(row_idx)
                
                if r == 0:
                    sidebar += f"{Colors.CYAN}PALETA:{Colors.RESET}"
                elif key_str in Colors.PALETTE:
                    _, col_p, name_p = Colors.PALETTE[key_str]
                    pointer = f" {Colors.CYAN}<--{Colors.RESET}" if active_color_key == key_str else ""
                    sidebar += f"{key_str}: {col_p}{name_p}{Colors.RESET}{pointer}"
                elif r == 7:
                    sidebar += f"E: {Colors.WHITE}Gumka{Colors.RESET}"
                
                output.append(row_str + sidebar + Colors.CLEAR_LINE)
            
            # Dolne menu z opcją iNfO
            output.append(f"\nPoz: [{x:2},{y:2}] | WASD: Ruch | R: Rysuj | P: Zapisz | O: Otwórz | N: iNfO | Q: Wyjdź{Colors.CLEAR_LINE}")
            if status_msg:
                output.append(f"{Colors.GREEN}>> {status_msg}{Colors.RESET}{Colors.CLEAR_LINE}")
                status_msg = ""
            else:
                output.append(Colors.CLEAR_LINE)

            sys.stdout.write("\n".join(output))
            sys.stdout.flush()

            key = msvcrt.getch().lower()

            if key == b'q': break
            elif key == b'n': # Wywołanie iNfO
                show_about()
                os.system('cls')
            elif key == b'w' and y > 0: y -= 1
            elif key == b's' and y < HEIGHT - 1: y += 1
            elif key == b'a' and x > 0: x -= 1
            elif key == b'd' and x < WIDTH - 1: x += 1
            elif key in [b'1', b'2', b'3', b'4', b'5']: active_color_key = key.decode()
            elif key == b'r':
                char_p, col_p, _ = Colors.PALETTE[active_color_key]
                board[y][x] = (char_p, col_p)
            elif key == b'e': board[y][x] = (".", Colors.WHITE)
            elif key == b'p':
                folder = get_paint_dir()
                fname = datetime.now().strftime("paint_%Y%m%d_%H%M%S.txt")
                with open(os.path.join(folder, fname), 'w', encoding='utf-8') as f:
                    for row in range(HEIGHT):
                        f.write("".join([board[row][col][0] for col in range(WIDTH)]) + "\n")
                status_msg = f"Zapisano: {fname}"
            elif key == b'o':
                nb, msg = open_file_menu(WIDTH, HEIGHT)
                if nb: board = nb
                status_msg = msg
                os.system('cls')
            elif key == b'c':
                board = [[(".", Colors.WHITE) for _ in range(WIDTH)] for _ in range(HEIGHT)]

    finally:
        sys.stdout.write('\033[?25h') # Przywrócenie kursora
        print("\nProgram zamknięty.")

if __name__ == "__main__":
    main()