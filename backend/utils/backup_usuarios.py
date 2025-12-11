from pathlib import Path
import zipfile as zf
from datetime import datetime as dt

def backup_usuarios():
    # Caminho base onde estão os usuários
    path = Path(r"C:\Users")
    users = list(path.iterdir())

    # Caminho para salvar os backups
    BasePath = Path(r"D:\Arquivos\BackupsUsuarios")

    # Lista apenas diretórios (usuários reais)
    UserList = [item for item in users if item.is_dir()]
    UserMap = {}
    UserId = 0
    today = dt.now()
    when = today.strftime("%Y-%m-%d")

    # Mapeia cada pasta de usuário para um número
    for item in UserList:
        if item.is_dir():
            UserId += 1
            UserMap[UserId] = item

    # Aqui você vai depois RECEBER o user_id via front-end
    # mas por enquanto vamos manter o input para testes:
    UserChoice = int(input("Digite o número do usuário a ser feito o backup: "))

    if UserChoice in UserMap:
        SelectedUser = UserMap[UserChoice]
    else:
        raise Exception("Usuário inválido!")

    # Caminho onde o backup desse usuário ficará
    UserDestination = BasePath / SelectedUser.name

    # Cria diretório se não existir
    UserDestination.mkdir(parents=True, exist_ok=True)

    # Nome do arquivo ZIP criado
    TargetZip = UserDestination / f"{SelectedUser.name}_backup-{when}.zip"

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

    return TargetZip  # útil para o front confirmar
