"""
ColorHelper utils

Copyright (c) 2015 - 2017 Isaac Muse <isaacmuse@gmail.com>
License: MIT
"""
import re
import decimal
from . import csscolors, pantone, ral
from .rgba import RGBA, round_int, clamp

FLOAT_TRIM_RE = re.compile(r'^(?P<keep>\d+)(?P<trash>\.0+|(?P<keep2>\.\d*[1-9])0+)$')

COLOR_PARTS = {
    "percent": r"[+\-]?(?:(?:\d*\.\d+)|\d+)%",
    "percent_opt": r"[+\-]?(?:(?:\d*\.\d+)|\d+)%?",  # unit is sometimes optional
    "float": r"[+\-]?(?:(?:\d*\.\d+)|\d+)",
    "deg": r"[+\-]?(?:(?:\d*\.\d+)|\d+)(?:deg)?"  # a float with optional deg unit
}

COMPLETE = r'''
    (?P<hexa>(\#|0x)(?P<hexa_content>[\dA-Fa-f]{8}))\b |
    (?P<hex>(\#|0x)(?P<hex_content>[\dA-Fa-f]{6}))\b |
    (?P<hexa_compressed>(\#|0x)(?P<hexa_compressed_content>[\dA-Fa-f]{4}))\b |
    (?P<hex_compressed>(\#|0x)(?P<hex_compressed_content>[\dA-Fa-f]{3}))\b |
    \b(?P<rgb>rgb\(\s*(?P<rgb_content>(?:%(float)s\s*(,\s*)?){2}%(float)s | (?:%(percent)s\s*(,\s*)?){2}%(percent)s)\s*\)) |
    \b(?P<rgba>rgba\(\s*(?P<rgba_content>
        (?:%(float)s\s*(,\s*)?){3}(?:%(percent)s|%(float)s) | (?:%(percent)s\s*(,\s*)?){3}(?:%(percent)s|%(float)s)
    )\s*\)) |
    \b(?P<hsl>hsl\(\s*(?P<hsl_content>%(deg)s\s*(,\s*)?%(percent_opt)s\s*(,\s*)?%(percent_opt)s)\s*\)) |
    \b(?P<hsla>hsla\(\s*(?P<hsla_content>%(deg)s\s*(,\s*)?(?:%(percent_opt)s\s*(,\s*)?){2}(?:%(percent)s|%(float)s))\s*\)) |
    \b(?P<hwb>hwb\(\s*(?P<hwb_content>%(deg)s\s*(,\s*)?%(percent)s\s*(,\s*)?%(percent)s)\s*\)) |
    \b(?P<hwba>hwb\(\s*(?P<hwba_content>%(deg)s\s*(,\s*)?(?:%(percent)s\s*(,\s*)?){2}(?:%(percent)s|%(float)s))\s*\)) |
    \b(?P<gray>gray\(\s*(?P<gray_content>%(float)s|%(percent)s)\s*\)) |
    \b(?P<graya>gray\(\s*(?P<graya_content>(?:%(float)s|%(percent)s)\s*(,\s*)?(?:%(percent)s|%(float)s))\s*\)) |
    \b(?P<pantone_code>((\d{2}-)?\d{3,5}\s|(black|blue|bright red|cool gray|dark blue|green|magenta|medium purple|orange|pink|process blue|purple|red|reflex blue|rhodamine red|rose gold|silver|violet|warm gray|warm red|yellow)\s(\d{1,5}\s)?|p\s\d{1,3}-\d{1,2}\s)[a-z]{1,3})\b |  # noqa: E501
    \b(?P<ral_code>RAL\s\d{3,4}(-[0-9A-Z])?(\s\d{2}\s\d{2})?)\b
''' % COLOR_PARTS

COLOR_NAMES = r'\b(?P<webcolors>%s)\b(?!\()' % '|'.join([name for name in csscolors.name2hex_map.keys()])

HEX_IS_GRAY_RE = re.compile(r'(?i)^#([0-9a-f]{2})\1\1')
HEX_COMPRESS_RE = re.compile(r'(?i)^#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(?:([0-9a-f])\4)?$')

COLOR_RE = re.compile(r'(?x)(?i)(?<![@#$.\-_])(?:%s|%s)(?![@#$.\-_])' % (COMPLETE, COLOR_NAMES))


def fmt_float(f, p=0):
    """Set float precision and trim precision zeros."""

    string = str(
        decimal.Decimal(f).quantize(decimal.Decimal('0.' + ('0' * p) if p > 0 else '0'), decimal.ROUND_HALF_UP)
    )

    m = FLOAT_TRIM_RE.match(string)
    if m:
        string = m.group('keep')
        if m.group('keep2'):
            string += m.group('keep2')
    return string


