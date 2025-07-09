from sbs_utils import faces
from sbs_utils.procedural.gui import gui_clipboard_copy
import sys



def copy_clipboard(msg):
    t = msg
    gui_clipboard_copy(msg)
    return msg

def char_editor_build_face(race, enables, values):
    race = race.lower()
    match race:
        case "arvonian":
            args = values[0:5]
            args[0]=0
            for i,e in enumerate(enables):
                if not e:
                    args[i] = None
            return faces.arvonian(*args)
        case "kralien":
            args = values[0:5]
            args[0]=0
            for i,e in enumerate(enables):
                if not e:
                    args[i] = None
            return faces.kralien(*args)
        case "skaraan":
            args = values[0:5]
            args[0]=0
            for i,e in enumerate(enables):
                if not e:
                    args[i] = None
            return faces.skaraan(*args)
        case "terran":
            args = values[:10]
            for i,e in enumerate(enables):
                if not e:
                    args[i] = None
            return faces.terran(*args)

        case "torgoth":
            args = values[0:6]
            args[0]=0
            for i,e in enumerate(enables):
                if not e:
                    args[i] = None
            return faces.torgoth(*args)
        case "ximni":
            args = values[0:6]
            args[0]=0
            for i,e in enumerate(enables):
                if not e:
                    args[i] = None
            return faces.ximni(*args)
            
        
    return faces.Characters.URSULA