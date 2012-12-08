from gi.repository import Gtk, Pango


class CustomHScale(Gtk.HScale):
    def __init__(self, container, def_value, min_value, max_value, step=1):
        Gtk.HScale.__init__(self)
        container.add(self)
        adj = Gtk.Adjustment(def_value, min_value, max_value, step)
        self.set_adjustment(adj)
        self.set_value_pos(Gtk.PositionType.RIGHT)
        self.set_digits(0)
        

class LabeledHBox(Gtk.HBox):
    def __init__(self, Label, container=None, CWidth=12):
        ''' hbox with label'''
        Gtk.HBox.__init__(self, spacing=4)
        label = Gtk.Label(Label, use_markup=True)
        label.set_alignment(0, 0.5)
        label.set_width_chars(CWidth)
        self.pack_start(label, False, False, 0)
        if container != None:
            container.pack_start(self, False, False, 0)


class TimeLayout(Gtk.HBox):
    def __init__(self, container, Label):
        '''    Time widget    '''
        Gtk.HBox.__init__(self)
        self._spin_h = Gtk.SpinButton().new_with_range(0, 5, 1)
        self._spin_m = Gtk.SpinButton().new_with_range(0, 59, 1)
        self._spin_s = Gtk.SpinButton().new_with_range(0, 59, 1)
        
        label = Gtk.Label(Label, use_markup=True)
        label.set_alignment(0, 0.5)
        label.set_width_chars(10)
        self.pack_start(label, False, False, 0)
        self.pack_start(self._spin_h, False, False, 3)
        self.pack_start(Gtk.Label(label=_('hr')), False, False, 0)
        self.pack_start(self._spin_m, False, False, 3)
        self.pack_start(Gtk.Label(label=_('min')), False, False, 0) 
        self.pack_start(self._spin_s, False, False, 3)
        self.pack_start(Gtk.Label(label=_('sec')), False, False, 0)
        container.pack_start(self, False, False, 0)
    
    def set_duration(self, duration):
        ''' Set duration in seconds '''
        self._spin_h.set_value(duration/3600)
        self._spin_m.set_value((duration%3600)/60)
        self._spin_s.set_value((duration%3600)%60)
    
    def get_duration(self):
        ''' Return duration in sec '''
        return self._spin_h.get_value()*3600 \
                       + self._spin_m.get_value()*60 \
                       + self._spin_s.get_value()
    
    def get_time_str(self):
        ''' Return time str like 00:00:00'''
        return '{:02.0f}:{:02.0f}:{:02.0f}'.format(self._spin_h.get_value(), 
                                                   self._spin_m.get_value(), 
                                                   self._spin_s.get_value())


class LabeledComboEntry(Gtk.ComboBoxText):
    ''' Create custom ComboBoxText with entry'''
    def __init__(self, Container, Label, with_entry=True):
        Gtk.ComboBoxText.__init__(self, has_entry=with_entry)
        self.connect('changed', self.on_combo_changed)
        hbox = Gtk.HBox()
        hbox.set_spacing(4)
        self._label = Gtk.Label(Label, use_markup=True)
        self._label.set_alignment(0, 0.5)
        self._label.set_width_chars(15)
        self.set_entry_text_column(0)
        hbox.pack_start(self._label, False, False, 0)
        hbox.pack_start(self, False, False, 0)
        Container.pack_start(hbox, False, False, 0)
    
    def set_list(self, list_of_elements):
        ''' Fill combobox with list directly [] '''
        self.remove_all()
        map(self.append_text, list_of_elements)
        self.set_active(0)
    
    def get_text(self):
        return self.get_active_text()
    
    def set_text(self, Text):
        ''' Set text to Entry '''
        entry = self.get_child()
        entry.set_text(Text)
    
    def on_combo_changed(self, *args):
        enabled = self.get_text() == 'default' and len(self.get_model()) < 2
        self.set_sensitive(not enabled)
    
    def set_label_width(self, charwidth):
        self._label.set_width_chars(charwidth)
    

class LogDialog(Gtk.Dialog):
    def __init__(self, prnt, log_file):
        Gtk.Dialog.__init__(self, parent=prnt)
        self.set_size_request(550, 450)
        self.set_border_width(6)
        self.set_title(_('Errors detail'))
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        text_log = Gtk.TextView()
        text_log.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        text_log.set_border_width(6)
        text_log.set_editable(False)
        text_log.set_cursor_visible(False)
        
        font_desc = Pango.FontDescription('Monospace')
        text_log.override_font(font_desc)
        
        text_buffer = Gtk.TextBuffer()
        text_log.set_buffer(text_buffer)
        
        scroll.add(text_log)
        self.vbox.pack_start(scroll, True, True, 0)
        
        self.add_button(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)
        
        with open(log_file, 'r') as log:
            text_buffer.set_text(log.read())
    
    def show_dialog(self):
        self.show_all()
        self.run()
        self.destroy()












            
            