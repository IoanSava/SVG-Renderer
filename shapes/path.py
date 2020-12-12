import math

from helpers import colors

DEFAULT_COLOR = (0, 0, 0)  # black
LINE_COMMANDS = ('m', 'M', 'l', 'L', 'h', 'H', 'v', 'V', 'z', 'Z')
CURVE_COMMANDS = ('c', 'C', 's', 'S', 'q', 'Q', 't', 'T')
ARC_COMMANDS = ('a', 'A')
last_t_control_point = ()


def insert_space_between_command_and_args(commands):
    """Insert spaces between commands and arguments.

    :param commands: A string of available commands for a path svg element.
    :return: The same string with spaces between command name and args.
    :rtype: string
    """

    formatted_commands = ''
    length_of_commands = len(commands)
    for i in range(length_of_commands):
        if i > 0 and (commands[i].isdigit() or commands[i] == '-') and commands[i - 1].isalpha():
            formatted_commands += ' '
        formatted_commands += commands[i]

    return formatted_commands


def separate_commands(commands):
    """Separate string of path commands into a list.

    :param commands: A string of path commands.
    :return: A list where each element is a string with a specific path command.
    :rtype: list
    """

    start_index = 0
    length_of_commands = len(commands)
    separated_commands = []
    for i in range(length_of_commands):
        if i > 0 and commands[i].isalpha():
            separated_commands.append(commands[start_index:(i - 1)])
            start_index = i

    separated_commands.append(commands[start_index:])
    separated_commands = [command.split() for command in separated_commands]
    return separated_commands


def parse_curve_command(command):
    """Parse a curve string command.

    :param command: A string with a curve command for a path.
    :return: A list with parsed command.
    :rtype: list
    """

    result = []
    for i in range(len(command)):
        command[i] = command[i].replace(',', '').replace(' ', '')

    command = list(filter(lambda x: x != '', command))

    result.append(command[0])
    for i in range(1, len(command[1:]), 2):
        result.append((float(command[i]), float(command[i + 1])))

    return result


def parse_arc_command(command):
    """Parse a arc string command.

    :param command: A string with a arc command for a path.
    :return: A list with parsed command.
    :rtype: list
    """

    result = []
    for element in command:
        element = element.replace(',', '').replace(' ', '')
        if element[0].isalpha():
            result.append(element)
        else:
            result.append(float(element))

    return result


def parse_commands_to_list(commands):
    """Convert list of path commands to a more convenient format.

    :param commands: A string of available commands for a path svg element.
    :return: List of commands in a more convenient and easy to work with format.
    :rtype: list
    """

    commands = insert_space_between_command_and_args(commands)
    commands = separate_commands(commands)

    result = []
    for command in commands:
        if command[0] in LINE_COMMANDS:
            result.append([element if element[0].isalpha() else float(element) for element in command])
        elif command[0] in CURVE_COMMANDS:
            result.append(parse_curve_command(command))
        elif command[0] in ARC_COMMANDS:
            result.append(parse_arc_command(command))

    return result


def get_attributes(svg_attributes):
    """Update the path element attributes in order to draw it.

    :param svg_attributes: Attributes of a path svg item.
    :return: Attributes of path element.
    :rtype: dict
    """

    attributes = {
        'commands': parse_commands_to_list(svg_attributes['d'])
    }

    if 'fill' in svg_attributes:
        if svg_attributes['fill'] != 'none':
            attributes['color'] = colors.convert_color_to_rgb(svg_attributes['fill'])
    else:
        attributes['color'] = DEFAULT_COLOR

    if 'stroke' in svg_attributes:
        attributes['stroke_color'] = colors.convert_color_to_rgb(svg_attributes['stroke'])
        attributes['stroke_width'] = float(svg_attributes['stroke-width']) if 'stroke-width' in svg_attributes else 1

    return attributes


def get_reflection_point(point1, point2):
    """Return the reflection of point1 over the point2.

    :param point1: A 2D point.
    :param point2: A 2D point.
    :return: The reflection of point1 over the point2.
    """

    x, y = point1[0] - point2[0], point1[1] - point2[1]
    return point2[0] - x, point2[1] - y


def draw_smooth_curveto(context, command, previous_command):
    """Draw a smooth curveto on cairo context.

    :param context: The cairo context
    :param command: A S/s path command.
    :param previous_command: The previous path command.
    """

    current_point = context.get_current_point()
    first_control_point = ()
    if previous_command == () or previous_command[0] not in ('s', 'S', 'c', 'C'):
        first_control_point = current_point
    else:
        operation = previous_command[0]
        if operation.isupper():
            if operation == 'C':
                first_control_point = get_reflection_point(previous_command[2], current_point)
            else:
                first_control_point = get_reflection_point(previous_command[1], current_point)
        else:
            if operation == 'c':
                x, y = previous_command[4][0] + previous_command[2][0], previous_command[4][1] + previous_command[2][1]
                first_control_point = get_reflection_point((x, y), current_point)
            else:
                x, y = previous_command[3][0] + previous_command[1][0], previous_command[3][1] + previous_command[1][1]
                first_control_point = get_reflection_point((x, y), current_point)

    if command[0].isupper():
        context.curve_to(*first_control_point, *command[1], *command[2])
    else:
        first_control_point = first_control_point[0] - current_point[0], first_control_point[1] - current_point[1]
        context.rel_curve_to(*first_control_point, *command[1], *command[2])


