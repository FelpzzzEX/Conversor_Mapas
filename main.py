import math
import os
import tkinter as tk
from tkinter import Frame, Canvas, Button, Label, messagebox
from PIL import Image
from collections import Counter

# Dicionários de mapeamento de cores RGB para caracteres de terreno.
TERRAIN_COLORS = {
    (34, 177, 76): 'G',   # Grama (Verde escuro)
    (127, 211, 118): 'g', # Grama (Verde claro)
    (99, 155, 255): 'A',  # Água
    (185, 122, 87): 'M',  # Montanha/Terra
    (234, 210, 163): 'S', # Areia/Caminho claro
    (0, 100, 0): 'F',     # Floresta
}

DUNGEON_COLORS = {
    (230, 230, 230): 'C',  # Caminho (Cinza claro)
    (177, 177, 177): '#',  # Parede (Cinza médio)
}

def find_closest_terrain_char(rgb_tuple, color_map, tolerance=40):
    """Encontra o caractere de terreno mais próximo para um único píxel."""
    min_dist = float('inf')
    closest_char = '?'
    for map_rgb, terrain_char in color_map.items():
        # Calcula a distância Euclidiana entre as duas cores
        dist = math.sqrt(sum([(c1 - c2) ** 2 for c1, c2 in zip(rgb_tuple, map_rgb)]))
        if dist < min_dist:
            min_dist = dist
            closest_char = terrain_char
            
    # Retorna o caractere apenas se a distância estiver dentro da tolerância
    return closest_char if min_dist <= tolerance else '?'

