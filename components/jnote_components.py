import curses, subprocess
from .curses_components import *      

class ModeBar(ScrollPageComponent):

    def __init__(self, height=10, width=10, begin_y=0, begin_x=0):
        super().__init__(height, width, begin_y, begin_x)
        
        self.items = ["create", "edit", "delete", "copy", "echo"]
        self.focus = 1

    def draw(self):

        item_width = self.width // len(self.items)

        for i, item in enumerate(self.items):

            if i == self.focus:
                self.win.addstr(0, item_width * i, item.center(item_width), curses.A_STANDOUT)
            else:
                self.win.addstr(0, item_width * i, item.center(item_width))

        self.win.refresh()

class ScrollPage(ScrollPageComponent):

    def __init__(self, height=10, width=10, begin_y=0, begin_x=0, notes_dir=""):
        super().__init__(height, width, begin_y, begin_x)
        self.notes_dir = notes_dir
        self.filtered_items = []

    
    def contains_str(self, note, filter_str):

        grep_result = subprocess.run(['grep', '-il', filter_str, self.notes_dir + note], stdout=subprocess.PIPE).stdout.decode('utf-8')
        return True if grep_result else False

    def apply_filter(self, filter_str, filter_is_more_specific):

        items_before_len = len(self.items) 

        if filter_is_more_specific:

            items_helper = []
            
            for item in self.items:

                if item.startswith(filter_str) or self.contains_str(item, filter_str):
                    items_helper.append(item)
                else:
                    self.filtered_items.append(item)

            self.items = items_helper

        else:

            filtered_items_helper = []
            
            for item in self.filtered_items:

                if item.startswith(filter_str) or self.contains_str(item, filter_str):
                    self.items.append(item)
                else:
                    filtered_items_helper.append(item)

            self.filtered_items = filtered_items_helper
            self.items = sorted(self.items)

        if not items_before_len == len(self.items):

            self.focus = 0

class TextBox(TextBoxComponent):

    def __init__(self, height=10, width=10, begin_y=0, begin_x=0, notes_dir=""):
        super().__init__(height, width, begin_y, begin_x)
        self.notes_dir = notes_dir
        self.note = ""
        self.startline = 0

    def increment_startline(self):
        self.startline += 3

    def decrement_startline(self):
        if self.startline >= 3: self.startline -=3

    def draw(self):

        self.win.clear()
        if not self.note: return

        with open(self.notes_dir + self.note, 'r') as note_file:
            note_contents = note_file.readlines()

        for i, line in enumerate(note_contents[self.startline:]):

            if i == self.height - 1: break

            self.win.addstr(i, 0, line[:self.width-1])
            self.win.clrtoeol()

        
        self.win.refresh()