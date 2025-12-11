from pathlib import Path
import zipfile as zf
from datetime import datetime as dt

"""
Função responsável por criar o backup de um usuário específico.
Recebe o ID do usuário escolhido (inteiro)
"""
def backup_usuarios():
    # Caminho base onde estão os usuários
    path = Path(r"C:\Users")

    # Caminho para salvar os backups
    base_path = Path(r"D:\Arquivos\BackupsUsuarios")

    # Lista apenas diretórios (usuários reais)
    user_list = [item for item in path.iterdir() if item.is_dir()]

    # Mapeamento numerico
    user_map = {i+1: user for i, user in enumerate(user_list)}
        
    # Verifica se o uusário existe no mapa
    if user_choice not in user_map:
        raise ValueError("Usuário inválido!")
    SelectedUser = user_map[user_choice]

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

    return f"Backup criado com sucesso: {TargetZip}"