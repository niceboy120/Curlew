#-*- coding:utf-8 -*-

from gi.repository import Gtk
from os.path import join


class SpinsFrame(Gtk.Frame):
    '''4 SpinButton collection'''
    def __init__(self, title):
        Gtk.Frame.__init__(self)
        
        self._top = 0
        self._buttom = 0
        self._left = 0
        self._right = 0
        self._sum = 0
        
        hbox = Gtk.HBox(sensitive=False, spacing=2, border_width=4)
        self.add(hbox)
        
        self.check_btn = Gtk.CheckButton(title)
        self.set_label_widget(self.check_btn)
        
        # Adjustments
        adj_top    = Gtk.Adjustment(0, 0, 10000, 1)
        adj_buttom = Gtk.Adjustment(0, 0, 10000, 1)
        adj_left   = Gtk.Adjustment(0, 0, 10000, 1)
        adj_right  = Gtk.Adjustment(0, 0, 10000, 1)
        
        # Top spin
        self.spin_top = Gtk.SpinButton(adjustment=adj_top)
        self.spin_top.set_numeric(True)
        hbox.pack_start(Gtk.Label(_('Top')), False, False, 0)
        hbox.pack_start(self.spin_top, False, False, 0)
        
        hbox.pack_start(Gtk.VSeparator(), False, False, 8)
        
        # Buttom spin
        self.spin_buttom = Gtk.SpinButton(adjustment=adj_buttom)
        self.spin_buttom.set_numeric(True)
        hbox.pack_start(Gtk.Label(_('Button')), False, False, 0)
        hbox.pack_start(self.spin_buttom, False, False, 0)
        
        hbox.pack_start(Gtk.VSeparator(), False, False, 8)
        
        # Left Spin
        self.spin_left = Gtk.SpinButton(adjustment=adj_left)
        self.spin_left.set_numeric(True)
        hbox.pack_start(Gtk.Label(_('Left')), False, False, 0)
        hbox.pack_start(self.spin_left, False, False, 0)
        
        hbox.pack_start(Gtk.VSeparator(), False, False, 8)
        
        # Right spin
        self.spin_right = Gtk.SpinButton(adjustment=adj_right)
        self.spin_right.set_numeric(True)
        hbox.pack_start(Gtk.Label(_('Right')), False, False, 0)
        hbox.pack_start(self.spin_right, False, False, 0)
        
        
        # Connection
        self.spin_top.connect('value-changed', self._on_spins_changed)
        self.spin_buttom.connect('value-changed', self._on_spins_changed)
        self.spin_left.connect('value-changed', self._on_spins_changed)
        self.spin_right.connect('value-changed', self._on_spins_changed)
        self.check_btn.connect('toggled', self._on_check_cb, hbox)
    
    def _on_check_cb(self, check_btn, hbox):
        hbox.set_sensitive(check_btn.get_active())
    
    def _on_spins_changed(self, spin):
        self._top = self.spin_top.get_value_as_int()
        self._buttom = self.spin_buttom.get_value_as_int()
        self._left = self.spin_left.get_value_as_int()
        self._right = self.spin_right.get_value_as_int()
        
        self._sum = self._top + self._buttom + self._left + self._right
    
    def get_active(self):
        return self.check_btn.get_active() and self._sum != 0
    
    def get_crop(self):
        return 'crop=iw-{}:ih-{}:{}:{}'.format(self._left+self._right,
                                               self._top+self._buttom,
                                               self._left, self._top)
    
    def get_pad(self):
        return 'pad=iw+{}:ih+{}:{}:{}'.format(self._left+self._right,
                                               self._top+self._buttom,
                                               self._left, self._top)
    
    
class CustomToolButton(Gtk.ToolButton):
    def __init__(self, name, label, tooltip, callback, toolbar):
        
        Gtk.ToolButton.__init__(self)
        self._name = name + '.png'
        self.set_tooltip_markup(tooltip)
        self.set_label(label)
        self.connect('clicked', callback)
        toolbar.insert(self, -1)
    
    def set_icon(self, path):
        image_path = join(path, self._name)
        image = Gtk.Image.new_from_file(image_path)
        self.set_icon_widget(image)
        
        
class CustomHScale(Gtk.HScale):
    def __init__(self, container, def_value, min_value, max_value, step=1):
        Gtk.HScale.__init__(self)
        container.add(self)
        adj = Gtk.Adjustment(def_value, min_value, max_value, step)
        self.set_adjustment(adj)
        self.set_value_pos(Gtk.PositionType.RIGHT)
        self.set_digits(0)
        

class LabeledHBox(Gtk.HBox):
    def __init__(self, label, container=None, width_chars=11):
        ''' hbox with label'''
        Gtk.HBox.__init__(self, spacing=4)
        _label = Gtk.Label(label, use_markup=True)
        _label.set_alignment(0, 0.5)
        _label.set_width_chars(width_chars)
        self.pack_start(_label, False, False, 0)
        if container != None:
            container.pack_start(self, False, False, 0)


class TimeLayout(Gtk.HBox):
    def __init__(self, container, label):
        '''    Time widget    '''
        Gtk.HBox.__init__(self)
        self._spin_h = Gtk.SpinButton().new_with_range(0, 5, 1)
        self._spin_m = Gtk.SpinButton().new_with_range(0, 59, 1)
        self._spin_s = Gtk.SpinButton().new_with_range(0, 59, 1)
        
        _label = Gtk.Label(label, use_markup=True)
        _label.set_alignment(0, 0.5)
        _label.set_width_chars(10)
        
        self.pack_start(_label, False, False, 0)
        
        self.pack_start(self._spin_h, False, False, 3)
        self.pack_start(Gtk.Label(label=_('hr')), False, False, 0)
        
        self.pack_start(Gtk.Label(6*' '), False, False, 0)
        
        self.pack_start(self._spin_m, False, False, 3)
        self.pack_start(Gtk.Label(label=_('min')), False, False, 0)
        
        self.pack_start(Gtk.Label(6*' '), False, False, 0)
        
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
    def __init__(self, Container, label, with_entry=True):
        Gtk.ComboBoxText.__init__(self, has_entry=with_entry)
        self.connect('changed', self._on_combo_changed)
        hbox = Gtk.HBox()
        hbox.set_spacing(4)
        self._label = Gtk.Label(label, use_markup=True)
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
    
    def set_text(self, text):
        ''' Set text to Entry '''
        entry = self.get_child()
        entry.set_text(text)
    
    def _on_combo_changed(self, *args):
        enabled = self.get_text() == 'default' and len(self.get_model()) < 2
        self.set_sensitive(not enabled)
    
    def set_label_width(self, charwidth):
        self._label.set_width_chars(charwidth)
    
    def not_default(self):
        return self.get_active_text() != 'default'











            
            
