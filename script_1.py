
UB = "eyJ0aXRsZSI6ICLri6jslrQg6rOE64uoIO2AtOymiCIsICJoaW50IjogIu2VnOq1reyWtCDrnLsgLT4g7JiB7Ja0IOuLqOyWtCDsnoXroKU6IiwgInBsYWNlaG9sZGVyIjogIuyYgeyWtCDri6jslrTrpbwg7J6F66Cl7ZWY7IS47JqULi4uIiwgImJ0bl9jaGVjayI6ICLsoJXri7Ug7ZmV7J24IiwgImJ0bl9uZXh0IjogIuuLpOydjCDrrLjsoJwiLCAiYnRuX3JldHJ5IjogIuyymOydjOu2gO2EsCDri6Tsi5wiLCAiY29ycmVjdCI6ICLsoJXri7UhICAtPiAgIiwgIndyb25nIjogIuyYpOuLtSEgIOygleuLtTogIiwgImVtcHR5IjogIuuovOyggCDri6jslrTrpbwg7J6F66Cl7ZWY7IS47JqUISIsICJzdGFpciI6ICLtmITsnqwg6rOE64uoOiAiLCAic2NvcmUiOiAiICB8ICDsoJXri7U6ICIsICJxX2xhYmVsIjogIuusuOygnCAgIiwgIndpbl90aXRsZSI6ICLstpXtlZjtlanri4jri6QhIiwgIndpbl9tc2ciOiAi67O066y87J2EIOyGkOyXkCDrhKPsl4jsirXri4jri6QhXG7rqqjrk6Ag6rOE64uo7J2EIOyYrOudvCDrs7TrrLzsnYQg7ZqN65Od7ZaI7Ja07JqUIVxu7LWc7KKFIOygleuLtTogIiwgImVuZF90aXRsZSI6ICLqsozsnoQg7KKF66OMIiwgImVuZF9tc2ciOiAi7JWE7Im96rKM64+EIOuztOusvOyXkCDri7/sp4Ag66q77ZaI7Ja07JqULlxu7KCV64u1OiAiLCAiZW5kX21zZzIiOiAiIOusuOygnFxu64uk7IucIOuPhOyghO2VtCDrs7TshLjsmpQhIiwgInNsaWRlIjogIuuvuOuBhOufrOynkCEgIOygleuLtTogIiwgImZpbGVfZXJyIjogInZvY2FiLmpzb24g7YyM7J287J2EIOywvuydhCDsiJgg7JeG7Iq164uI64ukLlxu6rCZ7J2AIO2PtOuNlOyXkCB2b2NhYi5qc29uIOydhCDrhKPslrTso7zshLjsmpQuIiwgImZpbGVfZXJyMiI6ICJ2b2NhYi5qc29uIOydveq4sCDsmKTrpZg6ICIsICJyZXRyeV9jb25maXJtIjogIuyymOydjOu2gO2EsCDri6Tsi5wg7Iuc7J6R7ZWg6rmM7JqUPyIsICJyZXRyeV90aXRsZSI6ICLsnqzsi5zsnpEifQ=="

