import sbslibs
from  sbs_utils.handlerhooks import *
from sbs_utils.gui import Gui
from sbs_utils.mast.maststorypage import StoryPage
from sbs_utils.mast.maststory import MastStory

from sbs_utils.mast.mast import Mast
from story import start_server, start_client


class Story(MastStory):
    pass

class SimpleAiPage(StoryPage):
    story = Story()
    main_server = start_server
    main_client = start_client



Mast.include_code = True

Gui.server_start_page_class(SimpleAiPage)
Gui.client_start_page_class(SimpleAiPage)
