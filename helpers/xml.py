import xml.etree.ElementTree as element_tree


def check_if_file_is_svg(filename):
    """Check if a file has a svg extension.

    :param filename: A path to a svg file.
    :raise: ValueError if filename has not .svg extension.
    """

    if not filename.lower().endswith('.svg'):
        raise ValueError


def get_items_from_svg_root(svg_filename):
    """Get the children of the root element in a svg file."""
    xml_tree = element_tree.parse(svg_filename)
    root = xml_tree.getroot()
    return [item for item in root]


def remove_namespace(element_tag):
    """Remove namespace from an element tag of a svg file."""
    return element_tag.split('}')[1]


def get_svg_dimensions(svg_filename):
    """Get svg file dimensions (i.e. width and height)."""
    xml_tree = element_tree.parse(svg_filename)
    root = xml_tree.getroot()
    return int(root.attrib['width']), int(root.attrib['height'])