def get_dominant_terrain_from_tile(pixels, center_x, center_y, color_map, tolerance, sample_size=5):
    """
    Analisa uma área, classifica cada píxel e retorna o tipo de terreno mais comum.
    """
    terrain_votes = []
    # Cria uma caixa de amostragem maior (5x5) à volta do píxel central
    for i in range(center_x - sample_size // 2, center_x + sample_size // 2 + 1):
        for j in range(center_y - sample_size // 2, center_y + sample_size // 2 + 1):
            try:
                pixel_rgb = pixels[i, j]
                # Para cada píxel, encontra o seu tipo de terreno correspondente
                terrain_char = find_closest_terrain_char(pixel_rgb, color_map, tolerance)
                if terrain_char != '?': # Só contabiliza votos válidos
                    terrain_votes.append(terrain_char)
            except IndexError:
                continue
    
    if not terrain_votes:
        return '?' # Retorna '?' se nenhum píxel na amostra foi reconhecido

    # Usa Counter para contar os "votos" e encontrar o terreno mais comum
    most_common_terrain = Counter(terrain_votes).most_common(1)[0][0]
    return most_common_terrain

def extract_map(image_path, grid_size, color_map, filename, tolerance=40):
    """Extrai um mapa de texto de uma imagem usando o método de votação de terreno."""
    try:
        img = Image.open(image_path).convert('RGB')
        pixels = img.load()
    except FileNotFoundError:
        print(f"Aviso: Ficheiro de imagem não encontrado em '{image_path}'. A extração foi ignorada.")
        return False
        
    width, height = img.size
    rows, cols = grid_size
    tile_w, tile_h = width / cols, height / rows

    with open(filename, 'w') as f:
        for row in range(rows):
            line = []
            for col in range(cols):
                center_x = int(col * tile_w + tile_w / 2)
                center_y = int(row * tile_h + tile_h / 2)
                
                # Obtém o terreno dominante através de votação
                terrain = get_dominant_terrain_from_tile(pixels, center_x, center_y, color_map, tolerance)
                line.append(terrain)
            f.write("".join(line) + '\n')
    print(f"Mapa '{filename}' extraído/atualizado com sucesso.")
    return True

def run_full_extraction():
    """Função para extrair todos os mapas de uma vez."""
    print("--- Iniciando a extração de todos os mapas ---")
    INPUT_FOLDER = 'mapas_brutos' # Define a pasta de entrada
    OUTPUT_FOLDER = 'mapas_processados' # Define a pasta de saída
    
    # Verifica se a pasta de entrada existe
    if not os.path.isdir(INPUT_FOLDER):
        messagebox.showerror("Erro de Pasta", f"A pasta de entrada '{INPUT_FOLDER}' não foi encontrada.")
        return

    # Cria a pasta de saída se ela não existir
    if not os.path.isdir(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Pasta '{OUTPUT_FOLDER}' criada.")

    # Lista de mapas para processar (ajustar conforme a necessidade)
    maps_to_process = [
        {'img': 'mapa_hyrule.png', 'grid': (42, 42), 'colors': TERRAIN_COLORS, 'txt': 'hyrule.txt', 'tol': 75},
        {'img': 'masmorra_1.png', 'grid': (28, 28), 'colors': DUNGEON_COLORS, 'txt': 'masmorra1.txt', 'tol': 50},
        {'img': 'masmorra_2.png', 'grid': (28, 28), 'colors': DUNGEON_COLORS, 'txt': 'masmorra2.txt', 'tol': 50},
        {'img': 'masmorra_3.png', 'grid': (28, 28), 'colors': DUNGEON_COLORS, 'txt': 'masmorra3.txt', 'tol': 50},
    ]

    for map_info in maps_to_process:
        img_path = os.path.join(INPUT_FOLDER, map_info['img'])
        txt_path = os.path.join(OUTPUT_FOLDER, map_info['txt']) # Usa a pasta de saída
        extract_map(img_path, map_info['grid'], map_info['colors'], txt_path, tolerance=map_info['tol'])

    print("--- Extração concluída ---")
    messagebox.showinfo("Extração Concluída", f"Confira a geração nos botôes na parte superior. Mapas disponíveis em: '{OUTPUT_FOLDER}'!")

TILE_VISUAL_COLORS = {
    'G': 'darkgreen', 'g': 'limegreen', 'A': 'royalblue', 'M': '#A0522D',
    'S': 'khaki', 'F': 'darkolivegreen', 'C': '#E0E0E0', '#': 'dimgray', '?': 'black'
}

class MapViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Mapas")
        self.geometry("800x650")
        self.map_data = []
        self.output_folder = 'mapas_processados' # Informa a classe sobre a pasta

        control_frame = Frame(self, pady=10)
        control_frame.pack(side="top", fill="x")

        self.canvas = Canvas(self, bg="black")
        self.canvas.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        Button(control_frame, text="Ver Hyrule", command=lambda: self.load_map_from_file('hyrule.txt')).pack(side="left", padx=5)
        Button(control_frame, text="Ver Masmorra 1", command=lambda: self.load_map_from_file('masmorra1.txt')).pack(side="left", padx=5)
        Button(control_frame, text="Ver Masmorra 2", command=lambda: self.load_map_from_file('masmorra2.txt')).pack(side="left", padx=5)
        Button(control_frame, text="Ver Masmorra 3", command=lambda: self.load_map_from_file('masmorra3.txt')).pack(side="left", padx=5)
        
        Button(control_frame, text="(Re)Gerar Mapas", command=run_full_extraction, bg="#FFDDDD").pack(side="right", padx=10)

    def load_map_from_file(self, filename):
        """Lê um ficheiro .txt da pasta de saída e o carrega para ser desenhado."""
        filepath = os.path.join(self.output_folder, filename) # Monta o caminho completo
        try:
            with open(filepath, 'r') as f:
                self.map_data = [line.strip() for line in f.readlines()]
            self.title(f"Visualizador de Mapas - {filename}")
            self.canvas.bind("<Configure>", lambda event: self.draw_map())
            self.draw_map()
        except FileNotFoundError:
            messagebox.showerror("Erro", f"Ficheiro '{filepath}' não encontrado!\n\nClique em '(Re)Gerar Mapas' para o criar.")
            
    def draw_map(self, event=None):
        self.canvas.delete("all")
        if not self.map_data: return

        map_rows, map_cols = len(self.map_data), len(self.map_data[0])
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        tile_w, tile_h = canvas_width / map_cols, canvas_height / map_rows
        
        for row_idx, row_str in enumerate(self.map_data):
            for col_idx, tile_char in enumerate(row_str):
                x0, y0 = col_idx * tile_w, row_idx * tile_h
                x1, y1 = x0 + tile_w, y0 + tile_h
                color = TILE_VISUAL_COLORS.get(tile_char, 'magenta')
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

if __name__ == "__main__":
    app = MapViewer()
    messagebox.showinfo(
        "Bem-vindo!",
        "1. Certifique-se de que a pasta 'mapas_teste' está no mesmo diretório que este script.\n\n"
        "2. Clique em '(Re)Gerar Mapas' para criar ou atualizar os mapas na pasta 'mapas_processados'.\n\n"
        "3. Use os outros botões para visualizar cada mapa."
    )
    app.mainloop()