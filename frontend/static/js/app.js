// =================== BARRA DE PROGRESSO ===================

function startProgress() {
    const barContainer = document.querySelector('.progress-container');
    const bar = document.getElementById('progress-bar');
    
    barContainer.style.display = "block";
    bar.style.width = "0%";

    let width = 0;
    const interval = setInterval(() => {
        width += 2;
        if (width >= 95) width = 95;
        bar.style.width = width + "%";
    }, 150);

    return interval;
}

function finishProgress(interval) {
    clearInterval(interval);
    const bar = document.getElementById('progress-bar');
    bar.style.width = "100%";

    setTimeout(() => {
        document.querySelector('.progress-container').style.display = "none";
        bar.style.width = "0%";
    }, 800);
}



// =================== GERAR BACKUP ===================

async function gerarBackup() {
    const statusBox = document.getElementById("status-box");
    const userSelect = document.getElementById("user-select");

    const userName = userSelect.value;

    // Verifica se o usuário foi selecionado
    if (!userName) {
        statusBox.className = "status error";
        statusBox.innerText = "Selecione um usuário!";
        return;
    }

    // Inicia barra de progresso
    const progressInterval = startProgress();

    // Mostra mensagem
    statusBox.className = "status";
    statusBox.innerText = "Gerando backup... Aguarde.";

    try {
        const response = await fetch("/api/backup_usuarios", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ user_name: userName })
        });

        const data = await response.json();

        // Finaliza barra
        finishProgress(progressInterval);

        // Caso dê erro
        if (!response.ok || data.erro) {
            statusBox.className = "status error";
            statusBox.innerText = data.erro || "Erro desconhecido!";
            return;
        }

        // Sucesso
        statusBox.className = "status ok";
        statusBox.innerHTML = `
            Backup gerado com sucesso! <br><br>
            <strong>Arquivo:</strong><br>
            ${data.arquivo}
        `;

    } catch (error) {
        finishProgress(progressInterval);

        statusBox.className = "status error";
        statusBox.innerText = "Erro ao conectar com o servidor: " + error;
    }
}
