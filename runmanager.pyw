#!/usr/bin/env python

import os

import gtk
import pango
import h5py

if os.name == 'nt':
    # Have Windows 7 consider this program to be a separate app, and not
    # group it with other Python programs in the taskbar:
    import ctypes
    myappid = 'monashbec.labscript.runmanager.1-0' # arbitrary string
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

class FileOps:
    
    def new_file(self,filename):
        with h5py.File(filename,'w') as f:
            f.create_group('globals')
    
    def get_grouplist(self,filename):
        with h5py.File(filename,'r') as f:
            try:
                grouplist = f['globals']
                # File closes after this function call, so have to
                # convert the grouplist generator to a list of strings
                # before its file gets dereferenced:
                return list(grouplist), True
            except:
                raise
                return [], False
        
    def new_group(self,filename,groupname):
        pass
    
    def delete_group(self,filename,groupname):
        pass
    
    def get_globals_list(self,filename,groupname):
        pass
    
    def new_global(self,filename,groupname,globalname):
        pass
    
    def get_value(self,filename,groupname,globalname):
        pass
    
    def set_value(self,filename,groupname,globalname):
        pass
    
    def delete_global(self,filenmae,groupname,globalname):
        pass
    
    
class Global(object):
    def __init__(self, table, n_globals):
        
        self.table = table
        self.builder = gtk.Builder()
        self.builder.add_from_file('global.glade')
        
        self.entry_name = self.builder.get_object('entry_name')
        self.entry_units = self.builder.get_object('entry_units')
        self.label_name = self.builder.get_object('label_name')
        self.label_units = self.builder.get_object('label_units')
        self.entry_value = self.builder.get_object('entry_value')
        self.vbox_value = self.builder.get_object('vbox_value')
        self.hbox_buttons = self.builder.get_object('hbox_buttons')
        self.vbox_buttons = self.builder.get_object('vbox_buttons')
        self.toggle_edit = self.builder.get_object('toggle_edit')
        self.button_remove = self.builder.get_object('button_remove')
        self.vbox_name = self.builder.get_object('vbox_name')
        self.vbox_units = self.builder.get_object('vbox_units')
        
        for widget in [self.entry_name,self.label_name,self.entry_value]:
            widget.modify_font(pango.FontDescription("monospace 10"))
        
        self.insert_at_position(n_globals + 1)
        
        self.entry_name.select_region(0, -1)
        self.entry_name.grab_focus()
            
        self.builder.connect_signals(self)
        
    def insert_at_position(self,n):
        self.table.attach(self.vbox_name,0,1,n,n+1)
        self.table.attach(self.vbox_value,1,2,n,n+1)
        self.table.attach(self.vbox_units,2,3,n,n+1)
        self.table.attach(self.vbox_buttons,3,4,n,n+1)
        
        self.vbox_name.show()
        self.vbox_units.show()
        self.vbox_buttons.show()
        self.vbox_value.show()
        
    def on_edit_toggled(self,widget):
        if widget.get_active():
            self.entry_name.show()
            self.entry_units.show()
            self.button_remove.show()
            self.label_name.hide()
            self.label_units.hide()
            self.entry_name.select_region(0, -1)
            self.entry_name.grab_focus()
        else:
            self.entry_name.hide()
            self.entry_units.hide()
            self.button_remove.hide()
            self.label_units.set_text(self.entry_units.get_text())
            self.label_name.set_text(self.entry_name.get_text())
            self.label_name.show()
            self.label_units.show()
    
       
    def on_entry_keypress(self,widget,event):
        widget.set_width_chars(len(widget.get_text()))
        if event.keyval == 65307: #escape
            self.entry_units.set_text(self.label_units.get_text())
            self.entry_name.set_text(self.label_name.get_text())
            self.toggle_edit.set_active(False)
            self.toggle_edit.toggled()
        elif event.keyval == 65293 or event.keyval == 65421: #enter
            self.toggle_edit.set_active(False)
            self.toggle_edit.toggled()
        
    def on_remove_clicked(self,widget):
        # TODO "Are you sure? This will remove the global from the h5
        # file and cannot be undone."
        self.table.remove(self.vbox_name)
        self.table.remove(self.vbox_value)
        self.table.remove(self.vbox_units)
        self.table.remove(self.vbox_buttons)
        del self
        
        
