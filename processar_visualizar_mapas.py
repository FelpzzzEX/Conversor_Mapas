import math
import tkinter as tk
from tkinter import Frame, Canvas, Button, Label, messagebox
from PIL import Image

# ==============================================================================
# PARTE 1: LÓGICA DE EXTRAÇÃO DE MAPA (do script anterior)
# ==============================================================================

# Dicionários de mapeamento de cores RGB para caracteres de terreno.
TERRAIN_COLORS = {
    (34, 177, 76): 'G',   # Grama (Verde escuro)
    (127, 211, 118): 'g', # Grama (Verde claro)
    (36, 113, 178): 'A',  # Água (CORRIGIDO NOVAMENTE para o tom exato da imagem)
    (185, 122, 87): 'M',  # Montanha/Terra
    (234, 210, 163): 'S', # Areia/Caminho claro
    (0, 100, 0): 'F',     # Floresta
}

DUNGEON_COLORS = {
    (230, 230, 230): 'C',  # Caminho (Cinza claro)
    (177, 177, 177): '#',  # Parede (Cinza médio)
}

def find_closest_color(rgb_tuple, color_map, tolerance=40):
    min_dist = float('inf')
    closest_char = '?'
    for map_rgb, terrain_char in color_map.items():
        dist = math.sqrt(sum([(c1 - c2) ** 2 for c1, c2 in zip(rgb_tuple, map_rgb)]))
        if dist < min_dist:
            min_dist = dist
            closest_char = terrain_char
    return closest_char if min_dist <= tolerance else '?'

def extract_map(image_path, grid_size, color_map, filename, tolerance=40):
    try:
        img = Image.open(image_path).convert('RGB')
        pixels = img.load()
    except FileNotFoundError:
        print(f"Aviso: Arquivo de imagem não encontrado em '{image_path}'. Pulando extração.")
        return False
        
    width, height = img.size
    rows, cols = grid_size
    tile_w, tile_h = width / cols, height / rows

    with open(filename, 'w') as f:
        for row in range(rows):
            line = []
            for col in range(cols):
                x, y = int(col * tile_w + tile_w / 2), int(row * tile_h + tile_h / 2)
                terrain = find_closest_color(pixels[x, y], color_map, tolerance)
                line.append(terrain)
            f.write("".join(line) + '\n')
    print(f"Mapa '{filename}' extraído/atualizado com sucesso.")
    return True

def run_full_extraction():
    """Função para extrair todos os mapas de uma vez."""
    print("--- Iniciando extração de todos os mapas ---")
    MAPS_FOLDER = 'mapas_teste/'
    extract_map(f'{MAPS_FOLDER}mapa_hyrule.png', (42, 42), TERRAIN_COLORS, 'hyrule.txt', 50)
    extract_map(f'{MAPS_FOLDER}masmorra_1.png', (28, 28), DUNGEON_COLORS, 'masmorra1.txt')
    extract_map(f'{MAPS_FOLDER}masmorra_2.png', (28, 28), DUNGEON_COLORS, 'masmorra2.txt')
    extract_map(f'{MAPS_FOLDER}masmorra_3.png', (28, 28), DUNGEON_COLORS, 'masmorra3.txt')
    print("--- Extração concluída ---")
    messagebox.showinfo("Extração Concluída", "Os arquivos de mapa (.txt) foram gerados com sucesso!")


# ==============================================================================
# PARTE 2: LÓGICA DE VISUALIZAÇÃO GRÁFICA (novo código)
# ==============================================================================

# Dicionário que mapeia os caracteres do mapa para cores da interface gráfica.
TILE_VISUAL_COLORS = {
    'G': 'darkgreen',
    'g': 'limegreen',
    'A': 'royalblue',
    'M': '#A0522D',  # Cor "sienna" (marrom-avermelhado)
    'S': 'khaki',
    'F': 'darkolivegreen',
    'C': '#E0E0E0',  # Um cinza bem claro
    '#': 'dimgray',
    '?': 'black'     # Para qualquer tile não reconhecido
}

class MapViewer(tk.Tk):
    """
    Classe principal da aplicação de visualização de mapas.
    Herda de tk.Tk para se tornar a janela principal.
    """
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Mapas")
        self.geometry("800x650")

        self.map_data = []

        # --- Criação dos Widgets ---
        # Frame para os botões de controle
        control_frame = Frame(self, pady=10)
        control_frame.pack(side="top", fill="x")

        # Canvas onde o mapa será desenhado
        self.canvas = Canvas(self, bg="black")
        self.canvas.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Adicionando botões para cada mapa
        Button(control_frame, text="Ver Hyrule", command=lambda: self.load_map_from_file('hyrule.txt')).pack(side="left", padx=5)
        Button(control_frame, text="Ver Masmorra 1", command=lambda: self.load_map_from_file('masmorra1.txt')).pack(side="left", padx=5)
        Button(control_frame, text="Ver Masmorra 2", command=lambda: self.load_map_from_file('masmorra2.txt')).pack(side="left", padx=5)
        Button(control_frame, text="Ver Masmorra 3", command=lambda: self.load_map_from_file('masmorra3.txt')).pack(side="left", padx=5)
        
        # Botão para (Re)gerar os arquivos de mapa
        Button(control_frame, text="(Re)Gerar Mapas", command=run_full_extraction, bg="#FFDDDD").pack(side="right", padx=10)

    def load_map_from_file(self, filepath):
        """Lê um arquivo .txt e o carrega para ser desenhado."""
        try:
            with open(filepath, 'r') as f:
                # Lê todas as linhas, removendo quebras de linha no final
                self.map_data = [line.strip() for line in f.readlines()]
            self.title(f"Visualizador de Mapas - {filepath}")
            self.draw_map()
        except FileNotFoundError:
            messagebox.showerror("Erro", f"Arquivo '{filepath}' não encontrado!\n\nClique em '(Re)Gerar Mapas' para criá-lo.")
            
    def draw_map(self):
        """Desenha o mapa carregado no canvas."""
        self.canvas.delete("all")  # Limpa o canvas antes de desenhar um novo mapa

        if not self.map_data:
            return

        # Pega as dimensões do mapa e do canvas
        map_rows = len(self.map_data)
        map_cols = len(self.map_data[0])
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calcula o tamanho de cada "tile" para que o mapa caiba no canvas
        tile_w = canvas_width / map_cols
        tile_h = canvas_height / map_rows
        
        # Itera por cada célula do mapa (cada caractere)
        for row_idx, row_str in enumerate(self.map_data):
            for col_idx, tile_char in enumerate(row_str):
                # Define as coordenadas (x0, y0) e (x1, y1) do retângulo
                x0 = col_idx * tile_w
                y0 = row_idx * tile_h
                x1 = x0 + tile_w
                y1 = y0 + tile_h

                # Pega a cor correspondente ao caractere do tile
                color = TILE_VISUAL_COLORS.get(tile_char, 'magenta') # 'magenta' para erros

                # Desenha o retângulo no canvas
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

# ==============================================================================
# PONTO DE ENTRADA PRINCIPAL DA APLICAÇÃO
# ==============================================================================
if __name__ == "__main__":
    # Cria a instância da nossa aplicação gráfica
    app = MapViewer()
    
    # Exibe uma mensagem inicial para o usuário
    messagebox.showinfo(
        "Bem-vindo!",
        "Primeiro, clique em '(Re)Gerar Mapas' para garantir que os arquivos .txt estão atualizados.\n\nDepois, use os outros botões para visualizar cada mapa."
    )
    
    # Inicia o loop principal da interface gráfica
    app.mainloop()