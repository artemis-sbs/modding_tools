from sbs_utils.procedural.gui import gui_row, gui_text, gui_icon, gui_sub_section, gui_blank
from sbs_utils import fs
from sbs_utils.procedural.execution import get_shared_variable

import os


def history_item_template(item):
    gui_row("row-height: 3.5 em;padding:3px;")
    theme = get_theme_data(item)
    color = theme['color']
    icon = theme['icon']
    
    gui_icon(f"color:{color};icon_index:{icon};", "padding:0,0.2em;row-height: 3.5 em;col-width: 3.5 em;")
    with gui_sub_section("padding: 0.5em, 0.5em;") as fred:
        gui_row("row-height: 1.5em;")
        gui_text(f"text: {item['name']};justify: left;font:gui-3;color:{color};")
        gui_row("row-height: 1em;")
        roles = item['roles'].replace(",", " ")
        gui_text(f"text:{roles};justify: left;font:gui-2;color:{color};")
    
def roles_item_template(item):
    gui_row("row-height: 1.5em;padding:3px;")
    gui_text(f"text:{item};justify: left;")


def grid_data_files_title_template():
    gui_row("row-height: 1.5em;padding:3px;")
    gui_text(f"text:FILE;justify: left;", "col-width:15em;")
    gui_text(f"text:MISSION;justify: left;")


def grid_data_files_item_template(item):
    gui_row("row-height: 1.5em;padding:3px;")
    file = os.path.basename(item['file'])
    gui_text(f"text:{file};justify: left;", "col-width:15em;")
    gui_text(f"text:{item['mod']};justify: left;")


def icon_item_template(item):
    gui_row("row-height: 2em;padding:3px,3px,3px,3px;")
    gui_blank()
    gui_icon(f"color:white;icon_index:{item};") # , "padding:0,0.2em;row-height: 3.5 em;col-width: 3.5 em;")
    gui_blank()



def grid_editor_menu_template(item):
    gui_row("row-height: 48px;padding:3px")
    gui_icon(f"icon_index: {item['icon']};color:white;")
    gui_row("row-height: 1.2em")
    gui_text(f"text:{item['text']};justify:left;")
    



def get_mod_dirs_with_file(file_name):
    missions = []
    dir = fs.get_missions_dir()
    file_list = os.listdir(dir)
    for file in file_list:
        fn = os.path.join(dir, file, file_name)
        if os.path.isdir(fn):
            continue
        if os.path.isfile(fn):
            tfn = os.path.join(dir, file, "grid_theme.json")
            missions.append({"mod": file, "file": fn, "theme": tfn})
    return missions

def get_mod_dirs_with_grid_data():
    return get_mod_dirs_with_file("extra_grid_data.json")

def get_mission_has_grid_data():
    mission_gd = fs.get_artemis_data_dir_filename("grid_data.json")
    return os.path.isfile(mission_gd)

def get_theme_data(item, grid_theme_data=None):
    # called by templates
    #  get theme data and active theme
    # USe roles to find the right theme
    if grid_theme_data is None:
        grid_theme_data = get_shared_variable("current_grid_theme")
    if grid_theme_data is None:
        return {"color": "white", "icon": 1, "scale": 1.0}
    
    colors = grid_theme_data.get("colors", {"default": "white"})
    icons = grid_theme_data.get("icons", {"default": {"icon": 129,"scale": 1.0}})

    roles = item.get("roles", "default")
    roles = roles.split(",")
    
    color = None
    icon = None
    for role in reversed(roles):
        role = role.strip()
        if color is None:
            color = colors.get(role)
        if icon is None:
            icon = icons.get(role)

    if color is None:
        color = colors.get("default", "white")
        

    if icon is None:
        icon = icons.get("default", {"icon": 129,"scale": 1.0})
        

    # Make sure these have a value
    icon_index = icon.get("icon", 120)
    scale = icon.get("scale", 1.0)

    return {"color": color, "icon": icon_index, "scale": scale}


