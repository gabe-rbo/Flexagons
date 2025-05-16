from pathlib import Path
import os
import cv2

from PIL import Image, ImageDraw
from Tetraflexagonos.Facas.GeradorDeFacas import criar_marcas_registro_vetoriais

def right_triangle_crop(img: Image.Image, orientation='top-right'):
    """
    Crop image to right triangle with transparent background

    Parameters:
    - image_path: Input image path
    - output_path: Output path (must be PNG for transparency)
    - orientation: One of:
        'bottom-right' (default) - right angle at bottom-right
        'bottom-left' - right angle at bottom-left
        'top-right' - right angle at top-right
        'top-left' - right angle at top-left
    """
    img = img.convert('RGBA')
    width, height = img.size

    # Create transparent result image
    result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # Define points based on orientation
    if orientation == 'bottom-right':
        points = [(0, 0), (0, height), (width, height)]
    elif orientation == 'bottom-left':
        points = [(width, 0), (0, height), (width, height)]
    elif orientation == 'top-right':
        points = [(0, 0), (width, 0), (width, height)]
    elif orientation == 'top-left':
        points = [(0, 0), (width, 0), (0, height)]
    else:
        raise ValueError("Invalid orientation. Choose from: 'bottom-right', 'bottom-left', 'top-right', 'top-left'")

    # Draw the triangle and apply mask
    draw.polygon(points, fill=255)
    result.paste(img, (0, 0), mask=mask)

    return result


def create_triangle_mask(size, orientation='bottom-right'):
    """Create a triangular mask with specified orientation"""
    width, height = size
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)

    if orientation == 'bottom-right':
        points = [(0, 0), (0, height), (width, height)]
    elif orientation == 'bottom-left':
        points = [(width, 0), (0, height), (width, height)]
    elif orientation == 'top-right':
        points = [(0, 0), (width, 0), (width, height)]
    elif orientation == 'top-left':
        points = [(0, 0), (width, 0), (0, height)]
    else:
        raise ValueError("Invalid orientation")

    draw.polygon(points, fill=255)
    return mask

def paste_triangle_directly(IMGaserTriangulada, IMGaserColada,
                            orientation='bottom-right', position=(0, 0)):
    # Open images
    foreground = IMGaserTriangulada.convert('RGBA')
    background = IMGaserColada.convert('RGBA')

    # Create mask
    mask = create_triangle_mask((58, 58), orientation)

    # Apply mask to foreground
    foreground.putalpha(mask)

    # Composite images
    background.paste(foreground, position, foreground)

    return background


