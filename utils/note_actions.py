import os

def get_notes(notes_dir):

    notes_dir_contents = sorted(os.listdir(notes_dir))
    begin_index = 0

    for note in notes_dir_contents:

        if note.startswith("."): begin_index +=1
        else: break
            
    return notes_dir_contents[begin_index:]

def edit_note(notes_dir, note):

    os.system("vim " + notes_dir + note)

def create_note(notes_dir, note):

    os.system("rm " + notes_dir + note)
    os.system("touch " + notes_dir + note)
    os.system("vim " + notes_dir + note)

def delete_note(notes_dir, note):

    os.system("rm " + notes_dir + note)

def copy_note(notes_dir, note):
    pass

def echo_note(notes_dir, note):

    os.system("cat " + notes_dir + note)