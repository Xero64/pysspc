from math import pi, cos, sin, atan, degrees, atan2, radians
from matplotlib.pyplot import figure
from matplotlib.patches import Rectangle
from py2md.classes import MDHeading, MDTable
from .. import config

class ThinWalledSection(object):
    y = None
    z = None
    t = None
    label: str = None
    segs = None
    _A = None
    _Ay = None
    _Az = None
    _cy = None
    _cz = None
    _Ayy = None
    _Azz = None
    _Ayz = None
    _Iyy = None
    _Izz = None
    _Iyz = None
    _θp = None
    _Iyp = None
    _Izp = None
    def __init__(self, y: list, z: list, t: list, label: str=None):
        lent = len(t)
        leny = len(y)
        lenz = len(z)
        if leny != lenz:
            print('The length of y does not equal the length of z.')
            return
        if lent != leny and lent != leny-1:
            print('The length of thickness is not consistant with the geometry.')
            return
        self.y = y
        self.z = z
        self.t = t
        self.label = label
        self.generate_segments()
    def check_area(self, display=True):
        self._A = None
        if self.A < 0.0:
            if display:
                print('Reversed coordinates.')
            self.y.reverse()
            self.z.reverse()
            self.t.reverse()
            self.generate_segments()
        self._A = None
    def generate_segments(self):
        lent = len(self.t)
        lenp = len(self.y)
        self.segs = []
        for i in range(lent-1):
            ya = self.y[i]
            za = self.z[i]
            yb = self.y[i+1]
            zb = self.z[i+1]
            ts = self.t[i]
            ws = WallSegment(ya, za, yb, zb, ts)
            self.segs.append(ws)
        if lenp > lent:
            ya = self.y[-2]
            za = self.z[-2]
            yb = self.y[-1]
            zb = self.z[-1]
            ts = self.t[-1]
        else:
            ya = self.y[-1]
            za = self.z[-1]
            yb = self.y[0]
            zb = self.z[0]
            ts = self.t[-1]
        ws = WallSegment(ya, za, yb, zb, ts)
        self.segs.append(ws)
        if lenp != lent:
            self.segs[0].set_free_at_a(True)
            self.segs[-1].set_free_at_b(True)
    def reset(self):
        self._A = None
        self._Ay = None
        self._Az = None
        self._cy = None
        self._cz = None
        self._Ayy = None
        self._Azz = None
        self._Ayz = None
        self._Iyy = None
        self._Izz = None
        self._Iyz = None
        self._θp = None
        self._Iyp = None
        self._Izp = None
        self.check_area(display=False)
    def mirror_y(self):
        z = [-zi for zi in self.z]
        self.z = z
        self.reset()
        self.generate_segments()
        self.check_area(display=False)
    def mirror_z(self):
        y = [-yi for yi in self.y]
        self.y = y
        self.reset()
        self.generate_segments()
        self.check_area(display=False)
    def translate(self, yt: float, zt: float):
        y = [-yi+yt for yi in self.y]
        self.y = y
        z = [-zi+zt for zi in self.z]
        self.z = z
        self.reset()
        self.generate_segments()
        self.check_area(display=False)
    @property
    def A(self):
        if self._A is None:
            self._A = 0.0
            for seg in self.segs:
                self._A += seg.A
        return self._A
    @property
    def Ay(self):
        if self._Ay is None:
            self._Ay = 0.0
            for seg in self.segs:
                self._Ay += seg.Ay
        return self._Ay
    @property
    def Az(self):
        if self._Az is None:
            self._Az = 0.0
            for seg in self.segs:
                self._Az += seg.Az
        return self._Az
    @property
    def cy(self):
        if self._cy is None:
            self._cy = self.Ay/self.A
        return self._cy
    @property
    def cz(self):
        if self._cz is None:
            self._cz = self.Az/self.A
        return self._cz
    @property
    def Ayy(self):
        if self._Ayy is None:
            self._Ayy = 0.0
            for seg in self.segs:
                self._Ayy += seg.Ayy
        return self._Ayy
    @property
    def Azz(self):
        if self._Azz is None:
            self._Azz = 0.0
            for seg in self.segs:
                self._Azz += seg.Azz
        return self._Azz
    @property
    def Ayz(self):
        if self._Ayz is None:
            self._Ayz = 0.0
            for seg in self.segs:
                self._Ayz += seg.Ayz
        return self._Ayz
    @property
    def Iyy(self):
        if self._Iyy is None:
            self._Iyy = self.Azz-self.A*self.cz**2
        return self._Iyy
    @property
    def Izz(self):
        if self._Izz is None:
            self._Izz = self.Ayy-self.A*self.cy**2
        return self._Izz
    @property
    def Iyz(self):
        if self._Iyz is None:
            self._Iyz = self.Ayz-self.A*self.cy*self.cz
        return self._Iyz
    @property
    def θp(self):
        if self._θp is None:
            tol = 1e-12
            if abs(2*self.Iyz) < tol:
                self._θp = 0.0
            elif abs(self.Izz-self.Iyy) < tol:
                self._θp = pi/4
            else:
                self._θp = atan(2*self.Iyz/(self.Izz-self.Iyy))/2
        return self._θp
    @property
    def Iyp(self):
        if self._Iyp is None:
            c = cos(self.θp)
            s = sin(self.θp)
            self._Iyp = self.Iyy*c**2+self.Izz*s**2-2*self.Iyz*c*s
        return self._Iyp
    @property
    def Izp(self):
        if self._Izp is None:
            c = cos(self.θp)
            s = sin(self.θp)
            self._Izp = self.Iyy*s**2+self.Izz*c**2+2*self.Iyz*c*s
        return self._Izp
    def plot(self, ax=None):
        if ax is None:
            fig = figure(figsize=(12, 8))
            ax = fig.gca()
        from matplotlib.collections import PatchCollection
        rects = []
        for seg in self.segs:
            rects.append(seg.mpl_rectangle())
        patchcol = PatchCollection(rects)
        ax.add_collection(patchcol)
        ax.set_aspect('equal')
        miny = min(self.y)
        maxy = max(self.y)
        minz = min(self.z)
        maxz = max(self.z)
        maxt = max(self.t)
        ax.set_xlim(miny-maxt/2, maxy+maxt/2)
        ax.set_ylim(minz-maxt/2, maxz+maxt/2)
        return ax
    def __repr__(self):
        if self.label is None:
            outstr = '<ThinWalledSection>'
        else:
            outstr = f'<ThinWalledSection {self.label:s}>'
        return outstr
    def __str__(self):
        lunit = config.lunit
        l1frm = config.l1frm
        l2frm = config.l2frm
        l3frm = config.l3frm
        l4frm = config.l4frm
        angfrm = config.angfrm
        if self.label is None:
            head = 'Thin-Walled Section Properties'
        else:
            head = f'Thin-Walled Section Properties - {self.label:s}'
        heading = MDHeading(head, 3)
        mdstr = str(heading)
        table = MDTable()
        table.add_column(f'A ({lunit:s}<sup>2</sup>)', l2frm, data=[self.A])
        table.add_column(f'Ay ({lunit:s}<sup>3</sup>)', l3frm, data=[self.Ay])
        table.add_column(f'Az ({lunit:s}<sup>3</sup>)', l3frm, data=[self.Az])
        table.add_column(f'c<sub>y</sub> ({lunit:s})', l1frm, data=[self.cy])
        table.add_column(f'c<sub>z</sub> ({lunit:s})', l1frm, data=[self.cz])
        table.add_column(f'Ayy ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Ayy])
        table.add_column(f'Azz ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Azz])
        table.add_column(f'Ayz ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Ayz])
        mdstr += str(table)
        table = MDTable()
        table.add_column(f'I<sub>yy</sub> ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Iyy])
        table.add_column(f'I<sub>zz</sub> ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Izz])
        table.add_column(f'I<sub>yz</sub> ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Iyz])
        table.add_column('&theta;<sub>p</sub> (&deg;)', angfrm, data=[degrees(self.θp)])
        table.add_column(f'I<sub>yp</sub> ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Iyp])
        table.add_column(f'I<sub>zp</sub> ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Izp])
        mdstr += str(table)
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()

class WallSegment(object):
    ya = None
    za = None
    yb = None
    zb = None
    ts = None
    fa = None
    fb = None
    dy = None
    dz = None
    ls = None
    th = None
    ccc = None
    _A = None
    _Ay = None
    _Az = None
    _cy = None
    _cz = None
    _Ayy = None
    _Azz = None
    _Ayz = None
    _Iyy = None
    _Izz = None
    _Iyz = None
    _θp = None
    _Iyp = None
    _Izp = None
    def __init__(self, ya: float, za: float, yb: float, zb: float, ts: float):
        self.ya = ya
        self.za = za
        self.yb = yb
        self.zb = zb
        self.ts = ts
        self.update()
    def update(self):
        self.fa = False
        self.fb = False
        self.dy = self.yb-self.ya
        self.dz = self.zb-self.za
        self.ls = (self.dy**2+self.dz**2)**0.5
        self.th = degrees(atan2(self.dz, self.dy))
    def set_free_at_a(self, fa):
        self.fa = fa
    def set_free_at_b(self, fb):
        self.fb = fb
    def is_oef(self):
        if self.fa and not self.fb:
            return True
        if not self.fa and self.fb:
            return True
        return False
    def is_nef(self):
        if not self.fa and not self.fb:
            return True
        return False
    @property
    def A(self):
        if self._A is None:
            self._A = self.ts*self.ls
        return self._A
    @property
    def Ay(self):
        if self._Ay is None:
            self._Ay = self.A*(self.yb+self.ya)/2
        return self._Ay
    @property
    def Az(self):
        if self._Az is None:
            self._Az = self.A*(self.zb+self.za)/2
        return self._Az
    @property
    def Ayy(self):
        if self._Ayy is None:
            self._Ayy = self.A*(self.yb**2+self.yb*self.ya+self.ya**2)/3
        return self._Ayy
    @property
    def Azz(self):
        if self._Azz is None:
            self._Azz = self.A*(self.zb**2+self.zb*self.za+self.za**2)/3
        return self._Azz
    @property
    def Ayz(self):
        if self._Ayz is None:
            tmp = (self.zb*self.yb+self.za*self.ya+(self.zb*self.ya+self.za*self.yb)/2)/3
            self._Ayz = self.A*tmp
        return self._Ayz
    def mpl_rectangle(self):
        thrad = radians(self.th)
        yo = self.ya+self.ts/2*sin(thrad)
        zo = self.za-self.ts/2*cos(thrad)
        rect = Rectangle((yo, zo), self.ls, self.ts, self.th)
        return rect
    def __repr__(self):
        return '<WallSegment>'
