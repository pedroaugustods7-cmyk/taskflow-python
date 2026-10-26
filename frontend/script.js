
const API = "http://127.0.0.1:8000";

// Carregar tarefas
async function carregarTarefas() {
    try {
        const resposta = await fetch(`${API}/tarefas`);

        if (!resposta.ok) {
            throw new Error("Erro ao buscar tarefas");
        }

        const dados = await resposta.json();
        const lista = document.getElementById("listaTarefas");

        lista.innerHTML = "";

        dados.tarefas.forEach(tarefa => {
            const item = document.createElement("li");

            // Checkbox para concluir tarefa
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.checked = tarefa.concluida;

            // Título da tarefa
            const titulo = document.createElement("span");
            titulo.textContent = tarefa.titulo;

            if (tarefa.concluida) {
                titulo.classList.add("concluida");
            }

            // Marcar ou desmarcar tarefa
            checkbox.onchange = async () => {
                try {
                    const resposta = await fetch(
                        `${API}/tarefas/${tarefa.id}/concluir`,
                        { method: "PATCH" }
                    );

                    if (!resposta.ok) {
                        throw new Error("Erro ao atualizar tarefa");
                    }

                    await carregarTarefas();
                } catch (erro) {
                    console.error(erro);
                    alert("Não foi possível atualizar a tarefa.");
                    await carregarTarefas();
                }
            };

            // Botão editar
            const botaoEditar = document.createElement("button");
            botaoEditar.textContent = "Editar";
            botaoEditar.className = "botao-editar";

            botaoEditar.onclick = async () => {
                const novoTitulo = prompt(
                    "Digite o novo nome da tarefa:",
                    tarefa.titulo
                );

                if (novoTitulo === null || !novoTitulo.trim()) {
                    return;
                }

                try {
                    const resposta = await fetch(
                        `${API}/tarefas/${tarefa.id}`,
                        {
                            method: "PUT",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                titulo: novoTitulo.trim()
                            })
                        }
                    );

                    if (!resposta.ok) {
                        throw new Error("Erro ao editar tarefa");
                    }

                    await carregarTarefas();

                } catch (erro) {
                    console.error(erro);
                    alert("Não foi possível editar a tarefa.");
                }
            };

            // Botão excluir
            const botaoExcluir = document.createElement("button");
            botaoExcluir.textContent = "Excluir";

            botaoExcluir.onclick = async () => {
                try {
                    const resposta = await fetch(
                        `${API}/tarefas/${tarefa.id}`,
                        { method: "DELETE" }
                    );

                    if (!resposta.ok) {
                        throw new Error("Erro ao excluir tarefa");
                    }

                    await carregarTarefas();

                } catch (erro) {
                    console.error(erro);
                    alert("Não foi possível excluir a tarefa.");
                }
            };

            // Adicionar elementos na interface
            item.appendChild(checkbox);
            item.appendChild(titulo);
            item.appendChild(botaoEditar);
            item.appendChild(botaoExcluir);

            lista.appendChild(item);
        });

    } catch (erro) {
        console.error("Erro ao carregar tarefas:", erro);
    }
}


// Adicionar nova tarefa
async function adicionarTarefa() {
    const campo = document.getElementById("novaTarefa");
    const titulo = campo.value.trim();

    if (!titulo) {
        alert("Digite uma tarefa!");
        return;
    }

    try {
        const resposta = await fetch(`${API}/tarefas`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ titulo })
        });

        if (!resposta.ok) {
            throw new Error("Erro ao criar tarefa");
        }

        campo.value = "";
        await carregarTarefas();

    } catch (erro) {
        console.error(erro);
        alert("Não foi possível adicionar a tarefa.");
    }
}


// Carregar automaticamente quando a página abrir
document.addEventListener("DOMContentLoaded", () => {
    carregarTarefas();
});
