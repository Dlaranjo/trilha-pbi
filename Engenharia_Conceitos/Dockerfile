# Um Dockerfile define o ambiente e os passos para criar uma imagem de container
# Isso garante portabilidade, reprodutibilidade e isolamento do seu código

# 1. Escolha da imagem base (Python oficial, versão 3.10, leve)
FROM python:3.10-slim

# 1.1 Instala o Java (OpenJDK 17) necessário para o PySpark
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copia os arquivos necessários para dentro do container
COPY 1_Processo_ETL/etl.py .
COPY 1_Processo_ETL/vendas.csv .

# 4. Instala as dependências necessárias para rodar o ETL
# pandas: manipulação de dados
# openpyxl: leitura de arquivos Excel
# polars: processamento de dados rápido
# pyspark: engine distribuído
RUN pip install pandas openpyxl polars pyspark

# 5. Comando padrão para rodar o ETL ao iniciar o container
CMD ["python", "etl.py"]

# Para construir a imagem:
# docker build -t etl-demo .
# Para rodar o container:
# docker run --rm -v "${PWD}/1_Processo_ETL/data_lake:/app/data_lake" etl-demo 