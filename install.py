# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-30 10:23:13'

"""

"""
import os
import sys
import json
import shutil

MAYA_DIR = r"C:\Program Files\Autodesk\Maya2017"
DIR = os.path.dirname(__file__)
TK = False
Qt = False
try:
    from Tkinter import *
    TK = True
except ImportError:
    try:
        from tkinter import *
        TK = True
    except ImportError:
        try:
            from PySide.QtCore import *
            from PySide.QtGui import *
            Qt = True
        except ImportError:
            from PySide2.QtWidgets import *
            from PySide2.QtGui import *
            from PySide2.QtCore import *
            Qt = True

def installMiniMaya(maya_dir=None,install_dir=None,shell=False):
    maya_dir = maya_dir if type(maya_dir) is str and os.path.exists(maya_dir) else MAYA_DIR if os.path.exists(MAYA_DIR) else None
    install_dir = install_dir if type(install_dir) is str and os.path.exists(install_dir) else os.path.realpath(os.path.dirname(__file__))
    if maya_dir is None:
        raise RuntimeError('Default Maya Installation Directory not exists')
    
    with open(os.path.join(DIR,"dir_tree.json"),'r') as f:
        dir_tree = json.load(f,encoding="utf-8")
    
    def dict_to_path(data,root=None):
        """
        https://stackoverflow.com/questions/25226208/represent-directory-tree-as-json
        """
        file_type = data.get("type")
        file_name = data.get("name")
        target_path = os.path.join(root,file_name)
        if not os.path.exists(target_path) and file_type == "directory":
            os.mkdir(target_path)
        elif file_type == "file":
            source_path = target_path.replace(os.path.join(install_dir,"mini_maya"),maya_dir)
            shutil.copy(source_path,os.path.dirname(target_path))
            if shell:
                print(source_path," -> ",target_path)
            
        for child in data.get("children",[]):
            dict_to_path(child,target_path)
            
    maya_dir = maya_dir.replace("\\","/")
    install_dir = install_dir.replace("\\","/")
    dict_to_path(dir_tree,install_dir)

def TK_GUI():
    try:
        from tkinter import filedialog,messagebox
    except ImportError:
        import tkFileDialog as filedialog
        import tkMessageBox as messagebox
    
    def getDirectory(e): 
        path = filedialog.askdirectory()
        e.delete(0,END)
        e.insert(0,path)

    def install(master_window,maya_dir,install_dir):
        maya_dir = maya_dir.get()
        install_dir = install_dir.get()
        try:
            installMiniMaya(maya_dir,install_dir)
        except:
            import traceback
            messagebox.showerror("Error", traceback.format_exc())
        else:
            messagebox.showinfo("Congradulation", "Installation Complete")
            master_window.destroy()


    master_window = Tk()
    master_window.winfo_toplevel().title("Mini Maya Installer")

    # Parent widget for the buttons
    group = Frame(master_window)
    group.grid(row=0, column=0, columnspan=3, sticky=E+W)    

    Label(group, text='Maya Installation Path').grid(row=0) 
    Label(group, text='Mini Maya Installation Path').grid(row=1) 

    e1 = Entry(group,text='',width=50) 
    e1.insert(0,MAYA_DIR if os.path.exists(MAYA_DIR) else '')
    e2 = Entry(group,width=50) 
    e2.insert(0,os.path.realpath(os.path.dirname(__file__)))
    e1.grid(row=0, column=1,sticky=E+W) 
    e2.grid(row=1, column=1,sticky=E+W) 

    btn_1 = Button(group,text = "Browse",command=lambda: getDirectory(e1)) 
    btn_2 = Button(group,text = "Browse",command=lambda: getDirectory(e2)) 
    btn_1.grid(row=0, column=2, padx=10) 
    btn_2.grid(row=1, column=2, padx=10) 
    
    # Group1 Frame ----------------------------------------------------
    group1 = Frame(master_window)
    group1.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky=E+W)

    btn_3 = Button(group1,text = "Install",width=80,command=lambda: install(master_window,e1,e2)) 
    btn_3.pack(padx=10, pady=10,side="top",expand=1,fill="x") 

    master_window.columnconfigure(0, weight=1)
    master_window.rowconfigure(1, weight=1)
    
    # group.rowconfigure(0, weight=1)
    group.columnconfigure(1, weight=1)
    # group1.rowconfigure(0, weight=1)
    group1.columnconfigure(1, weight=1)

    mainloop()

def Qt_GUI():
    app = QApplication(sys.argv)

    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)


    def getDirectory(line): 
        path = QFileDialog.getExistingDirectory(QApplication.activeWindow())
        line.setText(path)

    def install(window,maya_dir,install_dir):
        maya_dir = maya_dir.text()
        install_dir = install_dir.text()
        try:
            installMiniMaya(maya_dir,install_dir)
        except:
            import traceback
            QMessageBox.critical(window,"Error", traceback.format_exc())
        else:
            QMessageBox.information(window,"Congradulation", "Installation Complete")
            window.close()

    layout1 = QHBoxLayout()
    label_1 = QLabel("Maya Installation Path")
    label_1.setMinimumWidth(170)
    line_1 = QLineEdit()
    line_1.setText(MAYA_DIR if os.path.exists(MAYA_DIR) else '')
    btn_1 = QPushButton("Browse")
    btn_1.clicked.connect(lambda:getDirectory(line_1))

    layout1.addWidget(label_1)
    layout1.addWidget(line_1)
    layout1.addWidget(btn_1)

    layout2 = QHBoxLayout()
    label_2 = QLabel("Mini Maya Installation Path")
    label_2.setMinimumWidth(170)
    line_2 = QLineEdit()
    line_2.setText(os.path.realpath(os.path.dirname(__file__)))
    btn_2 = QPushButton("Browse")
    btn_2.clicked.connect(lambda:getDirectory(line_2))

    layout2.addWidget(label_2)
    layout2.addWidget(line_2)
    layout2.addWidget(btn_2)

    btn_3 = QPushButton("Install")
    btn_3.clicked.connect(lambda: install(window,line_1,line_2))
    layout.addLayout(layout1)
    layout.addLayout(layout2)
    layout.addWidget(btn_3)


    window.show()
    app.exec_()

def main():
    
    if TK:
        TK_GUI()
    elif Qt:
        Qt_GUI()
    else:
        print("Run On Command Line mode")
        installMiniMaya(next(iter(sys.argv[1:]),None),next(iter(sys.argv[2:]),None),shell=True)
        print("Installation Complete")

if __name__ == "__main__":
    main()
