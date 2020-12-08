from helpers import colors

DEFAULT_COLOR = (0, 0, 0)  # black


def get_attributes(svg_attributes, size):
    """Update the rectangle element attributes in order to draw it.

    :param svg_attributes: Attributes of a rect svg item.
    :param size: Size of image.
    :return: Attributes of rectangle element.
    :rtype: dict
    """

    width, height = size
    attributes = {
        'x': int(svg_attributes['x']) if 'x' in svg_attributes else 0,
        'y': int(svg_attributes['y']) if 'y' in svg_attributes else 0,
        'width': int(svg_attributes['width']) if not svg_attributes['width'].endswith('%') else int(int(
            svg_attributes['width'][:-1]) / 100 * width),
        'height': int(svg_attributes['height']) if not svg_attributes['height'].endswith('%') else int(int(
            svg_attributes['height'][:-1]) / 100 * height)
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
    """Draw a rectangle on cairo context.

    :param context: The cairo context.
    :param attributes: A dictionary which contains specific attributes of rectangle (e.g. width, height, color).
    """

    context.rectangle(attributes['x'], attributes['y'], attributes['width'], attributes['height'])

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
