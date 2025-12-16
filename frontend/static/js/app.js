// Tudo que precisa rodar ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
    // Carrega a lista de usuários assim que a página abrir
    carregarUsuarios();

    // Conecta o botão à função de backup
    const botaoBackup = document.getElementById("gerarBackup");
    if (botaoBackup) {
        botaoBackup.addEventListener("click", gerarBackup);
    }
});

// =========================
// Carrega usuários do back-end
// =========================
async function carregarUsuarios() {
    const selectUsuarios = document.getElementById("usuarios");

    try {
        const response = await fetch("/api/usuarios");
        const data = await response.json();

        // Limpa o select
        selectUsuarios.innerHTML = '<option value="">Selecione um usuário</option>';

        // Preenche com os usuários retornados pelo back-end
        data.usuarios.forEach(usuario => {
            const option = document.createElement("option");
            option.value = usuario;
            option.textContent = usuario;
            selectUsuarios.appendChild(option);
        });

    } catch (error) {
        console.error("Erro ao carregar usuários:", error);
        selectUsuarios.innerHTML = '<option value="">Erro ao carregar usuários</option>';
    }
}

// =========================
// Gera backup do usuário selecionado
// =========================
async function gerarBackup() {
    const selectUsuarios = document.getElementById("usuarios");
    const statusBox = document.getElementById("status-box");

    const userName = selectUsuarios.value;

    // Validação
    if (!userName) {
        statusBox.className = "status error";
        statusBox.innerText = "Selecione um usuário.";
        return;
    }

    // Feedback visual
    statusBox.className = "status";
    statusBox.innerText = "Gerando backup... aguarde.";

    try {
        const response = await fetch("/api/backup_usuarios", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_name: userName
            })
        });

        const data = await response.json();

        // Erro retornado pelo back-end
        if (!response.ok || data.erro) {
            statusBox.className = "status error";
            statusBox.innerText = data.erro || "Erro ao gerar backup.";
            return;
        }

        // Sucesso
        statusBox.className = "status ok";
        statusBox.innerHTML = `
            Backup gerado com sucesso!<br><br>
            <strong>Arquivo:</strong><br>
            ${data.arquivo}
        `;

    } catch (error) {
        statusBox.className = "status error";
        statusBox.innerText = "Erro ao conectar com o servidor.";
        console.error(error);
    }
}
