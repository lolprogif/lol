# LOI CATFARM PRO - macro independente baseado nas telas/vídeos fornecidos
# Python 3.10+ / Windows
import ctypes
# Define a escala de coordenadas antes de inicializar Tkinter e os hooks.
try:
 ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))  # Per-monitor v2
except Exception:
 try:
  ctypes.windll.user32.SetProcessDPIAware()
 except Exception:
  pass

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading, time, json, random
from pathlib import Path

try:
    import keyboard
    from pynput import mouse
    import pydirectinput as pdi
    import pygetwindow as gw
    from pynput import keyboard as pynput_keyboard
except Exception:
    keyboard = None
    mouse = None
    pdi = None
    gw = None
    pynput_keyboard = None

BG="#202326"; PANEL="#292e33"; FIELD="#343a40"; BLUE="#167ba7"; CYAN="#35b9e8"
DEFAULT={
 "game_title":"NEWMT2",
 "mount_on":True,"mount_key":"1","mount_interval":1.0,
 "attack_on":True,"attack_key":"space","attack_interval":0.15,
 "loot_on":False,"loot_key":"z","loot_interval":0.2,
 "camera_on":False,"camera_key":"q","camera_interval":3.0,
 "combo_on":False,"combo_key":"q+w","combo_hold":3.5,"combo_pause":4.2,
 "wasd_on":False,"wasd_interval":2.0,
 "random_delay":False,"random_amount":0.15,"window_delay":0.0,
 "rest_cycle_on":True,"active_minutes":25,"rest_min":45,"rest_max":90,
 "click_route_on":False,"route_repeat":True,"route_pause":1.0,
 "r1_on":True,"r2_on":False,"r3_on":False,
 "r1_wait":1.0,"r2_wait":1.0,"r3_wait":1.0,
 "r1_walk":1.0,"r2_walk":1.0,"r3_walk":1.0,
 "r1_mount":False,"r2_mount":False,"r3_mount":False,
 "r1_loot":True,"r2_loot":True,"r3_loot":True,
 "r1_attack":True,"r2_attack":True,"r3_attack":True
}

