import pandas as pd

def build_aspect_matrix(planets, aspects):
    """
    Constructs a symmetrical aspect matrix between planets using their aspect symbols.

    Parameters:
        planets (list of dict): List of planetary data including 'Symbol'.
        aspects (list of dict): List of aspect data including 'Planet1', 'Planet2', and 'Symbol'.

    Returns:
        pandas.DataFrame: A matrix with planetary symbols as rows and columns, filled with aspect symbols.
    """
    planet_symbols = [p['Symbol'] for p in planets]
    size = len(planet_symbols)

    # Initialize empty matrix
    matrix = pd.DataFrame('', index=planet_symbols, columns=planet_symbols)

    # Fill the matrix with aspect symbols
    for aspect in aspects:
        p1 = aspect['Planet1']
        p2 = aspect['Planet2']
        symbol = aspect['Symbol']

        matrix.loc[p2, p1] = symbol

    return matrix
