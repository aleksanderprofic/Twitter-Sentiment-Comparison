"""
Module for making plots
"""
import io
from typing import Dict, Tuple

import matplotlib.pyplot as plt


def make_plot(sentiments_with_names: Dict[str, float]) -> Tuple[io.BytesIO, int, int]:
    """ Function for making a bar plot

    Arguments:
        sentiments_with_names {Dict} -- dictionary with names (keywords) and their sentiments
    Returns:
        Tuple with plot image converted to BytesIO object, width and height of the image
    """
    keywords = sentiments_with_names.keys()
    values = sentiments_with_names.values()
    number_of_keywords = len(keywords)

    dpi = 80
    if number_of_keywords < 4:
        fig_size = (5, 5)
    else:
        fig_size = (10, 5)
    plt.clf()
    plt.figure(figsize=fig_size, dpi=dpi)
    plt.bar(keywords, values, edgecolor='black')
    plt.title("Sentiment comparison")

    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)

    return bytes_image, fig_size[0] * dpi, fig_size[1] * dpi