class App:
 def __init__(self,root):
  self.root=root; root.title("LOI CATFARM PRO"); root.geometry("760x760"); root.minsize(700,680); root.configure(bg=BG)
  self.v={}; self.running=False; self.recording=False; self.mouse_listener=None
  self.events=[]; self.route_points=[]; self.started=0; self.action_count=0
  self.playback_stop=threading.Event()
  self.mouse_buttons=set(); self.last_mouse_pos=None; self.camera_sweep_active=False; self.camera_sweep_requested=False
  self.cursor_clipped=False; self.clip_guard_active=False
  self.raw_mouse_thread=None; self.raw_mouse_tid=None; self.raw_mouse_stop=False
  self.key_listener=None; self.key_hook=None; self.game_rect=None; self.record_started=0.0; self.pressed_keys=set()
  self.build(); self.set_defaults(); root.protocol("WM_DELETE_WINDOW",self.close)
  if keyboard:
   try:
    keyboard.add_hotkey("F8",lambda:root.after(0,self.toggle))
    keyboard.add_hotkey("F9",lambda: self.hotkey_stop(), suppress=False, trigger_on_release=False)
    keyboard.on_press_key("f9",lambda event: self.hotkey_stop(), suppress=False)
   except Exception: pass
  self.tick()

 def var(self,k,val):
  self.v[k]=tk.StringVar(value=str(val)); return self.v[k]
 def bool(self,k,val=False):
  self.v[k]=tk.BooleanVar(value=val); return self.v[k]
 def label(self,p,t,fg="#eee",bg=PANEL,**kw):
  return tk.Label(p,text=t,fg=fg,bg=bg,**kw)
 def section(self,p,t):
  self.label(p,t,CYAN,BG,font=("Segoe UI",10,"bold")).pack(anchor="w",padx=12,pady=(12,5))
 def row(self,p):
  f=tk.Frame(p,bg=PANEL); f.pack(fill="x",padx=8,pady=3); return f
 def entry(self,p,k,title,val,w=8):
  self.label(p,title).pack(side="left",padx=(8,4))
  tk.Entry(p,textvariable=self.var(k,val),width=w,bg=FIELD,fg="white",insertbackground="white",relief="flat").pack(side="left",ipady=4,padx=(0,7))
 def check(self,p,k,title,val=False):
  ttk.Checkbutton(p,text=title,variable=self.bool(k,val)).pack(side="left",padx=8,pady=5)
 def button(self,p,t,cmd,color=BLUE):
  tk.Button(p,text=t,command=cmd,bg=color,fg="white",activebackground=color,relief="flat",padx=9,pady=5).pack(side="left",padx=3)

 def build(self):
  st=ttk.Style(); st.theme_use("clam")
  st.configure("TNotebook",background=BG,borderwidth=0)
  st.configure("TNotebook.Tab",background="#363c42",foreground="white",padding=(12,8))
  st.map("TNotebook.Tab",background=[("selected",BLUE)])
  st.configure("TCheckbutton",background=PANEL,foreground="white")
  head=tk.Frame(self.root,bg="#15191d"); head.pack(fill="x")
  self.label(head,"◆ LOI CATFARM PRO",CYAN,"#15191d",font=("Segoe UI",15,"bold")).pack(side="left",padx=14,pady=10)
  self.label(head,"Macro independente • F8 ligar / F9 pausar","#e5c45d","#15191d").pack(side="right",padx=14)
  stats=tk.Frame(self.root,bg=PANEL); stats.pack(fill="x",padx=12,pady=8)
  self.clock=self.label(stats,"Tempo: 00:00:00"); self.clock.pack(side="left",padx=14,pady=8)
  self.count=self.label(stats,"Passos Gravados: 0"); self.count.pack(side="right",padx=14)
  self.nb=ttk.Notebook(self.root); self.nb.pack(fill="both",expand=True,padx=12,pady=4)
  self.pages={}
  for name in ("Módulos","Jogo","Cliques","Skills","Anti-Ban","Perfis"):
   f=tk.Frame(self.nb,bg=PANEL); self.nb.add(f,text=name); self.pages[name]=f
  self.make_modules(); self.make_game(); self.make_clicks(); self.make_skills(); self.make_antiban(); self.make_profiles()
  foot=tk.Frame(self.root,bg="#15191d"); foot.pack(fill="x",padx=12,pady=8)
  self.status=self.label(foot,"Status: Pausado",fg="#e5b45b",bg="#15191d",anchor="w"); self.status.pack(fill="x",padx=9,pady=6)
  bar=tk.Frame(foot,bg="#15191d"); bar.pack(fill="x",padx=6,pady=(0,7))
  self.button(bar,"▶ LIGAR BOT (F8)",self.start,"#20b968")
  self.button(bar,"Ⅱ PAUSAR (F9)",self.stop,"#247da8")
  self.button(bar,"■ LIMPAR ROTA",self.clear_route,"#d58232")
  tk.Button(bar,text="Salvar Configs",command=self.save,bg="#287ba8",fg="white",relief="flat").pack(side="right",padx=4)

 def make_modules(self):
  p=self.pages["Módulos"]; self.section(p,"MÓDULOS AUTOMÁTICOS")
  for k,t,desc,default in [
   ("mount","Ativar Montaria","Aciona a tecla de montaria",True),
   ("attack","Ativar Ataque","Repete o comando de ataque",True),
   ("loot","Ativar Coleta (Loot)","Coleta itens no intervalo",True),
   ("camera","Giro Câmera","Repete a tecla de câmera",False),
   ("combo","Ativar Giro Q+W","Executa uma combinação configurável",False),
   ("wasd","Usar Rota Teclado (WASD)","Sequência de movimento",False),
   ("click_route","Ativar Rota por Cliques","Executa os pontos gravados",False)]:
   r=self.row(p); self.check(r,k+"_on",t,default); self.label(r,desc,fg="#aeb7bd").pack(side="left",padx=8)
  self.section(p,"CONTROLES")
  self.label(p,"F8 liga/desliga • F9 pausa • O jogo precisa estar em primeiro plano.",fg="#e2c16b").pack(anchor="w",padx=14,pady=8)

 def make_game(self):
  p=self.pages["Jogo"]; self.section(p,"TÍTULO DA JANELA DO JOGO")
  r=self.row(p); self.entry(r,"game_title","Título:",DEFAULT["game_title"],24)
  self.label(p,"Deixe o jogo em primeiro plano antes de iniciar. As teclas são enviadas ao aplicativo ativo.",fg="#aeb7bd").pack(anchor="w",padx=14,pady=7)
  self.section(p,"MONTARIA / ATAQUE")
  for k,title,key,ival,dk,di in [("mount","Ativar Montaria","mount_key","mount_interval","1",1.0),("attack","Ativar Ataque","attack_key","attack_interval","space",.15)]:
   r=self.row(p); self.check(r,k+"_on",title,True); self.entry(r,key,"Tecla:",dk); self.entry(r,ival,"Intervalo (s):",di)
  r=self.row(p); self.entry(r,"window_delay","Delay troca janela (s):",0.0)

 def make_clicks(self):
  p=self.pages["Cliques"]; self.section(p,"CÂMERA POR TECLA (Q) — FUNÇÃO INDEPENDENTE")
  r=self.row(p); self.check(r,"camera_on","Giro Câmera (Q)",False); self.entry(r,"camera_key","Tecla:","q"); self.entry(r,"camera_interval","Intervalo (s):",3.0)
  self.label(p,"A tecla Q é uma ação independente. Ela não altera nem substitui os movimentos reais do mouse gravados na rota.",fg="#c7cdd2",wraplength=590,justify="left").pack(anchor="w",padx=14,pady=6)
  self.section(p,"ROTAS POR PONTOS DE MOUSE")
  self.label(p,"Segure o botão direito e mova o mouse para gravar a câmera; cliques e teclas também são registrados com seus tempos reais. Mantenha NEWMT2 em primeiro plano.",fg="#c7cdd2",wraplength=590,justify="left").pack(anchor="w",padx=14,pady=6)
  r=self.row(p); self.button(r,"● GRAVAR MOUSE + TECLADO",self.record_route); self.button(r,"■ PARAR",self.stop_record,"#a94d45"); self.button(r,"▶ TESTAR ROTA",self.play_route,"#179b60")
  r=self.row(p); self.check(r,"route_repeat","Repetir rota continuamente",True); self.entry(r,"route_pause","Pausa entre ciclos (s):",1.0)
  self.routebox=tk.Text(p,height=8,bg=FIELD,fg="white",insertbackground="white"); self.routebox.pack(fill="both",expand=True,padx=12,pady=8)

 def make_skills(self):
  p=self.pages["Skills"]; self.section(p,"COMBINAÇÃO DE HABILIDADES")
  r=self.row(p); self.check(r,"combo_on","Ativar Giro Q+W",False); self.entry(r,"combo_key","Combo:", "q+w")
  r=self.row(p); self.entry(r,"combo_hold","Segurar (s):",3.5); self.entry(r,"combo_pause","Pausa (s):",4.2)
  r=self.row(p); self.check(r,"wasd_on","Usar Rota Teclado (WASD)",False); self.entry(r,"wasd_interval","Intervalo WASD (s):",2.0)
  self.label(p,"Informe teclas separadas por + para combos, por exemplo q+w.",fg="#aeb7bd").pack(anchor="w",padx=14,pady=8)

 def make_antiban(self):
  p=self.pages["Anti-Ban"]; self.section(p,"AJUSTE DE INTERVALOS")
  r=self.row(p); self.check(r,"random_delay","Variação aleatória moderada dos intervalos",False)
  r=self.row(p); self.entry(r,"random_amount","Variação máxima (s):",.15)
  self.section(p,"PAUSAS AUTOMÁTICAS")
  r=self.row(p); self.check(r,"rest_cycle_on","Ativar pausa periódica",True)
  r=self.row(p); self.entry(r,"active_minutes","Tempo ativo (min):",25)
  r=self.row(p); self.entry(r,"rest_min","Descanso mínimo (s):",45)
  self.entry(r,"rest_max","Descanso máximo (s):",90)
  self.label(p,"A pausa periódica interrompe o macro por um intervalo configurável e depois retoma. Isso é apenas gerenciamento de descanso; não garante proteção contra detecção ou punições. Confira as regras do jogo.",fg="#e6bd70",wraplength=590,justify="left").pack(anchor="w",padx=14,pady=10)

 def make_profiles(self):
  p=self.pages["Perfis"]; self.section(p,"PERFIS")
  r=self.row(p); self.button(r,"Salvar Perfil...",self.save); self.button(r,"Carregar Perfil...",self.load); self.button(r,"Restaurar Padrões",self.defaults)
  self.section(p,"ROTAS GRAVADAS")
  self.label(p,"As rotas são incluídas no arquivo de perfil JSON.",fg="#bfc6cc").pack(anchor="w",padx=14,pady=5)

 def defaults(self):
  self.set_defaults()

 def set_defaults(self):
  for k,v in DEFAULT.items():
   if k in self.v:self.v[k].set(v)

 def getnum(self,k,default):
  try:return max(.03,float(self.v[k].get()))
  except:return default
 def send(self,key):
  if pdi is None:return
  key=str(key).strip().lower()
  if not key:return
  try:
   if "+" in key:
    keys=[x.strip() for x in key.split("+") if x.strip()]
    pdi.hotkey(*keys)
   else:pdi.press(key)
  except Exception as e:self.root.after(0,lambda:self.status.config(text="Falha ao enviar tecla: "+str(e)))
 def start(self):
  if keyboard is None or pdi is None:
   messagebox.showerror("Dependências","Execute instalar.bat para instalar keyboard, pynput e pydirectinput."); return
  if self.running:return
  if "loot_on" in self.v:
   self.v["loot_on"].set(False)
  self.playback_stop.clear()
  self.running=True; self.started=time.time()
  # Não captura/bloqueia o cursor: evita sensação de mouse travado.
  self.unclip_cursor()
  threading.Thread(target=self.loop,daemon=True).start()
  self.status.config(text="Status: Ligado — volte ao jogo. F9 pausa.")
 def toggle(self):
  if self.running:self.stop()
  else:self.start()
 def clip_cursor_to_game(self):
  # Bloqueio do cursor desativado: o mouse permanece livre para o usuário.
  self.unclip_cursor()
 def start_clip_guard(self):
  # Guarda mantida por compatibilidade; não restringe mais o cursor.
  self.unclip_cursor()
 def unclip_cursor(self):
  try: ctypes.windll.user32.ClipCursor(None)
  except Exception: pass
  self.cursor_clipped=False
 def release_inputs(self):
  # Solta todos os controles e restaura o cursor mesmo se a rota estiver no meio.
  self.camera_sweep_requested=False
  if pdi is not None:
   for key in ("space", "w", "a", "s", "d"):
    try: pdi.keyUp(key)
    except Exception: pass
   for button in ("right", "left", "middle"):
    try: pdi.mouseUp(button=button)
    except Exception: pass
  self.unclip_cursor()
 def hotkey_stop(self):
  # Sinaliza primeiro: playback e varredura da câmera verificam self.running.
  self.running=False
  self.playback_stop.set()
  self.camera_sweep_requested=False
  self.release_inputs()
  try: self.root.after(0,lambda:self.status.config(text="Status: Pausado"))
  except Exception: pass
 def stop(self):
  self.hotkey_stop()
 def loop(self):
  last={}
  active_started=time.monotonic()
  rest_until=0.0
  actions=[("mount","mount_key","mount_interval"),("attack","attack_key","attack_interval"),("camera","camera_key","camera_interval")]
  while self.running:
   now=time.monotonic()
   if self.v["rest_cycle_on"].get():
    if rest_until and now < rest_until:
     time.sleep(.15)
     continue
    if rest_until and now >= rest_until:
     rest_until=0.0
     active_started=now
     self.root.after(0,lambda:self.status.config(text="Pausa automática encerrada — macro retomado."))
    active_for=max(1.0,self.getnum("active_minutes",25)*60)
    if not rest_until and now-active_started >= active_for:
     lo=max(1.0,self.getnum("rest_min",45))
     hi=max(lo,self.getnum("rest_max",90))
     rest_duration=random.uniform(lo,hi)
     rest_until=now+rest_duration
     self.root.after(0,lambda d=int(rest_duration):self.status.config(text=f"Pausa automática: {d}s. O macro retomará sozinho."))
     time.sleep(.15)
     continue
   # MODO ROTA EXCLUSIVA: se existe uma gravação, F8 a reproduz automaticamente,
   # sem exigir que a caixa de rota por cliques esteja marcada. Esses módulos
   # enviam toques extras (inclusive ataque) e podem interromper ESPAÇO/W.
   if self.running and self.events:
    # F8: executa a rota sem módulos concorrentes e respeita exatamente
    # os eventos gravados de pressionar/soltar as teclas.
    self.execute_route(bot_mode=True)
    if self.running:
     if self.v["route_repeat"].get():
      time.sleep(0.01)
     else:
      self.running = False
    continue
   for mod,key,ival in actions:
    if self.running and self.v[mod+"_on"].get():
     interval=self.getnum(ival,1)
     if self.v["random_delay"].get():interval+=random.uniform(0,self.getnum("random_amount",.15))
     if now-last.get(mod,0)>=interval:self.send(self.v[key].get());last[mod]=now;self.action_count+=1
   if self.running and self.v["combo_on"].get() and now-last.get("combo",0)>=self.getnum("combo_pause",4.2):
    self.send(self.v["combo_key"].get());time.sleep(min(self.getnum("combo_hold",3.5),8));last["combo"]=time.monotonic()
   if self.running and self.v["wasd_on"].get() and now-last.get("wasd",0)>=self.getnum("wasd_interval",2):
    for key in "wasd":
     if not self.running:break
     self.send(key);time.sleep(.12)
    last["wasd"]=time.monotonic()
   if self.running and self.v["click_route_on"].get() and self.route_points and now-last.get("route",0)>=self.getnum("route_pause",1):
    self.execute_route();last["route"]=time.monotonic()
   time.sleep(.02)
  self.root.after(0,lambda:self.status.config(text="Status: Pausado"))
 def find_game_window(self):
  """Retorna a janela do jogo pelo título configurado."""
  if gw is None:
   return None
  title=str(self.v["game_title"].get()).strip().lower()
  try:
   wins=[w for w in gw.getAllWindows() if w.title and title in w.title.lower() and w.width>0 and w.height>0]
   if wins:
    w=max(wins,key=lambda x:x.width*x.height)
    return (int(w.left),int(w.top),int(w.width),int(w.height))
  except Exception:
   pass
  return None

 def game_window_is_active(self):
  """Confere o foco usando o título da janela em primeiro plano."""
  title=str(self.v["game_title"].get()).strip().lower()
  if not title:
   return False
  try:
   active=gw.getActiveWindow() if gw else None
   if active and active.title and title in active.title.lower():
    return True
  except Exception:
   pass
  # Fallback nativo do Windows caso pygetwindow não identifique o foco.
  try:
   hwnd=ctypes.windll.user32.GetForegroundWindow()
   buf=ctypes.create_unicode_buffer(512)
   ctypes.windll.user32.GetWindowTextW(hwnd,buf,512)
   return title in buf.value.lower()
  except Exception:
   return False

 def record_route(self):
  if mouse is None or pynput_keyboard is None or pdi is None or gw is None:
   messagebox.showerror("Dependências","Execute ABRIR_AQUI.bat para instalar pynput, keyboard, pydirectinput e pygetwindow.")
   return
  rect=self.find_game_window()
  if not rect:
   messagebox.showerror("Janela do jogo não encontrada",
    "Não encontrei uma janela com o título configurado na aba Jogo. Ajuste o título para um trecho que apareça na barra de título do jogo e tente novamente.")
   return
  if self.recording:
   return
  self.game_rect=rect
  self.recording=True
  self.route_points=[]
  self.events=[]
  self.record_started=time.monotonic()
  self.pressed_keys.clear()
  self.mouse_buttons.clear()
  self.last_mouse_pos=None
  # pynput fica responsável pelos cliques/botões; os deltas da câmera vêm de
  # Raw Input do Windows, que continua funcionando com o cursor capturado pelo jogo.
  self.mouse_listener=mouse.Listener(on_click=self.on_click)
  self.mouse_listener.start()
  self.start_raw_mouse_capture()
  # Usa o hook global da biblioteca keyboard para capturar teclas mesmo quando
  # pynput não recebe eventos em alguns clientes/janelas do Windows.
  try:
   self.key_hook=keyboard.hook(self.on_keyboard_event)
  except Exception as e:
   self.key_hook=None
   self.status.config(text="Mouse gravando; falha no hook do teclado: "+str(e))
  else:
   self.status.config(text="GRAVANDO: clique e pressione teclas dentro do NEWMT2. Ações aparecem na lista.")
  # Segundo capturador de teclado como redundância; eventos repetidos são filtrados.
  try:
   self.key_listener=pynput_keyboard.Listener(
    on_press=self.on_key_press, on_release=self.on_key_release)
   self.key_listener.start()
  except Exception as e:
   self.status.config(text="Mouse/Hook ativo; fallback de teclado indisponível: "+str(e))
  self.root.after(0,self.render_route)

 def in_game_rect(self,x,y):
  if not self.game_rect:
   return False
  left,top,width,height=self.game_rect
  return left <= x < left+width and top <= y < top+height

 def on_click(self,x,y,button,pressed):
  if not self.recording:
   return
  btn=str(button).split(".")[-1]
  # Guarda o estado contínuo do botão direito: ele precisa permanecer
  # pressionado enquanto o mouse se desloca para girar a câmera.
  if btn == "right":
   if pressed:
    if not self.game_window_is_active():
     return
    self.mouse_buttons.add(btn)
    self.events.append({"t":time.monotonic()-self.record_started,"type":"mouse_down","button":"right"})
   else:
    if btn not in self.mouse_buttons:
     return
    self.mouse_buttons.discard(btn)
    self.events.append({"t":time.monotonic()-self.record_started,"type":"mouse_up","button":"right"})
   self.root.after(0,self.render_route)
   return
  if not pressed:
   return
  current_rect=self.find_game_window()
  if current_rect:
   self.game_rect=current_rect
  if not self.in_game_rect(x,y):
   return
  event={"t":time.monotonic()-self.record_started,"type":"click",
         "x":int(x-self.game_rect[0]),"y":int(y-self.game_rect[1]),"button":btn}
  self.events.append(event)
  self.route_points.append(event.copy())
  self.root.after(0,self.render_route)

 def on_move(self,x,y):
  # Não usar coordenadas absolutas para a câmera: jogos com cursor capturado
  # frequentemente o mantêm no centro e escondem o deslocamento real.
  return

 def start_raw_mouse_capture(self):
  """Inicia uma única janela Raw Input; ela permanece ativa entre gravações."""
  if self.raw_mouse_thread and self.raw_mouse_thread.is_alive():
   return
  self.raw_mouse_stop=False
  self.raw_mouse_thread=threading.Thread(target=self._raw_mouse_message_loop,daemon=True)
  self.raw_mouse_thread.start()

 def _raw_mouse_message_loop(self):
  """Captura deltas relativos do dispositivo físico via WM_INPUT (Windows x64/x86)."""
  from ctypes import wintypes
  user32=ctypes.WinDLL("user32",use_last_error=True)
  kernel32=ctypes.WinDLL("kernel32",use_last_error=True)
  WM_INPUT=0x00FF; WM_QUIT=0x0012; RID_INPUT=0x10000003
  RIDEV_INPUTSINK=0x00000100
  HWND_MESSAGE=ctypes.c_void_p(-3)
  LRESULT=ctypes.c_ssize_t

  class RAWINPUTDEVICE(ctypes.Structure):
   _fields_=[("usUsagePage",wintypes.USHORT),("usUsage",wintypes.USHORT),
             ("dwFlags",wintypes.DWORD),("hwndTarget",wintypes.HWND)]
  class RAWINPUTHEADER(ctypes.Structure):
   _fields_=[("dwType",wintypes.DWORD),("dwSize",wintypes.DWORD),
             ("hDevice",wintypes.HANDLE),("wParam",wintypes.WPARAM)]
  class RAWHID(ctypes.Structure):
   _fields_=[("dwSizeHid",wintypes.DWORD),("dwCount",wintypes.DWORD),("bRawData",ctypes.c_byte*1)]
  class RAWMOUSE_BUTTONS(ctypes.Structure):
   _fields_=[("usButtonFlags",wintypes.USHORT),("usButtonData",wintypes.USHORT)]
  class RAWMOUSE_UNION(ctypes.Union):
   _fields_=[("ulButtons",wintypes.ULONG),("buttons",RAWMOUSE_BUTTONS)]
  class RAWMOUSE(ctypes.Structure):
   _fields_=[("usFlags",wintypes.USHORT),("buttonUnion",RAWMOUSE_UNION),
             ("ulRawButtons",wintypes.ULONG),("lLastX",wintypes.LONG),
             ("lLastY",wintypes.LONG),("ulExtraInformation",wintypes.ULONG)]
  class RAWDATA(ctypes.Union):
   _fields_=[("mouse",RAWMOUSE),("hid",RAWHID),("padding",ctypes.c_byte*24)]
  class RAWINPUT(ctypes.Structure):
   _fields_=[("header",RAWINPUTHEADER),("data",RAWDATA)]
  WNDPROC=ctypes.WINFUNCTYPE(LRESULT,wintypes.HWND,wintypes.UINT,wintypes.WPARAM,wintypes.LPARAM)
  class WNDCLASS(ctypes.Structure):
   _fields_=[("style",wintypes.UINT),("lpfnWndProc",WNDPROC),("cbClsExtra",ctypes.c_int),
             ("cbWndExtra",ctypes.c_int),("hInstance",wintypes.HINSTANCE),
             ("hIcon",wintypes.HICON),("hCursor",wintypes.HANDLE),
             ("hbrBackground",wintypes.HBRUSH),("lpszMenuName",wintypes.LPCWSTR),
             ("lpszClassName",wintypes.LPCWSTR)]

  # Declarar protótipos evita truncamento de HWND/HANDLE em Python 64 bits.
  user32.DefWindowProcW.argtypes=[wintypes.HWND,wintypes.UINT,wintypes.WPARAM,wintypes.LPARAM]
  user32.DefWindowProcW.restype=LRESULT
  user32.RegisterClassW.argtypes=[ctypes.POINTER(WNDCLASS)]; user32.RegisterClassW.restype=wintypes.ATOM
  user32.CreateWindowExW.argtypes=[wintypes.DWORD,wintypes.LPCWSTR,wintypes.LPCWSTR,wintypes.DWORD,
   ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,wintypes.HWND,wintypes.HMENU,wintypes.HINSTANCE,ctypes.c_void_p]
  user32.CreateWindowExW.restype=wintypes.HWND
  user32.RegisterRawInputDevices.argtypes=[ctypes.POINTER(RAWINPUTDEVICE),wintypes.UINT,wintypes.UINT]
  user32.RegisterRawInputDevices.restype=wintypes.BOOL
  user32.GetRawInputData.argtypes=[wintypes.HANDLE,wintypes.UINT,ctypes.c_void_p,ctypes.POINTER(wintypes.UINT),wintypes.UINT]
  user32.GetRawInputData.restype=wintypes.UINT
  user32.GetMessageW.argtypes=[ctypes.POINTER(wintypes.MSG),wintypes.HWND,wintypes.UINT,wintypes.UINT]
  user32.GetMessageW.restype=ctypes.c_int
  user32.TranslateMessage.argtypes=[ctypes.POINTER(wintypes.MSG)]
  user32.DispatchMessageW.argtypes=[ctypes.POINTER(wintypes.MSG)]
  user32.DestroyWindow.argtypes=[wintypes.HWND]
  user32.UnregisterClassW.argtypes=[wintypes.LPCWSTR,wintypes.HINSTANCE]
  kernel32.GetModuleHandleW.argtypes=[wintypes.LPCWSTR]; kernel32.GetModuleHandleW.restype=wintypes.HMODULE
  kernel32.GetCurrentThreadId.restype=wintypes.DWORD

  class_name=f"LOICatfarmRawMouseWindow_{threading.get_ident()}"
  @WNDPROC
  def wndproc(hwnd,msg,wparam,lparam):
   if msg==WM_INPUT:
    size=wintypes.UINT(0)
    header_size=ctypes.sizeof(RAWINPUTHEADER)
    result=user32.GetRawInputData(wintypes.HANDLE(lparam),RID_INPUT,None,ctypes.byref(size),header_size)
    if result==0xFFFFFFFF or size.value<header_size:
     return user32.DefWindowProcW(hwnd,msg,wparam,lparam)
    buf=ctypes.create_string_buffer(size.value)
    got=user32.GetRawInputData(wintypes.HANDLE(lparam),RID_INPUT,buf,ctypes.byref(size),header_size)
    if got!=0xFFFFFFFF and got>=ctypes.sizeof(RAWINPUTHEADER)+ctypes.sizeof(RAWMOUSE):
     raw=ctypes.cast(buf,ctypes.POINTER(RAWINPUT)).contents
     if raw.header.dwType==0:
      dx=int(raw.data.mouse.lLastX); dy=int(raw.data.mouse.lLastY)
      if dx or dy:
       self.on_raw_mouse_delta(dx,dy)
    # Obrigatório chamar DefWindowProc para limpar WM_INPUT em RIDEV_INPUTSINK.
    return user32.DefWindowProcW(hwnd,msg,wparam,lparam)
   return user32.DefWindowProcW(hwnd,msg,wparam,lparam)

  hinst=kernel32.GetModuleHandleW(None)
  wc=WNDCLASS(); wc.lpfnWndProc=wndproc; wc.hInstance=hinst; wc.lpszClassName=class_name
  if not user32.RegisterClassW(ctypes.byref(wc)):
   self.root.after(0,lambda:self.status.config(text="Falha ao registrar captura Raw Input do mouse."))
   return
  hwnd=user32.CreateWindowExW(0,class_name,"",0,0,0,0,0,HWND_MESSAGE,None,hinst,None)
  if not hwnd:
   user32.UnregisterClassW(class_name,hinst)
   self.root.after(0,lambda:self.status.config(text="Falha ao criar janela de captura do mouse."))
   return
  device=RAWINPUTDEVICE(1,2,RIDEV_INPUTSINK,hwnd)
  if not user32.RegisterRawInputDevices(ctypes.byref(device),1,ctypes.sizeof(device)):
   user32.DestroyWindow(hwnd); user32.UnregisterClassW(class_name,hinst)
   self.root.after(0,lambda:self.status.config(text="Windows recusou a captura Raw Input do mouse."))
   return
  self.raw_mouse_tid=kernel32.GetCurrentThreadId()
  self.root.after(0,lambda:self.status.config(text="Captura de mouse físico ativa; grave segurando o botão direito."))
  msg=wintypes.MSG()
  while not self.raw_mouse_stop:
   result=user32.GetMessageW(ctypes.byref(msg),None,0,0)
   if result<=0: break
   user32.TranslateMessage(ctypes.byref(msg)); user32.DispatchMessageW(ctypes.byref(msg))
  user32.DestroyWindow(hwnd)
  user32.UnregisterClassW(class_name,hinst)
  self.raw_mouse_tid=None

 def on_raw_mouse_delta(self,dx,dy):
  if not self.recording or "right" not in self.mouse_buttons:
   return
  if not self.game_window_is_active():
   return
  # Cada delta físico é guardado individualmente com seu instante real.
  self.events.append({"t":time.monotonic()-self.record_started,
                      "type":"mouse_move","dx":int(dx),"dy":int(dy)})

 def normalize_key(self,key):
  try:
   if hasattr(key,"char") and key.char:
    return key.char.lower()
   name=str(key).replace("Key.","").lower()
   aliases={"space":"space","enter":"enter","esc":"esc","tab":"tab",
            "shift":"shift","shift_r":"right shift","ctrl":"ctrl","ctrl_r":"right ctrl",
            "alt":"alt","alt_gr":"alt"}
   return aliases.get(name,name)
  except Exception:
   return None

 def on_keyboard_event(self,event):
  """Recebe eventos globais; F9 sempre tem prioridade para parar o macro."""
  name=str(getattr(event,"name","") or "").lower()
  kind=str(getattr(event,"event_type","")).lower()
  if name=="f9" and kind=="down" and self.running:
   self.hotkey_stop()
   return
  if not self.recording:
   return
  if not name or name in ("f8","f9","esc"):
   return
  # Exige foco do jogo para key_down, mas nunca descarte key_up por troca de foco.
  if kind == "down" and not self.game_window_is_active():
   return
  kind=str(getattr(event,"event_type","" )).lower()
  if kind=="down":
   if name in self.pressed_keys:
    return
   self.pressed_keys.add(name)
   self.events.append({"t":time.monotonic()-self.record_started,"type":"key_down","key":name})
  elif kind=="up" and name in self.pressed_keys:
   self.pressed_keys.discard(name)
   self.events.append({"t":time.monotonic()-self.record_started,"type":"key_up","key":name})
  self.root.after(0,self.render_route)

 def on_key_press(self,key):
  if not self.recording or not self.game_window_is_active():
   return
  name=self.normalize_key(key)
  if not name or name in ("f8","f9","esc") or name in self.pressed_keys:
   return
  self.pressed_keys.add(name)
  self.events.append({"t":time.monotonic()-self.record_started,"type":"key_down","key":name})

 def on_key_release(self,key):
  # A tecla pode ser solta durante uma troca rápida de foco; não descarte key_up.
  if not self.recording:
   return
  name=self.normalize_key(key)
  if name and name in self.pressed_keys:
   self.pressed_keys.discard(name)
   self.events.append({"t":time.monotonic()-self.record_started,"type":"key_up","key":name})

 def stop_record(self):
  # PARAR encerra a captura E qualquer reprodução/macro que esteja em andamento.
  self.running=False
  self.playback_stop.set()
  self.release_inputs()
  # Fecha qualquer tecla ainda marcada como pressionada na gravação.
  # Isso evita que uma rota termine sem o key_up correspondente.
  stop_t=time.monotonic()-self.record_started
  for key in list(self.pressed_keys):
   self.events.append({"t":stop_t,"type":"key_up","key":key})
  self.pressed_keys.clear()
  self.recording=False
  if self.mouse_listener:
   try:self.mouse_listener.stop()
   except Exception:pass
   self.mouse_listener=None
  if self.key_listener:
   try:self.key_listener.stop()
   except Exception:pass
   self.key_listener=None
  if self.key_hook is not None and keyboard:
   try:keyboard.unhook(self.key_hook)
   except Exception:pass
   self.key_hook=None
  self.pressed_keys.clear()
  self.mouse_buttons.clear()
  self.last_mouse_pos=None
  self.events.sort(key=lambda e:e.get("t",0))
  self.status.config(text=f"Gravação encerrada: {len(self.events)} ações.")
  self.render_route()

 def render_route(self):
  if hasattr(self,"routebox"):
   self.routebox.delete("1.0","end")
   for i,e in enumerate(self.events):
    if e["type"]=="click":
     line=f'{i+1}. {e["t"]:.2f}s | CLIQUE {e["button"]} | X={e["x"]} Y={e["y"]} (relativo ao jogo)'
    elif e["type"] in ("mouse_down","mouse_up"):
     line=f'{i+1}. {e["t"]:.2f}s | {e["type"].upper()} {e["button"]}'
    elif e["type"]=="mouse_move":
     line=f'{i+1}. {e["t"]:.2f}s | MOUSE RELATIVO dx={e["dx"]} dy={e["dy"]}'
    else:
     line=f'{i+1}. {e["t"]:.2f}s | {e["type"].upper()} {e.get("key","")}'
    self.routebox.insert("end",line+"\\n")
  self.count.config(text=f"Passos Gravados: {len(self.events)}")

 def clear_route(self):
  self.stop_record()
  self.events=[]
  self.route_points=[]
  self.render_route()

 def start_camera_sweep(self):
  # Desativado para evitar que a câmera deslize sozinha para os lados.
  self.camera_sweep_requested=False
  return

 def send_relative_mouse(self,dx,dy):
  """Envia deslocamento relativo e deixa o Windows agrupar eventos muito próximos.

  Em jogos que capturam o mouse, cada delta gravado deve chegar separadamente;
  MOVE_NOCOALESCE evita que o Windows funda movimentos consecutivos.
  """
  class MOUSEINPUT(ctypes.Structure):
   _fields_=[("dx",ctypes.c_long),("dy",ctypes.c_long),("mouseData",ctypes.c_ulong),
             ("dwFlags",ctypes.c_ulong),("time",ctypes.c_ulong),("dwExtraInfo",ctypes.c_void_p)]
  class INPUT_UNION(ctypes.Union):
   _fields_=[("mi",MOUSEINPUT)]
  class INPUT(ctypes.Structure):
   _fields_=[("type",ctypes.c_ulong),("union",INPUT_UNION)]
  # MOUSEEVENTF_MOVE | MOUSEEVENTF_MOVE_NOCOALESCE: preserva cada delta
  # relativo gravado, em vez de fundir movimentos rápidos consecutivos.
  flags=0x0001 | 0x2000  # MOVE + MOVE_NOCOALESCE
  item=INPUT(); item.type=0; item.union.mi=MOUSEINPUT(int(dx),int(dy),0,flags,0,None)
  sent=ctypes.windll.user32.SendInput(1,ctypes.byref(item),ctypes.sizeof(INPUT))
  if sent != 1:
   raise ctypes.WinError()

 def execute_route(self,bot_mode=False):
  if pdi is None or not self.events:
   return
  rect=self.find_game_window()
  if not rect:
   self.root.after(0,lambda:self.status.config(text="Janela do jogo não encontrada; rota não executada."))
   return
  # Salva a posição do cursor e garante a soltura de TODAS as teclas/botões,
  # inclusive se a reprodução falhar. Movimento relativo via Windows SendInput.
  held_keys=set(); held_buttons=set()
  # pydirectinput aplica uma pausa padrao apos CADA comando. Em rotas com
  # muitos deltas de mouse isso cria travadas artificiais. Desative-a apenas
  # durante a reproducao; os tempos gravados ja controlam o ritmo.
  old_pause=getattr(pdi,"PAUSE",0.1)
  pdi.PAUSE=0
  playback_start=time.perf_counter()
  try:
   for event in sorted(list(self.events), key=lambda item:item.get("t",0)):
    # F9 interrompe a rota do F8 imediatamente; o finally solta tudo.
    if self.playback_stop.is_set() or (bot_mode and not self.running):
     break
    # Agenda pelo relógio monotônico absoluto para reduzir deriva e
    # preservar os intervalos curtos entre movimentos consecutivos.
    target=playback_start+max(0.0,float(event.get("t",0)))
    while True:
     remaining=target-time.perf_counter()
     if remaining <= 0: break
     if self.playback_stop.is_set() or (bot_mode and not self.running): break
     if remaining > 0.004: time.sleep(min(remaining-0.002,0.01))
    if self.playback_stop.is_set() or (bot_mode and not self.running):
     break
    if event["type"]=="click":
     pdi.click(rect[0]+event["x"],rect[1]+event["y"],button=event.get("button","left"))
    elif event["type"]=="mouse_down":
     btn=event.get("button","right"); pdi.mouseDown(button=btn); held_buttons.add(btn)
     # Não inicia varredura automática independente. A câmera só recebe
     # os movimentos mouse_move que foram realmente gravados na rota.
    elif event["type"]=="mouse_up":
     btn=event.get("button","right")
     # Sempre libera o botão ao fim do arraste; não o mantém pressionado
     # entre ciclos, evitando câmera/cursor presos ou movimento contínuo.
     pdi.mouseUp(button=btn); held_buttons.discard(btn)
     if btn=="right": self.camera_sweep_requested=False
    elif event["type"]=="mouse_move":
     dx=int(event.get("dx",0)); dy=int(event.get("dy",0))
     # SendInput com MOVE_NOCOALESCE evita que o Windows funda vários
     # pequenos deslocamentos num único movimento grande. Mantém relativo.
     self.send_relative_mouse(dx,dy)
    elif event["type"]=="key_down":
     key=event["key"]; pdi.keyDown(key); held_keys.add(key)
    elif event["type"]=="key_up":
     # Respeita a soltura gravada: quando o usuario solta ESPACO,
     # o bot tambem deve parar de atacar.
     key=event["key"]
     pdi.keyUp(key); held_keys.discard(key)
  except Exception as e:
   self.root.after(0,lambda err=str(e):self.status.config(text="Erro na reprodução: "+err))
  finally:
   for key in list(held_keys):
    try:pdi.keyUp(key)
    except Exception:pass
   # Trava de segurança: nunca deixa o ESPAÇO preso entre ciclos da rota.
   try:pdi.keyUp("space")
   except Exception:pass
   for btn in list(held_buttons):
    try:pdi.mouseUp(button=btn)
    except Exception:pass
   # Não reposiciona o cursor ao final: evita saltos involuntários.
   try:pdi.PAUSE=old_pause
   except Exception:pass
   if bot_mode and not self.running:
    self.unclip_cursor()

 def play_route(self):
  if not self.events:
   messagebox.showinfo("Rota","Grave cliques ou teclas no jogo primeiro.")
   return
  if not self.find_game_window():
   messagebox.showerror("Jogo não encontrado","Confira o título da janela na aba Jogo.")
   return
  self.playback_stop.clear()
  threading.Thread(target=self.test_route,daemon=True).start()

 def test_route(self):
  self.execute_route()
  if not self.playback_stop.is_set():
   self.root.after(0,lambda:self.status.config(text="Teste da rota concluído."))

 def save(self):
  path=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("Perfil JSON","*.json")],initialfile="loi_catfarm_perfil.json")
  if path:
   d={k:v.get() for k,v in self.v.items()};d["route_points"]=self.route_points;d["events"]=self.events
   Path(path).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
   self.status.config(text="Perfil salvo.")
 def load(self):
  path=filedialog.askopenfilename(filetypes=[("Perfil JSON","*.json")])
  if not path:return
  try:
   d=json.loads(Path(path).read_text(encoding="utf-8"))
   for k,val in d.items():
    if k=="route_points":self.route_points=val
    elif k=="events":self.events=val
    elif k in self.v:self.v[k].set(val)
   if not self.events and self.route_points:self.events=self.route_points
   self.render_route();self.status.config(text="Perfil carregado.")
  except Exception as e:messagebox.showerror("Erro",str(e))
 def tick(self):
  if self.running and self.started:
   s=int(time.time()-self.started);self.clock.config(text=f"Tempo: {s//3600:02}:{s//60%60:02}:{s%60:02}")
  self.root.after(500,self.tick)
 def close(self):
  self.stop();self.stop_record()
  self.raw_mouse_stop=True
  if self.raw_mouse_tid:
   try:
    user32=ctypes.WinDLL("user32",use_last_error=True)
    user32.PostThreadMessageW.argtypes=[ctypes.c_ulong,ctypes.c_uint,ctypes.c_size_t,ctypes.c_ssize_t]
    user32.PostThreadMessageW(self.raw_mouse_tid,0x0012,0,0)
   except Exception: pass
  if self.raw_mouse_thread and self.raw_mouse_thread is not threading.current_thread():
   self.raw_mouse_thread.join(timeout=1.0)
  if keyboard:
   try:keyboard.unhook_all()
   except:pass
  self.root.destroy()

if __name__=="__main__":
 root=tk.Tk();app=App(root);root.mainloop()
