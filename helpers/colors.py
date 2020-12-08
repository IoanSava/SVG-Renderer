from matplotlib import colors


def convert_color_to_rgb(color):
    """ Convert a color in any format to rgb format.

    :param color: A string color in any format (hex, plaintext).
    :return: The color received as a parameter converted to rgb format.
    :rtype: list

    :example:
    >>> from helpers import colors
    >>> colors.convert_color_to_rgb('#ACDEDF')
    (0.6745098039215687, 0.8705882352941177, 0.8745098039215686)
    """

    if color.startswith('rgb'):
        values = color.split('(')[1].split(')')[0].split(',')
        return [int(number) / 255 for number in values]

    return colors.to_rgb(color)
