from sbs_utils import faces
from sbs_utils.procedural.gui import gui_clipboard_copy


def copy_clipboard(msg):
    gui_clipboard_copy(msg)
    return msg


def char_editor_features(race):
    """The controls to draw for a race, straight from the library's own recipe.

    This addon used to carry its own copy of the per-race control table - the third of
    four in the tree - and hand-rolled argument lists per race into the individual
    builders. All of it drifted after the 2026-09 sheet redraw: "Uniform" and "Long Hair"
    stopped existing, Terran gained eyewear and a headset, and every max was wrong.
    `faces.FACE_FEATURES` is generated from the layer tables, so it cannot disagree with
    the art.
    """
    return faces.FACE_FEATURES.get(str(race).lower(), [])


def char_editor_build_face(race, enables, values):
    """A face string from the editor's control state.

    Tolerates lists that are the wrong length in either direction: the race picker
    rebuilds them, and a stale list left over from a race with more controls used to
    feed extra positional arguments straight into a builder.
    """
    feats = char_editor_features(race)
    values = list(values or [])[:len(feats)]
    values += [0] * (len(feats) - len(values))
    enables = list(enables or [])[:len(feats)]
    enables += [not f.get("optional", False) for f in feats[len(enables):]]
    return faces.build_face(str(race).lower(), values, enables)


def char_editor_defaults(race):
    """(values, enables) sized for THIS race, with optional features switched off."""
    feats = char_editor_features(race)
    return [0] * len(feats), [not f.get("optional", False) for f in feats]


#: Above this many options a dropdown stops being usable in the engine. The owner's call:
#: "anything over 15 gets ugly - even 10". 8 sits under that and lands where the content
#: does - short enumerable lists stay dropdowns, the 39-tone skin palette gets a slider.
CHAR_EDITOR_DROPDOWN_MAX = 8


def char_editor_use_slider(names):
    """True when a named feature should be a slider-with-a-name rather than a dropdown."""
    return len(names or []) > CHAR_EDITOR_DROPDOWN_MAX


def char_editor_choice_label(label, names, index):
    """`"<Feature>: <name>"` as a text prop, for the label beside a named slider.

    One widget carrying both, rather than a third control on the row: the controls live
    in a narrow column and a label, a name and a slider do not fit across it.
    """
    names = list(names or [])
    if not names:
        return "text: " + _char_clean(label)
    try:
        current = names[int(index) % len(names)]
    except (TypeError, ValueError):
        current = names[0]
    return "text: " + _char_clean(label) + ": " + _char_clean(current)


def _char_clean(text):
    """Strip what would break a style string or a MAST assignment: ':' and ';' inject
    style properties, and '{' is re-run as an f-string and reported against the caller."""
    out = str(text or "")
    for bad in ("{", "}", ":", ";", "`"):
        out = out.replace(bad, " ")
    return out.strip()


def char_editor_choice_style(names, index):
    """A `gui_drop_down` style showing `index` and offering `names`.

    Emits no braces: MAST re-runs an assigned string through f-string formatting, so a
    '{' handed back from Python is a SyntaxError reported against the caller's line.
    """
    names = [str(n).replace(",", " ") for n in (names or [])]
    if not names:
        return "text: ;list: "
    try:
        current = names[int(index) % len(names)]
    except (TypeError, ValueError):
        current = names[0]
    return "text: " + current + ";list: " + ", ".join(names)


def char_editor_choice_index(names, value):
    """The index `value` picked, or 0 when the label is not one we offered."""
    names = [str(n).replace(",", " ") for n in (names or [])]
    try:
        return names.index(str(value))
    except ValueError:
        return 0
