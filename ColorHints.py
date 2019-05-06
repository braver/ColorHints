import sublime
import sublime_plugin
from .lib import util, pantone

TEMPLATE = '''
    <body id="inline-color-hint">
        <style>
            div.color-box {{
                padding: .5em;
                border: 1px solid var(--foreground);
                background-color: {color};
            }}
        </style>
        <div class="color-box"></div>
    </body>
'''


def plugin_loaded():
    pantone.load()


def get_cursor_color(view, region):
    """Get cursor color."""

    color = None
    alpha = None
    alpha_dec = None
    point = region.begin()
    visible = view.visible_region()
    start = point - 50
    end = point + 50
    if start < visible.begin():
        start = visible.begin()
    if end > visible.end():
        end = visible.end()
    bfr = view.substr(sublime.Region(start, end))
    ref = point - start
    for m in util.COLOR_RE.finditer(bfr):
        if ref >= m.start(0) and ref < m.end(0):
            color, alpha, alpha_dec = util.translate_color(m, True)
            break
    return color, alpha, alpha_dec


def render_hints(view, phantom_set, rule):
    # render hints accoring to a rule, ie. always, or only in a certain scope
    sels = view.sel()
    ps = []
    for sel in sels:
        if rule == 'always' or view.match_selector(sel.b, rule):
            color = get_cursor_color(view, sel)
            print(color)
            if color[0] is not None:
                line_end = view.line(sel).end()
                region = sublime.Region(line_end, line_end)
                ps.append(sublime.Phantom(
                        region,
                        TEMPLATE.format(color=color[0]),
                        sublime.LAYOUT_INLINE))

    phantom_set.update(ps)


class ManualColorHint(sublime_plugin.TextCommand):

    def __init__(self, view):
        self.view = view
        self.phantom_set = sublime.PhantomSet(view, 'manual_color_hints')

    def run(self, paths):
        render_hints(self.view, self.phantom_set, 'always')


class ClearManualColorHints(sublime_plugin.ViewEventListener):

    def on_modified_async(self):
        self.view.erase_phantoms('manual_color_hints')


class ShowColorHints(sublime_plugin.ViewEventListener):

    def __init__(self, view):
        self.view = view
        self.phantom_set = sublime.PhantomSet(view, 'color_hints')

    def on_selection_modified_async(self):
        settings = sublime.load_settings('ColorHints.sublime-settings')
        rule = settings.get('live_hints', 'always')
        if settings.get('live_hints') != 'never':
            render_hints(self.view, self.phantom_set, rule)
