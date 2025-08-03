import math
from PIL import Image

# Mapeamento de cores RGB para tipo de terreno
# As cores foram ligeiramente ajustadas para corresponder melhor às imagens.
TERRAIN_COLORS = {
    (34, 177, 76): 'G',   # Grama (Verde escuro)
    (127, 211, 118): 'g', # Grama (Verde claro - adicionado)
    (63, 72, 204): 'A',   # Água
    (185, 122, 87): 'M',  # Montanha/Terra
    (234, 210, 163): 'S', # Areia/Caminho claro
    (0, 100, 0): 'F',     # Floresta
}

DUNGEON_COLORS = {
    (230, 230, 230): 'C',  # Caminho (um cinza bem claro, não branco puro)
    (128, 128, 128): '#',  # Parede
}

def find_closest_color(rgb_tuple, color_map, tolerance=40):
    """
    Encontra a cor mais próxima em um dicionário de cores dentro de uma tolerância.

    Args:
        rgb_tuple (tuple): A tupla (R, G, B) da cor do pixel.
        color_map (dict): O dicionário mapeando cores RGB para caracteres.
        tolerance (int): A distância máxima para considerar uma cor como correspondente.

    Returns:
        str: O caractere do terreno correspondente ou '?' se nenhuma cor próxima for encontrada.
    """
    min_dist = float('inf')
    closest_char = '?'

    # Itera por todas as cores conhecidas para encontrar a mais próxima
    for map_rgb, terrain_char in color_map.items():
        # Calcula a distância Euclidiana entre as duas cores no espaço 3D (RGB)
        dist = math.sqrt(
            (rgb_tuple[0] - map_rgb[0]) ** 2 +
            (rgb_tuple[1] - map_rgb[1]) ** 2 +
            (rgb_tuple[2] - map_rgb[2]) ** 2
        )

        if dist < min_dist:
            min_dist = dist
            closest_char = terrain_char

    # Se a cor mais próxima estiver dentro da nossa tolerância, nós a aceitamos.
    # Caso contrário, retornamos '?' para indicar um terreno desconhecido.
    if min_dist <= tolerance:
        return closest_char
    else:
        # Opcional: descomente a linha abaixo para depurar cores não reconhecidas.
        # print(f"Cor não reconhecida: {rgb_tuple}, mais próxima: {closest_char}, distância: {min_dist:.2f}")
        return '?'

def extract_map(image_path, grid_size, color_map, filename='mapa.txt', tolerance=40):
    """
    Extrai um mapa de texto de uma imagem baseada em cores de tiles.

    Args:
        image_path (str): O caminho para o arquivo de imagem.
        grid_size (tuple): Uma tupla (linhas, colunas) do grid do mapa.
        color_map (dict): O dicionário de cores a ser usado.
        filename (str): O nome do arquivo de texto para salvar o mapa.
        tolerance (int): A tolerância para a correspondência de cores.
    """
    try:
        img = Image.open(image_path).convert('RGB') # Garante que a imagem está em modo RGB
        pixels = img.load()
    except FileNotFoundError:
        print(f"Erro: Arquivo de imagem não encontrado em '{image_path}'")
        return

    width, height = img.size
    rows, cols = grid_size

    # Calcula o tamanho de cada tile baseado no tamanho da imagem e do grid
    tile_w = width / cols
    tile_h = height / rows

    print(f"Processando '{image_path}' com grid {grid_size}...")
    with open(filename, 'w') as f:
        for row in range(rows):
            line = []
            for col in range(cols):
                # Pega o pixel central de cada tile para determinar sua cor
                x = int(col * tile_w + tile_w / 2)
                y = int(row * tile_h + tile_h / 2)
                
                rgb = pixels[x, y]
                
                # Usa a nova função para encontrar a cor mais próxima
                terrain = find_closest_color(rgb, color_map, tolerance)
                line.append(terrain)
            f.write("".join(line))
            f.write('\n')
    print(f"Mapa salvo com sucesso em: '{filename}'")

# --- Exemplo de Uso ---
# Certifique-se de que as imagens estão no caminho correto.
# Se as imagens estiverem na mesma pasta do script, remova 'mapas/'.
# A tolerância pode ser ajustada se necessário.

# Caminho para a pasta de mapas. Altere se necessário.
MAPS_FOLDER = 'mapas/' 

extract_map(
    f'{MAPS_FOLDER}mapa_hyrule.png',
    grid_size=(42, 42),
    color_map=TERRAIN_COLORS,
    filename='hyrule.txt',
    tolerance=50 # Hyrule tem mais variações de cor, então uma tolerância maior ajuda
)

extract_map(
    f'{MAPS_FOLDER}masmorra_1.png',
    grid_size=(28, 28),
    color_map=DUNGEON_COLORS,
    filename='masmorra1.txt'
)

extract_map(
    f'{MAPS_FOLDER}masmorra_2.png',
    grid_size=(28, 28),
    color_map=DUNGEON_COLORS,
    filename='masmorra2.txt'
)

extract_map(
    f'{MAPS_FOLDER}masmorra_3.png',
    grid_size=(28, 28),
    color_map=DUNGEON_COLORS,
    filename='masmorra3.txt'
)