def is_gray(color):
    """Check if color is gray (all channels the same)."""

    m = HEX_IS_GRAY_RE.match(color)
    return m is not None


def compress_hex(color):
    """Compress hex."""

    m = HEX_COMPRESS_RE.match(color)
    if m:
        color = '#' + m.group(1) + m.group(2) + m.group(3)
        if m.group(4):
            color += m.group(4)
    return color


def alpha_dec_normalize(dec):
    """Normalize a decimal alpha value."""

    temp = float(dec)
    if temp < 0.0 or temp > 1.0:
        dec = fmt_float(clamp(float(temp), 0.0, 1.0), 3)
    alpha = "%02X" % round_int(float(dec) * 255.0)
    return alpha, dec


def alpha_percent_normalize(perc):
    """Normalize a percent alpha value."""

    alpha_float = clamp(float(perc.strip('%')), 0.0, 100.0) / 100.0
    alpha_dec = fmt_float(alpha_float, 3)
    alpha = "%02X" % round_int(alpha_float * 255.0)
    return alpha, alpha_dec


def decode_and_split(data, decode=False):
    data = data.replace('deg', '')  # remove the optional deg unit

    """Optionally decode and then split over , or space."""
    if decode:
        data = data.decode('utf-8')

    splitter = ' '
    if ',' in data:
        splitter = ','
    return [x.strip() for x in data.split(splitter)]


def string_to_8bit(value):
    """Convert a float or percentage to a 0-255 value"""
    if value.endswith('%'):
        value = float(value.strip('%')) / 100
        value = value * 255
    else:
        value = float(value)

    return clamp(round_int(value), 0, 255)


def percentage_to_float(value):
    """Convert a percentage string ("50%) to a float (0.5)"""
    return clamp(float(value.strip('%')), 0.0, 100.0) / 100.0