def plano(img1: str, img2: str, img3: str, img4: str, img5: str, img6: str, grafica: bool = False,
          nome_arq: str = ''):
    """
    Esse código é uma ramificação do Tritetraflexágono. As dimensões das imagens serão interpoladas para o mesmo tamanho.
    A mesma nomenclatura\notações se aplicam aqui.

    :param img1: Verso
    :param img2: Frente
    :param img3:
    :param img4:
    :param img5:
    :param img6:
    :param grafica:
    :return:
    """


    """
    img1 = Image.open(img1)
    img2 = Image.open(img2)
    img3 = Image.open(img3)
    img4 = Image.open(img4)
    img5 = Image.open(img5)
    img6 = Image.open(img6)

    imagens = [img1, img2, img3, img4, img5, img6]

    tem_imagem_muito_pequena = False
    for imagem in imagens:
        if imagem.size[0] * imagem.size[1] <= 320356 and not tem_imagem_muito_pequena:
            tem_imagem_muito_pequena = True"""

    tem_imagem_muito_pequena = False
    if not tem_imagem_muito_pequena:

        print('''
            >>> CORTANDO IMAGENS <<<
            ''')

        # Vamos editar e formar o plano
        """
        Para fazer isso, dividiremos cada imagem em quatro quadrantes, contados no mesmo sentido do cartesiano:
          2  |  1
        -----------
          3  |  4
        O python utiliza o canto superior esquerdo como a origem (0,0) do plano.  
        """

        print('REDIMENSIONANDO')

        if grafica:
            tamanho = (562 + 58) * 2
            tamanho_plano, tamanho_bordas, distancia_borda = (562 * 4 + 58 * 2 + 28 * 2, 562 * 4 + 58 * 2 + 28 * 2), (562, 58), 28 + 58
        elif not grafica:
            tamanho = 562 * 2  # Caso não seja preciso planos para gráfica, retiramos o incremento da largura da borda
            # do tamanho final das interpolações das imagens.
            tamanho_plano, tamanho_bordas, distancia_borda = (tamanho * 2 + 28 * 2 + 58, tamanho * 2 + 28 * 2 + 58), (562, 58), 28 + 28

        img1 = cv2.imread(img1)
        img2 = cv2.imread(img2)
        img3 = cv2.imread(img3)
        img4 = cv2.imread(img4)
        img5 = cv2.imread(img5)
        img6 = cv2.imread(img6)

        os.makedirs(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados', exist_ok=True)

        img1_resized = cv2.resize(img1, (tamanho, tamanho), interpolation=cv2.INTER_LANCZOS4)
        img2_resized = cv2.resize(img2, (tamanho, tamanho), interpolation=cv2.INTER_LANCZOS4)
        img3_resized = cv2.resize(img3, (tamanho, tamanho), interpolation=cv2.INTER_LANCZOS4)
        img4_resized = cv2.resize(img4, (tamanho, tamanho), interpolation=cv2.INTER_LANCZOS4)
        img5_resized = cv2.resize(img5, (tamanho, tamanho), interpolation=cv2.INTER_LANCZOS4)
        img6_resized = cv2.resize(img6, (tamanho, tamanho), interpolation=cv2.INTER_LANCZOS4)

        imgs_resized = [img1_resized, img2_resized, img3_resized, img4_resized, img5_resized, img6_resized]

        os.makedirs(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados', exist_ok=True)
        for i, img_resized in enumerate(imgs_resized):
            img = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img.save(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / f'img{i + 1}_resized.png')

        img1 = Image.open(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'img1_resized.png')
        img2 = Image.open(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'img2_resized.png')
        img3 = Image.open(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'img3_resized.png')
        img4 = Image.open(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'img4_resized.png')
        img5 = Image.open(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'img5_resized.png')
        img6 = Image.open(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'img6_resized.png')

        ajuste = 0
        if grafica:
            ajuste = tamanho_bordas[1]

        img1F1 = img1.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2)).rotate(180)
        img1F2 = img1.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2))
        img1F3 = img1.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste)).rotate(180)
        img1F4 = img1.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste))

        img2F1 = img2.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2)).rotate(180)
        img2F2 = img2.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2))
        img2F3 = img2.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste)).rotate(180)
        img2F4 = img2.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste))

        img3F1 = img3.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2)).rotate(180)
        img3F2 = img3.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2)).rotate(180)
        img3F3 = img3.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste)).rotate(180)
        img3F4 = img3.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste)).rotate(180)

        img4F1 = img4.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2)).rotate(270)
        img4F2 = img4.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2)).rotate(270)
        img4F3 = img4.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste)).rotate(270)
        img4F4 = img4.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste)).rotate(270)

        img5F1 = img5.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2)).rotate(90)
        img5F2 = img5.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2)).rotate(90)
        img5F3 = img5.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste)).rotate(90)
        img5F4 = img5.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste)).rotate(90)
        
        img6F1 = img6.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2))
        img6F2 = img6.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2))
        img6F3 = img6.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste))
        img6F4 = img6.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste))

        print("CRIANDO PLANOS")

        PlanoFrontal = Image.new('RGB', tamanho_plano, color='white')
        PlanoTraseiro = Image.new('RGB', tamanho_plano, color='white')

        # Montando Plano Frontal (Updated Coordinates)
        PlanoFrontal.paste(img4F3, (distancia_borda, distancia_borda))
        PlanoFrontal.paste(img2F1, (distancia_borda + int(tamanho / 2) - ajuste, distancia_borda))
        PlanoFrontal.paste(img6F2, (distancia_borda + tamanho - 2 * ajuste, distancia_borda))
        PlanoFrontal.paste(img6F1, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda))
        PlanoFrontal.paste(img2F2, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + int(tamanho / 2) - ajuste))
        PlanoFrontal.paste(img4F2, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + tamanho - 2 * ajuste))
        PlanoFrontal.paste(img4F1, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
        PlanoFrontal.paste(img2F3, (distancia_borda + tamanho - 2 * ajuste, distancia_borda + int(tamanho * 3 / 2 - 3 * ajuste)))
        PlanoFrontal.paste(img6F4, (distancia_borda + int(tamanho / 2) - ajuste, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
        PlanoFrontal.paste(img6F3, (distancia_borda, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
        PlanoFrontal.paste(img2F4, (distancia_borda, distancia_borda + tamanho - 2 * ajuste))
        PlanoFrontal.paste(img4F4, (distancia_borda, distancia_borda + int(tamanho / 2) - ajuste))

        # Montando Plano Traseiro (Updated Coordinates)
        PlanoTraseiro.paste(img5F4, (distancia_borda, distancia_borda))
        PlanoTraseiro.paste(img1F1, (distancia_borda + int(tamanho / 2) - ajuste, distancia_borda))
        PlanoTraseiro.paste(img3F1, (distancia_borda + tamanho - 2 * ajuste, distancia_borda))
        PlanoTraseiro.paste(img3F2, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda))
        PlanoTraseiro.paste(img1F2, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + int(tamanho / 2) - ajuste))
        PlanoTraseiro.paste(img5F1, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + tamanho - 2 * ajuste))
        PlanoTraseiro.paste(img5F2, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
        PlanoTraseiro.paste(img1F3, (distancia_borda + tamanho - 2 * ajuste, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
        PlanoTraseiro.paste(img3F3, (distancia_borda + int(tamanho / 2) - ajuste, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
        PlanoTraseiro.paste(img3F4, (distancia_borda, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
        PlanoTraseiro.paste(img1F4, (distancia_borda, distancia_borda + tamanho - 2 * ajuste))
        PlanoTraseiro.paste(img5F3, (distancia_borda, distancia_borda + int(tamanho / 2) - ajuste))

        if grafica:

            # Recorte das bordas do plano frontal
            B24F3 = img4.crop((0, tamanho / 2, ajuste, tamanho - ajuste)).rotate(270, expand=True)
            B34F3 = img4.crop((0, tamanho - ajuste, tamanho / 2, tamanho)).rotate(270, expand=True)
            B12F1 = img2.crop((tamanho / 2, 0, tamanho - ajuste, ajuste)).rotate(180, expand=True)
            B32F1 = img2.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(180, expand=True)
            B16F2 = img6.crop((ajuste, 0, tamanho / 2, ajuste))
            B36F2 = img6.crop((ajuste, tamanho / 2, tamanho / 2, tamanho / 2 + ajuste))
            B16F1 = img6.crop((tamanho / 2, 0, tamanho, ajuste))
            B46F1 = img6.crop((tamanho - ajuste, ajuste, tamanho, tamanho / 2))
            B42F2 = img2.crop((tamanho / 2, ajuste, tamanho / 2 + ajuste, tamanho / 2))
            B22F2 = img2.crop((0, ajuste, ajuste, tamanho / 2))
            B14F2 = img4.crop((ajuste, 0, tamanho / 2, ajuste)).rotate(270, expand=True)
            B14F1 = img4.crop((tamanho / 2, 0, tamanho - ajuste, ajuste)).rotate(270, expand=True)
            B34F2 = img4.crop((ajuste, tamanho / 2, tamanho / 2, tamanho / 2 + ajuste)).rotate(270, expand=True)
            B44F1 = img4.crop((tamanho - ajuste, 0, tamanho, tamanho / 2)).rotate(270, expand=True)
            B32F3 = img2.crop((ajuste, tamanho - ajuste, tamanho / 2, tamanho)).rotate(180, expand=True)
            B12F3 = img2.crop((ajuste, tamanho / 2 - ajuste, tamanho / 2, tamanho / 2)).rotate(180, expand=True)
            B16F4 = img6.crop((tamanho / 2, tamanho / 2 - ajuste, tamanho - ajuste, tamanho / 2))
            B36F4 = img6.crop((tamanho / 2, tamanho - ajuste, tamanho - ajuste, tamanho))
            B26F3 = img6.crop((0, tamanho / 2, ajuste, tamanho - ajuste))
            B36F3 = img6.crop((0, tamanho - ajuste, tamanho / 2, tamanho))
            B22F4 = img2.crop((tamanho / 2 - ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste))
            B42F4 = img2.crop((tamanho - ajuste, tamanho / 2, tamanho, tamanho - ajuste))
            B14F4 = img4.crop((tamanho / 2, tamanho / 2 - ajuste, tamanho - ajuste, tamanho / 2)).rotate(270, expand=True)
            B34F4 = img4.crop((tamanho / 2, tamanho - ajuste, tamanho - ajuste, tamanho)).rotate(270, expand=True)

            # Recorte das bordas do plano traseiro
            B45F4 = img5.crop((tamanho - ajuste, tamanho / 2, tamanho, tamanho - ajuste)).rotate(90, expand=True)
            B15F4 = img5.crop((tamanho / 2, tamanho / 2 - ajuste, tamanho, tamanho / 2)).rotate(90, expand=True)
            B11F1 = img1.crop((tamanho / 2, 0, tamanho, ajuste)).rotate(180)
            B31F1 = img1.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(180)
            B13F1 = img3.crop((tamanho / 2, 0, tamanho - ajuste, ajuste)).rotate(180)
            B33F1 = img3.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(180)
            B33F2 = img3.crop((ajuste, tamanho / 2, tamanho / 2 + ajuste, tamanho / 2 + ajuste)).rotate(180)
            B23F2 = img3.crop((0, ajuste, ajuste, tamanho / 2)).rotate(180)
            B21F2 = img1.crop((0, ajuste, ajuste, tamanho / 2))
            B41F2 = img1.crop((tamanho / 2, ajuste, tamanho / 2 + ajuste, tamanho / 2))
            B15F1 = img5.crop((tamanho / 2, 0, tamanho - ajuste, ajuste)).rotate(90, expand=True)
            B35F1 = img5.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(90, expand=True)
            B35F2 = img5.crop((0, tamanho / 2, tamanho / 2, tamanho / 2 + ajuste)).rotate(90, expand=True)
            B25F2 = img5.crop((0, ajuste, ajuste, tamanho / 2)).rotate(90, expand=True)
            B31F3 = img1.crop((0, tamanho - ajuste, tamanho / 2 - ajuste, tamanho)).rotate(180)
            B11F3 = img1.crop((ajuste, tamanho / 2 - ajuste, tamanho / 2, tamanho / 2)).rotate(180)
            B33F3 = img3.crop((ajuste, tamanho - ajuste, tamanho / 2, tamanho)).rotate(180)
            B13F3 = img3.crop((ajuste, tamanho / 2 - ajuste, tamanho / 2, tamanho / 2)).rotate(180)
            B13F4 = img3.crop((tamanho / 2, tamanho / 2 - ajuste, tamanho, tamanho / 2)).rotate(180)
            B43F4 = img3.crop((tamanho - ajuste, tamanho / 2, tamanho, tamanho - ajuste)).rotate(180)
            B21F4 = img1.crop((tamanho / 2 - ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste))
            B41F4 = img1.crop((tamanho - ajuste, tamanho / 2, tamanho, tamanho - ajuste))
            B15F3 = img5.crop((ajuste, tamanho / 2 - ajuste, tamanho / 2, tamanho / 2)).rotate(90, expand=True)
            B35F3 = img5.crop((ajuste, tamanho - ajuste, tamanho / 2, tamanho)).rotate(90, expand=True)

            # Bordinhas do plano frontal
            PlanoFrontal.paste(B24F3, (28 + ajuste, 28))
            PlanoFrontal.paste(B34F3, (28, 28))
            PlanoFrontal.paste(B32F1, (28 + 562 + ajuste, 28))
            PlanoFrontal.paste(B12F1, (28 + 562 + ajuste, 28 + 562 + ajuste))
            PlanoFrontal.paste(B16F2, (28 + 2 * 562 + ajuste, 28))
            PlanoFrontal.paste(B36F2, (28 + 2 * 562 + ajuste, 28 + 562 + ajuste))
            PlanoFrontal.paste(B16F1, (28 + 3 * 562 + ajuste, 28))
            PlanoFrontal.paste(B46F1, (28 + 4 * 562 + ajuste, 28 + ajuste))
            PlanoFrontal.paste(B42F2, (28 + 4 * 562 + ajuste, 28 + 562 + ajuste))

            # Vamos precisar de uma junta triangular aqui
            B36F2_q = B36F2.crop((562 - ajuste, 0, 562, ajuste))
            B22F2 = paste_triangle_directly(B36F2_q, B22F2, 'top-left')
            PlanoFrontal.paste(B22F2, (28 + 3 * 562, 28 + 562 + ajuste))

            PlanoFrontal.paste(B14F2, (28 + 4 * 562 + ajuste, 28 + 2 * 562 + ajuste))
            PlanoFrontal.paste(B14F1, (28 + 4 * 562 + ajuste, 28 + 3 * 562 + ajuste))
            PlanoFrontal.paste(B34F2, (28 + 3 * 562         , 28 + 2 * 562 + ajuste))
            PlanoFrontal.paste(B44F1, (28 + 3 * 562 + ajuste, 28 + 4 * 562 + ajuste))

            # Vamos precisar de mais uma junta triangular.
            B34F2_q = B34F2.crop((0, 562 - ajuste, ajuste, 562))
            B32F3 = paste_triangle_directly(B34F2_q, B32F3, 'top-right', position=(562 - ajuste, 0))
            PlanoFrontal.paste(B32F3, (562 * 2 + 28 + ajuste, 28 + 562 * 3))

            PlanoFrontal.paste(B12F3, (562 * 2 + 28 + ajuste, 28 + 562 * 4 + ajuste))
            PlanoFrontal.paste(B16F4, (562 * 1 + 28 + ajuste, 28 + 562 * 3))
            PlanoFrontal.paste(B36F4, (562 * 1 + 28 + ajuste, 28 + 562 * 4 + ajuste))
            PlanoFrontal.paste(B26F3, (28, 28 + 562 * 3 + ajuste))
            PlanoFrontal.paste(B36F3, (28, 28 + 562 * 4 + ajuste))
            PlanoFrontal.paste(B22F4, (28, 28 + 562 * 2 + ajuste))

            # Vamos precisar de mais uma junta triangular
            B16F4_q = (B16F4.crop((0, 0, ajuste, ajuste)))
            B42F4 = paste_triangle_directly(B16F4_q, B42F4, 'bottom-left', position=(0, 562 - ajuste))
            PlanoFrontal.paste(B42F4, (562 * 1 + 28 + ajuste, 28 + 562 * 2 + ajuste))

            PlanoFrontal.paste(B34F4, (28, 28 + 562 * 1 + ajuste))

            # Última junta triangular do plano frontal
            B12F1_q = B12F1.crop((0, 0, ajuste, ajuste))
            B14F4 = paste_triangle_directly(B12F1_q, B14F4, 'top-right')
            PlanoFrontal.paste(B14F4, (28 + 562 + ajuste, 28 + 562 + ajuste))

            # Agora vamos montar o Plano Traseiro
            # ----------------------------------------------------------------------------------------------------------

            PlanoTraseiro.paste(B45F4, (28 + ajuste, 28))
            PlanoTraseiro.paste(B15F4, (28, 28))
            PlanoTraseiro.paste(B31F1, (28 + 562 + ajuste, 28))
            PlanoTraseiro.paste(B11F1, (28 + 562 + ajuste, 28 + 562 + ajuste))
            PlanoTraseiro.paste(B33F1, (28 + 2 * 562 + ajuste, 28))
            PlanoTraseiro.paste(B13F1, (28 + 2 * 562 + ajuste, 28 + 562 + ajuste))
            PlanoTraseiro.paste(B33F2, (28 + 3 * 562 + ajuste, 28))
            PlanoTraseiro.paste(B23F2, (28 + 4 * 562 + ajuste, 28 + ajuste))
            PlanoTraseiro.paste(B41F2, (28 + 4 * 562 + ajuste, 28 + 562 + ajuste))

            # Vamos precisar de uma junta triangular aqui
            B13F1_q = B13F1.crop((562 - ajuste, 0, 562, ajuste))
            B21F2 = paste_triangle_directly(B13F1_q, B21F2, 'top-left')
            PlanoTraseiro.paste(B21F2, (28 + 3 * 562, 28 + 562 + ajuste))

            PlanoTraseiro.paste(B35F1, (28 + 4 * 562 + ajuste, 28 + 2 * 562 + ajuste))
            PlanoTraseiro.paste(B35F2, (28 + 4 * 562 + ajuste, 28 + 3 * 562 + ajuste))
            PlanoTraseiro.paste(B15F1, (28 + 3 * 562         , 28 + 2 * 562 + ajuste))
            PlanoTraseiro.paste(B25F2, (28 + 3 * 562 + ajuste, 28 + 4 * 562 + ajuste))

            # Vamos precisar de mais uma junta triangular.
            B15F1_q = B15F1.crop((0, 562 - ajuste, ajuste, 562))
            B31F3 = paste_triangle_directly(B15F1_q, B31F3, 'top-right', position=(562 - ajuste, 0))
            PlanoTraseiro.paste(B31F3, (562 * 2 + 28 + ajuste, 28 + 562 * 3))

            PlanoTraseiro.paste(B11F3, (562 * 2 + 28 + ajuste, 28 + 562 * 4 + ajuste))
            PlanoTraseiro.paste(B33F3, (562 * 1 + 28 + ajuste, 28 + 562 * 3))
            PlanoTraseiro.paste(B13F3, (562 * 1 + 28 + ajuste, 28 + 562 * 4 + ajuste))
            PlanoTraseiro.paste(B43F4, (28, 28 + 562 * 3 + ajuste))
            PlanoTraseiro.paste(B13F4, (28, 28 + 562 * 4 + ajuste))
            PlanoTraseiro.paste(B21F4, (28, 28 + 562 * 2 + ajuste))

            # Vamos precisar de mais uma junta triangular
            B33F3_q = (B33F3.crop((0, 0, ajuste, ajuste)))
            B41F4 = paste_triangle_directly(B33F3_q, B41F4, 'bottom-left', position=(0, 562 - ajuste))
            PlanoTraseiro.paste(B41F4, (562 * 1 + 28 + ajuste, 28 + 562 * 2 + ajuste))

            PlanoTraseiro.paste(B15F3, (28, 28 + 562 * 1 + ajuste))

            # Última junta triangular do plano traseiro
            B11F1_q = B11F1.crop((0, 0, ajuste, ajuste))
            B35F3 = paste_triangle_directly(B11F1_q, B35F3, 'top-right')
            PlanoTraseiro.paste(B35F3, (28 + 562 + ajuste, 28 + 562 + ajuste))

            PlanoFrontal = criar_marcas_registro_vetoriais(PlanoFrontal)
            PlanoTraseiro = criar_marcas_registro_vetoriais(PlanoTraseiro)

        if nome_arq:
            PlanoFrontal.save(f'Plano_Frontal_{nome_arq}.png')
            PlanoTraseiro.save(f'Plano_Traseiro_{nome_arq}.png')

        else:
            PlanoFrontal.save("PlanoFrontal.png")
            PlanoTraseiro.save("PlanoTraseiro.png")
 
plano('teste/face1.png', 'teste/face2.png', 'teste/face3.png',
     'teste/face4.png', 'teste/face5.png', 'teste/face6.png', grafica=True, nome_arq='Teste')
