import sublime
import sublime_plugin
from ColorHints.lib import util


TEMPLATE = '''
    <body id="inline-color-hint">
        <style>
            div.color-box {{
                padding: .5em;
                border: 1px solid #fff;
                background-color: {color};
            }}
        </style>
        <div class="color-box"></div>
    </body>
'''


def get_cursor_color(self, region):
    """Get cursor color."""

    color = None
    alpha = None
    alpha_dec = None
    point = region.begin()
    visible = self.view.visible_region()
    start = point - 50
    end = point + 50
    if start < visible.begin():
        start = visible.begin()
    if end > visible.end():
        end = visible.end()
    bfr = self.view.substr(sublime.Region(start, end))
    ref = point - start
    use_hex_argb = False
    allowed_colors = util.ALL
    for m in util.COLOR_RE.finditer(bfr):
        if ref >= m.start(0) and ref < m.end(0):
            if m.group('hex_compressed') and 'hex_compressed' not in allowed_colors:  # noqa 501
                continue
            elif m.group('hexa_compressed') and 'hexa_compressed' not in allowed_colors:  # noqa 501
                continue
            elif m.group('hex') and 'hex' not in allowed_colors:
                continue
            elif m.group('hexa') and 'hexa' not in allowed_colors:
                continue
            elif m.group('rgb') and 'rgb' not in allowed_colors:
                continue
            elif m.group('rgba') and 'rgba' not in allowed_colors:
                continue
            elif m.group('gray') and 'gray' not in allowed_colors:
                continue
            elif m.group('graya') and 'graya' not in allowed_colors:
                continue
            elif m.group('hsl') and 'hsl' not in allowed_colors:
                continue
            elif m.group('hsla') and 'hsla' not in allowed_colors:
                continue
            elif m.group('hwb') and 'hwb' not in allowed_colors:
                continue
            elif m.group('hwba') and 'hwba' not in allowed_colors:
                continue
            elif m.group('webcolors') and 'webcolors' not in allowed_colors:  # noqa 501
                continue
            color, alpha, alpha_dec = util.translate_color(
                                                        m,
                                                        bool(use_hex_argb))
            break
    return color, alpha, alpha_dec


class ColorHintAtCursor(sublime_plugin.TextCommand):

    def run(self, paths):
        self.view.erase_phantoms('color_hints')
        sels = self.view.sel()
        for sel in sels:
            color = get_cursor_color(self, sel)
            print(color)
            if color[0] is not None:
                line_end = self.view.line(sel).end()
                region = sublime.Region(line_end, line_end)
                self.view.add_phantom('color_hints',
                                      region,
                                      TEMPLATE.format(color=color[0]),
                                      sublime.LAYOUT_INLINE)


class ClearColorHints(sublime_plugin.EventListener):

    def on_modified_async(self, view):
        view.erase_phantoms('color_hints')
