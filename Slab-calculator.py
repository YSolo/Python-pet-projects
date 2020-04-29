

Skip to content
Using WV Construction cc Mail with screen readers
slab calculator 
Conversations
IT: Slab generator v.5

Eugene Solohub
Wed, Apr 3, 2019, 4:56 PM
Hello All, we have remastered our 'Slab generator' and now it is available as a standalone program (i.e. no other things are needed to make it work, yay) at W:\

Eugene Solohub
Wed, Apr 10, 2019, 10:42 PM
--

Eugene Solohub <e.solohub@wv-construction.com>
Attachments
Mon, Apr 15, 2019, 12:19 PM
to flowcontrol


Attachments area

Eugene Solohub
Wed, Jul 24, 2019, 9:33 PM
---------- Forwarded message --------- From:Eugene Solohub <e.solohub@wv-construction.com> Date: Wed, Apr 3, 2019, 4:56 PM Subject: IT: Slab generator v.5 To: D

Eugene Solohub <e.solohub@wv-construction.com>
Attachments
Wed, Jul 24, 2019, 9:33 PM
to Eugene.solohub


Attachments area

from Tkinter import *
import tkFileDialog, tkMessageBox
from math import ceil
from datetime import datetime
import os

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.number = 1
        self.slabs = []
        self.slabs_dict = []
        self.proj_data_entries = []
        self.proj_data = []
        self.grid()
        self.call_btn_Add_slab()
        self.call_btn_collect()
        self.add_slab()
        self.call_headers()
        self.call_prject_data()

    def call_prject_data(self):
        lblProjectNumber = Label(self,text="Project Number: ")
        lblProjectName = Label(self,text="Project Name: ")
        entProjectNumber = Entry(self)
        entProjectName = Entry(self)

        lblProjectNumber.grid(column=1,row=0)
        entProjectNumber.grid(column=2,row=0)
        lblProjectName.grid(column=3,row=0)
        entProjectName.grid(column=4,row=0, columnspan=3)


        self.proj_data_entries.append(entProjectNumber)
        self.proj_data_entries.append(entProjectName)

    def call_headers(self):
        lblSlabs =Label(self, text="Slabs")
        lblLength = Label(self, text="Length")
        lblWidth = Label(self, text="Width")
        lblFixed = Label(self, text="Fixed")
        lblDimpleSpacing = Label(self, text="DimpleSpacing")


        lblSlabs.grid(column=1,row=1)
        lblLength.grid(column=2, row=1)
        lblWidth.grid(column=3, row=1)
        lblFixed.grid(column=5, row=1)
        lblDimpleSpacing.grid(column=6, row=1)


    def call_btn_Add_slab(self):
        self.cloneSlabButton = Button ( self, text='+', command=self.add_slab)
        self.cloneSlabButton.grid(column=0)

    # Adds entry field and shifts '+' button under the entry
    def add_slab(self):
        slab = Entry(self)
        length = Entry(self)
        width = Entry(self)
        fixed = IntVar()
        chkbox_fixed = Checkbutton(self, onvalue =1, offvalue=0, variable=fixed)
        dimpleSpacing = Entry(self)

        slab.grid(column=1, row=self.number+1)
        length.grid(column=2, row=self.number+1)
        width.grid(column=3, row=self.number+1)
        chkbox_fixed.grid(column=5, row=self.number+1)
        dimpleSpacing.grid(column=6, row=self.number+1)
        dimpleSpacing.insert(END, 300)                          # default value for dimple spacing
        data = [slab,length,width, fixed, dimpleSpacing]
        self.slabs.append(data)

        self.cloneSlabButton.grid_forget()
        self.number += 1
        self.call_btn_Add_slab()

    def call_btn_collect(self):
        self.print_data = Button (self, text='Generate files',command=self.collect_data, bg="black", fg="white")
        self.print_data.grid(column=10,row=0)

    def collect_data(self):
        self.proj_data.append(self.proj_data_entries[0].get())       # get project number
        self.proj_data.append(self.proj_data_entries[1].get())       # get project name

        for slab_data in self.slabs:                             # for each slab in the sequence
            slab = {slab_data[0].get():[slab_data[1].get(),  # name and length
                                        slab_data[2].get(),  # width
                                        slab_data[3].get(),  # Fixed or not
                                        slab_data[4].get(),  # Dimple spacing
                                        ]}
            self.slabs_dict.append(slab)
        self.create_project_folder()

    #Creating folders and csv's
    def create_project_folder(self):
        current_dir = tkFileDialog.askdirectory(initialdir = "W:\\project_files\\")
        root_folder_name = ("%s_%s") % (self.proj_data[0], self.proj_data[1])
        project_folder = str(current_dir) + "/" + root_folder_name
        if not os.path.exists(project_folder):

            for d in self.slabs_dict:
                self.generate_csv_files(project_folder,d)
        else:
            tkMessageBox.showinfo("Already exists", "Folder already exists")
            quit()

        with open(project_folder+"\\summary.txt", "w") as f:
            f.write("Summary for " + root_folder_name + "\n")
            f.write("="*(12+len(root_folder_name)) + "\n")
            header = " %-10s | %-10s | %-10s | %-10s | %-10s | %-10s |\n"%("Name", "Length", "Width", "Fixed", "Spacing", "# of profiles")
            f.write(header)
            for slab in self.slabs_dict:
                dims = slab.values()[0]
                slab_info = " %-10s | %-10s | %-10s | %-10s | %-10s | %-10s |\n"%(slab.keys()[0], dims[0], dims[1], dims[2], dims[3], int(ceil(float(dims[1]) / 88)))
                f.write(slab_info)

        with open(project_folder+"\\csv_summary.csv", "w") as f:
            f.write("%s,%s,%s,%s,%s,%s\n"%("Name", "Length", "Width", "Fixed", "Spacing", "# of profiles"))
            for slab in self.slabs_dict:
                dims = slab.values()[0]
                f.write("%s,%s,%s,%s,%s,%s\n"%(slab.keys()[0], dims[0], dims[1], dims[2], dims[3], int(ceil(float(dims[1]) / 88))))
        tkMessageBox.showinfo("Done and dusted", "Factory request is created successfully")
        quit()


    def generate_csv_files(self,proj_folder,d):
        """get data for the slab"""
        slab_name = d.keys()[0]
        dimentions = d.values()
        dimentions = dimentions[0]
        length = float(dimentions[0])
        width = float(dimentions[1])
        fixed = dimentions[2]
        dimple_spacing = float(dimentions[3])

        """Calculate everything"""
        numberOfProfiles = int(ceil(width / 88))
        slab_folder_name = "%s - %sx %s mm" % (slab_name, numberOfProfiles, length)

        """Create folder"""

        path = ("%s\\%s" %(proj_folder, slab_folder_name))
        os.makedirs(path)

        """Create the range of dimples"""
        for profile in range(numberOfProfiles):
            dimple = 20.65
            dimples = []
            dimples.append(dimple)
            actual_spacing = (length - 20.65 * 2) / (int(ceil(length/dimple_spacing)))
            if fixed ==1:
                for d in range(int(length/dimple_spacing)-1):
                    dimple += dimple_spacing
                    dimples.append(dimple)
            else:
                for d in range(int(ceil(length/dimple_spacing))):
                    dimple += actual_spacing
                    dimples.append(round(dimple,2))

            """Generate csv files"""
            for p in range(numberOfProfiles):
                f = open(
                    "%s\\%s_%s_%sL%sW_L%s.csv" % (path,
                                                  self.proj_data[0],
                                                  slab_name,
                                                  (length / 1000),
                                                  (width / 1000),
                                                  (p + 1)),
                    "w")
                f.write("UNIT,MILLIMETRE\n" \
                        "PROFILE,41.30X89.00,Standard Profile\n" \
                        "FRAMESET,GI2,Ground_Floor,%s\n" % (self.proj_data[0]))

                f.write("COMPONENT,A-1,LABEL_NRM,1,%.2f" % (length), )
                for d in range(len(dimples)):
                    f.write(",DIMPLE,%.2f" % (dimples[d]), )


if __name__ == "__main__":
    app = Application()
    app.master.title("Slab Calculator 5.1")
    app.mainloop()
Slab_generator(v5).py
Displaying Slab_generator(v5).py.
