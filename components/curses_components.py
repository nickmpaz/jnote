import curses, time
from abc import ABC, abstractmethod

class Component(ABC):

    
    def __init__(self, height, width, begin_y, begin_x):
        self.set_window_size(height, width, begin_y, begin_x)
    
    def set_window_size(self, height, width, begin_y, begin_x):
        self.border_height = height
        self.border_width = width
        self.border_win = curses.newwin(height, width, begin_y, begin_x)
        # self.border_win.border()
        # self.border_win.refresh()
        self.height = height - 2
        self.width = width - 2
        self.win = curses.newwin(self.height, self.width, begin_y + 1, begin_x + 1)
        # self.win.refresh()

    def draw(self):
        self.border_win.border()
        self.border_win.refresh()

    
class SearchBarComponent(Component):

    def __init__(self, height=10, width=10, begin_y=0, begin_x=0):
        super().__init__(height, width, begin_y, begin_x)
        self.query = ""
        self.tab_string = ""

    def draw(self): 
        super().draw()
        text_line = (self.height // 2) 
        self.win.addstr(text_line, 0, self.query)
        self.win.clrtoeol()
        self.win.refresh()

class ScrollPageComponent(Component):

    def __init__(self, height=10, width=10, begin_y=0, begin_x=0):
        super().__init__(height, width, begin_y, begin_x)
        
        self.items = []
        self.focus = 0


    def increment_focus(self):
        if self.focus < len(self.items) - 1:
            self.focus += 1
            return True
        else:
            return False

    def decrement_focus(self):
        if self.focus > 0:
            self.focus -= 1
            return True
        else:
            return False

    def get_current_item(self):
        try:
            return self.items[self.focus]
        except:
            return None

    def draw_item(self, row, item_index):

        row_content = str(self.items[item_index])
        row_content = row_content.ljust(self.width - 1)

        if item_index == self.focus:
            self.win.addnstr(row, 0, row_content, self.width, curses.A_STANDOUT)
        else:
            self.win.addnstr(row, 0, row_content, self.width)

        self.win.clrtoeol()


    def draw(self):
        super().draw()
        if len(self.items) == 0:
            self.win.clear()
            self.win.refresh()

        max_items_on_page = self.height        

        # all the items fit on the page
        if len(self.items) <= max_items_on_page: 
            start_item = 0
            end_item = len(self.items) 

        # focus is above center
        elif self.focus < max_items_on_page // 2: 
            start_item = 0
            end_item = max_items_on_page 

        # focus is below center
        elif self.focus >= len(self.items) - (max_items_on_page // 2): 
            start_item = len(self.items) - max_items_on_page 
            end_item = len(self.items)

        # focus is in middle
        else:  
            start_item = self.focus - max_items_on_page // 2
            end_item = self.focus + max_items_on_page // 2 + max_items_on_page % 2
            
        for i, item_index in enumerate(range(start_item, end_item)):
            self.draw_item(i, item_index)            
            
            
        self.win.clrtobot()
        self.win.refresh()
        

class ProgressBarComponent(Component):

    def __init__(self, height=10, width=10, begin_y=0, begin_x=0):
        super().__init__(height, width, begin_y, begin_x)

        self.progress = 0
        self.message = "test"

    def draw(self):
        super().draw()
        bar_middle_y = self.height // 2 
        box_width = self.width // 2  
        bar_width = box_width - 2
        bar_start_x = (self.width - box_width) // 2
        progress = self.progress if self.progress <= 1 else 1
        bar_status = ("█" * int(bar_width * progress)).ljust(bar_width)

        self.win.addstr(bar_middle_y - 3, 0, self.message.center(self.width))
        self.win.addstr(bar_middle_y - 1, bar_start_x, "┌" + "─" * bar_width + "┐")
        self.win.addstr(bar_middle_y,     bar_start_x, "│" + bar_status +      "│")
        self.win.addstr(bar_middle_y + 1, bar_start_x, "└" + "─" * bar_width + "┘")
        self.win.addstr(bar_middle_y + 3, 0,(str(int(progress * 100)) + "%").center(self.width))

        self.win.refresh()


class TextBoxComponent(Component):

    def __init__(self, height=10, width=10, begin_y=0, begin_x=0):
        super().__init__(height, width, begin_y, begin_x)
        self.content = ""

    def draw(self): 
        super().draw()


class NotificationComponent(Component):
    
    def __init__(self, height=10, width=10, begin_y=0, begin_x=0, stdscr=None, prompt=""):
        super().__init__(height, width, begin_y, begin_x)
        self.prompt = prompt
        self.stdscr = stdscr

    def draw(self): 
        super().draw()
        self.win.clear()
        vertical_spacing = self.height // 3
        horizontal_spacing = self.width // 5

        self.win.addstr(vertical_spacing, 0, self.prompt.center(self.width))
        self.win.addstr(vertical_spacing * 2, horizontal_spacing*2, "continue".center(horizontal_spacing), curses.A_STANDOUT)
        self.win.refresh()


    def popup(self, prompt=None):

        if prompt: self.prompt = prompt
        self.draw()
        ch = self.stdscr.getkey()
        self.stdscr.clear()
        self.stdscr.refresh()


class ConfirmNotificationComponent(Component):

    def __init__(self, height=10, width=10, begin_y=0, begin_x=0, stdscr=None, prompt="", default_confirm=True):
        super().__init__(height, width, begin_y, begin_x)
        
        self.prompt = prompt
        self.confirm = default_confirm
        self.stdscr = stdscr

    def draw(self): 
        super().draw()
        self.win.clear()
        vertical_spacing = self.height // 3
        horizontal_spacing = self.width // 5

        self.win.addstr(vertical_spacing, 0, self.prompt.center(self.width))

        if self.confirm:
            self.win.addstr(vertical_spacing * 2, horizontal_spacing, "yes".center(horizontal_spacing), curses.A_STANDOUT)
            self.win.addstr(vertical_spacing * 2, horizontal_spacing * 3, "no".center(horizontal_spacing))
            

        else: 
            self.win.addstr(vertical_spacing * 2, horizontal_spacing, "yes".center(horizontal_spacing))
            self.win.addstr(vertical_spacing * 2, horizontal_spacing * 3, "no".center(horizontal_spacing), curses.A_STANDOUT)
        self.win.refresh()


    def popup(self, prompt=None):

        if prompt: self.prompt = prompt

        while True:

            self.draw()
            ch = self.stdscr.getkey()
            if ch == "\n": 
                break
            elif ch in ["KEY_LEFT", "KEY_RIGHT"]:
                self.confirm = not self.confirm
            
        self.stdscr.clear()
        self.stdscr.refresh()
        return self.confirm