from PIL import Image
from pathlib import Path
import os
import cv2


def plano(imgF: str, imgV: str, imgE: str, grafica: bool = False, montagem_simplificada: bool = False) -> None:
    """
    Função que define o plano final.
    Precisaremos de 3 imagens, as quais serão tratadas usando a biblioteca PIL.
    No roteiro enviado por Aniura, 2 representa a imagem que ficará na frente, 3 atrás e 1 será a imagem escondida.
    A notação utilizada no roteiro para representar as faces é simples: a(b), onde a é a face que está sendo vista e b à
    do verso do quadrado. Aqui, no entanto, usaremos a notação FaVb onde Fa representa "frente a" e Vb representa "verso
    b".

    As imagens são geradas em considerando 300 pixeis por polegada. (300DPI ~ 118 pixeis por centímetro)

    Características das imagens:
    1) É bom que sejam quadradas, pelo menos com boa resolução.
    2) O formato do arquivo deve ser PNG.
    3) Elas devem ter o mesmo tamanho.
    4) Eles serão formatadas para que os quadrados do plano tenham (562 + 58)px^2 e as sangrias 58px.

    Tamanho recomendado das imagens: 3.200 x 3.200 pixels

    Característica dos Planos:
    1) O tamanho do plano deve ser de 2980px x 1297px.

    :param imgF:  Imagem da frente do tritetraflexágono. A string deve ser o caminho da imagem.
    :param imgV: Imagem do verso do tritetraflexágono. A string deve ser o caminho da imagem.
    :param imgE: Imagem escondida do tritetraflexágono. A string deve ser o caminho da imagem.
    :param bordas: Esse parâmetro define a geração para ser enviada à gráfica: as bordas são levemente esticadas para
        guilhotina.
    :param montagem_simplificada: Esse parâmetro define se a montagem do tritetraflexágono será diferente da usual, isto
        pois há uma diferença na ordem das imagens. A imagem do verso se torna a imagem escondida e a imagem escondida
        se torna a imagem do verso.
    :return: A função não retorna nada, porém salva arquivos PNG dos planos gerados.
    """

    print('''
    >>> TRATANDO IMAGENS <<<
    ''')

    imFrente = Image.open(imgF)
    imVerso = Image.open(imgV)
    imEscondida = Image.open(imgE)
    ims = [imFrente, imVerso, imEscondida]

    tem_imagem_muito_pequena = False
    for im in ims:
        if im.size[0] * im.size[1] <= 320356 and not tem_imagem_muito_pequena:
            tem_imagem_muito_pequena = True

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

        if grafica:
            tamanho = (562 + 58) * 2
            tamanho_plano, tamanho_bordas, distancia_borda = (2980, 1297), (562, 58), 28 + 58
        elif not grafica:
            tamanho = 562 * 2  # Caso não seja preciso planos para gráfica, retiramos o incremento da largura da borda
            # do tamanho final das interpolações das imagens.
            tamanho_plano, tamanho_bordas, distancia_borda = (2980 - 58, 1297 - 58), (562, 58), 28 + 28

        frente = cv2.imread(imgF)
        verso = cv2.imread(imgV)
        escondida = cv2.imread(imgE)

        os.makedirs(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados', exist_ok=True)

        frente_resized = cv2.resize(frente, (tamanho, tamanho), interpolation=cv2.INTER_LANCZOS4)
        verso_resized = cv2.resize(verso, (tamanho, tamanho), interpolation=cv2.INTER_LANCZOS4)
        escondida = cv2.resize(escondida, (tamanho, tamanho), interpolation=cv2.INTER_LANCZOS4)

        cv2.imwrite(f"{Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'frente_resized.png'}", frente_resized)
        cv2.imwrite(f"{Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'verso_resized.png'}", verso_resized)
        cv2.imwrite(f"{Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'escondida_resized.png'}", escondida)

        imFrente = Image.open(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'frente_resized.png')
        imVerso = Image.open(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'verso_resized.png')
        imEscondida = Image.open(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / 'escondida_resized.png')

        if montagem_simplificada:
            # O verso troca de lugar com a escondida.
            temp = imVerso
            imVerso = imEscondida
            imEscondida = temp

        ajuste = 0
        if grafica:
            ajuste = tamanho_bordas[1]  # ajuste para as bordas serem parte da imagem.

            # Bordas do plano frontal
            # Imagens F.
            """B1F1 = imFrente.crop((tamanho/2, 0, tamanho, ajuste))
            B4F1 = imFrente.crop((tamanho - ajuste, 0, tamanho, tamanho/2))
            B2F4 = imFrente.crop((tamanho/2 - ajuste, tamanho / 2, tamanho / 2, tamanho))
            B3F4 = imFrente.crop((tamanho/2, tamanho - ajuste, tamanho - ajuste, tamanho))"""

            # Teste Aniura
            B1F1 = imFrente.crop((tamanho/2, 0, tamanho, ajuste)).rotate(180)
            B2F1 = imFrente.crop((tamanho/2 - ajuste, 0, tamanho / 2, tamanho / 2)).rotate(180)
            B4F1 = imFrente.crop((tamanho - ajuste, 0, tamanho, tamanho/2)).rotate(180)
            B2F4 = imFrente.crop((tamanho/2 - ajuste, tamanho / 2, tamanho / 2, tamanho)).rotate(180)
            B3F4 = imFrente.crop((tamanho/2, tamanho - ajuste, tamanho - ajuste, tamanho)).rotate(180)

            # Imagens V.
            B1V3 = imVerso.crop((ajuste, tamanho/2 - ajuste, tamanho / 2, tamanho / 2))
            B3V3 = imVerso.crop((ajuste, tamanho - ajuste, tamanho / 2, tamanho))
            B1V4 = imVerso.crop((tamanho/2, tamanho/2 - ajuste, tamanho, tamanho / 2))
            B3V4 = imVerso.crop((tamanho / 2, tamanho - ajuste, tamanho - ajuste, tamanho))
            B4V4 = imVerso.crop((tamanho - ajuste, tamanho / 2, tamanho, tamanho))

            # Imagens E.
            B1E1 = imEscondida.crop((tamanho/2, 0, tamanho - ajuste, ajuste))
            B3E1 = imEscondida.crop((tamanho/2, tamanho/2, tamanho - ajuste, ajuste + tamanho/2))
            B1E2 = imEscondida.crop((0, 0, tamanho/2, ajuste))
            B2E2 = imEscondida.crop((0, 0, ajuste, tamanho/2))
            B3E2 = imEscondida.crop((0, tamanho/2, tamanho / 2, tamanho / 2 + ajuste))
            # ---------------------------------------------------------------------------------------------------------

            # Bordas do plano traseiro
            # Imagens F
            """B1F2 = imFrente.crop((ajuste, 0, tamanho/2, ajuste)).rotate(180)
            B2F2 = imFrente.crop((0, 0, ajuste, tamanho/2)).rotate(180)
            B4F2 = imFrente.crop((tamanho/2, 0, tamanho/2 + ajuste, tamanho/2)).rotate(180)
            B2F3 = imFrente.crop((0, tamanho/2, ajuste, tamanho)).rotate(180)
            B3F3 = imFrente.crop((ajuste, tamanho - ajuste, tamanho / 2, tamanho)).rotate(180)"""

            # Teste Aniura
            B1F2 = imFrente.crop((ajuste, 0, tamanho/2, ajuste))
            #B2F2 = imFrente.crop((0, 0, ajuste, tamanho / 2)).rotate(180)
            B4F2 = imFrente.crop((tamanho/2, 0, tamanho/2 + ajuste, tamanho/2))
            B2F3 = imFrente.crop((0, tamanho/2, ajuste, tamanho))
            B3F3 = imFrente.crop((ajuste, tamanho - ajuste, tamanho / 2, tamanho))

            # Imagens E
            B1E3 = imEscondida.crop((ajuste, tamanho/2 - ajuste, tamanho/2, tamanho/2)).rotate(180)
            B3E3 = imEscondida.crop((ajuste, tamanho - ajuste, tamanho / 2, tamanho)).rotate(180)
            B3E4 = imEscondida.crop((tamanho/2, tamanho - ajuste, tamanho - ajuste, tamanho)).rotate(180)
            B4E4 = imEscondida.crop((tamanho - ajuste, tamanho / 2, tamanho, tamanho)).rotate(180)

            # Imagens V.
            B2V2 = imVerso.crop((0, 0, ajuste, tamanho/2)).rotate(180)
            B1V2 = imVerso.crop((ajuste, 0, tamanho/2, ajuste)).rotate(180)
            B1V1 = imVerso.crop((tamanho/2, 0, tamanho - ajuste, ajuste)).rotate(180)
            B3V1 = imVerso.crop((tamanho/2, tamanho/2, tamanho - ajuste, tamanho/2 + ajuste)).rotate(180)
            B4V1 = imVerso.crop((tamanho - ajuste, 0, tamanho, tamanho/2 + ajuste)).rotate(180)

        # quadrantes da frente
        F1 = imFrente.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2))
        F2 = imFrente.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2))
        F3 = imFrente.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste))
        F4 = imFrente.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste))

        # quadrantes do verso
        V1 = imVerso.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2))
        V2 = imVerso.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2))
        V3 = imVerso.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste))
        V4 = imVerso.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste))

        # quadrantes da escondida
        E1 = imEscondida.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2))
        E2 = imEscondida.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2))
        E3 = imEscondida.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste))
        E4 = imEscondida.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste))

        # criamos os planos e a caixa auxiliar
        PlanoFrontal = Image.new('RGB', size=tamanho_plano, color='white')
        PlanoTraseiro = Image.new('RGB', size=tamanho_plano, color='white')

        # Vamos começar montando o plano da frente da esquerda para a direita

        print('''
        >>> CRIANDO PLANOS <<<
        ''')

        PlanoFrontal.paste(E2, box=(distancia_borda, distancia_borda))  # Colocamos a primeira peça. Vamos colar a outra do lado.
        PlanoFrontal.paste(E1, box=(int(tamanho / 2) + distancia_borda - ajuste, distancia_borda))  # Colocamos + tamanho ao lado da anterior.
        #PlanoFrontal.paste(F1, box=(tamanho + distancia_borda - 2 * ajuste, distancia_borda))  # Colocamos outra ao lado
        PlanoFrontal.paste(F2, box=(tamanho + distancia_borda - 2 * ajuste, distancia_borda))
        # Terminamos a linha de cima

        # começamos a linha de baixo
        # PlanoFrontal.paste(F4, box=(tamanho + distancia_borda - 2 * ajuste, round(tamanho / 2) + distancia_borda - ajuste))
        PlanoFrontal.paste(F3, box=(tamanho + distancia_borda - 2 * ajuste, round(tamanho / 2) + distancia_borda - ajuste))
        PlanoFrontal.paste(V3, box=(round(tamanho * 3 / 2) + distancia_borda - 3 * ajuste, round(tamanho / 2 + distancia_borda - ajuste)))
        PlanoFrontal.paste(V4, box=(2 * tamanho + distancia_borda - 4 * ajuste, int(tamanho / 2) + distancia_borda - ajuste))
        # terminamos a linha de baixo

        # vamos rotacionar as imagens do verso.
        V1 = V1.rotate(180)
        V2 = V2.rotate(180)
        #F2 = F2.rotate(180)
        #F3 = F3.rotate(180)
        F1 = F1.rotate(180)
        F4 = F4.rotate(180)
        E3 = E3.rotate(180)
        E4 = E4.rotate(180)

        # Vamos montar o plano do verso, iniciado pela linha de baixo
        PlanoTraseiro.paste(V1, box=(round(tamanho / 2) + distancia_borda - ajuste, round(tamanho / 2) + distancia_borda - ajuste))
        PlanoTraseiro.paste(V2, box=(tamanho + distancia_borda - 2 * ajuste, round(tamanho / 2) + distancia_borda - ajuste))
        #PlanoTraseiro.paste(F2, box=(tamanho * 2 + distancia_borda - 4 * ajuste, round(tamanho / 2) + distancia_borda - ajuste))
        PlanoTraseiro.paste(F1, box=(tamanho * 2 + distancia_borda - 4 * ajuste, round(tamanho / 2) + distancia_borda - ajuste))
        # terminamos a linha de baixo

        # fazemos a linha de cima
        PlanoTraseiro.paste(E4, box=(tamanho + distancia_borda - 2 * ajuste, 0 + distancia_borda + ajuste - ajuste))
        PlanoTraseiro.paste(E3, box=(round(tamanho * 3 / 2) + distancia_borda - 3 * ajuste, 0 + distancia_borda + ajuste - ajuste))
        #PlanoTraseiro.paste(F3, box=(tamanho * 2 + distancia_borda - 4 * ajuste, 0 + distancia_borda + ajuste - ajuste))
        PlanoTraseiro.paste(F4, box=(tamanho * 2 + distancia_borda - 4 * ajuste, 0 + distancia_borda + ajuste - ajuste))
        # terminamos a linha de cima

        if grafica:
            # Vamos colar as bordas do Plano Frontal
            PlanoFrontal.paste(B1E2, box=(distancia_borda - ajuste, distancia_borda - ajuste))
            PlanoFrontal.paste(B2E2, box=(distancia_borda - ajuste, distancia_borda - ajuste))
            PlanoFrontal.paste(B3E2, box=(distancia_borda - ajuste, distancia_borda - ajuste + int(tamanho/2)))
            PlanoFrontal.paste(B1E1, box=(distancia_borda - ajuste + int(tamanho/2), distancia_borda - ajuste))
            PlanoFrontal.paste(B3E1, box=(distancia_borda - ajuste + int(tamanho/2), distancia_borda - ajuste + int(tamanho/2)))
            #PlanoFrontal.paste(B1F1, box=(distancia_borda - 2 * ajuste + tamanho, distancia_borda - ajuste))
            PlanoFrontal.paste(B1F2, box=(distancia_borda - 2 * ajuste + tamanho, distancia_borda - ajuste))
            #PlanoFrontal.paste(B4F1, box=(distancia_borda - 3 * ajuste + int(tamanho * 1.5), distancia_borda - ajuste))
            PlanoFrontal.paste(B4F2, box=(distancia_borda - 3 * ajuste + int(tamanho * 1.5), distancia_borda - ajuste))
            #PlanoFrontal.paste(B2F4, box=(distancia_borda - 3 * ajuste + tamanho, distancia_borda - ajuste + int(tamanho / 2)))
            PlanoFrontal.paste(B2F3, box=(distancia_borda - 3 * ajuste + tamanho, distancia_borda - ajuste + int(tamanho / 2)))
            #PlanoFrontal.paste(B3F4, box=(distancia_borda - 2 * ajuste + tamanho, distancia_borda - 2 * ajuste + int(tamanho)))
            PlanoFrontal.paste(B3F3, box=(distancia_borda - 2 * ajuste + tamanho, distancia_borda - 2 * ajuste + int(tamanho)))
            PlanoFrontal.paste(B1V3, box=(distancia_borda - 3 * ajuste + int(tamanho * 1.5), distancia_borda - 2 * ajuste + int(tamanho / 2)))
            PlanoFrontal.paste(B3V3, box=(distancia_borda - 3 * ajuste + int(tamanho * 1.5), distancia_borda - 2 * ajuste + int(tamanho)))
            PlanoFrontal.paste(B1V4, box=(distancia_borda - 4 * ajuste + tamanho * 2, distancia_borda - 2 * ajuste + int(tamanho / 2)))
            PlanoFrontal.paste(B3V4, box=(distancia_borda - 4 * ajuste + tamanho * 2, distancia_borda - 2 * ajuste + int(tamanho)))
            PlanoFrontal.paste(B4V4, box=(distancia_borda - 5 * ajuste + int(tamanho * 2.5), distancia_borda - ajuste + int(tamanho / 2)))

            # Vamos colar as bordas do plano traseiro.
            PlanoTraseiro.paste(B4V1, box=(distancia_borda + int(tamanho/2) - 2 * ajuste, int(tamanho/2) + distancia_borda - 2 * ajuste))
            PlanoTraseiro.paste(B3V1, box=(distancia_borda + int(tamanho/2) - ajuste, int(tamanho/2) + distancia_borda - 2 * ajuste))
            PlanoTraseiro.paste(B1V1, box=(distancia_borda + int(tamanho/2) - ajuste, tamanho + distancia_borda - 2 * ajuste))
            PlanoTraseiro.paste(B1V2, box=(distancia_borda + tamanho - 2 * ajuste, tamanho + distancia_borda - 2 * ajuste))
            PlanoTraseiro.paste(B2V2, box=(distancia_borda + int(tamanho * 1.5) - 3 * ajuste, distancia_borda + int(tamanho/2) - ajuste))
            PlanoTraseiro.paste(B4E4, box=(distancia_borda + tamanho - 3 * ajuste, distancia_borda - ajuste))
            PlanoTraseiro.paste(B3E4, box=(distancia_borda + tamanho - 2 * ajuste, distancia_borda - ajuste))
            PlanoTraseiro.paste(B3E3, box=(distancia_borda + int(tamanho * 1.5) - 3 * ajuste, distancia_borda - ajuste))
            #PlanoTraseiro.paste(B3F3, box=(distancia_borda + tamanho * 2 - 4 * ajuste, distancia_borda - ajuste))
            PlanoTraseiro.paste(B3F4, box=(distancia_borda + tamanho * 2 - 4 * ajuste, distancia_borda - ajuste))
            #PlanoTraseiro.paste(B2F3, box=(distancia_borda + int(tamanho * 2.5) - 5 * ajuste, distancia_borda - ajuste))
            PlanoTraseiro.paste(B2F4, box=(distancia_borda + int(tamanho * 2.5) - 5 * ajuste, distancia_borda - ajuste))
            #PlanoTraseiro.paste(B2F2, box=(distancia_borda + int(tamanho * 2.5) - 5 * ajuste, distancia_borda + int(tamanho / 2) - ajuste))
            PlanoTraseiro.paste(B2F1, box=(distancia_borda + int(tamanho * 2.5) - 5 * ajuste, distancia_borda + int(tamanho / 2) - ajuste))  # queremos arrumar isso
            #PlanoTraseiro.paste(B1F2, box=(distancia_borda + tamanho * 2 - 4 * ajuste, distancia_borda + tamanho - 2 * ajuste))
            PlanoTraseiro.paste(B1F1, box=(distancia_borda + tamanho * 2 - 4 * ajuste, distancia_borda + tamanho - 2 * ajuste))
            #PlanoTraseiro.paste(B4F2, box=(distancia_borda + tamanho * 2 - 5 * ajuste, distancia_borda + int(tamanho/2) - ajuste))
            PlanoTraseiro.paste(B4F1, box=(distancia_borda + tamanho * 2 - 5 * ajuste, distancia_borda + int(tamanho/2) - ajuste))
            PlanoTraseiro.paste(B1E3, box=(distancia_borda + int(tamanho * 1.5) - 3 * ajuste, distancia_borda + int(tamanho/2) - ajuste))

            """
            Para gerar as imagens com as facas ou apenas as marcas de corte, basta mudar os caminhos em MarcasFrontais 
            e Marcas Traseiras. A pasta 'Cortes' contém as marcas de corte e a pasta "Facas" contém as facas.
            """

            MarcasFrontais = Image.open(Path(os.getcwd()) / "Cortes" / "CorteFrontal.png")
            _, _, _, mask = MarcasFrontais.split()
            PlanoFrontal.paste(MarcasFrontais, (0, 0), mask)
            MarcasFrontais.close()

            MarcasTraseiras = Image.open(Path(os.getcwd()) / "Cortes" / "CorteTraseiro.png")
            _, _, _, mask = MarcasTraseiras.split()
            PlanoTraseiro.paste(MarcasTraseiras, (0, 0), mask)
            MarcasTraseiras.close()

        print('''
        >>> SALVANDO PLANOS <<<
        ''')

        PlanoFrontal.save(r'PlanoFrontal.png')
        PlanoTraseiro.save(r'PlanoTraseiro.png')

        imFrente.close()
        imVerso.close()
        imEscondida.close()

        for arq in os.listdir(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados'):
            os.remove(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados' / arq)
        os.rmdir(Path(os.getcwd()) / 'Temp_PNGs_Redimensionados')

    else:
        print('Alguma(s) de suas imagens é/são menor(es) que 320356 pixels^2.\n',
              'Tente pegar imagens maiores')

    print('''
    --- PLANOS CRIADOS ---
    ''')

    return None


plano(imgF=r'oceano1.png',
      imgV=r'oceano2.png',
      imgE=r'oceano3.png',
      grafica=True, montagem_simplificada=True)

"""
O argumento montagem_simplifcada é um booleano (True/False). Ele serve para inverter a imgV e imgE para a montagem mais
"simplificada".
Ou seja, a imagem do verso se torna a escondida e a imagem escondida se torna a do verso!
"""
