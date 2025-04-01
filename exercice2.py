# Importation des modules nécessaires
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
from rich.text import Text

# Création d'une instance de Console pour l'affichage
console = Console()

def generate_html(pizzas_data):
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Menu des Pizzas</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                padding: 20px;
                background-color: #ff6b6b;
                color: white;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .pizza-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                padding: 20px;
            }
            .pizza-card {
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }
            .pizza-card:hover {
                transform: translateY(-5px);
            }
            .pizza-name {
                color: #ff6b6b;
                font-size: 1.5em;
                margin-bottom: 10px;
                font-weight: bold;
            }
            .pizza-description {
                color: #666;
                margin-bottom: 15px;
                line-height: 1.6;
            }
            .order-button {
                display: inline-block;
                padding: 10px 20px;
                background-color: #ff6b6b;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            .order-button:hover {
                background-color: #ff5252;
            }
            .footer {
                text-align: center;
                padding: 20px;
                margin-top: 30px;
                color: #666;
            }
            @media (max-width: 768px) {
                .pizza-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🍕 Menu des Pizzas 🍕</h1>
            </div>
            <div class="pizza-grid">
    """
    
    for pizza in pizzas_data:
        html_content += f"""
                <div class="pizza-card">
                    <div class="pizza-name">{pizza['name']}</div>
                    <div class="pizza-description">{pizza['description']}</div>
                    <a href="{pizza['link']}" class="order-button">Commander</a>
                </div>
        """
    
    html_content += """
            </div>
            <div class="footer">
                <p>Bon appétit !</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open("menu_pizzas.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def scrape_pizzas():
    # Ouvrir le fichier HTML contenant les pizzas, en mode lecture avec encodage UTF-8
    with open("pizzas.html", "r", encoding="utf-8") as file:
        # Créer un objet BeautifulSoup pour parser le HTML
        soup = BeautifulSoup(file, "html.parser")

    # Trouver toutes les balises contenant les informations d'un produit
    pizzas = soup.find_all("div", class_="product-container")
    
    # Liste pour stocker les données des pizzas
    pizzas_data = []

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
            order_link = order_link_element.get('href', "#") if order_link_element else "#"
            
            # Ajouter les données à la liste
            pizzas_data.append({
                'name': name,
                'description': description,
                'link': order_link
            })

    # Générer la page HTML
    generate_html(pizzas_data)
    
    # Afficher un message de confirmation
    console.print(Panel.fit(
        "[bold green]✅ Page HTML générée avec succès ![/bold green]\n[italic]Ouvrez menu_pizzas.html dans votre navigateur pour voir le résultat.[/italic]",
        border_style="green"
    ))

if __name__ == "__main__":
    try:
        scrape_pizzas()
    except Exception as e:
        console.print(f"[bold red]Erreur :[/bold red] {str(e)}") 