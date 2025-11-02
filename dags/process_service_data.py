from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd

def retorna_tabela(lista,coluna, tabela):
    hook = PostgresHook(postgres_conn_id='data_db')
    lista_placeholder  = ','.join(['%s'] * len(lista))
    sql = f"SELECT * FROM alternativa.{tabela} WHERE {coluna} in ({lista_placeholder}) and fim_validade IS NULL"
    return hook.get_records(sql, parameters=tuple(lista))

def check_service_table():
    hook = PostgresHook(postgres_conn_id='data_db')
    df = pd.read_excel("/opt/airflow/files/dados_empresa_alternativa.xlsx", sheet_name='coletas')

    headers_list = {'id_cliente':"dim_cliente", 'id_caminhao':"dim_frota", 'id_residuo':"dim_residuo", 'id_funcionario':"dim_funcionario"}

    for k,v in headers_list.items():
        if k == 'id_funcionario':
            lista = df['id_motorista'].tolist()
        else:
            lista = df[k].tolist()
        result = retorna_tabela(lista, k, v)
        for registro in result:
            mapa_sk = {registro[1]: registro[0] for registro in result}
            if k == 'id_funcionario':
                df[k] = df['id_motorista'].map(mapa_sk)
            else:
                df[k] = df[k].map(mapa_sk)

    cols = [*headers_list.keys(),'data_solicitacao']
    lista = (df[cols].astype(str).agg(''.join, axis=1)).tolist()
    df['id'] = lista
    placeholders = ','.join(['%s'] * len(lista))
    sql = f"SELECT * FROM alternativa.fato_servico WHERE id_servico in ({placeholders})"
    existing_service = hook.get_records(sql, parameters=tuple(lista))

    for service in existing_service:
        id_service = service[0]
        df = df[df['id'] != id_service]
           
           
    insert_client_data(df)       
    
def insert_client_data(df):
    hook = PostgresHook(postgres_conn_id='data_db')
    sql = 'INSERT INTO "alternativa"."fato_servico" (id_servico, id_cliente, id_caminhao, id_residuo, id_motorista, data_solicitacao, tempo_resposta_horas, tempo_permanencia_dias, peso_residuos_kg, km_percorridos, taxa_ocupacao_percent) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)'
    for index, row in df.iterrows():
        id = row['id']
        id_cliente = int(row['id_cliente'])
        id_caminhao = int(row['id_caminhao'])
        id_residuo = int(row['id_residuo'])
        id_motorista = int(row['id_motorista'])
        data_solicitacao = row['data_solicitacao']
        tempo_resposta_horas = float(row['tempo_resposta_horas'])
        tempo_permanencia_dias = float(row['tempo_permanencia_dias'])
        peso_residuos_kg = float(row['peso_residuos_kg'])
        km_percorridos = float(row['km_percorridos'])
        taxa_ocupacao_percent = float(row['taxa_ocupacao_percent'])

        hook.run(sql, parameters=(id,id_cliente, id_caminhao, id_residuo, id_motorista, data_solicitacao, tempo_resposta_horas, tempo_permanencia_dias, peso_residuos_kg, km_percorridos, taxa_ocupacao_percent))



# Definição da DAG
with DAG(
    dag_id="process_service_data",
    description="Processa dados de serviços da planilha e atualiza o banco de dados",
    schedule="@daily",  # roda todo dia
    start_date=datetime(2025, 10, 28),
    catchup=False,  # não executa retroativamente
    default_args={
        "owner": "airflow",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:

    # Tarefa usando PythonOperator
    process_data = PythonOperator(
        task_id="process_data",
        python_callable=check_service_table,
    )
    

    # Se houver mais tarefas, você pode encadear assim:
    process_data