def draw_smooth_quadratic_curveto(context, command, previous_command):
    """Draw a smooth quadratic curveto on cairo context.

    :param context: The cairo context
    :param command: A T/t path command.
    :param previous_command: The previous path command.
    """

    global last_t_control_point
    current_point = context.get_current_point()

    if previous_command == () or previous_command[0] not in ('t', 'T', 'q', 'Q'):
        last_t_control_point = current_point

        if command[0] == 't':
            context.rel_line_to(*command[1])
        else:
            context.line_to(*command[1])
    else:
        control_point = ()
        operation = previous_command[0]
        if operation.isupper():
            if operation == 'Q':
                control_point = get_reflection_point(previous_command[1], current_point)
            else:
                control_point = get_reflection_point(last_t_control_point, current_point)
        else:
            if operation == 'q':
                x, y = previous_command[3][0] + previous_command[1][0], previous_command[3][1] + previous_command[1][1]
                control_point = get_reflection_point((x, y), current_point)
            else:
                control_point = get_reflection_point(last_t_control_point, current_point)

        last_t_control_point = control_point

        if command[0].isupper():
            context.curve_to(*control_point, *command[1], *command[1])
        else:
            control_point = control_point[0] - current_point[0], control_point[1] - current_point[1]
            context.rel_curve_to(*control_point, *command[1], *command[1])


def rotate(x, y, angle):
    """Rotate a point of an angle around the origin point."""
    return x * math.cos(angle) - y * math.sin(angle), y * math.cos(angle) + x * math.sin(angle)


def point_angle(cx, cy, px, py):
    """Return angle between x axis and point knowing given center."""
    return math.atan2(py - cy, px - cx)


def draw_arc(context, command):
    """Draw an arc on cairo context.

    :param context: The cairo context
    :param command: An A/a path command.
    """

    current_point = context.get_current_point()
    end_point = command[6], command[7]
    if command[0].isupper():
        # convert absolute coordinates to relative
        end_point = end_point[0] - current_point[0], end_point[1] - current_point[1]

    rx, ry = command[1], command[2]
    if rx == 0 or ry == 0:
        context.line_to(*end_point)
        return

    rotation = math.radians(command[3])
    large, sweep = command[4], command[5]
    if large not in (0, 1) or sweep not in (0, 1):
        return
    large, sweep = bool(large), bool(sweep)

    radiuses_ratio = ry / rx
    new_x, new_y = rotate(end_point[0], end_point[1], -rotation)
    new_y = new_y / radiuses_ratio
    angle = point_angle(0, 0, new_x, new_y)
    new_x = math.sqrt(new_x ** 2 + new_y ** 2)
    rx = max(rx, new_x / 2)

    cx = new_x / 2
    cy = (rx ** 2 - cx ** 2) ** .5
    cy = -cy if large == sweep else cy

    arc = context.arc if sweep else context.arc_negative
    new_x, new_y = rotate(new_x, 0, angle)
    cx, cy = rotate(cx, cy, angle)
    angle1 = point_angle(cx, cy, 0, 0)
    angle2 = point_angle(cx, cy, new_x, new_y)

    context.save()
    context.translate(*current_point)
    context.rotate(rotation)
    context.scale(1, radiuses_ratio)
    arc(cx, cy, rx, angle1, angle2)
    context.restore()


def execute_command_with_absolute_coordinates(context, command, previous_command):
    """Execute a path command with absolute coordinates.

    :param context: The cairo context.
    :param command: The current path command.
    :param previous_command: The previous path command.
    """

    action = command[0]

    if action == 'M':
        context.move_to(command[1], command[2])
    elif action == 'L':
        context.line_to(command[1], command[2])
    elif action == 'H':
        context.line_to(command[1], context.get_current_point()[1])
    elif action == 'V':
        context.line_to(context.get_current_point()[0], command[1])
    elif action == 'Z':
        context.close_path()
    elif action == 'C':
        context.curve_to(*command[1], *command[2], *command[3])
    elif action == 'Q':
        context.curve_to(*command[1], *command[2], *command[2])
    elif action == 'S':
        draw_smooth_curveto(context, command, previous_command)
    elif action == 'T':
        draw_smooth_quadratic_curveto(context, command, previous_command)
    elif action == 'A':
        draw_arc(context, command)


def execute_command_with_relative_coordinates(context, command, previous_command):
    """Execute a path command with relative coordinates.

    :param context: The cairo context.
    :param command: A path command.
    :param previous_command: The previous path command.
    """

    action = command[0]

    if action == 'm':
        context.rel_move_to(command[1], command[2])
    elif action == 'l':
        context.rel_line_to(command[1], command[2])
    elif action == 'h':
        context.rel_line_to(command[1], 0)
    elif action == 'v':
        context.rel_line_to(0, command[1])
    elif action == 'z':
        context.close_path()
    elif action == 'c':
        context.rel_curve_to(*command[1], *command[2], *command[3])
    elif action == 'q':
        context.rel_curve_to(*command[1], *command[2], *command[2])
    elif action == 's':
        draw_smooth_curveto(context, command, previous_command)
    elif action == 't':
        draw_smooth_quadratic_curveto(context, command, previous_command)
    elif action == 'a':
        draw_arc(context, command)


def draw(context, attributes):
    """Draw a path on cairo context.

    :param context: The cairo context.
    :param attributes: A dictionary which contains specific attributes of path (e.g. commands, color, stroke).
    """

    previous_command = ()

    for command in attributes['commands']:
        current_endpoint = context.get_current_point()
        action = command[0]
        if action.isupper():
            execute_command_with_absolute_coordinates(context, command, previous_command)
        else:
            execute_command_with_relative_coordinates(context, command, previous_command)
        previous_command = command
        previous_command.append(current_endpoint)

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
