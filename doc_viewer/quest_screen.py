from sbs_utils.procedural.gui import gui_row, gui_text, gui_icon
from sbs_utils.procedural.quest import QuestState, document_get_amd_file 

from sbs_utils.procedural.gui.listbox import gui_list_box_is_header
from sbs_utils.helpers import FrameContext
from sbs_utils.procedural.inventory import set_inventory_value
from sbs_utils import fs
from sbs_utils.agent import Agent


def quest_item(item):
    
    if not gui_list_box_is_header(item):
        gui_row("row-height: 1.5em;padding:8px,0,0,0;")
        if item.get("state"):
            if item.state == QuestState.COMPLETE:
                gui_icon("icon_index:101;color:#151;", "padding:0,0,5px,0;")
            elif item.state == QuestState.FAILED:
                gui_icon("icon_index:101;color:#a22;", "padding:0,0,5px,0;")
            else:
                gui_icon("icon_index:121;color:#eee;", "padding:0,0,5px,0;")
        display_text = item.get("display_text")
        gui_text(f"$text:{display_text};justify: left;draw_layer:1000;","padding:5px,6px,0,0;")
    else:
        gui_row("row-height: 1.5em;padding:8px,0,0,0;")

        data = item.data
        if data is not None:
            if not gui_list_box_is_header(item) and item.get("state"):
                if data.state == QuestState.COMPLETE:
                    gui_icon("icon_index:101;color:#151;", "padding:0,0,5px,0;")
                else:
                    gui_icon("icon_index:121;color:#eee;", "padding:0,0,5px,0;")
                
        icon_index = 155 if not item.collapse else 154

        
        text = gui_text(f"$text:{item.label};justify: left;color:#fff;", "padding:5px,6px,0,0;background: #1578")
        # if item.data is not None and not data.get("root"):
        #     icon = gui_icon(f"icon_index:{icon_index};color:#fff;", "padding:0,0,5px,0;background: #1578;")
        if item.data is not None and not data.get("root"):
            icon = gui_icon(f"icon_index:{icon_index};color:#fff;", "padding:0,0,5px,0;background: #1578;")
            if item.selectable:
                icon.click_text = ""
                icon.click_tag = item.collapse_tag
                icon.click_background = "#aaaa"
                icon.click_color = "black"
                icon.background_color = "#1576"
                text.background_color = "#1576"
    return
    
def quest_title():
    gui_row("row-height: 1.5em;padding:3px;background:#157e;")
    gui_text(f"$text:QUESTS;justify: center;")



import ctypes
import ctypes.wintypes as wintypes

LPOFNHOOKPROC = ctypes.c_voidp # TODO
LPCTSTR = LPTSTR = ctypes.c_wchar_p

class OPENFILENAME(ctypes.Structure):
    _fields_ = [("lStructSize", wintypes.DWORD),
                ("hwndOwner", wintypes.HWND),
                ("hInstance", wintypes.HINSTANCE),
                ("lpstrFilter", LPCTSTR),
                ("lpstrCustomFilter", LPTSTR),
                ("nMaxCustFilter", wintypes.DWORD),
                ("nFilterIndex", wintypes.DWORD),
                ("lpstrFile", LPTSTR),
                ("nMaxFile", wintypes.DWORD),
                ("lpstrFileTitle", LPTSTR),
                ("nMaxFileTitle", wintypes.DWORD),
                ("lpstrInitialDir", LPCTSTR),
                ("lpstrTitle", LPCTSTR),
                ("flags", wintypes.DWORD),
                ("nFileOffset", wintypes.WORD),
                ("nFileExtension", wintypes.WORD),
                ("lpstrDefExt", LPCTSTR),
                ("lCustData", wintypes.LPARAM),
                ("lpfnHook", LPOFNHOOKPROC),
                ("lpTemplateName", LPCTSTR),
                ("pvReserved", wintypes.LPVOID),
                ("dwReserved", wintypes.DWORD),
                ("flagsEx", wintypes.DWORD)]

GetOpenFileName = ctypes.windll.comdlg32.GetOpenFileNameW
GetSaveFileName = ctypes.windll.comdlg32.GetSaveFileNameW

OFN_ENABLESIZING      =0x00800000
OFN_PATHMUSTEXIST     =0x00000800
OFN_OVERWRITEPROMPT   =0x00000002
OFN_NOCHANGEDIR       =0x00000008
MAX_PATH=1024


def _buildOFN(title, default_extension, filter_string, fileBuffer):
    ofn = OPENFILENAME()
    ofn.lStructSize = ctypes.sizeof(OPENFILENAME)
    ofn.lpstrTitle = title
    ofn.lpstrFile = ctypes.cast(fileBuffer, LPTSTR)
    ofn.nMaxFile = MAX_PATH
    ofn.lpstrDefExt = default_extension
    ofn.lpstrFilter = filter_string
    ofn.Flags = OFN_ENABLESIZING | OFN_PATHMUSTEXIST | OFN_OVERWRITEPROMPT | OFN_NOCHANGEDIR
    return ofn


def getOpenFileName(title, default_extension, filter_string, initialPath):

    if initialPath is None:
        initialPath = ""
    filter_string = filter_string.replace("|", "\0")
    fileBuffer = ctypes.create_unicode_buffer(initialPath, MAX_PATH)
    ofn = _buildOFN(title, default_extension, filter_string, fileBuffer)

    if GetOpenFileName(ctypes.byref(ofn)):
        return fileBuffer.value
        #return "".join(raw_contents_as_list)
    else:
        return None

def getSaveFileName(title, default_extension, filter_string, initialPath):

    if initialPath is None:
        initialPath = ""
    filter_string = filter_string.replace("|", "\0")
    fileBuffer = ctypes.create_unicode_buffer(initialPath, MAX_PATH)
    ofn = _buildOFN(title, default_extension, filter_string, fileBuffer)
    
    if GetSaveFileName(ctypes.byref(ofn)):
        return fileBuffer.value
        #return "".join(raw_contents_as_list)
    else:
        return None
    


def quest_file_open():
    ret = getOpenFileName("Open", "*.amd", "amd|Artemis Markdown", None)
    return ret



import os
import sys 
import time

class Watcher(object):
    # Constructor
    def __init__(self, watch_file):
        self._cached_stamp = 0
        self.filename = watch_file

    def reset(self, watch_file):
        self._cached_stamp = 0
        self.filename = watch_file

    # Look for changes
    def look(self):
        try:
            stamp = os.stat(self.filename).st_mtime
            if stamp != self._cached_stamp:
                self._cached_stamp = stamp
                # File has changed, so do something...
                return True
        except Exception:
            print("EXP")
        return False

def quest_get_watcher(watch_file):
    return Watcher(watch_file)  # also call custom action function
    