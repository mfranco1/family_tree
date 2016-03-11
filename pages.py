import pickle
from tkinter import *
from people import *

class Root(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title("Family Forest pre-alpha")
        self.frames = {}
        self.family_tree = []

        for F in (HomePage, NewTree, EditTree, DeleteTree, HelpPage, TraversePage):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def get_family_tree(self):
        return self.family_tree

    def set_family_tree(self,person):
        if person:
            self.family_tree.append(person)
            print("added "+person.get_full_name()+"\n")
            link_child_parent(person)
            link_parent_child(self.family_tree,person)
            link_spouse(self.family_tree,person)

    def load_family_tree(self):
        x=0

class HomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        #title frame
        title_frame = Frame(self)
        title_frame.grid(row=0,column=0)

        #title label to be replaced with image
        title = StringVar()
        title_label = Label(title_frame,textvariable=title,relief=RAISED)
        title.set("WELCOME TO FAMILY FOREST pre-alpha!")
        title_label.pack()

        #options frame
        option_frame = Frame(self)
        option_frame.grid(row=1,column=0)

        #home option buttons
        new_tree_button = Button(option_frame,text="New Person",command=lambda:controller.show_frame("NewTree"))
        new_tree_button.grid(row=0,column=0)
        edit_tree_button = Button(option_frame,text="Edit Person",command=lambda:controller.show_frame("EditTree"))
        edit_tree_button.grid(row=0,column=1)
        delete_tree_button = Button(option_frame,text="Delete Tree",command=lambda:controller.show_frame("DeleteTree"))
        delete_tree_button.grid(row=0,column=2)
        traverse_tree_button = Button(option_frame,text="Traverse",command=lambda:controller.show_frame("TraversePage"))
        traverse_tree_button.grid(row=0,column=3)
        open_tree_button = Button(option_frame,text="Open Tree",command=lambda:self.open_filedialogue())
        open_tree_button.grid(row=1,column=0)
        save_tree_button = Button(option_frame,text="Save Tree",command=lambda:self.open_filedialogue())
        save_tree_button.grid(row=1,column=1)

    def open_filedialogue(self):
        x=0


class NewTree(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, text="New Person")
        label.grid(row=0,column=0)

        #get person info
        data_frame = Frame(self)
        data_frame.grid(row=1,column=0)

        self.f_name_label = Label(data_frame,text="First Name")
        self.f_name_label.grid(row=0,column=0)
        self.f_name_entry = Entry(data_frame, bd =5)
        self.f_name_entry.grid(row=0,column=1)

        self.l_name_label = Label(data_frame,text="Last Name")
        self.l_name_label.grid(row=1,column=0)
        self.l_name_entry = Entry(data_frame, bd =5)
        self.l_name_entry.grid(row=1,column=1)

        self.gender_label = Label(data_frame,text="Gender")
        self.gender_label.grid(row=2,column=0)
        self.gender_entry = Entry(data_frame, bd =5)
        self.gender_entry.grid(row=2,column=1)

        self.birth_date_label = Label(data_frame,text="Birthdate YYYY-MM-DD")
        self.birth_date_label.grid(row=3,column=0)
        self.birth_date_entry = Entry(data_frame, bd =5)
        self.birth_date_entry.grid(row=3,column=1)

        self.father_label = Label(data_frame,text="Father's Name")
        self.father_label.grid(row=4,column=0)
        self.father_entry = Entry(data_frame, bd =5)
        self.father_entry.grid(row=4,column=1)

        self.mother_label = Label(data_frame,text="Mother's Name")
        self.mother_label.grid(row=5,column=0)
        self.mother_entry = Entry(data_frame, bd =5)
        self.mother_entry.grid(row=5,column=1)

        self.spouse_label = Label(data_frame,text="Spouse's Name")
        self.spouse_label.grid(row=6,column=0)
        self.spouse_entry = Entry(data_frame, bd =5)
        self.spouse_entry.grid(row=6,column=1)

        #new tree option buttons
        option_frame = Frame(self)
        option_frame.grid(row=2,column=0)
        add_person_button = Button(option_frame,text="Add to Tree",command=lambda:controller.set_family_tree(self.process_entries()))
        add_person_button.grid(row=0,column=0)
        new_tree_home_button = Button(option_frame,text="Cancel",command=lambda:controller.show_frame("HomePage"))
        new_tree_home_button.grid(row=0,column=1)
        help_button = Button(option_frame,text="Help",command=lambda:controller.show_frame("HelpPage"))
        help_button.grid(row=0,column=2)

    def process_entries(self):
        self.sanitize_entries()
        if self.entries_are_safe():
            fname = self.f_name_entry.get()
            lname = self.l_name_entry.get()
            gender = self.gender_entry.get()
            birthdate = self.birth_date_entry.get()
            father = find_person(self.controller.get_family_tree(),self.father_entry.get())
            if not father:
                father = self.father_entry.get()
            mother = find_person(self.controller.get_family_tree(),self.mother_entry.get())
            if not mother:
                mother = self.mother_entry.get()
            spouse = find_person(self.controller.get_family_tree(),self.spouse_entry.get())
            if not spouse:
                spouse = self.spouse_entry.get()
            p = make_person(fname,lname,gender,birthdate,father,mother)
            p.set_spouse(spouse)
            return p

    def sanitize_entries(self):
        fname = self.f_name_entry.get()
        fname = fname.split(' ', 1)[0]
        fname = fname.title()
        self.f_name_entry.delete(0,END)
        self.f_name_entry.insert(0,fname)

        lname = self.l_name_entry.get()
        lname = lname.split(' ', 1)[0]
        lname = lname.title()
        self.l_name_entry.delete(0,END)
        self.l_name_entry.insert(0,lname)

        gender = self.gender_entry.get()
        gender = gender.split(' ', 1)[0]
        gender = gender.title()
        self.gender_entry.delete(0,END)
        self.gender_entry.insert(0,gender)

    def entries_are_safe(self):
        if not is_valid_fname(self.f_name_entry.get()):
            return False
        if not is_valid_lname(self.l_name_entry.get()):
            return False
        if not is_valid_gender(self.gender_entry.get()):
            return False
        if not is_valid_bdate(self.birth_date_entry.get()):
            return False
        return True


class EditTree(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, text="Edit Person")
        label.grid(row=0,column=0)

        #edit form
        data_frame = Frame(self)
        data_frame.grid(row=1,column=0)

        self.full_name_label = Label(data_frame,text="Full Name")
        self.full_name_label.grid(row=0,column=0)
        self.full_name_entry = Entry(data_frame, bd =5)
        self.full_name_entry.grid(row=0,column=1)

        self.f_name_label = Label(data_frame,text="First Name")
        self.f_name_label.grid(row=1,column=0)
        self.f_name_entry = Entry(data_frame, bd =5)
        self.f_name_entry.grid(row=1,column=1)
        self.f_name_edit = Button(data_frame,text="Edit",command=lambda:self.edit_person("temp","temp"))
        self.f_name_edit.grid(row=1,column=2)

        self.l_name_label = Label(data_frame,text="Last Name")
        self.l_name_label.grid(row=2,column=0)
        self.l_name_entry = Entry(data_frame, bd =5)
        self.l_name_entry.grid(row=2,column=1)
        self.l_name_edit = Button(data_frame,text="Edit",command=lambda:self.edit_person("temp","temp"))
        self.l_name_edit.grid(row=2,column=2)

        self.spouse_label = Label(data_frame,text="Spouse's Name")
        self.spouse_label.grid(row=3,column=0)
        self.spouse_entry = Entry(data_frame, bd =5)
        self.spouse_entry.grid(row=3,column=1)
        self.spouse_edit = Button(data_frame,text="Edit",command=lambda:self.edit_person("temp","temp"))
        self.spouse_edit.grid(row=3,column=2)

        self.child_label = Label(data_frame,text="Child's Name")
        self.child_label.grid(row=4,column=0)
        self.child_entry = Entry(data_frame, bd =5)
        self.child_entry.grid(row=4,column=1)
        self.child_edit = Button(data_frame,text="Edit",command=lambda:self.edit_person("temp","temp"))
        self.child_edit.grid(row=4,column=2)

        self.death_label = Label(data_frame,text="Last Name")
        self.death_label.grid(row=5,column=0)
        self.death_entry = Entry(data_frame, bd =5)
        self.death_entry.grid(row=5,column=1)
        self.death_edit = Button(data_frame,text="Edit",command=lambda:self.edit_person("temp","temp"))
        self.death_edit.grid(row=5,column=2)

        #edit tree option buttons
        option_frame = Frame(self)
        option_frame.grid(row=2,column=0)
        edit_person_button = Button(option_frame,text="Edit All",command=lambda:self.edit_person(controller.get_family_tree(),self.full_name_entry.get()))
        edit_person_button.grid(row=0,column=1)
        edit_tree_home_button = Button(option_frame,text="Cancel",command=lambda:controller.show_frame("HomePage"))
        edit_tree_home_button.grid(row=0,column=2)
        help_button = Button(option_frame,text="Help",command=lambda:controller.show_frame("HelpPage"))
        help_button.grid(row=0,column=3)

    def edit_person(self,list,name):
        if not find_person(list,name):
            print(self.full_name_entry.get()+" is not in the Tree")
            return False
        print(self.full_name_entry.get()+" has been edited successfully")
        return True


class DeleteTree(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, text="Delete Tree")
        label.grid(row=0,column=0)

        #delete tree option buttons
        option_frame = Frame(self)
        option_frame.grid(row=2,column=0)
        delete_tree_home_button = Button(option_frame,text="Cancel",command=lambda:controller.show_frame("HomePage"))
        delete_tree_home_button.grid(row=0,column=0)
        help_button = Button(option_frame,text="Help",command=lambda:controller.show_frame("HelpPage"))
        help_button.grid(row=0,column=1)


class TraversePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, text="Traverse Page")
        label.grid(row=0,column=0)

        #take inputs "NAME"
        data_frame = Frame(self)
        data_frame.grid(row=1,column=0)
        name_label = Label(data_frame,text="Traverse From (Full Name)")
        name_label.grid(row=0,column=0)
        name_entry = Entry(data_frame, bd =5)
        name_entry.grid(row=0,column=1)

        #traverse page option buttons
        option_frame = Frame(self)
        option_frame.grid(row=2,column=0)
        traverse_button = Button(option_frame,text="Traverse",command=lambda:self.call_traverse(controller.get_family_tree(),name_entry.get()))
        traverse_button.grid(row=0,column=0)
        trav_home_button = Button(option_frame,text="Cancel",command=lambda:controller.show_frame("HomePage"))
        trav_home_button.grid(row=0,column=1)
        help_button = Button(option_frame,text="Help",command=lambda:controller.show_frame("HelpPage"))
        help_button.grid(row=0,column=2)

    def call_traverse(self,list,name):
        p = find_person(list,name)
        traverse_from(p)


class HelpPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, text="Help Page")
        label.grid(row=0,column=0)

        #help page option buttons
        help_home_button = Button(self,text="Home",command=lambda:controller.show_frame("HomePage"))
        help_home_button.grid(row=1,column=0)