py = r"""# -*- coding: ascii -*-
# vocab_stairs.py  --  requires vocab.json in the same folder
import sys, os, random, base64, json, math
from dataclasses import dataclass
from PyQt5.QtCore    import Qt, QPropertyAnimation, pyqtProperty, QEasingCurve, QTimer, QRect, QPoint
from PyQt5.QtGui     import (QPainter, QColor, QLinearGradient, QPen,
                              QFont, QRadialGradient, QBrush, QPolygon)
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QLineEdit, QPushButton, QFrame,
                              QDialog, QSizePolicy, QMessageBox)

_UB = "UBPLACEHOLDER"
_ui = json.loads(base64.b64decode(_UB).decode("utf-8"))
STEP_SIZE = 1

@dataclass
class VocabItem:
    word: str
    meaning: str

def load_vocab():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocab.json")
    if not os.path.exists(path):
        QMessageBox.critical(None, "Error", _ui["file_err"]); sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [VocabItem(d["word"], d["meaning"]) for d in json.load(f)]
    except Exception as e:
        QMessageBox.critical(None, "Error", _ui["file_err2"] + str(e)); sys.exit(1)


class CelebrationDialog(QDialog):
    def __init__(self, score, total, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(480, 360)
        self._t, self._score, self._total = 0, score, total
        self._conf = [(random.randint(10,460), random.uniform(-20,340),
                       random.uniform(0.5,2.5), random.uniform(-1,1),
                       random.choice(["#FFD700","#FF6B6B","#6BFFB8","#6BB8FF","#FF6BFF","#FFAA00"]),
                       random.choice([4,6,8])) for _ in range(40)]
        t = QTimer(self); t.timeout.connect(self._tick); t.start(25)
        btn = QPushButton("  OK  ", self)
        btn.setStyleSheet("QPushButton{background:#f39c12;color:white;font-size:17px;"
                          "font-weight:bold;padding:10px 44px;border-radius:10px;"
                          "border:2px solid #e67e22;}QPushButton:hover{background:#e67e22;}")
        btn.move(186,306); btn.clicked.connect(self.accept)

    def _tick(self):
        self._t += 1
        for i,(x,y,sp,dx,col,sz) in enumerate(self._conf):
            self._conf[i] = (max(0,min(478,x+dx*math.sin(self._t*0.05+i))),
                             (y+sp)%380, sp, dx, col, sz)
        self.update()

    def paintEvent(self, _):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        W,H = self.width(), self.height()
        g = QLinearGradient(0,0,0,H)
        g.setColorAt(0,QColor(25,25,80,240)); g.setColorAt(1,QColor(5,5,30,240))
        p.setBrush(QBrush(g)); p.setPen(QPen(QColor(255,215,0),3))
        p.drawRoundedRect(2,2,W-4,H-4,20,20)
        for (x,y,_s,_d,col,sz) in self._conf:
            p.setPen(Qt.NoPen); p.setBrush(QColor(col))
            p.drawRoundedRect(int(x),int(y),sz,sz,2,2)
        cx=W//2; p.setPen(Qt.NoPen)
        gw=QRadialGradient(cx,90,60)
        gw.setColorAt(0,QColor(255,215,0,120)); gw.setColorAt(1,QColor(255,215,0,0))
        p.setBrush(QBrush(gw)); p.drawEllipse(cx-55,25,110,110)
        p.setBrush(QColor(255,215,0)); p.drawRoundedRect(cx-32,30,64,54,12,12)
        p.setBrush(QColor(255,255,200,140)); p.drawEllipse(cx-22,36,18,26)
        p.setBrush(QColor(220,180,0))
        p.drawRoundedRect(cx-48,40,18,28,8,8); p.drawRoundedRect(cx+30,40,18,28,8,8)
        p.setBrush(QColor(200,165,0))
        p.drawRect(cx-9,84,18,22); p.drawRoundedRect(cx-22,104,44,12,5,5)
        p.setBrush(QColor(255,230,0))
        for a in range(0,360,60):
            r=math.radians(a+self._t*2)
            p.drawEllipse(int(cx+52*math.cos(r))-5,int(78+30*math.sin(r))-5,10,10)
        p.setPen(QColor(255,215,0)); p.setFont(QFont("Arial",22,QFont.Bold))
        p.drawText(QRect(0,122,W,38),Qt.AlignCenter,_ui["win_title"])
        p.setPen(QColor(210,240,255)); p.setFont(QFont("Arial",12))
        p.drawText(QRect(24,162,W-48,90),Qt.AlignCenter|Qt.TextWordWrap,
                   _ui["win_msg"]+str(self._score)+" / "+str(self._total))


class StairCanvas(QWidget):
    def __init__(self, n, parent=None):
        super().__init__(parent)
        self.total_steps=n; self._sp=0.0; self.setMinimumSize(310,520)

    def get_sp(self): return self._sp
    def set_sp(self, v):
        self._sp=max(0.0,min(float(self.total_steps),v)); self.update()
    stairPos = pyqtProperty(float, fget=get_sp, fset=set_sp)

    def _bear(self, p, hx, hy):
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(0,0,0,30));   p.drawEllipse(hx-18,hy+12,38,10)
        p.setBrush(QColor(90,55,20))
        p.drawEllipse(hx-16,hy+2,18,12); p.drawEllipse(hx,hy+2,18,12)
        p.setBrush(QColor(60,30,10))
        for ox in [-13,-8,-3,3,8,13]: p.drawEllipse(hx+ox,hy+10,4,4)
        p.setBrush(QColor(165,100,40))
        p.drawRoundedRect(hx-14,hy-8,13,14,5,5); p.drawRoundedRect(hx+3,hy-8,13,14,5,5)
        p.setBrush(QColor(195,125,50)); p.drawEllipse(hx-22,hy-42,46,46)
        p.setBrush(QColor(235,195,140)); p.drawEllipse(hx-13,hy-34,28,28)
        p.setBrush(QColor(185,115,45))
        p.drawRoundedRect(hx-34,hy-38,14,22,7,7); p.drawRoundedRect(hx+22,hy-38,14,22,7,7)
        p.setBrush(QColor(155,90,30))
        p.drawEllipse(hx-37,hy-20,16,14); p.drawEllipse(hx+23,hy-20,16,14)
        p.setBrush(QColor(110,60,20))
        for ox2,oy2 in [(-35,-14),(-30,-12),(-25,-14),(25,-14),(30,-12),(35,-14)]:
            p.drawEllipse(hx+ox2,hy+oy2,4,4)
        p.setBrush(QColor(185,115,45)); p.drawEllipse(hx-8,hy-47,18,12)
        p.setBrush(QColor(170,100,35)); p.drawEllipse(hx-24,hy-88,50,50)
        p.setBrush(QColor(210,140,55)); p.drawEllipse(hx-23,hy-87,48,48)
        p.setBrush(QColor(240,200,140)); p.drawEllipse(hx-15,hy-78,32,30)
        p.setBrush(QColor(195,120,45))
        p.drawEllipse(hx-26,hy-96,22,22); p.drawEllipse(hx+6,hy-96,22,22)
        p.setBrush(QColor(230,155,130))
        p.drawEllipse(hx-22,hy-92,14,14); p.drawEllipse(hx+10,hy-92,14,14)
        p.setBrush(QColor(245,175,155,180))
        p.drawEllipse(hx-19,hy-89,8,8); p.drawEllipse(hx+13,hy-89,8,8)
        p.setPen(QPen(QColor(60,30,10),1)); p.setBrush(QColor(255,255,255))
        p.drawEllipse(hx-17,hy-77,14,15); p.drawEllipse(hx+5,hy-77,14,15)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(50,25,8))
        p.drawEllipse(hx-15,hy-76,10,12); p.drawEllipse(hx+7,hy-76,10,12)
        p.setBrush(QColor(8,4,2))
        p.drawEllipse(hx-14,hy-75,8,10); p.drawEllipse(hx+8,hy-75,8,10)
        p.setBrush(QColor(255,255,255))
        p.drawEllipse(hx-13,hy-74,5,5); p.drawEllipse(hx+9,hy-74,5,5)
        p.drawEllipse(hx-11,hy-69,2,2); p.drawEllipse(hx+11,hy-69,2,2)
        p.setPen(QPen(QColor(40,18,5),2))
        p.drawLine(hx-17,hy-77,hx-19,hy-81); p.drawLine(hx-12,hy-78,hx-12,hy-83)
        p.drawLine(hx-7,hy-77,hx-6,hy-81);   p.drawLine(hx+5,hy-77,hx+4,hy-81)
        p.drawLine(hx+11,hy-78,hx+11,hy-83); p.drawLine(hx+17,hy-77,hx+18,hy-81)
        p.setPen(QPen(QColor(80,40,12),3)); p.setBrush(Qt.NoBrush)
        p.drawArc(hx-18,hy-84,16,10,20*16,140*16); p.drawArc(hx+4,hy-84,16,10,20*16,140*16)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(255,130,110,75))
        p.drawEllipse(hx-20,hy-65,14,10); p.drawEllipse(hx+8,hy-65,14,10)
        p.setBrush(QColor(225,175,110)); p.drawEllipse(hx-10,hy-65,22,16)
        p.setBrush(QColor(20,10,5));     p.drawEllipse(hx-6,hy-63,14,9)
        p.setBrush(QColor(255,255,255,200)); p.drawEllipse(hx-4,hy-62,5,4)
        p.setPen(QPen(QColor(100,50,15),2)); p.setBrush(Qt.NoBrush)
        p.drawLine(hx+1,hy-54,hx+1,hy-50)
        p.drawArc(hx-8,hy-52,10,8,180*16,180*16); p.drawArc(hx+1,hy-52,10,8,0,-180*16)
        p.setPen(Qt.NoPen); p.setBrush(QColor(255,80,120))
        p.drawPolygon(QPolygon([QPoint(hx-14,hy-44),QPoint(hx-4,hy-41),QPoint(hx-14,hy-38)]))
        p.drawPolygon(QPolygon([QPoint(hx+16,hy-44),QPoint(hx+6,hy-41),QPoint(hx+16,hy-38)]))
        p.setBrush(QColor(255,120,160)); p.drawEllipse(hx-3,hy-44,8,8)
        p.setBrush(QColor(230,170,30));  p.drawRoundedRect(hx-44,hy-28,14,16,4,4)
        p.setBrush(QColor(200,140,20));  p.drawRoundedRect(hx-46,hy-30,18,6,3,3)
        p.setBrush(QColor(255,200,0,200)); p.drawEllipse(hx-40,hy-14,6,6)

    def paintEvent(self, _):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        W,H = self.width(), self.height()
        g=QLinearGradient(0,0,0,H)
        g.setColorAt(0,QColor(120,195,255)); g.setColorAt(0.6,QColor(200,235,255))
        g.setColorAt(1,QColor(230,248,210)); p.fillRect(0,0,W,H,g)
        p.setPen(Qt.NoPen)
        for cx,cy,pts in [(70,38,[(0,0,32,22),(-20,9,24,18),(22,7,24,18),(-8,14,20,14),(12,14,20,14)]),
                          (W-90,52,[(0,0,26,18),(-16,8,20,15),(18,6,20,15)])]:
            p.setBrush(QColor(255,255,255,210))
            for dx,dy,cw,ch in pts: p.drawEllipse(cx+dx-cw//2,cy+dy-ch//2,cw,ch)
        p.setBrush(QColor(255,230,60,200)); p.drawEllipse(W-52,12,36,36)
        p.setBrush(QColor(255,220,40,120))
        for a in range(0,360,45):
            r=math.radians(a)
            p.drawEllipse(int((W-34)+26*math.cos(r))-4,int(30+26*math.sin(r))-4,8,8)
        sw=W*0.70; sh=(H-95)/self.total_steps; lx=(W-sw)/2
        for i in range(self.total_steps):
            ty=H-55-(i+1)*sh; done=i<int(self._sp)
            bc,ec = (QColor(110,215,110),QColor(75,170,75)) if done else \
                    ((QColor(218,208,198),QColor(172,158,142)) if i%2==0 else
                     (QColor(198,188,178),QColor(155,142,128)))
            p.setBrush(bc); p.setPen(Qt.NoPen)
            p.drawRect(int(lx),int(ty),int(sw),int(sh))
            p.setBrush(QColor(255,255,255,55)); p.drawRect(int(lx),int(ty),int(sw),3)
            p.setBrush(ec); p.drawRect(int(lx),int(ty+sh-3),int(sw),3)
            p.setPen(QPen(QColor(140,125,108),1)); p.setBrush(Qt.NoBrush)
            p.drawRect(int(lx),int(ty),int(sw),int(sh))
            if sh>=9:
                p.setPen(QColor(90,72,55,170))
                p.setFont(QFont("Arial",max(5,int(sh*0.5))))
                p.drawText(int(lx+4),int(ty+sh-2),str(i+1))
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(130,210,85)); p.drawRect(0,H-55,W,55)
        p.setBrush(QColor(100,175,60)); p.drawRect(0,H-52,W,6)
        for fx in range(20,W,45):
            p.setBrush(QColor(255,255,255))
            for fa in range(0,360,72):
                fr=math.radians(fa)
                p.drawEllipse(int(fx+6*math.cos(fr))-3,int(H-48+4*math.sin(fr))-3,6,6)
            p.setBrush(QColor(255,220,0)); p.drawEllipse(fx-3,H-51,7,7)
        tx=int(lx+sw*0.60); ty2=int(H-55-self.total_steps*sh-60)
        gw=QRadialGradient(tx+26,ty2+26,46)
        gw.setColorAt(0,QColor(255,215,0,120)); gw.setColorAt(1,QColor(255,215,0,0))
        p.setBrush(QBrush(gw)); p.drawEllipse(tx-14,ty2-14,80,80)
        p.setBrush(QColor(160,90,20)); p.setPen(Qt.NoPen)
        p.drawRoundedRect(tx,ty2+18,52,32,6,6)
        p.setBrush(QColor(200,130,35)); p.drawRoundedRect(tx,ty2,52,22,6,6)
        p.setBrush(QColor(240,200,60)); p.setPen(QPen(QColor(180,140,0),1))
        p.drawEllipse(tx+20,ty2+8,12,12); p.drawRect(tx+23,ty2+16,7,8)
        p.setPen(Qt.NoPen)
        for ox,oy in [(-5,0),(5,-3),(15,1),(-2,10),(12,8),(8,-2)]:
            p.setBrush(QColor(255,200,0,190)); p.drawEllipse(tx+20+ox,ty2+40+oy,7,7)
        self._bear(p, int(lx+28), int(H-55-self._sp*sh))


class VocabStairsGame(QWidget):
    ANIM_MS = 480

    def __init__(self, vocab):
        super().__init__()
        self.V=vocab; self.N=len(vocab)
        self.setWindowTitle("Vocabulary Treasure Stairs")
        self.resize(840,580); self.setStyleSheet("background:#eef2ff;")
        self._build_ui()
        self._anim = QPropertyAnimation(self.canvas, b"stairPos")
        self._anim.setDuration(self.ANIM_MS)
        self._anim.setEasingCurve(QEasingCurve.OutBounce)
        self._reset_state()

    def _build_ui(self):
        self.canvas = StairCanvas(self.N)
        self.lbl_title = QLabel(_ui["title"])
        self.lbl_title.setStyleSheet(
            "font-size:22px;font-weight:bold;color:#1a2860;padding:4px 0;")
        self.lbl_prog = QLabel()
        self.lbl_prog.setStyleSheet("font-size:12px;color:#556;")
        sep = QFrame(); sep.setFrameShape(QFrame.HLine); sep.setStyleSheet("color:#ccd;")
        self.lbl_mean = QLabel(); self.lbl_mean.setWordWrap(True)
        self.lbl_mean.setMinimumHeight(75)
        self.lbl_mean.setStyleSheet(
            "font-size:17px;padding:14px;background:#fff;"
            "border-radius:10px;border:1px solid #c5d0f0;color:#1a2860;")
        self.lbl_fb = QLabel(" ")
        self.lbl_fb.setStyleSheet("font-size:14px;font-weight:bold;min-height:30px;")
        self.edit = QLineEdit(); self.edit.setPlaceholderText(_ui["placeholder"])
        self.edit.setStyleSheet(
            "font-size:15px;padding:9px;border:2px solid #99b;"
            "border-radius:7px;background:#fff;")
        self.edit.returnPressed.connect(self._check)
        self.btn_chk = QPushButton(_ui["btn_check"])
        self.btn_chk.setStyleSheet(self._bs("#2574a9"))
        self.btn_chk.clicked.connect(self._check)
        self.btn_nxt = QPushButton(_ui["btn_next"])
        self.btn_nxt.setStyleSheet(self._bs("#1e8449"))
        self.btn_nxt.setEnabled(False)
        self.btn_nxt.clicked.connect(self._next)
        self.btn_retry = QPushButton(_ui["btn_retry"])
        self.btn_retry.setStyleSheet(self._bs("#8e44ad"))
        self.btn_retry.clicked.connect(self._retry)
        self.lbl_sc = QLabel()
        self.lbl_sc.setStyleSheet("font-size:12px;color:#445;")
        self.lbl_f = QLabel("vocab.json")
        self.lbl_f.setStyleSheet(
            "font-size:11px;color:#aaa;padding:2px 6px;"
            "background:#f0f0f8;border-radius:4px;")
        rv = QVBoxLayout(); rv.setSpacing(11)
        for w in [self.lbl_title, self.lbl_prog, sep,
                  QLabel(_ui["hint"]), self.lbl_mean, self.lbl_fb, self.edit]:
            rv.addWidget(w)
        bh1 = QHBoxLayout()
        bh1.addWidget(self.btn_chk); bh1.addWidget(self.btn_nxt)
        rv.addLayout(bh1)
        rv.addWidget(self.btn_retry)
        rv.addStretch(1)
        rv.addWidget(self.lbl_sc); rv.addWidget(self.lbl_f)
        rc = QWidget(); rc.setLayout(rv)
        rc.setStyleSheet("padding:22px 22px 16px 16px;")
        rc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ml = QHBoxLayout(self); ml.setContentsMargins(0,0,0,0)
        ml.addWidget(self.canvas,5); ml.addWidget(rc,5)

    # ── reset all state ──────────────────────────────────────
    def _reset_state(self):
        self._anim.stop()
        self._qi=0; self._cc=0; self._ans=False; self._clr=False
        self._ord = list(range(self.N)); random.shuffle(self._ord)
        self.canvas.set_sp(0.0)
        self._refresh()

    # ── retry button ─────────────────────────────────────────
    def _retry(self):
        ans = QMessageBox.question(
            self, _ui["retry_title"], _ui["retry_confirm"],
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            self._reset_state()

    @staticmethod
    def _bs(c):
        return (f"QPushButton{{background:{c};color:white;font-size:14px;"
                f"padding:9px 18px;border-radius:7px;border:none;}}"
                f"QPushButton:hover{{background:{c}dd;}}"
                f"QPushButton:disabled{{background:#bbb;}}")

    def _refresh(self):
        it=self.V[self._ord[self._qi]]; pos=int(self.canvas.stairPos)
        self.lbl_prog.setText(
            _ui["q_label"]+str(self._qi+1)+" / "+str(self.N)+
            "   ["+"#"*pos+"-"*(self.N-pos)+"]")
        self.lbl_mean.setText(it.meaning); self.lbl_fb.setText(" ")
        self.lbl_fb.setStyleSheet("font-size:14px;font-weight:bold;min-height:30px;")
        self.edit.clear(); self.edit.setEnabled(True); self.edit.setFocus()
        self.btn_chk.setEnabled(True); self.btn_nxt.setEnabled(False)
        self._ans=False; self._upsc()

    def _upsc(self):
        self.lbl_sc.setText(
            _ui["stair"]+str(int(self.canvas.stairPos))+" / "+str(self.N)+
            _ui["score"]+str(self._cc)+" / "+str(self._qi))

    def _check(self):
        if self._ans: return
        ans=self.edit.text().strip()
        if not ans:
            self.lbl_fb.setText(_ui["empty"])
            self.lbl_fb.setStyleSheet("font-size:14px;font-weight:bold;color:#ca6f1e;"); return
        self._ans=True; self.edit.setEnabled(False); self.btn_chk.setEnabled(False)
        it=self.V[self._ord[self._qi]]; ok=ans.lower()==it.word.lower()
        if ok:
            self._cc+=1; self.lbl_fb.setText(_ui["correct"]+it.word)
            self.lbl_fb.setStyleSheet("font-size:14px;font-weight:bold;color:#1e8449;")
        else:
            self.lbl_fb.setText(_ui["slide"]+it.word)
            self.lbl_fb.setStyleSheet("font-size:14px;font-weight:bold;color:#c0392b;")
        d=+STEP_SIZE if ok else -STEP_SIZE
        s=self.canvas.stairPos; e=max(0.0,min(float(self.N),s+d))
        self._anim.stop(); self._anim.setStartValue(s); self._anim.setEndValue(e); self._anim.start()
        self._upsc()
        if e>=self.N and not self._clr:
            self._clr=True; self._anim.finished.connect(self._win)
        elif self._qi==self.N-1:
            self._anim.finished.connect(self._end)
        else:
            self.btn_nxt.setEnabled(True)

    def _next(self): self._qi+=1; self._refresh()

    def _win(self):
        try: self._anim.finished.disconnect(self._win)
        except: pass
        dlg = CelebrationDialog(self._cc, self._qi+1, self)
        dlg.exec_()

    def _end(self):
        try: self._anim.finished.disconnect(self._end)
        except: pass
        b=QMessageBox(self); b.setWindowTitle(_ui["end_title"])
        b.setText(_ui["end_msg"]+str(self._cc)+"/"+str(self.N)+_ui["end_msg2"])
        b.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VocabStairsGame(load_vocab())
    win.show(); sys.exit(app.exec_())
"""

py_final = py.replace("UBPLACEHOLDER", UB)
bad = [(i,c) for i,c in enumerate(py_final) if ord(c)>127]
print("Non-ASCII:", len(bad))
print("Lines:", py_final.count('\n'))
