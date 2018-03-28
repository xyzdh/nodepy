from kivy.input.motionevent import MotionEvent
'''打个补丁 使 touch_pos 以 左上角 为 坐标原点
'''
def scale_for_screen(self, w, h, p=None, rotation=0,smode='None', kheight=0):
    '''Scale position for the screen
    '''
    sx, sy = self.sx, 1 - self.sy #Patch in this
    if rotation == 0:
        self.x = sx * float(w)
        self.y = sy * float(h)
    elif rotation == 90:
        sx, sy = sy, 1 - sx
        self.x = sx * float(h)
        self.y = sy * float(w)
    elif rotation == 180:
        sx, sy = 1 - sx, 1 - sy
        self.x = sx * float(w)
        self.y = sy * float(h)
    elif rotation == 270:
        sx, sy = 1 - sy, sx
        self.x = sx * float(h)
        self.y = sy * float(w)

    if p:
        self.z = self.sz * float(p)

    if smode:
        if smode == 'pan':
            self.y -= kheight
        elif smode == 'scale':
            self.y += (kheight * (
                (self.y - kheight) / (h - kheight))) - kheight

    if self.ox is None:
        self.px = self.ox = self.x
        self.py = self.oy = self.y
        self.pz = self.oz = self.z

    self.dx = self.x - self.px
    self.dy = self.y - self.py
    self.dz = self.z - self.pz

    # cache position
    self.pos = self.x, self.y

MotionEvent.scale_for_screen = scale_for_screen
