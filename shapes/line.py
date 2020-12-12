from helpers import colors

DEFAULT_COLOR = (0, 0, 0)  # black


def get_attributes(svg_attributes):
    """Update the line element attributes in order to draw it.

    :param svg_attributes: Attributes of a line svg item.
    :return: Attributes of line element.
    :rtype: dict
    """

    attributes = {
        'x1': float(svg_attributes['x1']) if 'x1' in svg_attributes else 0,
        'y1': float(svg_attributes['y1']) if 'y1' in svg_attributes else 0,
        'x2': float(svg_attributes['x2']) if 'x2' in svg_attributes else 0,
        'y2': float(svg_attributes['y2']) if 'y2' in svg_attributes else 0
    }

    if 'stroke' in svg_attributes and svg_attributes['stroke'] != 'none':
        attributes['stroke_color'] = colors.convert_color_to_rgb(svg_attributes['stroke'])
        attributes['stroke_width'] = float(svg_attributes['stroke-width']) if 'stroke-width' in svg_attributes else 1

    return attributes


def draw(context, attributes):
    """Draw a line on cairo context.

    :param context: The cairo context.
    :param attributes: A dictionary which contains specific attributes of line (e.g. start, end).
    """

    context.move_to(attributes['x1'], attributes['y1'])
    context.line_to(attributes['x2'], attributes['y2'])

    if 'stroke_color' in attributes:
        context.set_source_rgb(*attributes['stroke_color'])
        context.set_line_width(attributes['stroke_width'])
        context.stroke()