def translate_color(m, use_hex_argb=False, decode=False):
    """Translate the match object to a color w/ alpha."""

    color = None
    alpha = None
    alpha_dec = None

    if m.group('hex_compressed'):
        content = m.group('hex_compressed_content')
        if decode:
            content = m.group('hex_compressed_content').decode('utf-8')
        color = "#%02x%02x%02x" % (
            int(content[0:1] * 2, 16), int(content[1:2] * 2, 16), int(content[2:3] * 2, 16)
        )

    elif m.group('hexa_compressed') and use_hex_argb:
        content = m.group('hexa_compressed_content')
        if decode:
            content = m.group('hexa_compressed_content').decode('utf-8')
        color = "#%02x%02x%02x" % (
            int(content[1:2] * 2, 16), int(content[2:3] * 2, 16), int(content[3:] * 2, 16)
        )
        alpha = content[0:1]
        alpha_dec = fmt_float(float(int(alpha, 16)) / 255.0, 3)

    elif m.group('hexa_compressed'):
        content = m.group('hexa_compressed_content')
        if decode:
            content = m.group('hexa_compressed_content').decode('utf-8')
        color = "#%02x%02x%02x" % (
            int(content[0:1] * 2, 16), int(content[1:2] * 2, 16), int(content[2:3] * 2, 16)
        )
        alpha = content[3:]
        alpha_dec = fmt_float(float(int(alpha, 16)) / 255.0, 3)

    elif m.group('hex'):
        content = m.group('hex_content')
        if decode:
            content = m.group('hex_content').decode('utf-8')
        if len(content) == 6:
            color = "#%02x%02x%02x" % (
                int(content[0:2], 16), int(content[2:4], 16), int(content[4:6], 16)
            )
        else:
            color = "#%02x%02x%02x" % (
                int(content[0:1] * 2, 16), int(content[1:2] * 2, 16), int(content[2:3] * 2, 16)
            )

    elif m.group('hexa') and use_hex_argb:
        content = m.group('hexa_content')
        if decode:
            content = m.group('hexa_content').decode('utf-8')
        if len(content) == 8:
            color = "#%02x%02x%02x" % (
                int(content[2:4], 16), int(content[4:6], 16), int(content[6:], 16)
            )
            alpha = content[0:2]
            alpha_dec = fmt_float(float(int(alpha, 16)) / 255.0, 3)
        else:
            color = "#%02x%02x%02x" % (
                int(content[1:2] * 2, 16), int(content[2:3] * 2, 16), int(content[3:] * 2, 16)
            )
            alpha = content[0:1]
            alpha_dec = fmt_float(float(int(alpha, 16)) / 255.0, 3)

    elif m.group('hexa'):
        content = m.group('hexa_content')
        if decode:
            content = m.group('hexa_content').decode('utf-8')
        if len(content) == 8:
            color = "#%02x%02x%02x" % (
                int(content[0:2], 16), int(content[2:4], 16), int(content[4:6], 16)
            )
            alpha = content[6:]
            alpha_dec = fmt_float(float(int(alpha, 16)) / 255.0, 3)
        else:
            color = "#%02x%02x%02x" % (
                int(content[0:1] * 2, 16), int(content[1:2] * 2, 16), int(content[2:3] * 2, 16)
            )
            alpha = content[3:]
            alpha_dec = fmt_float(float(int(alpha, 16)) / 255.0, 3)

    elif m.group('rgb'):
        content = decode_and_split(m.group('rgb_content'), decode)
        try:
            color = "#%02x%02x%02x" % (
                string_to_8bit(content[0]),
                string_to_8bit(content[1]),
                string_to_8bit(content[2])
            )
        except Exception:
            color = None

    elif m.group('rgba'):
        content = decode_and_split(m.group('rgba_content'), decode)
        try:
            color = "#%02x%02x%02x" % (
                string_to_8bit(content[0]),
                string_to_8bit(content[1]),
                string_to_8bit(content[2])
            )
            if content[3].endswith('%'):
                alpha, alpha_dec = alpha_percent_normalize(content[3])
            else:
                alpha, alpha_dec = alpha_dec_normalize(content[3])
        except Exception:
            color = None

    elif m.group('gray'):
        content = m.group('gray_content')
        if decode:
            content = m.group('gray_content').decode('utf-8')

        g = string_to_8bit(content)
        color = "#%02x%02x%02x" % (g, g, g)

    elif m.group('graya'):
        content = decode_and_split(m.group('graya_content'), decode)
        g = string_to_8bit(content[0])
        color = "#%02x%02x%02x" % (g, g, g)
        if content[1].endswith('%'):
            alpha, alpha_dec = alpha_percent_normalize(content[1])
        else:
            alpha, alpha_dec = alpha_dec_normalize(content[1])

    elif m.group('hsl'):
        content = decode_and_split(m.group('hsl_content'), decode)
        try:
            rgba = RGBA()
            hue = float(content[0])
            if hue < 0.0 or hue > 360.0:
                hue = hue % 360.0
            h = hue / 360.0
            s = percentage_to_float(content[1])
            lum = percentage_to_float(content[2])
            rgba.fromhls(h, lum, s)
            color = rgba.get_rgb()
        except Exception:
            color = None

    elif m.group('hsla'):
        content = decode_and_split(m.group('hsla_content'), decode)
        try:
            rgba = RGBA()
            hue = float(content[0])
            if hue < 0.0 or hue > 360.0:
                hue = hue % 360.0
            h = hue / 360.0
            s = percentage_to_float(content[1])
            lum = percentage_to_float(content[2])
            rgba.fromhls(h, lum, s)
            color = rgba.get_rgb()
            if content[3].endswith('%'):
                alpha, alpha_dec = alpha_percent_normalize(content[3])
            else:
                alpha, alpha_dec = alpha_dec_normalize(content[3])
        except Exception:
            color = None

    elif m.group('hwb'):
        content = decode_and_split(m.group('hwb_content'), decode)
        try:
            rgba = RGBA()
            hue = float(content[0])
            if hue < 0.0 or hue > 360.0:
                hue = hue % 360.0
            h = hue / 360.0
            w = percentage_to_float(content[1])
            b = percentage_to_float(content[2])
            rgba.fromhwb(h, w, b)
            color = rgba.get_rgb()
        except Exception:
            color = None

    elif m.group('hwba'):
        content = decode_and_split(m.group('hwba_content'), decode)
        try:
            rgba = RGBA()
            hue = float(content[0])
            if hue < 0.0 or hue > 360.0:
                hue = hue % 360.0
            h = hue / 360.0
            w = percentage_to_float(content[1])
            b = percentage_to_float(content[2])
            rgba.fromhwb(h, w, b)
            color = rgba.get_rgb()
            if content[3].endswith('%'):
                alpha, alpha_dec = alpha_percent_normalize(content[3])
            else:
                alpha, alpha_dec = alpha_dec_normalize(content[3])
        except Exception:
            color = None

    elif m.group('webcolors'):
        try:
            if decode:
                color = csscolors.name2hex(m.group('webcolors').decode('utf-8')).lower()
            else:
                color = csscolors.name2hex(m.group('webcolors')).lower()
        except Exception:
            pass
    elif m.group('pantone_code'):
        try:
            if decode:
                color = pantone.code2hex(m.group('pantone_code').decode('utf-8')).lower()
            else:
                color = pantone.code2hex(m.group('pantone_code')).lower()
        except Exception:
            pass
    elif m.group('ral_code'):
        try:
            if decode:
                color = ral.code2hex(m.group('ral_code').decode('utf-8')).lower()
            else:
                color = ral.code2hex(m.group('ral_code')).lower()
        except Exception:
            pass

    return color, alpha, alpha_dec
