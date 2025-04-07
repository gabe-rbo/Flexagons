from PIL import Image, ImageDraw
import math


def criar_marcas_registro_vetoriais(img: Image.Image, tamanho=(2420, 2420), margem=28, cor="black"):
    """
    Cria marcas de registro vetoriais profissionais para impressão gráfica.

    Parâmetros:
        output_path: caminho para salvar a imagem
        tamanho: tupla (largura, altura) em pixels
        margem: distância das marcas para as bordas
        cor: cor das marcas (pode ser RGB tuple ou string)
    """
    # Criar imagem em modo RGBA para suporte a transparência
    img = img.convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Configurações das marcas
    comprimento_marca = 20
    espessura = 2
    offset_cruz = 15  # Para a cruz central

    # Posições dos cantos (x, y)
    cantos = [
        (margem, margem),  # Superior esquerdo
        (tamanho[0] - margem, margem),  # Superior direito
        (margem, tamanho[1] - margem),  # Inferior esquerdo
        (tamanho[0] - margem, tamanho[1] - margem)  # Inferior direito
    ]

    # Desenhar marcas de canto
    for x, y in cantos:
        # Linhas horizontais
        draw.line([(x - comprimento_marca, y), (x, y)], fill=cor, width=espessura)
        draw.line([(x, y), (x + comprimento_marca, y)], fill=cor, width=espessura)
        # Linhas verticais
        draw.line([(x, y - comprimento_marca), (x, y)], fill=cor, width=espessura)
        draw.line([(x, y), (x, y + comprimento_marca)], fill=cor, width=espessura)

    # Cruz central de registro
    centro_x, centro_y = tamanho[0] // 2, tamanho[1] // 2
    draw.line([
        (centro_x - offset_cruz, centro_y),
        (centro_x + offset_cruz, centro_y)
    ], fill=cor, width=espessura)
    draw.line([
        (centro_x, centro_y - offset_cruz),
        (centro_x, centro_y + offset_cruz)
    ], fill=cor, width=espessura)

    # Círculo de registro central
    raio_circulo = 10
    draw.ellipse([
        (centro_x - raio_circulo, centro_y - raio_circulo),
        (centro_x + raio_circulo, centro_y + raio_circulo)
    ], outline=cor, width=espessura)

    # Linhas guia diagonais (opcional)
    draw.line([
        (centro_x - offset_cruz, centro_y - offset_cruz),
        (centro_x + offset_cruz, centro_y + offset_cruz)
    ], fill=cor, width=1)
    draw.line([
        (centro_x - offset_cruz, centro_y + offset_cruz),
        (centro_x + offset_cruz, centro_y - offset_cruz)
    ], fill=cor, width=1)

    # Salvar como PNG com fundo transparente
    # img.save(output_path, "PNG", dpi=(300, 300))  # Configurar DPI para impressão
    return img

def draw_dotted_line(draw, start, end, fill, width=1, dash_length=5, gap_length=5):
    """Draw a dotted line between two points"""
    x1, y1 = start
    x2, y2 = end

    # Calculate line length and angle
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    angle = math.atan2(y2 - y1, x2 - x1)

    # Calculate dash and gap steps
    dash_gap = dash_length + gap_length
    steps = int(length / dash_gap)

    for i in range(steps + 1):
        start_dash = x1 + math.cos(angle) * i * dash_gap, y1 + math.sin(angle) * i * dash_gap
        end_dash = x1 + math.cos(angle) * (i * dash_gap + dash_length), y1 + math.sin(angle) * (
                    i * dash_gap + dash_length)
        draw.line([start_dash, end_dash], fill=fill, width=width)

