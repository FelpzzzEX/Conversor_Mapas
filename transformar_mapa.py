from PIL import Image

# Mapeamento de cores RGB para tipo de terreno
TERRAIN_COLORS = {
    (34, 177, 76): 'G',   # Grama
    (63, 72, 204): 'A',   # Água
    (185, 122, 87): 'M',  # Montanha
    (255, 201, 14): 'S',  # Areia
    (0, 100, 0): 'F',     # Floresta
}

DUNGEON_COLORS = {
    (255, 255, 255): 'C',  # Caminho
    (128, 128, 128): '#',  # Parede
}

def extract_map(image_path, grid_size=(42, 42), tile_size=10, color_map=TERRAIN_COLORS, filename='mapa.txt'):
    img = Image.open(image_path)
    pixels = img.load()

    width, height = img.size
    rows, cols = grid_size

    tile_w = width // cols
    tile_h = height // rows

    with open(filename, 'w') as f:
        for row in range(rows):
            for col in range(cols):
                # Pega o pixel central de cada tile
                x = col * tile_w + tile_w // 2
                y = row * tile_h + tile_h // 2
                rgb = pixels[x, y][:3]
                terrain = color_map.get(rgb, '?')  # '?' para valores desconhecidos
                f.write(terrain)
            f.write('\n')
    print(f"Mapa salvo em: {filename}")

# Exemplo de uso:
extract_map('mapas/mapa_hyrule.png', grid_size=(42, 42), filename='hyrule.txt')
extract_map('mapas/masmorra_1.png', grid_size=(28, 28), color_map=DUNGEON_COLORS, filename='masmorra1.txt')
extract_map('mapas/masmorra_2.png', grid_size=(28, 28), color_map=DUNGEON_COLORS, filename='masmorra2.txt')
extract_map('mapas/masmorra_3.png', grid_size=(28, 28), color_map=DUNGEON_COLORS, filename='masmorra3.txt')
