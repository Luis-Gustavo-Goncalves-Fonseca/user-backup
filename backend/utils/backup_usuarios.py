from pathlib import Path
import zipfile as zf
from datetime import datetime as dt

"""
Função responsável por criar o backup de um usuário específico.
Recebe o nome do usuário escolhido
"""
def backup_usuarios(user_name):
    # Caminho base onde estão os usuários
    path = Path(r"C:\Users")

    # Caminho para salvar os backups
    base_path = Path(r"D:\Arquivos\BackupsUsuarios")

    # Caminho do usuário
    SelectedUser = path / user_name

    # Verificando se a pasta do usuário existe
    if not SelectedUser.exists():
        raise ValueError("Usuário não encontrado!")

    # Data para o nome do arquivo
    today = dt.now()
    when = today.strftime("%Y-%m-%d")

    # Caminho onde o backup desse usuário ficará
    user_destination = base_path / SelectedUser.name
    
    # Cria diretório se não existir
    user_destination.mkdir(parents=True, exist_ok=True)

    # Nome do arquivo ZIP criado
    TargetZip = user_destination / f"{SelectedUser.name}_backup-{when}.zip"

    # Cria o ZIP com todos os arquivos do usuário
    with zf.ZipFile(TargetZip, "w", zf.ZIP_DEFLATED) as zipf:
        for file in SelectedUser.rglob("*"):
            if file.is_file():
                try:
                    zipf.write(
                        file,
                        file.relative_to(SelectedUser)  # mantém estrutura interna
                    )
                except Exception as e:
                    print(f"[IGNORADO] {file} -> {e}")

    return {"status": "ok", "arquivo": str(TargetZip)}