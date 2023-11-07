import json
import os
import requests
import csv

# Importar a biblioteca do MinIO
from minio import Minio

# Definir as credenciais do MinIO
access_key = "minioadmin"
secret_key = "minioadmin"
endpoint = "http://localhost:9000"
bucket = "municipios"

# Definir o caminho para os datasets
path = "C:\python-basics"

# Ler os datasets
for file in os.listdir(path):
  # Abrir o arquivo JSON
  with open(os.path.join(path, file), "r") as f:
    data = json.load(f)

  # Obter a sigla da UF
  uf = data["uf"]

  # Criar a pasta para o estado
  if not os.path.exists(f"{path}/{uf}"):
    os.mkdir(f"{path}/{uf}")

  # Criar o arquivo CSV
  with open(f"{path}/{uf}/cidades.csv", "w") as f:
    f.write("nome,uf\n")
    for municipio in data["municipios"]:
      f.write(f"{municipio['nome']},{uf}\n")

# Importar os arquivos para o MinIO
minio = Minio(endpoint=endpoint, access_key=access_key, secret_key=secret_key)
minio.fput_object(bucket, f"{uf}/cidades.csv", f"{path}/{uf}/cidades.csv")

# Exportar os dados para o MongoDB
import pymongo

# Conectar ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["municipios"]
collection = db["cidades"]

# Inserir os dados no MongoDB
for uf in os.listdir(path):
  with open(f"{path}/{uf}/cidades.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
      collection.insert_one({
        "nome": row[0],
        "uf": row[1]
      })

# Visualizar os dados no MongoDB
for cidade in collection.find():
  print(cidade)