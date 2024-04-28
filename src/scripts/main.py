import pandas as pd
# para gerenciar e manipular diretorios do sistema operacional e outras coisas
import os 
# Ele serve para manipular diretorio e nome de arquivos em massa (para n precisar pegar 1 por 1)
import glob 


# definir o caminho da raw, é melhor guardar o caminho na variavel, para se caso mudar o local do arquivo a gente precisa mudar só aqui, e nao o codigo todo
folder_path = 'src\\data\\raw'

# Lista todos os arquivos de exel / chamamos o os. para lidar caminhos / .join para juntar todos os caminhos da folder_path / '*.xlsx' = pega todos os arquivos que terminam com xlsx
excel_files = glob.glob(os.path.join(folder_path, '*.xlsx'))

if not excel_files:
    print('Nenhum arquivo compativel encontrado')
else:
    
    # dataframe = tabela na memória para guardar os conteúdos dos arquivos
    dfs = []

    for excel_file in excel_files:

        try:
            df_temp = pd.read_excel(excel_file)
            
            #Pegando o nome do arquivo (expecificamentem queremos pegar o páis)
            file_name = os.path.basename(excel_file)
            
            # Adicionando a SIGLA de cada país 
            if 'brasil' in file_name.lower():
                df_temp['location'] = 'br'
            elif 'france' in file_name.lower():
                df_temp['location'] = 'fr'
            elif 'italian' in file_name.lower():
                df_temp['location'] = 'it'

            '''
            Expressão regex nos ajudando a pegar uma parte de um LINK
            ex:  https://servicostreaming.com.br?utm_campaign=sunshine 
            (vamos pegar apenas o 'sunshine' que é o lugar onde o usuario clicou no link de inscrição para netflix)

            '''
            df_temp['campaing'] = df_temp['utm_link'].str.extract(r'utm_campaign=(.*)')

            # Guardando os dados tratados dentro do nosso dataframe dfs
            dfs.append(df_temp)

            print(dfs)
        except Exception as e:
            print(f'Erro ao ler arquivo {excel_file} : {e}')
            
if dfs: 
    # concaternar e fazer p pandas enteder que são varias subtabeças
    result = pd.concat(dfs, ignore_index=True)

    # caminho de saida
    output_file = os.path.join('src', 'data', 'ready', 'clean.json')
    
    # # Leva os dados do resultado a serem escritos no json ( ou outro tipo de outro arquivo) configurado
    result.to_json(output_file)

    # # Salva o arquivo de excel
    # writer._save()
else:
    print('Nenhum dado para ser salvo')