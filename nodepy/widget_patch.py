from kivy.properties import NumericProperty, ReferenceListProperty

from kivy.uix.widget import Widget

Widget.pos_hint_x = NumericProperty(0, allownone=True)

Widget.pos_hint_y = NumericProperty(0, allownone=True)

Widget.pos_hint = ReferenceListProperty(Widget.pos_hint_x, Widget.pos_hint_y)