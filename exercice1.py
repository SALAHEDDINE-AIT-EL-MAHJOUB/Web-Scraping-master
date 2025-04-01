# Importation des modules nécessaires
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Création d'une instance de Console pour l'affichage
console = Console()

def list_pizzas():
    # Ouvrir le fichier HTML téléchargé en mode lecture avec encodage UTF-8
    with open("pizzas.html", "r", encoding="utf-8") as file:
        # Créer un objet BeautifulSoup pour analyser le contenu HTML du fichier
        soup = BeautifulSoup(file, "html.parser")

    # Chercher tous les éléments span avec la classe "menu-entry"
    pizzas = soup.find_all("span", class_="menu-entry")
    
    # Créer un tableau pour afficher les pizzas
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("🍕 Liste des Pizzas", style="cyan")

    # Parcourir la liste des éléments trouvés
    for pizza in pizzas:
        # Extraire le texte de chaque balise <span>
        pizza_name = pizza.get_text(strip=True)
        if pizza_name:  # Only add non-empty names
            table.add_row(pizza_name)

    # Afficher un titre stylisé
    console.print(Panel.fit(
        "[bold yellow]🍕 Liste des Pizzas Disponibles 🍕[/bold yellow]",
        border_style="yellow"
    ))
    
    # Afficher le tableau
    console.print(table)
    
    # Afficher un pied de page
    console.print(Panel.fit(
        "[italic]Bon appétit ![/italic]",
        border_style="green"
    ))

if __name__ == "__main__":
    try:
        list_pizzas()
    except Exception as e:
        console.print(f"[bold red]Erreur :[/bold red] {str(e)}")