# Create a blank white image
width, height = 2420, 2420
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Draw shapes
draw.line([28 + 58, 28 + 58, 2420 - 28 - 58, 28 + 58], width=5, fill='black')
draw.line([28 + 58, 2420 - 28 - 58, 2420 - 28 - 58, 2420 - 28 - 58], width=5, fill='black')
draw.line([28 + 58, 28 + 58, 28 + 58, 2420 - 28 - 58], width=5, fill='black')
draw.line([2420 - 28 - 58, 28 + 58, 2420 - 28 - 58, 2420 - 28 - 58], width=5, fill='black')
draw.line([2420 - 1772, 648, 1772, 648], width=5, fill='black')
draw.line([2420 - 1772, 2420 - 648, 1772, 2420 - 648], width=5, fill='black')
draw.line([2420 - 1772, 648, 2420 - 1772, 2420 - 648], width=5, fill='black')
draw.line([1772, 648, 1772, 2420 - 648], width=5, fill='black')

draw_dotted_line(draw, (2420 - 1772, 28 + 58), (2420 - 1772, 562 + 28 + 58), 'black', width=5, dash_length=50, gap_length=35)
draw_dotted_line(draw, (2420 - 1772 + 562, 28 + 58), (2420 - 1772 + 562, 562 + 28 + 58), 'black', width=5, dash_length=50, gap_length=35)
draw_dotted_line(draw, (2420 - 1772 + 562 * 2, 28 + 58), (2420 - 1772 + 562 * 2, 562 + 28 + 58), 'black', width=5, dash_length=50, gap_length=35)
draw_dotted_line(draw, (2420 - 1772, 28 + 58 + 562 * 3), (2420 - 1772, 562 * 4 + 28 + 58), 'black', width=5, dash_length=50, gap_length=35)
draw_dotted_line(draw, (2420 - 1772 + 562, 28 + 58 + 562 * 3), (2420 - 1772 + 562, 562 * 4 + 28 + 58), 'black', width=5, dash_length=50, gap_length=35)
draw_dotted_line(draw, (2420 - 1772 + 562 * 2, 28 + 58 + 562 * 3), (2420 - 1772 + 562 * 2, 562 * 4 + 28 + 58), 'black', width=5, dash_length=50, gap_length=35)
draw_dotted_line(draw, (28 + 58, 28 + 58 + 562), (28 + 58 + 562, 28 + 58 + 562), 'black', width=5, dash_length=50, gap_length=35)
draw_dotted_line(draw, (28 + 58 + 562 * 3, 28 + 58 + 562), (28 + 58 + 562 * 4, 28 + 58 + 562), 'black', width=5, dash_length=50, gap_length=35)
draw_dotted_line(draw, (28 + 58 + 562 * 0, 28 + 58 + 562 * 2), (28 + 58 + 562 * 1, 28 + 58 + 562 * 2), 'black', width=5, dash_length=50, gap_length=35)
draw_dotted_line(draw, (28 + 58 + 562 * 3, 28 + 58 + 562 * 2), (28 + 58 + 562 * 4, 28 + 58 + 562 * 2), 'black', width=5, dash_length=50, gap_length=35)
draw_dotted_line(draw, (28 + 58 + 562 * 0, 28 + 58 + 562 * 3), (28 + 58 + 562 * 1, 28 + 58 + 562 * 3), 'black', width=5, dash_length=50, gap_length=35)
draw_dotted_line(draw, (28 + 58 + 562 * 3, 28 + 58 + 562 * 3), (28 + 58 + 562 * 4, 28 + 58 + 562 * 3), 'black', width=5, dash_length=50, gap_length=35)

draw.line([58 + 28, 0, 58 + 28, 58], width=3, fill='gray')
draw.line([0, 58 + 28, 58, 58 + 28], width=3, fill='gray')

draw.line([58 + 28, 2420, 58 + 28, 2420 - 58], width=3, fill='gray')
draw.line([0, 2420 - 58 - 28, 58, 2420 - 58 - 28], width=3, fill='gray')

draw.line([2420 - 58, 2420 - 58 - 28, 2420, 2420 - 58 - 28], width=3, fill='gray')
draw.line([2420 - 58 - 28, 2420 - 58, 2420 - 58 - 28, 2420], width=3, fill='gray')

draw.line([2420 - 58 - 28, 0, 2420 - 58 - 28, 58], width=3, fill='gray')
draw.line([2420 - 58, 58 + 28, 2420, 58 + 28], width=3, fill='gray')

image = criar_marcas_registro_vetoriais(image)

# Save as PNG
image.save("faca.png", "PNG")