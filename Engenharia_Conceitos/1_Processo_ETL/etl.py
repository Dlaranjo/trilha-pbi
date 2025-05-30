import os
import sys

# ETL com Pandas: ideal para pequenos/médios volumes de dados
# Lê a planilha, calcula o total e salva em CSV
def etl_pandas():
    import pandas as pd
    print('\n[ETL Pandas] Lendo vendas.xlsx...')
    df = pd.read_csv('vendas.csv')
    df['total'] = df['quantidade'] * df['preco_unitario']
    os.makedirs('data_lake', exist_ok=True)
    df.to_csv('data_lake/vendas_tratadas_pandas.csv', index=False)
    print('[ETL Pandas] Arquivo gerado: data_lake/vendas_tratadas_pandas.csv')

# ETL com Polars: mais rápido e eficiente em RAM
# Lê a planilha, faz limpeza, calcula o total e salva em CSV
# Usa schema_overrides para evitar warning de depreciação
# Polars é excelente para dados tabulares e processamento em lote

def etl_polars():
    import polars as pl
    print('\n[ETL Polars] Lendo vendas.csv...')
    df = pl.read_csv('vendas.csv', schema_overrides={'quantidade': pl.Utf8, 'preco_unitario': pl.Utf8})
    # Limpar espaços em branco
    df = df.with_columns([
        pl.col('quantidade').cast(pl.Int64),
        pl.col('preco_unitario').cast(pl.Float64)
    ])
    df = df.with_columns([
        (pl.col('quantidade') * pl.col('preco_unitario')).alias('total')
    ])
    df.write_csv('data_lake/vendas_tratadas_polars.csv')
    print('[ETL Polars] Arquivo gerado: data_lake/vendas_tratadas_polars.csv')

# ETL com PySpark: ideal para grandes volumes e processamento distribuído
# Aqui usamos apenas em memória para fins didáticos
# O bloco abaixo é OPCIONAL e serve apenas para suprimir mensagens de erro do Spark no Windows

def etl_pyspark():
    # OPCIONAL: Suprimir logs de shutdown do Spark (apenas para ambiente Windows)
    import logging
    import os
    import contextlib
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.ERROR)
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--conf spark.ui.showConsoleProgress=false pyspark-shell'
    class DummyFile(object):
        def write(self, x): pass
        def flush(self): pass
    with contextlib.redirect_stderr(DummyFile()):

        # Começo do processo ETL com PySpark
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col
        print('\n[ETL PySpark] Lendo vendas.csv...')
        
        # Criar sessão Spark
        spark = SparkSession.builder.appName('ETL').getOrCreate()
        
        # Ler o arquivo CSV
        df = spark.read.csv('vendas.csv', header=True, inferSchema=True)
        
        # Calcular o total
        df = df.withColumn('total', col('quantidade') * col('preco_unitario'))
        
        print('[ETL PySpark] Exemplo de DataFrame:')
        df.show()
        # df.coalesce(1).write.mode('overwrite').option('header', 'true').csv('data_lake/vendas_tratadas_pyspark')
        # OBS: A escrita de arquivos com Spark pode exigir ambiente Linux/Cloud devido a dependências do Hadoop.
        print('[ETL PySpark] Finalizado! (A escrita em disco está comentada para evitar erros no Windows)')
        SparkSession.builder.getOrCreate().stop()

if __name__ == '__main__':
    print('Iniciando pipeline ETL didático...')
    etl_pandas()
    etl_polars()
    etl_pyspark()
    print('\nPipeline ETL finalizado! Veja os arquivos gerados na pasta data_lake/.')