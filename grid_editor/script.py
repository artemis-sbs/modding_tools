import sbslibs
from  sbs_utils.handlerhooks import *
from sbs_utils.gui import Gui
from sbs_utils.mast.maststorypage import StoryPage
from sbs_utils.mast.maststory import MastStory
from sbs_utils.mast.mast import Mast


class Story(MastStory):
    pass

class ThisStoryPage(StoryPage):
    story_file = "grid_editor.mast"


Mast.include_code = True

Gui.server_start_page_class(ThisStoryPage)
Gui.client_start_page_class(ThisStoryPage)
