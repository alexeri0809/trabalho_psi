def get_bmp_header(width, height):
    """
    Gera o cabeçalho do arquivo BMP, incluindo o cabeçalho DIB.
    """
    row_size = width * 3  # Cada pixel tem 3 bytes (BGR)
    padding_size = (4 - (row_size % 4)) % 4  # Padding para múltiplo de 4 bytes
    image_size = (row_size + padding_size) * height
    file_size = 54 + image_size  # Tamanho total do arquivo

    # Cabeçalho BMP (14 bytes)
    bmp_header = (
        b'BM' +
        file_size.to_bytes(4, 'little') +  # Tamanho total do arquivo
        b'\x00\x00' +                     # Reservado
        b'\x00\x00' +                     # Reservado
        (54).to_bytes(4, 'little')         # Offset para os dados da imagem (54 bytes)
    )

    # Cabeçalho DIB (40 bytes)
    dib_header = (
        (40).to_bytes(4, 'little') +       # Tamanho do cabeçalho DIB
        width.to_bytes(4, 'little') +      # Largura da imagem
        height.to_bytes(4, 'little', signed=True) +  # Altura negativa para ordem correta
        (1).to_bytes(2, 'little') +        # Número de planos (sempre 1)
        (24).to_bytes(2, 'little') +       # Profundidade de cor (24 bits)
        (0).to_bytes(4, 'little') +        # Compressão (0 = sem compressão)
        image_size.to_bytes(4, 'little') + # Tamanho dos dados de imagem
        (2835).to_bytes(4, 'little') +     # Resolução horizontal (pixels por metro)
        (2835).to_bytes(4, 'little') +     # Resolução vertical (pixels por metro)
        (0).to_bytes(4, 'little') +        # Número de cores (0 = todas as cores disponíveis)
        (0).to_bytes(4, 'little')          # Cores importantes (0 = todas as cores importantes)
    )

    return bmp_header + dib_header


def create_rgb888_lines(width, height, mode="green_purple"):
    """
    Gera dados de pixel diretamente no formato RGB888, com cores alternadas entre verde, vermelho e azul.
    """
    if mode == "green_purple":
        # Define a cor verde e roxa
        green = [0, 255, 0] * width  # Linha verde
        purple = [128, 0, 128] * width  # Linha roxa
        
        # A cor verde ficará nas linhas superiores e a roxa nas linhas inferiores
        middle = height // 2  # Divide a imagem ao meio
        pattern = [green] * middle + [purple] * (height - middle)
    
    elif mode == "rgb":
        # Para o modo RGB (vermelho, verde, azul), define as cores
        red = [0, 0, 255] * width  # Linha vermelha
        green = [0, 255, 0] * width  # Linha verde
        blue = [255, 0, 0] * width  # Linha azul
        
        # Garantir que o padrão tenha o número correto de linhas
        pattern = [red, green, blue] * ((height + 2) // 3)  # Multiplica para garantir que cubra toda a altura
        pattern = pattern[:height]  # Trunca a lista para garantir que tenha exatamente a altura necessária

    rgb888_data = []
    for i in range(height):
        line_data = pattern[i]  # Pega a linha correspondente
        rgb888_data.extend(line_data)

    return rgb888_data


def save_bmp_rgb888(filename, width, height, mode="green_purple"):
    """
    Salva um BMP contendo padrões de cores predefinidos no formato RGB888 (24 bits).
    """
    print(f"🔄 Gerando imagem {filename} com padrão RGB ({mode})...")

    header = get_bmp_header(width, height)
    rgb888_data = create_rgb888_lines(width, height, mode)

    row_size = width * 3
    padding_size = (4 - (row_size % 4)) % 4
    print(f"📏 Largura: {width} px, Altura: {height} px")
    print(f"📂 Tamanho da linha (sem padding): {row_size} bytes")
    print(f"➕ Padding por linha: {padding_size} bytes")

    padded_data = []

    for i in range(height):
        line_start = (height - 1 - i) * row_size
        line_end = line_start + row_size
        line_data = rgb888_data[line_start:line_end]

        line_data.extend([0] * padding_size)  # Adiciona padding ao final de cada linha
        padded_data.extend(line_data)

    print(f"📦 Tamanho final da imagem com padding: {len(padded_data)} bytes")

    with open(filename, "wb") as f:
        f.write(header)
        f.write(bytearray(padded_data))

    print(f"✅ Imagem BMP '{filename}' criada com sucesso!")


# Gerar a imagem verde e roxa
save_bmp_rgb888("imagem_rgb888_green_purple.bmp", 10, 5, "green_purple")

# Gerar a imagem com o padrão RGB (vermelho, verde e azul)
save_bmp_rgb888("imagem_rgb888_rgb_pattern.bmp", 10, 5, "rgb")
