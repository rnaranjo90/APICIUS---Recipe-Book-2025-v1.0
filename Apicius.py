#  APICIUS - Recipe Book 2025 v1.0

"""
APICIUS - Recipe Book 2025 v1.0

This Python script is a command-line recipe manager that allows users to:
- View the total number of stored recipes.
- Select and display a recipe from categorized collections.
- Create new recipes and categories.
- Delete recipes and categories.
- Navigate through an interactive menu.

Key functionalities:
- Uses pathlib for file management.
- Implements recursive directory searches.
- Validates user input to ensure correct menu selection.
- Manages recipe storage within the "Recetas" directory in the user's home folder.

Developed for personal recipe organization with an intuitive interface.
"""

# Import
from pathlib import *
from os import system
import shutil

# Funtions
def contador_recetas(ruta_recetas): # Recipe counter: Given the route with the recipes, it tells me how many there are in total.
    cantidad_recetas = 0
    for txt in Path(ruta_recetas).glob("**/*txt"):
        cantidad_recetas+=1
    return f"* We have a total of {cantidad_recetas} recipes"

def chosen_option(): # Show options to user and choose
    print("""* Choose the desired option:   
     [1] Select recipe
     [2] Create recipe
     [3] Create category
     [4] Delete recipe
     [5] Delete category
     [6] End program
                      """)
    option = int(input("Option: "))
    if option in range(1,7):
        return option
    else:
        print("Out of range!!!")
        return chosen_option()

def create_menu(lista): # Create menu: Given a list of options, it designs a menu for us
    cont = 1
    for item in range(0, len(lista)):
        print(f"[{cont}] - {lista[item]}")
        cont += 1
    return ""

def range_validator(lista): # Range Validator: Validates that the entered value is within the range of the list
    eleccion = int(input("Option: "))
    if eleccion in range(1,len(lista)+1):
        return int(eleccion)
    else:
        print("Out of range!!!")
        return range_validator(lista)

def categorias(): # Create a list with the recipe book categories
    ruta_categorias = Path.home() / "Recetas"
    categorias = [categ.name for categ in ruta_categorias.iterdir() if categ.is_dir()]
    return categorias

def recipe(categorias,elecc_categoria): # Create a list with the recipes
    ruta_recetas = Path(Path.home(),"Recetas",categorias[elecc_categoria - 1])
    recetas = [rece.name for rece in ruta_recetas.iterdir() if rece.is_file()]
    return recetas

def select_category(categorias): # Select categorys: Given the list of categories, it returns the selected category in an integer value.
    print(create_menu(categorias))
    elecc_categoria = (range_validator(categorias))
    return elecc_categoria

def select_recipe(categorias,recetas,elecc_categoria): # Select recipes
    """
    :param categorias:  Contains a list of categories
    :param recetas:     Contains a list of recipes
    :param elecc_categoria: Contains the position of the selected category
    :return: Returns the position of the chosen recipe from the list
    """
    print(create_menu(recetas))
    elecc_receta = (range_validator(recetas))
    return elecc_receta

def show_recipe(categorias,recetas,elecc_categoria,elecc_receta): # Select recipe to display
    ruta_final = Path(Path.home(),"Recetas",categorias[elecc_categoria - 1],recetas[elecc_receta - 1])
    return (ruta_final.read_text() + "\n")


def choose_recipe(): # [1] Choose recipe
    """
     Gives the user the ability to select the recipe by first
      asking them to select the Category and then the desired recipe within it.
    :return: Displays the content of the selected recipe
    """
    categorias_ = categorias()
    elecc_categoria = select_category(categorias_)
    recetas_ = recipe(categorias_,elecc_categoria)
    elecc_receta = select_recipe(categorias_,recetas_,elecc_categoria)
    return show_recipe(categorias_,recetas_,elecc_categoria,elecc_receta)

def create_recipe(): # [2] Create recipe
    """
    Once the category is selected, it asks us for the name of the new recipe and its content to create the new file
    and place the recipe
    :return: Returns whether the recipe was saved successfully or not.
    """
    categorias_ = categorias()
    elecc_categoria = select_category(categorias_)
    categoria = categorias_[elecc_categoria-1]

    nombre_receta = input("Write recipe name: ")
    contenido_receta = input("Describe recipe: ")

    ubicacion = Path(Path.home()/"Recetas",categoria,f"{nombre_receta}.txt")
    print(ubicacion)

    if ubicacion.exists():
        return "This location already exists. It will not be created again.\n"
    else:
        ubicacion.write_text(contenido_receta)
        return "Recipe saved successfully\n"

def create_category(category): # [3] Create category: Given a category, create the file with the name of the same
    categorias_ = categorias()

    if category in categorias_:
        return f"This category ({category}) already exists\n"
    else:
        ubicacion = Path(Path.home() , "Recetas", category)
        ubicacion.mkdir()
        return f"Category ({category}) created successfully\n"

def delete_recipe(): # [4] Delete recipe
    """
    Asking the user to choose the category and the recipe deletes it permanently
    :return: Returns whether the Delete recipe operation was executed correctly
    """
    categorias_ = categorias()
    elecc_categoria = select_category(categorias_)
    recetas_ = recipe(categorias_,elecc_categoria)
    elecc_receta = select_recipe(categorias_,recetas_,elecc_categoria)
    ubicacion = Path(Path.home(), "Recetas", categorias_[elecc_categoria-1],recetas_[elecc_receta-1])
    ubicacion.unlink()
    return ("Recipe successfully deleted\n")

def delete_category(): # [5] Delete catregory
    """
    Asks the user for a category to be deleted
    :return: Returns whether the Delete category operation is executed successfully
    """
    categorias_ = categorias()
    elecc_categoria = select_category(categorias_)

    ubicacion = Path(Path.home(), "Recetas", categorias_[elecc_categoria-1])
    shutil.rmtree(ubicacion)
    return ("Category successfully deleted\n")


# Welcome
print("\n                                Welcome to APICIUS\n")

# Show where the recipes are
ruta_recetas = Path.home() / "Recetas"
print(f"* The file with the recipes is located at: {ruta_recetas}")

# Number of recipes we have
print(contador_recetas(ruta_recetas))

# Chosen option: Displays the project's main menu, giving the user the possibility to select an option.
eleccion = chosen_option()
while eleccion in range(1,7):
    match eleccion:
        case 1:
            print(f"You chose: Select recipe")
            print(choose_recipe())
            eleccion = chosen_option()
        case 2:
            print(f"You chose: Create recipe")
            print(create_recipe())
            eleccion = chosen_option()
        case 3:
            print(f"You chose: Create category")
            category = input("Introduce una nueva categoría: ")
            print(create_category(category))
            eleccion = chosen_option()
        case 4:
            print(f"You chose: Delete recipe")
            print(delete_recipe())
            eleccion = chosen_option()
        case 5:
            print(f"You chose: Delete category")
            print(delete_category())
            eleccion = chosen_option()
        case 6:
            print(f"End program")
            break