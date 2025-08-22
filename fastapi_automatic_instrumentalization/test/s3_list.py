from minio import Minio
from minio.error import S3Error

# Configure o cliente MinIO com as credenciais fornecidas
client = Minio(
    "br-se1.magaluobjects.com",  # Endpoint da Magalu Cloud
    access_key="2d3ec5d2-2dd4-40db-9f36-1a1f7d707976",  # Sua Access Key
    secret_key="b3181d81-2f57-4c8b-acfd-68e43bfdfd3c",  # Sua Secret Key
    secure=True,  # Utilizando HTTPS
)


# Função para adicionar arquivo ao bucket
def add_file_to_bucket(file_path, bucket_name, object_name):
    try:
        # Verifica se o bucket existe
        if not client.bucket_exists(bucket_name):
            print(f"O bucket {bucket_name} não existe.")
            return
        # Faz o upload do arquivo
        client.fput_object(bucket_name, object_name, file_path)
        print(
            f'Arquivo "{object_name}" subido com sucesso para o bucket "{bucket_name}".'
        )
    except S3Error as err:
        print(f"Erro ao subir o arquivo: {err}")


# Função para listar arquivos do bucket
def list_objects_in_bucket(bucket_name):
    try:
        # Verifica se o bucket existe
        if not client.bucket_exists(bucket_name):
            print(f"O bucket {bucket_name} não existe.")
            return
        # Lista os objetos no bucket
        objects = client.list_objects(bucket_name)
        from icecream import ic

        ic(list(objects))
    except S3Error as err:
        print(f"Erro ao acessar o bucket: {err}")


# Função para deletar arquivo do bucket
def delete_file_from_bucket(bucket_name, object_name):
    try:
        # Verifica se o bucket existe
        if not client.bucket_exists(bucket_name):
            print(f"O bucket {bucket_name} não existe.")
            return
        # Deleta o arquivo do bucket
        client.remove_object(bucket_name, object_name)
        print(
            f'Arquivo "{object_name}" deletado com sucesso do bucket "{bucket_name}".'
        )
    except S3Error as err:
        print(f"Erro ao deletar o arquivo: {err}")


# Exemplo de uso
if __name__ == "__main__":
    bucket_name = "loki-pve"

    # Função para adicionar um arquivo
    file_path = "compose.yaml"  # Caminho do arquivo local
    object_name = "compose.yaml"  # Nome do arquivo no bucket
    # add_file_to_bucket(file_path, bucket_name, object_name)

    # Função para listar arquivos
    list_objects_in_bucket(bucket_name)

    # Função para deletar um arquivo
    # delete_file_from_bucket(bucket_name, object_name)
