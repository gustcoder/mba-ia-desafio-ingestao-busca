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

        result = search_prompt(user_question)

        if not result:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return
        print(f"[bold purple]RESPOSTA: {result}[/bold purple]\n\n")

if __name__ == "__main__":
    main()
