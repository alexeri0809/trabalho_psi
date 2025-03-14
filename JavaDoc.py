# /**
#  * Gera o cabeçalho do arquivo BMP, incluindo o cabeçalho DIB.
#  *
#  * @param width  Largura da imagem em pixels.
#  * @param height Altura da imagem em pixels.
#  * @return Array de bytes representando o cabeçalho BMP.
#  */
def get_bmp_header(width, height):
    row_size = width * 3  # Cada pixel tem 3 bytes (BGR)
    padding_size = (4 - (row_size % 4)) % 4  # Padding para múltiplo de 4 bytes
    image_size = (row_size + padding_size) * height
    file_size = 54 + image_size  # Tamanho total do arquivo

    bmp_header = (
        b'BM' +
        file_size.to_bytes(4, 'little') +
        b'\x00\x00' +
        b'\x00\x00' +
        (54).to_bytes(4, 'little')
    )

    dib_header = (
        (40).to_bytes(4, 'little') +
        width.to_bytes(4, 'little') +
        height.to_bytes(4, 'little', signed=True) +
        (1).to_bytes(2, 'little') +
        (24).to_bytes(2, 'little') +
        (0).to_bytes(4, 'little') +
        image_size.to_bytes(4, 'little') +
        (2835).to_bytes(4, 'little') +
        (2835).to_bytes(4, 'little') +
        (0).to_bytes(4, 'little') +
        (0).to_bytes(4, 'little')
    )

    return bmp_header + dib_header

# /**
#  * Gera dados de pixel diretamente no formato RGB888.
#  *
#  * @param width  Largura da imagem em pixels.
#  * @param height Altura da imagem em pixels.
#  * @param mode   Modo de cor ("green_purple" ou "rgb").
#  * @return Lista de bytes representando os dados RGB888.
#  */
def create_rgb888_lines(width, height, mode="green_purple"):
    if mode == "green_purple":
        green = [0, 255, 0] * width
        purple = [128, 0, 128] * width
        middle = height // 2
        pattern = [green] * middle + [purple] * (height - middle)
    elif mode == "rgb":
        red = [0, 0, 255] * width
        green = [0, 255, 0] * width
        blue = [255, 0, 0] * width
        pattern = [red, green, blue] * ((height + 2) // 3)
        pattern = pattern[:height]

    rgb888_data = []
    for i in range(height):
        line_data = pattern[i]
        rgb888_data.extend(line_data)

    return rgb888_data

# /**
#  * Salva um arquivo BMP com dados de imagem no formato RGB888.
#  *
#  * @param filename Nome do arquivo BMP a ser salvo.
#  * @param width    Largura da imagem em pixels.
#  * @param height   Altura da imagem em pixels.
#  * @param mode     Modo de cor ("green_purple" ou "rgb").
#  */
def save_bmp_rgb888(filename, width, height, mode="green_purple"):
    print(f"\U0001F504 Gerando imagem {filename} com padrão RGB ({mode})...")

    header = get_bmp_header(width, height)
    rgb888_data = create_rgb888_lines(width, height, mode)

    row_size = width * 3
    padding_size = (4 - (row_size % 4)) % 4
    print(f"\U0001F4CF Largura: {width} px, Altura: {height} px")
    print(f"\U0001F4C2 Tamanho da linha (sem padding): {row_size} bytes")
    print(f"➕ Padding por linha: {padding_size} bytes")

    padded_data = []

    for i in range(height):
        line_start = (height - 1 - i) * row_size
        line_end = line_start + row_size
        line_data = rgb888_data[line_start:line_end]
        line_data.extend([0] * padding_size)
        padded_data.extend(line_data)

    print(f"\U0001F4E6 Tamanho final da imagem com padding: {len(padded_data)} bytes")

    with open(filename, "wb") as f:
        f.write(header)
        f.write(bytearray(padded_data))

    print(f"✅ Imagem BMP '{filename}' criada com sucesso!")

save_bmp_rgb888("imagem_rgb888_green_purple.bmp", 3145, 3226, "green_purple")
save_bmp_rgb888("imagem_rgb888_rgb_pattern.bmp", 2131, 4211, "rgb")
