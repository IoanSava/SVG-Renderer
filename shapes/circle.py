import math

from helpers import colors

DEFAULT_COLOR = (0, 0, 0)  # black


def get_attributes(svg_attributes):
    """Update the circle element attributes in order to draw it.

    :param svg_attributes: Attributes of a circle svg item.
    :return: Attributes of circle element.
    :rtype: dict
    """

    attributes = {
        'cx': int(svg_attributes['cx']) if 'cx' in svg_attributes else 0,
        'cy': int(svg_attributes['cy']) if 'cy' in svg_attributes else 0,
        'radius': int(svg_attributes['r'])
    }

    if 'fill' in svg_attributes:
        if svg_attributes['fill'] != 'none':
            attributes['color'] = colors.convert_color_to_rgb(svg_attributes['fill'])
    else:
        attributes['color'] = DEFAULT_COLOR

    if 'stroke' in svg_attributes and svg_attributes['stroke'] != 'none':
        attributes['stroke_color'] = colors.convert_color_to_rgb(svg_attributes['stroke'])
        attributes['stroke_width'] = int(svg_attributes['stroke-width']) if 'stroke-width' in svg_attributes else 1

    return attributes


def draw(context, attributes):
    """Draw a circle on cairo context.

    :param context: The cairo context.
    :param attributes: A dictionary which contains specific attributes of circle (e.g. center point, radius).
    """

    context.arc(attributes['cx'], attributes['cy'], attributes['radius'], 0, 2 * math.pi)

    if 'color' in attributes:
        context.set_source_rgb(*attributes['color'])
        if 'stroke_color' in attributes:
            context.fill_preserve()
        else:
            context.fill()

    if 'stroke_color' in attributes:
        context.set_source_rgb(*attributes['stroke_color'])
        context.set_line_width(attributes['stroke_width'])
        context.stroke()
