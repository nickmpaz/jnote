import os, pathlib

class NotesHandler():

    def __init__(self):
        self.notes_dir = os.path.expanduser("~") + "/.notes/"
        self.copy_file = None
        pathlib.Path(self.notes_dir).mkdir(parents=True, exist_ok=True)

    def up_dir(self):
        if self.notes_dir == os.path.expanduser("~") + "/.notes/": return
        self.notes_dir = str(pathlib.Path(self.notes_dir).parent) + "/"

    def down_dir(self, ch_dir):
        self.notes_dir += ch_dir + "/"

    def is_dir(self, note, ch_dir=""):
        if not note or note == "": return False
        return os.path.isdir(self.notes_dir + ch_dir + "/"+ note)

    def get_notes(self, ch_dir=""):

        notes_dir_contents = sorted(os.listdir(self.notes_dir + ch_dir))
        begin_index = 0

        for note in notes_dir_contents:

            if note.startswith("."): begin_index +=1
            else: break
                
        return notes_dir_contents[begin_index:]

    def edit_note(self, note):

        os.system("vim " + self.notes_dir + note + ' 2>/dev/null')

    def create_note(self, note):

        os.system("rm " + self.notes_dir + note + ' 2>/dev/null')
        os.system("touch " + self.notes_dir + note + ' 2>/dev/null')
        os.system("vim " + self.notes_dir + note + ' 2>/dev/null')

    def create_dir(self, ch_dir):
        os.system("mkdir "+ self.notes_dir + ch_dir + ' 2>/dev/null')

    def delete_note(self, note):

        os.system("rm " + self.notes_dir + note + ' 2>/dev/null')

    def delete_dir(self, ch_dir):
        os.system("rm -rf " + self.notes_dir + ch_dir)

    def copy_note(self):
        if self.copy_file: os.system("xclip -selection clipboard %s" % (self.copy_file))

    def echo_note(self, note):

        os.system("cat " + self.notes_dir + note + ' 2>/dev/null')

        