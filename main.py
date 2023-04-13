import pandas as pd
import json

def leer_archivos():
    #LEER ARCHIVO MUESTRA
    df = pd.read_csv('instituciones_educativas.csv', sep=',')

    #LEER ARCHIVO UNIVERSIDADES
    with open('Universidades.json', encoding='utf-8') as fh:
        data = json.load(fh)
    return df, data

def preprocesamiento(df, data):
    #LIMPIEZA DEL ARCHIVO UNIVERSIDADES
    input_2 = {d['Siglas ']: d['Nombre '] for d in data}
    return df, input_2

def homologacion(df, df_homologacion, df_final):
    #CRUCE ENTRE EL DF DE MUESTRA Y EL DF HOMOLOGADO
    df_aux = df.merge(df_homologacion, on='value', how='left')
    df_final = df_final.append(df_aux.loc[~df_aux['universidad homologada'].isnull()])
    df_no_homologada = df_aux.loc[df_aux['universidad homologada'].isnull()]

    #RETORNA DF DE MUESTRA QUE FALTA HOMOLOGAR, MÁS EL DF QUE YA FUE HOMOLOGADO
    return df_no_homologada[['candidateId','value']], df_final

def metodo_1(input_1, input_2):
    #VALIDACION ENTRE SIGLAS DE LAS UNIVERSIDADES (I2) Y LOS COMENTARIOS (I1) QUE POSEEN SIGLAS EN SU ESTRUCTURA
    dict_aux = dict()
    input_1['value'] = input_1['value'].str.replace('-',' ').replace('.',' ').replace(')',' ').replace('(',' ').replace('Y',' ')
    dict_aux = {row[2]: value for row in input_1.itertuples() for key, value in input_2.items() if key.upper() in row[2].upper().split(' ')}
    df_homologado_1 = pd.DataFrame(dict_aux.items(), columns=['value', 'universidad homologada'])

    return df_homologado_1

def metodo_2(input_1, input_2):
    #VALIDACION ENTRE LOS COMENTARIOS (I1) SIN STOP WORDS LOS CUALES ESTÁN CONTENIDOS EN LOS NOMBRES DE LAS UNIVERSIDADES (I2) Y SOLO DE UNIVERSIDADES
    dict_aux = dict()
    df_aux = input_1[input_1['value'].str.contains('Universidad')]
    df_aux['split'] = df_aux['value'].str.split()

    #ELIMINAR STOP WORDS
    df_aux['split'] = df_aux['split'].apply(lambda row: [val for val in row if val not in ['Universidad','San','De','Nacional','Privada','Peruana','Del','La']])

    for i, row in df_aux.iterrows():
        for word in input_2.values():
            if (set( row['split'] ).issubset(set( word.split() ))):
                dict_aux[input_1.at[i,'value']] = word

    df_homologado_2 = pd.DataFrame(dict_aux.items(), columns=['value', 'universidad homologada'])

    return input_1[input_1['value'].str.contains('Universidad')], df_homologado_2

def main():
    df_final = pd.DataFrame()

    #1. LEER ARCHIVOS
    df, data = leer_archivos()

    #2. PREPROCESAMIENTO
    input_1, input_2 = preprocesamiento(df, data)
    
    #3. INDISTINCION DE VOCALES CON TILDES EN ARCHIVO MUESTRA Y ARCHIVO DE UNIVERSIDADES PARA UNA MAYOR PRECISION
    reemplazos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
    for k, v in input_2.items():
        for acento, vocal in reemplazos.items():
            v = v.replace(acento, vocal)
        input_2[k] = v
    input_1['value'] = input_1['value'].replace(reemplazos, regex=True)

    #4, APLICAR METODO 1
    df_homologacion_1 = metodo_1(input_1, input_2)
    #5. HOMOLOGACION 1
    input_1, df_final = homologacion(df, df_homologacion_1, df_final)

    #6. APLICAR METODO 2
    input_1, df_homologacion_2 = metodo_2(input_1, input_2)
    #7. HOMOLOGACION 2
    input_1, df_final = homologacion(input_1, df_homologacion_2, df_final)

    #8. EXTRAER SINONIMOS DE LAS UNIVERSIDADES
    universidades = df_final.groupby('universidad homologada')['value'].apply(list).reset_index()
    universidades['sinonimos'] = universidades['value'].apply(lambda x: list(set(x)))
    universidades = universidades[['universidad homologada', 'sinonimos']]
    
    #9. EXPORTAR UNIVERSIDADES HOMOLOGADAS
    df_final = df_final.sort_values('candidateId')
    df_final.to_csv('universidades_homologadas.csv', sep=',', index=False)

    #10. EXPORTAR SINONIMO DE UNIVERSIDADES
    universidades.to_json('sinonimo_universidades.json', orient='records')

if __name__ == '__main__':
    main()