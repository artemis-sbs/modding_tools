import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.mast.maststorypage import StoryPage
from sbs_utils.mast.label import label
from sbs_utils.mast.pollresults import PollResults
from sbs_utils.mast.mast import Mast
from sbs_utils.gui import Gui
from sbs_utils.agent import clear_shared

#import pymast.simple_ai as simple_ai
#import pymast.simple_science as simple_science
#import pymast.simple_comms as simple_comms
#import pymast.simple_gui as simple_gui

from sbs_utils.procedural.gui import gui_reroute_server, gui_row, gui_button, gui, gui_section, gui_text
from sbs_utils.procedural.execution import AWAIT
from sbs_utils import fs

start_text = f"text:This is an A >> \u0041 << Some custom glyphs >> \u0001 << AA ;font:gui-3;"
Mast.include_code = True
mission_name = fs.get_mission_name()

@label()
def start_client():
    gui_section("area:2,20,80,35;")
    gui_text(f"""Waiting for the server to select example mission. MY Glyphs >> \u0130 \u0131 <<""")

    yield AWAIT(gui())
    # It should never go beyond this
    assert(False)


@label()
def start_server():
    yield PollResults.OK_RUN_AGAIN
    gui_section("area:2,20,80,35;")
    gui_text(f""" {start_text}""")
    sbs.suppress_client_connect_dialog(0)


    gui_section("area:25,30,85,95;row-height: 35px")
    gui_button("Grid editor", on_message=lambda : sbs.run_next_mission(f"{mission_name}/grid_editor"))
    gui_row()
    gui_button("Scatter editor", on_message=lambda : sbs.run_next_mission(f"{mission_name}/scatter"))
    gui_row()
    gui_button("Face editor", on_message=lambda : sbs.run_next_mission(f"{mission_name}/char_editor"))

    yield AWAIT(gui())
    assert(False)
    
            
