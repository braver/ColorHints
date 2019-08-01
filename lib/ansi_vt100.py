"""
ANSI/VT100 color escape sequences for 4 bit colors.

A simple escape sequence to hex map of colors.
Assumes "default background" to be black and "foreground" white.
Colors taken from Terminal.app defaults.

https://en.m.wikipedia.org/wiki/ANSI_escape_code#Colors
"""
code2hex_map = {
    '39': '#ffffff',  # default foreground
    '49': '#000000',  # default background

    '30': '#000000',  # black
    '40': '#000000',

    '31': '#990000',  # red
    '41': '#990000',

    '32': '#00a600',  # green
    '42': '#00a600',

    '33': '#999900',  # yellow
    '43': '#999900',

    '34': '#0000b2',  # blue
    '44': '#0000b2',

    '35': '#b200b2',  # magenta
    '45': '#b200b2',

    '36': '#00a6b2',  # cyan
    '46': '#00a6b2',

    '37': '#ffffff',  # white
    '47': '#ffffff',

    '90': '#666666',  # bright black
    '100': '#666666',
    '1;30': '#666666',  # bold + black
    '1;40': '#666666',

    '91': '#e50000',  # bright red
    '101': '#e50000',
    '1;31': '#e50000',  # bold + red
    '1;41': '#e50000',

    '92': '#00d900',  # bright green
    '102': '#00d900',
    '1;32': '#00d900',  # bold + green
    '1;42': '#00d900',

    '93': '#e5e500',  # bright yellow
    '103': '#e5e500',
    '1;33': '#e5e500',  # bold + yellow
    '1;43': '#e5e500',

    '94': '#0000ff',  # bright blue
    '104': '#0000ff',
    '1;34': '#0000ff',  # bold + blue
    '1;44': '#0000ff',

    '95': '#e500e5',  # bright magenta
    '105': '#e500e5',
    '1;35': '#e500e5',  # bold + magenta
    '1;45': '#e500e5',

    '96': '#00e5e5',  # bright cyan
    '106': '#00e5e5',
    '1;36': '#00e5e5',  # bold + cyan
    '1;46': '#00e5e5',

    '97': '#e5e5e5',  # bright white
    '107': '#e5e5e5',
    '1;37': '#e5e5e5',  # bold + white
    '1;47': '#e5e5e5',
}

hex2code_map = dict([(v, k) for k, v in code2hex_map.items()])


def hex2code(value):
    """Convert CSS hex to webcolor name."""

    return hex2code_map.get(value.lower(), None)


def code2hex(name):
    """Convert webcolor name to CSS hex."""

    print(name.split(';'))

    return code2hex_map.get(name.lower(), None)
