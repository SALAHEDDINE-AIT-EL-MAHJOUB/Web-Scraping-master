# Importation des modules nécessaires
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
from rich.text import Text

# Création d'une instance de Console pour l'affichage
console = Console()

def scrape_pizzas():
    # Ouvrir le fichier HTML contenant les pizzas, en mode lecture avec encodage UTF-8
    with open("pizzas.html", "r", encoding="utf-8") as file:
        # Créer un objet BeautifulSoup pour parser le HTML
        soup = BeautifulSoup(file, "html.parser")

    # Trouver toutes les balises contenant les informations d'un produit
    pizzas = soup.find_all("div", class_="product-container")
    
    # Créer un tableau pour afficher les pizzas
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("🍕 Pizza", style="cyan")
    table.add_column("📝 Description", style="green")
    table.add_column("🔗 Lien", style="blue")

    # Parcourir chaque bloc de pizza trouvé
    for pizza in pizzas:
        # Extraire le nom de la pizza
        name_element = pizza.find("span", class_="menu-entry")
        if name_element:
            name = name_element.get_text(strip=True)
            
            # Extraire la description de la pizza
            description_element = pizza.find("p", class_="menu-page-product-description")
            description = description_element.get_text(strip=True) if description_element else "Pas de description"
            
            # Trouver le lien de commande
            order_link_element = pizza.find("a", class_="order-now")
            order_link = order_link_element.get('href', "Pas de lien") if order_link_element else "Pas de lien"
            
            # Ajouter les données au tableau
            table.add_row(name, description, order_link)

    # Afficher un titre stylisé
    console.print(Panel.fit(
        "[bold yellow]🍕 Menu des Pizzas 🍕[/bold yellow]",
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
        scrape_pizzas()
    except Exception as e:
        console.print(f"[bold red]Erreur :[/bold red] {str(e)}")
