    
import pytest
from fastapi.testclient import TestClient

import backend.main as backend


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    # Usa um banco temporário para não alterar seus dados reais
    banco_teste = tmp_path / "teste.db"
    monkeypatch.setattr(backend, "BANCO", banco_teste)

    with TestClient(backend.app) as client:
        yield client


def test_listar_tarefas(cliente):
    resposta = cliente.get("/tarefas")

    assert resposta.status_code == 200
    assert resposta.json() == {"tarefas": []}


def test_criar_tarefa(cliente):
    resposta = cliente.post(
        "/tarefas",
        json={"titulo": "Estudar Pytest"}
    )

    assert resposta.status_code == 201
    assert resposta.json()["tarefa"]["titulo"] == "Estudar Pytest"


def test_editar_tarefa(cliente):
    criada = cliente.post(
        "/tarefas",
        json={"titulo": "Tarefa original"}
    )

    tarefa_id = criada.json()["tarefa"]["id"]

    resposta = cliente.put(
        f"/tarefas/{tarefa_id}",
        json={"titulo": "Tarefa editada"}
    )

    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Tarefa editada"


def test_concluir_tarefa(cliente):
    criada = cliente.post(
        "/tarefas",
        json={"titulo": "Fazer exercícios"}
    )

    tarefa_id = criada.json()["tarefa"]["id"]

    resposta = cliente.patch(
        f"/tarefas/{tarefa_id}/concluir"
    )

    assert resposta.status_code == 200
    assert resposta.json()["concluida"] is True


def test_excluir_tarefa(cliente):
    criada = cliente.post(
        "/tarefas",
        json={"titulo": "Tarefa para excluir"}
    )

    tarefa_id = criada.json()["tarefa"]["id"]

    resposta = cliente.delete(f"/tarefas/{tarefa_id}")

    assert resposta.status_code == 200

    lista = cliente.get("/tarefas").json()["tarefas"]
    assert lista == []
