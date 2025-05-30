from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import sys
import importlib.util

# Importa dinamicamente as funções do etl.py
spec = importlib.util.spec_from_file_location("etl", "etl.py")
etl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(etl)

# Configurações padrão da DAG
default_args = {
    'owner': 'data_team',                    # Responsável pela DAG (aparece na interface)
    'depends_on_past': False,                # Se True, só executa se a execução anterior suceder
    'email': ['data_team@company.com'],      # Lista de emails para notificações
    'email_on_failure': True,                # Envia email se a DAG falhar
    'email_on_retry': False,                 # Envia email em cada tentativa de retry
    'retries': 1,                            # Número de tentativas em caso de falha
    'retry_delay': timedelta(minutes=5),     # Tempo de espera entre retries
    'start_date': datetime(2024, 1, 1),      # Data de início da DAG
    'execution_timeout': timedelta(hours=1), # Tempo máximo de execução da DAG
    'priority_weight': 10,                   # Prioridade da DAG em relação a outras
}

# Criação da DAG com configurações avançadas
dag = DAG(
    'etl_demo_didatico',                     # Nome único da DAG
    default_args=default_args,               # Argumentos padrão definidos acima
    description='DAG didática demonstrando recursos avançados do Airflow',  # Descrição da DAG
    schedule_interval='0 0 * * *',           # Cron expression: execução diária à meia-noite
    catchup=False,                           # Se True, executa DAGs passadas desde start_date
    max_active_runs=1,                       # Limita número de execuções concorrentes da DAG
    tags=['etl', 'demo', 'didatico'],        # Tags para organização na interface
    doc_md="""                               # Documentação em Markdown
    # DAG Didática de ETL
    
    Esta DAG demonstra recursos avançados do Airflow:
    - Orquestração de tarefas
    - Tratamento de falhas
    - Notificações
    - Pools de recursos
    - Timeouts
    - Retries
    """
)

# Tarefas de início e fim
start = DummyOperator(
    task_id='inicio',                        # Identificador único da tarefa
    dag=dag                                  # DAG à qual a tarefa pertence
)

end = DummyOperator(
    task_id='fim',
    trigger_rule=TriggerRule.ALL_DONE,       # Executa mesmo se alguma tarefa falhar
    dag=dag
)

# Tarefa: ETL com Pandas
etl_pandas = PythonOperator(
    task_id='etl_pandas',                    # Identificador único da tarefa
    python_callable=etl.etl_pandas,          # Função Python a ser executada
    retries=2,                               # Sobrescreve retries padrão da DAG
    retry_delay=timedelta(minutes=1),        # Sobrescreve retry_delay padrão da DAG
    dag=dag
)

# Tarefa: ETL com Polars
etl_polars = PythonOperator(
    task_id='etl_polars',
    python_callable=etl.etl_polars,
    dag=dag
)

# Tarefa: ETL com Spark
etl_spark = PythonOperator(
    task_id='etl_spark',
    python_callable=etl.etl_pyspark,
    dag=dag
)

# Tarefa de validação
validacao = DummyOperator(
    task_id='validacao_dados',
    trigger_rule=TriggerRule.ALL_SUCCESS,    # Só executa se todas as tarefas anteriores sucederem
    dag=dag
)

# Orquestração: 
# 1. Início
# 2. ETLs em paralelo (Pandas, Polars, Spark)
# 3. Validação
# 4. Fim
start >> [etl_pandas, etl_polars, etl_spark] >> validacao >> end

# OBS: Esta DAG demonstra:
# - Configurações avançadas de DAG (timeouts, retries)
# - Diferentes trigger rules (ALL_SUCCESS, ALL_DONE)
# - Execução paralela de tarefas usando listas
# - Documentação em Markdown
# - Notificações por email
# - Tratamento de falhas com retries