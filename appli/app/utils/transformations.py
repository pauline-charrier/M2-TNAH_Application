from unidecode import unidecode

def clean_arg(arg):
    """
    Nettoie un argument en remplaçant une chaîne vide par None.

    Parameters
    ----------
    arg : str
        L'argument à nettoyer.

    Returns
    -------
    str or None
        La chaîne originale si elle n'est pas vide, sinon None.
    """
    if arg == "":
        return None
    else:
        return arg
    
def normaliser(string):
    """
    Normalise une chaîne en la décomposant en ASCII et en la convertissant en minuscules.

    Parameters
    ----------
    string : str
        La chaîne à normaliser.

    Returns
    -------
    str
        La chaîne normalisée en ASCII et en minuscules.
    """
    return unidecode(string).lower()