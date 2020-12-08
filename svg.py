import cairo
import sys
from helpers import xml
from shapes import rectangle, circle, ellipse, line, polyline

PIXEL_SCALE = 10
PNG_FILENAME = 'outputs/image.png'


def init_surface(size):
    """Initialize the cairo surface to hold drawing.

    :param size: Size of the image (i.e. width and height).
    :return: The initialized cairo surface.
    :rtype: cairo.ImageSurface
    """

    width, height = size

    return cairo.ImageSurface(cairo.FORMAT_RGB24,
                              width * PIXEL_SCALE,
                              height * PIXEL_SCALE)


def init_cairo_context(surface, size):
    """Initialize cairo context used to draw with.

    :param surface: The cairo surface.
    :param size: Size of the image (i.e. width and height).
    :return: The initialized cairo context.
    :rtype: cairo.Context
    """

    width, height = size

    context = cairo.Context(surface)
    context.scale(PIXEL_SCALE, PIXEL_SCALE)
    context.rectangle(0, 0, width, height)
    context.fill()

    return context


def fill_context(context, size, items):
    """Fill cairo context with elements from svg items.

    :param context: The cairo context.
    :param size: Size of the image (i.e. width and height).
    :param items: Children of the root element in the input svg file.
    """

    for item in items:
        item_tag = xml.remove_namespace(item.tag)
        if item_tag == 'rect':
            rectangle.draw(context, rectangle.get_attributes(item.attrib, size))
        elif item_tag == 'circle':
            circle.draw(context, circle.get_attributes(item.attrib))
        elif item_tag == 'ellipse':
            ellipse.draw(context, ellipse.get_attributes(item.attrib))
        elif item_tag == 'line':
            line.draw(context, line.get_attributes(item.attrib))
        elif item_tag == 'polyline':
            polyline.draw(context, polyline.get_attributes(item.attrib))


def build_cairo_context(size, items, surface):
    """Build the cairo context needed to do
     the conversion from svg format to png format.

    :param size: Size of the image (i.e. width and height).
    :param items: Children of the root element in the input svg file.
    :param surface: The cairo surface.
    :return: The final cairo context.
    :rtype: cairo.Context
    """

    context = init_cairo_context(surface, size)
    fill_context(context, size, items)
    return context


def draw_image(png_filename, surface):
    """Translate the cairo surface into a png file.

    :param png_filename: Path to png file (result for svg to png conversion).
    :param surface: The cairo surface.
    """

    surface.write_to_png(png_filename)


def main(argv):
    """Convert a svg file to png format.

    :param argv: The list of arguments received from command line.
           argv[0]: Path to a svg file.
    """

    if len(argv) != 1:
        print('Invalid arguments. Format: svg.py image.svg')
    else:
        svg_file = argv[0]
        try:
            xml.check_if_file_is_svg(svg_file)
            items = xml.get_items_from_svg_root(svg_file)
            size = xml.get_svg_dimensions(svg_file)
            surface = init_surface(size)
            build_cairo_context(size, items, surface)
            draw_image(PNG_FILENAME, surface)
        except ValueError:
            print('Invalid file. Should be a svg')
        except FileNotFoundError:
            print('File', svg_file, 'not found')


if __name__ == '__main__':
    main(sys.argv[1:])
