import subprocess
import sys


PATTERN = "telegram-bot|main.py|telegram_manager"


def run() -> None:
    try:
        result = subprocess.run(
            ["pkill", "-f", PATTERN],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("pkill não está disponível no sistema.")
        sys.exit(2)

    if result.returncode == 0:
        print("Processos encerrados com sucesso.")
        return

    if result.returncode == 1:
        print("Nenhum processo encontrado para encerrar.")
        return

    error = result.stderr.strip() or "Erro desconhecido ao encerrar processos."
    print(error)
    sys.exit(result.returncode)


if __name__ == "__main__":
    run()
