
from pathlib import Path
from contextlib import asynccontextmanager
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


# Caminho do banco de dados
BASE_DIR = Path(__file__).resolve().parent
BANCO = BASE_DIR / "tarefas.db"


# Conexão com SQLite
def conectar():
    conexao = sqlite3.connect(BANCO, timeout=10)
    conexao.row_factory = sqlite3.Row
    return conexao


# Criar tabela quando a aplicação iniciar
@asynccontextmanager
async def lifespan(app: FastAPI):
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                concluida INTEGER NOT NULL DEFAULT 0
            )
        """)
        conexao.commit()
    yield


app = FastAPI(title="TaskFlow API", lifespan=lifespan)


# Modelo das tarefas
class NovaTarefa(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)


# Listar tarefas
@app.get("/tarefas")
def listar_tarefas():
    with conectar() as conexao:
        registros = conexao.execute(
            "SELECT * FROM tarefas ORDER BY id DESC"
        ).fetchall()

    tarefas = [
        {
            "id": t["id"],
            "titulo": t["titulo"],
            "concluida": bool(t["concluida"])
        }
        for t in registros
    ]

    return {"tarefas": tarefas}


# Criar tarefa
@app.post("/tarefas", status_code=201)
def criar_tarefa(nova_tarefa: NovaTarefa):
    with conectar() as conexao:
        cursor = conexao.execute(
            "INSERT INTO tarefas (titulo) VALUES (?)",
            (nova_tarefa.titulo,)
        )
        tarefa_id = cursor.lastrowid
        conexao.commit()

    return {
        "mensagem": "Tarefa criada com sucesso!",
        "tarefa": {
            "id": tarefa_id,
            "titulo": nova_tarefa.titulo,
            "concluida": False
        }
    }


# Excluir tarefa
@app.delete("/tarefas/{tarefa_id}")
def excluir_tarefa(tarefa_id: int):
    with conectar() as conexao:
        cursor = conexao.execute(
            "DELETE FROM tarefas WHERE id = ?",
            (tarefa_id,)
        )
        conexao.commit()

    if cursor.rowcount == 0:
        raise HTTPException(404, "Tarefa não encontrada")

    return {"mensagem": "Tarefa excluída com sucesso!"}


# Concluir ou desmarcar tarefa
@app.patch("/tarefas/{tarefa_id}/concluir")
def concluir_tarefa(tarefa_id: int):
    with conectar() as conexao:
        cursor = conexao.execute(
            """
            UPDATE tarefas
            SET concluida = CASE concluida
                WHEN 0 THEN 1
                ELSE 0
            END
            WHERE id = ?
            """,
            (tarefa_id,)
        )
        conexao.commit()

        if cursor.rowcount == 0:
            raise HTTPException(404, "Tarefa não encontrada")

        registro = conexao.execute(
            "SELECT * FROM tarefas WHERE id = ?",
            (tarefa_id,)
        ).fetchone()

    return {
        "id": registro["id"],
        "titulo": registro["titulo"],
        "concluida": bool(registro["concluida"])
    }


# Modelo para editar tarefas
class EditarTarefa(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)


# Editar uma tarefa existente
@app.put("/tarefas/{tarefa_id}")
def editar_tarefa(tarefa_id: int, dados: EditarTarefa):
    with conectar() as conexao:
        cursor = conexao.execute(
            "UPDATE tarefas SET titulo = ? WHERE id = ?",
            (dados.titulo, tarefa_id)
        )
        conexao.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada"
            )

    return {
        "mensagem": "Tarefa atualizada com sucesso!",
        "id": tarefa_id,
        "titulo": dados.titulo
    }

# Exibir o frontend
pasta_frontend = BASE_DIR.parent / "frontend"

app.mount(
    "/",
    StaticFiles(directory=pasta_frontend, html=True),
    name="frontend"
)