class Group(object):
    
    def __init__(self,name,filepath,notebook,vbox):
        self.name = name
        self.filepath = filepath
        self.notebook = notebook
        self.vbox = vbox
        
        self.builder = gtk.Builder()
        self.builder.add_from_file('grouptab.glade')
        self.toplevel = self.builder.get_object('tab_toplevel')
        self.global_table = self.builder.get_object('global_table')
        self.scrolledwindow_globals = self.builder.get_object('scrolledwindow_globals')
        self.label_groupname = self.builder.get_object('label_groupname')
        self.entry_groupname = self.builder.get_object('entry_groupname')
        self.label_h5_path = self.builder.get_object('label_h5_path')
        self.toggle_group_name_edit = self.builder.get_object('toggle_group_name_edit')
        self.adjustment = self.scrolledwindow_globals.get_vadjustment()
        self.tab = gtk.HBox()
        
        #get a stock close button image
        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        image_w, image_h = gtk.icon_size_lookup(gtk.ICON_SIZE_MENU)
        
        #make the close button
        btn = gtk.Button()
        btn.set_relief(gtk.RELIEF_NONE)
        btn.set_focus_on_click(False)
        btn.add(close_image)
        
        #this reduces the size of the button
        style = gtk.RcStyle()
        style.xthickness = 0
        style.ythickness = 0
        btn.modify_style(style)
        
        self.tablabel = gtk.Label(self.name)
        self.tablabel.set_ellipsize(pango.ELLIPSIZE_END)
        self.tablabel.set_tooltip_text(self.name)
        self.tab.pack_start(self.tablabel)
        self.tab.pack_start(btn, False, False)
        self.tab.show_all()
        notebook.append_page(self.toplevel, tab_label = self.tab)
                     
        self.checkbox = gtk.CheckButton(self.name)
        self.vbox.pack_start(self.checkbox,expand=False,fill=False)
        self.vbox.show_all()
        notebook.set_tab_reorderable(self.toplevel,True)
        
        self.label_groupname.set_text(self.name)
        self.entry_groupname.set_text(self.name)
        self.label_h5_path.set_text(self.filepath)
        
        notebook.show()

        #connect the close button
        btn.connect('clicked', self.on_closetab_button_clicked)

        self.builder.connect_signals(self)
        
        self.globals = []
        
    def on_closetab_button_clicked(self, *args):
        #get the page number of the tab we wanted to close
        pagenum = self.notebook.page_num(self.toplevel)
        #and close it
        self.notebook.remove_page(pagenum)
        self.checkbox.destroy()
    
    def changename(self, newname):
        self.name = newname
        self.label_groupname.set_text(self.name)
        self.tablabel.set_text(self.name)
        self.checkbox.get_children()[0].set_text(self.name) 
              
    def on_groupname_edit_toggle(self,widget):
        if widget.get_active():
            self.entry_groupname.set_text(self.name)
            self.entry_groupname.show()
            self.label_groupname.hide()
            self.entry_groupname.select_region(0, -1)
            self.entry_groupname.grab_focus()
        else:
            self.changename(self.entry_groupname.get_text())
            self.entry_groupname.hide()
            self.label_groupname.show() 
            
    def on_entry_keypress(self,widget,event):
        if event.keyval == 65307: #escape
            widget.set_text(self.label_groupname.get_text())
            self.toggle_group_name_edit.set_active(False)
            self.toggle_group_name_edit.toggled()
        elif event.keyval == 65293 or event.keyval == 65421: #enter
            self.toggle_group_name_edit.set_active(False)
            self.toggle_group_name_edit.toggled()
        
    def on_new_global_clicked(self,button):
        self.globals.append(Global(self.global_table, len(self.globals)))  
        self.adjustment.value = self.adjustment.upper     
        
class RunManager(object):
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file('interface.glade')
        
        self.window = self.builder.get_object('window1')
        self.notebook = self.builder.get_object('notebook1')
        self.output_view = self.builder.get_object('textview1')
        self.output_buffer = self.output_view.get_buffer()
        self.use_globals_vbox = self.builder.get_object('use_globals_vbox')
        self.grouplist_vbox = self.builder.get_object('grouplist_vbox')
        self.no_file_opened = self.builder.get_object('label_no_file_opened')
        self.chooser_h5_file = self.builder.get_object('chooser_h5_file')
        self.window.show_all()
        
        area=self.builder.get_object('drawingarea1')
        pixbuf=gtk.gdk.pixbuf_new_from_file(os.path.join('assets','grey.png'))
        pixmap, mask=pixbuf.render_pixmap_and_mask()
        area.window.set_back_pixmap(pixmap, False)
        self.output_view.modify_font(pango.FontDescription("monospace 10"))
        self.window.set_icon_from_file(os.path.join('assets','icon.png'))
        self.builder.get_object('filefilter1').add_pattern('*.h5')
        self.builder.get_object('filefilter2').add_pattern('*.py')
        self.grouplist_vbox.hide()
        
        self.builder.connect_signals(self)
        
        self.groups = []
    
    def output(self,text):
        """Prints text to the output textbox"""
        print text,
        self.output_buffer.insert_at_cursor(text)
        # Automatically keep the textbox scrolled to the bottom:
        self.output_view.scroll_to_mark(app.output_buffer.get_insert(),0)
        # Make sure that GTK renders the text right away, without waiting
        # for callbacks to finish:
        while gtk.events_pending():
            gtk.main_iteration()
            
    def run(self):
        self.output('ready\n')
        gtk.main()
            
    def button_create_new_group(self,*args):
        entry_name = self.builder.get_object('entry_tabname')
        name = entry_name.get_text()
        filepath = self.chooser_h5_file.get_filenames()[0]
        self.groups.append(Group(name,filepath,self.notebook,self.use_globals_vbox))
        entry_name.set_text('')
    
    def on_file_chosen(self,chooser):
        self.grouplist_vbox.show()
        self.no_file_opened.hide()
        filename = self.chooser_h5_file.get_filenames()[0]
        grouplist, success = file_ops.get_grouplist(filename) 
        if success:
            for group in grouplist:
                print group
                #TODO: populate vbox with groups
        else:
            chooser.set_current_folder('')
            self.on_selection_changed(chooser)           
        
    def on_selection_changed(self,chooser):
        """This is just to detect when the h5 file chooser comes back
        without a file so we can put the 'no file open' label back'"""
        if not self.chooser_h5_file.get_filenames():
            self.grouplist_vbox.hide()
            #TODO: remove existing entries from vbox
            self.no_file_opened.show()
              
    def do_it(self,*args):
        self.output('do it\n')
 
if __name__ == '__main__':        
    app = RunManager()
    file_ops = FileOps()
    app.run()