import typer
from rich import print
from search import search_prompt

def main():
    print(f"[bold green]Bem-vindo(a) ao chat![/bold green] Para sair digite [bold red]exit[/bold red].\n")
    while True:
        user_question = typer.prompt("PERGUNTA")
        
        if user_question.lower() in ["sair", "exit", "quit"]:
            print("[bold red]Sessão encerrada.[/bold red]")
            break
        
        info = f"IA: Buscando informações sobre '{user_question}'..."
        
        print(f"[bold blue]{info}[/bold blue]\n\n")

        chain = search_prompt(user_question)

        if not chain:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return
        pass

if __name__ == "__main__":
    main()