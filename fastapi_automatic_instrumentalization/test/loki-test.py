import datetime
import json

import requests

# Configuração da URL do Loki
LOKI_URL = "https://loki.your_domain.dev/"


def test_loki_connection():
    """Testa a conexão básica com o servidor Loki"""
    try:
        response = requests.get(f"{LOKI_URL}/ready")
        if response.status_code == 200:
            print(f"✅ Conexão com Loki estabelecida! Status: {response.status_code}")
            return True
        else:
            print(f"❌ Falha na conexão com Loki. Status: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar com Loki: {e}")
        return False


def test_loki_query():
    """Testa uma consulta simples no Loki"""
    try:
        # Definindo um intervalo de tempo para a consulta (última hora)
        now = datetime.datetime.now()
        one_hour_ago = now - datetime.timedelta(hours=1)

        # Convertendo para formato Unix timestamp em nanossegundos
        start_time = int(one_hour_ago.timestamp() * 1e9)
        end_time = int(now.timestamp() * 1e9)

        # Consulta simples para buscar logs
        query_params = {
            "query": '{job="test"}',
            "start": start_time,
            "end": end_time,
            "limit": 10,
        }

        response = requests.get(
            f"{LOKI_URL}/loki/api/v1/query_range", params=query_params
        )

        print(f"📊 Resultado da consulta (status {response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao executar consulta no Loki: {e}")
        return False


def test_loki_push_log():
    """Testa o envio de um log para o Loki"""
    try:
        # Timestamp atual em nanossegundos
        current_time_ns = int(datetime.datetime.now().timestamp() * 1e9)

        # Payload para enviar um log de teste
        payload = {
            "streams": [
                {
                    "stream": {"job": "test", "service": "python-test"},
                    "values": [
                        [
                            str(current_time_ns),
                            "Este é um log de teste enviado pelo Python",
                        ]
                    ],
                }
            ]
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            f"{LOKI_URL}/loki/api/v1/push", headers=headers, data=json.dumps(payload)
        )

        if response.status_code == 204:
            print("✅ Log enviado com sucesso para o Loki!")
            return True
        else:
            print(f"❌ Falha ao enviar log. Status: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar log para o Loki: {e}")
        return False


def test_loki_labels():
    """Testa a obtenção de labels do Loki"""
    try:
        response = requests.get(f"{LOKI_URL}/loki/api/v1/labels")

        print(f"🏷️ Labels disponíveis (status {response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao obter labels do Loki: {e}")
        return False


if __name__ == "__main__":
    print("🔍 Iniciando testes de conexão com Grafana Loki...")
    print("-" * 50)

    # Executa os testes
    connection_ok = test_loki_connection()
    from time import sleep

    for i in range(100000):
        sleep(1)
        if connection_ok:
            print("-" * 50)
            test_loki_labels()

            print("-" * 50)
            test_loki_push_log()

            print("-" * 50)
            test_loki_query()

    # print("-" * 50)
    # print("✨ Testes concluídos!")
