from helpers import colors

DEFAULT_COLOR = (0, 0, 0)  # black


def parse_string_points_to_list(string_points):
    """Transform string list of points to list of points.

    :param string_points: A string list of 2D points separated by spaces.
    :return: A list of tuples of 2D points.
    :rtype: list
    """

    points = []
    for point in string_points.split():
        x, y = point.split(',')
        points.append((int(x), int(y)))

    return points


def get_attributes(svg_attributes):
    """Update the polyline element attributes in order to draw it.

    :param svg_attributes: Attributes of a polyline svg item.
    :return: Attributes of polyline element.
    :rtype: dict
    """

    attributes = {
        'points': parse_string_points_to_list(svg_attributes['points'])
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
    """Draw a polyline on cairo context.

    :param context: The cairo context.
    :param attributes: A dictionary which contains specific attributes of polyline (e.g. points).
    """

    points = attributes['points']
    number_of_points = len(points)

    if number_of_points > 0:
        context.move_to(points[0][0], points[0][1])
        for i in range(1, number_of_points):
            context.line_to(points[i][0], points[i][1])

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
