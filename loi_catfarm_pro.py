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
from tkinter import ttk, filedialog, messagebox, colorchooser
import threading, time, json, random, os, sys, subprocess, shutil, webbrowser, urllib.request, hashlib, tempfile, re
from pathlib import Path
try:
    import cv2
    import numpy as np
    from PIL import ImageGrab
except Exception:
    cv2 = None
    np = None
    ImageGrab = None

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

BG="#202326"; PANEL="#292e33"; FIELD="#343a40"; BLUE="#167ba7"; PRIMARY=BLUE; CYAN="#35b9e8"
THEMES={
 "Dark Neon":{"bg":"#171b22","panel":"#222a35","field":"#303b49","primary":"#168bd2","accent":"#35c9f4","text":"#f2f6fa","muted":"#b8c5d1","header":"#10151c","button":"#168bd2"},
 "Dark Red":{"bg":"#1b1719","panel":"#2b2326","field":"#3b3034","primary":"#b83242","accent":"#ff5968","text":"#fff3f3","muted":"#d0bfc2","header":"#120e10","button":"#b83242"},
 "RGB":{"bg":"#171522","panel":"#252036","field":"#342b49","primary":"#874de8","accent":"#21d6c5","text":"#f7f3ff","muted":"#c9bddc","header":"#100d19","button":"#874de8"},
 "Personalizado":{"bg":"#202326","panel":"#292e33","field":"#343a40","primary":"#167ba7","accent":"#35b9e8","text":"#eeeeee","muted":"#aeb7bd","header":"#15191d","button":"#167ba7"}
,
 "Cyberpunk Neon":{"bg":"#100b1d","panel":"#211532","field":"#332047","primary":"#a020f0","accent":"#ff42f5","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#a020f0"},
 "RGB Gaming":{"bg":"#101018","panel":"#20202d","field":"#303044","primary":"#7c3aed","accent":"#00e5ff","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#7c3aed"},
 "Holográfico":{"bg":"#081a25","panel":"#123044","field":"#1b4054","primary":"#00bcd4","accent":"#9af7ff","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#00bcd4"},
 "Minimalista":{"bg":"#20242a","panel":"#2b3139","field":"#39424d","primary":"#64748b","accent":"#cbd5e1","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#64748b"},
 "Glassmorphism":{"bg":"#17152a","panel":"#292641","field":"#393653","primary":"#8b5cf6","accent":"#c4b5fd","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#8b5cf6"},
 "Neumorphism":{"bg":"#252a32","panel":"#303743","field":"#3b4552","primary":"#6d8eb5","accent":"#b7c8dc","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#6d8eb5"},
 "Militar Tático":{"bg":"#151b16","panel":"#222d23","field":"#303d31","primary":"#657d3d","accent":"#b4cf78","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#657d3d"},
 "Premium Dourado":{"bg":"#171512","panel":"#29251d","field":"#3a3327","primary":"#b58a32","accent":"#f2d27a","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#b58a32"},
 "Synthwave":{"bg":"#190d27","panel":"#2b1740","field":"#402052","primary":"#e843a6","accent":"#31d6ff","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#e843a6"},
 "Matrix":{"bg":"#07150c","panel":"#102719","field":"#1a3825","primary":"#168a36","accent":"#59ff79","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#168a36"},
 "Blue Electric":{"bg":"#081526","panel":"#102b4b","field":"#1a3d66","primary":"#087de0","accent":"#36c5ff","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#087de0"},
 "Clean Light":{"bg":"#edf1f5","panel":"#ffffff","field":"#e0e6ed","primary":"#2878c7","accent":"#1b456b","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#2878c7"},
 "Industrial":{"bg":"#1c2023","panel":"#2c3338","field":"#3b444a","primary":"#c06b25","accent":"#e6a45e","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#c06b25"},
 "Galaxy":{"bg":"#100d20","panel":"#211a38","field":"#30264d","primary":"#7651c8","accent":"#d1a6ff","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#7651c8"},
 "Anime Gamer":{"bg":"#171126","panel":"#2a1d40","field":"#3b2a59","primary":"#ec4899","accent":"#8be9fd","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#ec4899"},
 "Transparente":{"bg":"#18212b","panel":"#263543","field":"#35495a","primary":"#4aa3c7","accent":"#b5e8ff","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#4aa3c7"},
 "Flat Design":{"bg":"#202a35","panel":"#2d3b4a","field":"#3c4d5e","primary":"#2980b9","accent":"#5dade2","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#2980b9"},
 "Pixel Retro":{"bg":"#171b2b","panel":"#252d45","field":"#35415f","primary":"#e0a52b","accent":"#f6d365","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#e0a52b"},
 "Futurista Premium":{"bg":"#0c1423","panel":"#17253b","field":"#233752","primary":"#2563eb","accent":"#00d9ff","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#2563eb"},
 "Ocean Neon":{"bg":"#071c25","panel":"#103341","field":"#19495a","primary":"#008fa8","accent":"#42e8e0","text":"#f4f7fb","muted":"#b8c4d1","header":"#0b1019","button":"#008fa8"}
}
DEFAULT={
 "game_title":"NEWMT2",
 "mount_on":False,"mount_key":"1","mount_interval":1.0,
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
  self.multi_run_targets=[]; self.multi_broadcast_active=False
  self.multi_client_routes={}; self._recording_multi_key=None
  self.cycle4_events={1:[],2:[],3:[],4:[]}; self._cycle4_record_slot=None; self.cycle4_running=False; self.cycle4_stop=threading.Event(); self.cycle4_window_refs=[]; self.cycle4_window_map={}
  self.mouse_buttons=set(); self.last_mouse_pos=None; self.camera_sweep_active=False; self.camera_sweep_requested=False
  self.cursor_clipped=False; self.clip_guard_active=False
  self.raw_mouse_thread=None; self.raw_mouse_tid=None; self.raw_mouse_stop=False
  self.key_listener=None; self.key_hook=None; self.game_rect=None; self.record_started=0.0; self.pressed_keys=set()
  self._recording_target_hwnd=0; self._recording_target_window=None
  self._recording_waiting_focus=False; self._recording_capture_started=False
  self.build(); self.set_defaults(); self.load_appearance(); root.protocol("WM_DELETE_WINDOW",self.close)
  if keyboard:
   try:
    keyboard.add_hotkey("F5",lambda:root.after(0,self.toggle), suppress=False)
    keyboard.add_hotkey("F8",lambda:root.after(0,self.handle_f8_hotkey))
    keyboard.add_hotkey("F7",lambda:root.after(0,self.record_individual_hotkey), suppress=False)
    keyboard.add_hotkey("F6",lambda:root.after(0,self.record_mgp_hotkey), suppress=False)
    keyboard.add_hotkey("F9",lambda: self.hotkey_stop(), suppress=False, trigger_on_release=False)
    keyboard.on_press_key("f9",lambda event: self.hotkey_stop(), suppress=False)
   except Exception: pass
  self.potion_hotkey_handle=None
  self.apply_potion_hotkey(show_errors=False)
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
  self.label(head,"F7 individual • F6 gravar MGP • F5 ligar/desligar • F9 pausar","#e5c45d","#15191d").pack(side="right",padx=14)
  stats=tk.Frame(self.root,bg=PANEL); stats.pack(fill="x",padx=12,pady=8)
  self.clock=self.label(stats,"Tempo: 00:00:00"); self.clock.pack(side="left",padx=14,pady=8)
  self.count=self.label(stats,"Passos Gravados: 0"); self.count.pack(side="right",padx=14)
  self.nb=ttk.Notebook(self.root); self.nb.pack(fill="both",expand=True,padx=12,pady=4)
  self.pages={}; self.page_canvases={}
  for name in ("Módulos + Jogo","Cliques","Skills","Anti-Ban","Perfis","MGP Multicliente","Poções","Cores","Clientes & Automação","Ciclo 4 Etapas","TV","Spotify"):
   outer=tk.Frame(self.nb,bg=PANEL)
   self.nb.add(outer,text=name)
   canvas=tk.Canvas(outer,bg=PANEL,highlightthickness=0,borderwidth=0)
   scrollbar=ttk.Scrollbar(outer,orient="vertical",command=canvas.yview)
   canvas.configure(yscrollcommand=scrollbar.set)
   scrollbar.pack(side="right",fill="y")
   canvas.pack(side="left",fill="both",expand=True)
   content=tk.Frame(canvas,bg=PANEL)
   window_id=canvas.create_window((0,0),window=content,anchor="nw")
   content.bind("<Configure>",lambda e,c=canvas:c.configure(scrollregion=c.bbox("all")))
   canvas.bind("<Configure>",lambda e,c=canvas,w=window_id:c.itemconfigure(w,width=e.width))
   canvas.bind("<Enter>",lambda e,c=canvas:self._enable_wheel(c))
   canvas.bind("<Leave>",lambda e:self._disable_wheel())
   content.bind("<Enter>",lambda e,c=canvas:self._enable_wheel(c))
   content.bind("<Leave>",lambda e:self._disable_wheel())
   self.pages[name]=content
   self.page_canvases[name]=canvas
  # Alias keeps the existing page builders intact while combining their sections.
  self.pages["Módulos"] = self.pages["Módulos + Jogo"]
  self.pages["Jogo"] = self.pages["Módulos + Jogo"]
  self.make_modules(); self.make_game(); self.make_clicks(); self.make_skills(); self.make_antiban(); self.make_profiles(); self.make_multiclient(); self.make_potions(); self.make_appearance(); self.make_client_automation(); self.make_cycle4(); self.make_tv(); self.make_spotify()
  foot=tk.Frame(self.root,bg="#15191d"); foot.pack(fill="x",padx=12,pady=8)
  self.status=self.label(foot,"Status: Pausado",fg="#e5b45b",bg="#15191d",anchor="w"); self.status.pack(fill="x",padx=9,pady=6)
  bar=tk.Frame(foot,bg="#15191d"); bar.pack(fill="x",padx=6,pady=(0,7))
  self.button(bar,"▶ LIGAR BOT (F8)",self.start,"#20b968")
  self.button(bar,"Ⅱ PAUSAR (F9)",self.stop,"#247da8")
  self.button(bar,"■ LIMPAR ROTA",self.clear_route,"#d58232")
  tk.Button(bar,text="Salvar Configs",command=self.save,bg="#287ba8",fg="white",relief="flat").pack(side="right",padx=4)
  tk.Button(bar,text="↻ VERIFICAR / ATUALIZAR",command=self.check_updates,bg="#7b5bd6",fg="white",relief="flat").pack(side="right",padx=4)

 def make_cycle4(self):
  p=self.pages["Ciclo 4 Etapas"]
  self.section(p,"SEQUÊNCIA AUTOMÁTICA — 2 CLIENTES / 4 ETAPAS")
  self.label(p,"Configure qual janela será o Cliente 1 e qual será o Cliente 2. Grave cada etapa separadamente; a ordem de execução será 1 → 2 → 3 → 4, trocando o foco automaticamente assim que cada etapa terminar.",fg="#c7cdd2",wraplength=620,justify="left").pack(anchor="w",padx=14,pady=6)
  r=self.row(p); self.button(r,"ATUALIZAR JANELAS MGP",self.refresh_cycle4_windows,"#687b8c")
  self.cycle4_client1=tk.StringVar(value="")
  self.cycle4_client2=tk.StringVar(value="")
  r=self.row(p); self.label(r,"Cliente 1:").pack(side="left",padx=8)
  self.cycle4_combo1=ttk.Combobox(r,textvariable=self.cycle4_client1,state="readonly",width=54); self.cycle4_combo1.pack(side="left",padx=5)
  r=self.row(p); self.label(r,"Cliente 2:").pack(side="left",padx=8)
  self.cycle4_combo2=ttk.Combobox(r,textvariable=self.cycle4_client2,state="readonly",width=54); self.cycle4_combo2.pack(side="left",padx=5)
  self.section(p,"GRAVAÇÃO DAS ETAPAS")
  self.cycle4_stage=tk.IntVar(value=1)
  r=self.row(p); self.label(r,"Etapa para gravar:").pack(side="left",padx=8)
  ttk.Combobox(r,textvariable=self.cycle4_stage,values=[1,2,3,4],state="readonly",width=5).pack(side="left",padx=5)
  self.label(p,"Etapa 1 = Cliente 1 • Etapa 2 = Cliente 2 • Etapa 3 = Cliente 1 • Etapa 4 = Cliente 2",fg="#e5c45d",wraplength=620).pack(anchor="w",padx=14,pady=4)
  r=self.row(p); self.button(r,"● GRAVAR ETAPA SELECIONADA",self.start_cycle4_record,"#20845e"); self.button(r,"■ PARAR / SALVAR ETAPA",self.stop_record,"#a94d45")
  self.cycle4_status=self.label(p,"Nenhuma etapa gravada.",fg="#aeb7bd",wraplength=620,justify="left"); self.cycle4_status.pack(anchor="w",padx=14,pady=6)
  self.cycle4_stage_labels={}
  for n,who in [(1,"Cliente 1"),(2,"Cliente 2"),(3,"Cliente 1"),(4,"Cliente 2")]:
   v=self.label(p,f"Etapa {n} — {who}: ainda não gravada",fg="#d8e0e5")
   v.pack(anchor="w",padx=18,pady=2); self.cycle4_stage_labels[n]=v
  self.section(p,"EXECUÇÃO E CONFIGURAÇÕES")
  self.cycle4_repeat=tk.BooleanVar(value=False)
  self.cycle4_f8=tk.BooleanVar(value=False)
  r=self.row(p); ttk.Checkbutton(r,text="Repetir as quatro etapas continuamente",variable=self.cycle4_repeat).pack(side="left",padx=8,pady=5)
  r=self.row(p); ttk.Checkbutton(r,text="Usar F8 para iniciar este ciclo (substitui o F8 geral enquanto marcado)",variable=self.cycle4_f8).pack(side="left",padx=8,pady=5)
  r=self.row(p); self.button(r,"▶ INICIAR CICLO (F8)",self.start_cycle4,"#20b968"); self.button(r,"Ⅱ PARAR CICLO (F9)",self.stop_cycle4,"#247da8")
  r=self.row(p); self.button(r,"SALVAR CONFIGURAÇÃO",self.save_cycle4,"#596675"); self.button(r,"CARREGAR CONFIGURAÇÃO",self.load_cycle4,"#596675")
  self.label(p,"A alternância usa ativação normal de janelas visíveis e entrada comum do Windows. Não executa em segundo plano, não injeta código e não contorna o anti-cheat. O cursor pode se mover durante a reprodução.",fg="#e6bd70",wraplength=620,justify="left").pack(anchor="w",padx=14,pady=8)
  self.refresh_cycle4_windows(); self.update_cycle4_status()

 def refresh_cycle4_windows(self):
  """Enumera as janelas por HWND próprio; não depende da seleção da lista MGP."""
  if not hasattr(self,"cycle4_combo1"): return
  try:
   old1=self.cycle4_selected_window(1) if self.cycle4_window_map else None
   old2=self.cycle4_selected_window(2) if self.cycle4_window_map else None
   old_hwnd1=int(getattr(old1,"_hWnd",0) or 0) if old1 else 0
   old_hwnd2=int(getattr(old2,"_hWnd",0) or 0) if old2 else 0
   if gw is None:
    wins=[]
   else:
    title=str(self.v.get("game_title",tk.StringVar(value="NEWMT2")).get()).strip().lower()
    found=gw.getAllWindows()
    wins=[]; seen=set()
    for w in found:
     try:
      hwnd=int(getattr(w,"_hWnd",0) or 0)
      if not hwnd or not w.title or title not in w.title.lower() or int(w.width)<=0 or int(w.height)<=0 or hwnd in seen:
       continue
      seen.add(hwnd); wins.append(w)
     except Exception:
      continue
   self.cycle4_window_refs=list(wins)
   self.cycle4_window_map={}
   vals=[]
   for i,w in enumerate(wins):
    hwnd=int(getattr(w,"_hWnd",0) or 0)
    label=f"{i+1}. {w.title} [HWND {hwnd}]"
    vals.append(label); self.cycle4_window_map[label]=w
   self.cycle4_combo1["values"]=vals; self.cycle4_combo2["values"]=vals
   by_hwnd={int(getattr(w,"_hWnd",0) or 0):label for label,w in self.cycle4_window_map.items()}
   if vals:
    self.cycle4_client1.set(by_hwnd.get(old_hwnd1, vals[0]))
    default2=vals[1] if len(vals)>1 else vals[0]
    self.cycle4_client2.set(by_hwnd.get(old_hwnd2, default2))
    if len(vals)<2:
     self.cycle4_status.config(text="Só encontrei uma janela NEWMT2. Abra o segundo cliente e clique em ATUALIZAR JANELAS MGP.")
    elif self.cycle4_client1.get()==self.cycle4_client2.get():
     self.cycle4_status.config(text="Atenção: Cliente 1 e Cliente 2 apontam para a mesma janela. Escolha HWNDs diferentes.")
   else:
    self.cycle4_client1.set(""); self.cycle4_client2.set("")
    self.cycle4_status.config(text="Nenhuma janela NEWMT2 válida encontrada.")
   self.update_cycle4_status()
  except Exception as e:
   self.cycle4_status.config(text=f"Falha ao atualizar janelas: {e}")

 def cycle4_selected_window(self, client_num):
  choice=(self.cycle4_client1.get() if client_num==1 else self.cycle4_client2.get())
  return self.cycle4_window_map.get(choice)

 def update_cycle4_status(self):
  if not hasattr(self,"cycle4_stage_labels"): return
  for n,who in [(1,"Cliente 1"),(2,"Cliente 2"),(3,"Cliente 1"),(4,"Cliente 2")]:
   count=len(self.cycle4_events.get(n,[]))
   self.cycle4_stage_labels[n].config(text=f"Etapa {n} — {who}: {count} ações gravadas" if count else f"Etapa {n} — {who}: ainda não gravada")

 def start_cycle4_record(self):
  if self.recording or self.running or self.cycle4_running:
   messagebox.showwarning("Ciclo 4 Etapas","Pare a gravação ou os macros ativos antes de gravar uma etapa."); return
  slot=int(self.cycle4_stage.get())
  client_num=1 if slot in (1,3) else 2
  w1=self.cycle4_selected_window(1); w2=self.cycle4_selected_window(2)
  hwnd1=int(getattr(w1,"_hWnd",0) or 0) if w1 else 0
  hwnd2=int(getattr(w2,"_hWnd",0) or 0) if w2 else 0
  if not hwnd1 or not hwnd2 or hwnd1==hwnd2:
   messagebox.showwarning("Ciclo 4 Etapas","Escolha dois clientes diferentes nos campos Cliente 1 e Cliente 2. Confira os números HWND exibidos nas listas.")
   return
  target=self.cycle4_selected_window(client_num)
  if target is None:
   messagebox.showwarning("Ciclo 4 Etapas",f"Selecione uma janela válida para o Cliente {client_num}."); return
  if not self.activate_target_window(target,allow_when_stopped=True):
   messagebox.showerror("Ciclo 4 Etapas",f"Não consegui ativar {target.title}. A gravação não começou."); return
  self._recording_target_window=target
  self._recording_target_hwnd=int(getattr(target,"_hWnd",0) or 0)
  self._cycle4_record_slot=slot
  self.record_route()
  if self.recording:
   self.cycle4_status.config(text=f"Gravando etapa {slot} em {target.title} (HWND {self._recording_target_hwnd}). Clique em PARAR / SALVAR ETAPA quando terminar.")
  else:
   self._cycle4_record_slot=None

 def save_cycle4_recorded_stage(self):
  slot=self._cycle4_record_slot
  if slot is None: return
  self.cycle4_events[int(slot)]=list(self.events)
  self._cycle4_record_slot=None
  self.update_cycle4_status()
  self.cycle4_status.config(text=f"Etapa {slot} salva com {len(self.cycle4_events[int(slot)])} ações.")

 def handle_f8_hotkey(self):
  if hasattr(self,"cycle4_f8") and self.cycle4_f8.get():
   self.start_cycle4()
  else:
   self.toggle()

 def start_cycle4(self):
  if self.recording or self.running or self.cycle4_running:
   messagebox.showwarning("Ciclo 4 Etapas","Finalize a gravação e pare outros macros antes de iniciar."); return
  missing=[n for n in range(1,5) if not self.cycle4_events.get(n)]
  if missing:
   messagebox.showwarning("Ciclo 4 Etapas","Grave todas as quatro etapas. Faltam: "+", ".join(map(str,missing))); return
  w1=self.cycle4_selected_window(1); w2=self.cycle4_selected_window(2)
  if not w1 or not w2 or int(getattr(w1,"_hWnd",0))==int(getattr(w2,"_hWnd",0)):
   messagebox.showwarning("Ciclo 4 Etapas","Selecione dois clientes diferentes."); return
  if pdi is None:
   messagebox.showerror("Dependências","Execute ABRIR_AQUI.bat para instalar as dependências."); return
  self.cycle4_stop.clear(); self.cycle4_running=True
  threading.Thread(target=self.cycle4_worker,args=(w1,w2),daemon=True).start()
  self.cycle4_status.config(text="Ciclo iniciado: 1 → 2 → 3 → 4.")

 def cycle4_worker(self,w1,w2):
  try:
   while not self.cycle4_stop.is_set():
    for slot,target in [(1,w1),(2,w2),(3,w1),(4,w2)]:
     if self.cycle4_stop.is_set(): break
     self.root.after(0,lambda n=slot,t=target:self.cycle4_status.config(text=f"Ativando {t.title} — etapa {n}/4"))
     if not self.activate_target_window(target,allow_when_stopped=True):
      raise RuntimeError(f"Não foi possível confirmar o foco de {target.title}; ciclo interrompido por segurança.")
     time.sleep(self.multi_delay())
     rect=(int(target.left),int(target.top),int(target.width),int(target.height))
     original=self.events
     self.events=list(self.cycle4_events[slot])
     self.playback_stop.clear()
     try:
      ok=self.execute_route_for_rect(rect,bot_mode=False,expected_hwnd=int(getattr(target,"_hWnd",0)))
     finally:
      self.events=original
     if not ok:
      raise RuntimeError(f"Etapa {slot} interrompida: foco não confirmado ou entrada não liberada.")
     self.root.after(0,lambda n=slot:self.cycle4_status.config(text=f"Etapa {n} concluída; próxima troca automática."))
     time.sleep(0.10)
    if not self.cycle4_repeat.get() or self.cycle4_stop.is_set(): break
  except Exception as e:
   self.root.after(0,lambda err=str(e):self.cycle4_status.config(text="Ciclo parado: "+err))
  finally:
   self.cycle4_running=False
   if self.cycle4_stop.is_set(): self.root.after(0,lambda:self.cycle4_status.config(text="Ciclo pausado pelo usuário."))
   elif not self.cycle4_repeat.get(): self.root.after(0,lambda:self.cycle4_status.config(text="As quatro etapas foram concluídas."))

 def stop_cycle4(self):
  if self.cycle4_running:
   self.cycle4_stop.set(); self.playback_stop.set()
   self.cycle4_status.config(text="Solicitando parada segura do ciclo...")

 def save_cycle4(self):
  path=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("Ciclo 4 Etapas","*.json")],initialfile="Ciclo_4_Etapas.json")
  if not path:return
  data={"format":2,"events":self.cycle4_events,"client1":self.cycle4_client1.get(),"client2":self.cycle4_client2.get(),"client1_hwnd":int(getattr(self.cycle4_selected_window(1),"_hWnd",0) or 0),"client2_hwnd":int(getattr(self.cycle4_selected_window(2),"_hWnd",0) or 0),"repeat":self.cycle4_repeat.get(),"f8_cycle":self.cycle4_f8.get()}
  Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
  self.cycle4_status.config(text="Configuração do ciclo salva.")

 def load_cycle4(self):
  path=filedialog.askopenfilename(filetypes=[("Ciclo 4 Etapas","*.json")])
  if not path:return
  try:
   data=json.loads(Path(path).read_text(encoding="utf-8"))
   ev=data.get("events",{})
   self.cycle4_events={i:ev.get(str(i),ev.get(i,[])) for i in range(1,5)}
   self.cycle4_repeat.set(bool(data.get("repeat",False)))
   self.cycle4_f8.set(bool(data.get("f8_cycle",False)))
   self.refresh_cycle4_windows()
   for attr,key,hwnd_key in [("cycle4_client1","client1","client1_hwnd"),("cycle4_client2","client2","client2_hwnd")]:
    val=data.get(key,"")
    wanted=int(data.get(hwnd_key,0) or 0)
    match=next((label for label,w in self.cycle4_window_map.items() if wanted and int(getattr(w,"_hWnd",0) or 0)==wanted),None)
    if match: getattr(self,attr).set(match)
    elif val in self.cycle4_combo1["values"]: getattr(self,attr).set(val)
   self.update_cycle4_status(); self.cycle4_status.config(text="Configuração do ciclo carregada.")
  except Exception as e: messagebox.showerror("Ciclo 4 Etapas",str(e))

 def make_tv(self):
  p=self.pages["TV"]
  self.tv_profiles=[]; self.tv_channels=[]; self.tv_player=None; self.tv_vlc=None; self.tv_vlc_events=[]; self.tv_full=None; self.tv_pip=None; self.tv_pip_frame=None
  self.tv_profile_var=tk.StringVar(); self.tv_type_var=tk.StringVar(value="Xtream Codes"); self.tv_search_var=tk.StringVar(value="")
  self.tv_name_var=tk.StringVar(value="Meu servidor"); self.tv_url_var=tk.StringVar(); self.tv_user_var=tk.StringVar(); self.tv_pass_var=tk.StringVar(); self.tv_key_var=tk.StringVar(); self.tv_mac_var=tk.StringVar()
  self.section(p,"CENTRAL DE TV — CADASTRE SUA PRÓPRIA ASSINATURA")
  self.label(p,"Use somente servidores e assinaturas aos quais você tem autorização. Os dados ficam salvos localmente neste computador.",fg="#e5c45d",wraplength=650,justify="left").pack(anchor="w",padx=14,pady=4)
  row=self.row(p); self.label(row,"Conexão").pack(side="left",padx=5)
  ttk.Combobox(row,textvariable=self.tv_type_var,values=["Xtream Codes","M3U / URL","Stalker Portal","Lista local"],state="readonly",width=18).pack(side="left",padx=4)
  self.label(row,"Nome").pack(side="left",padx=5); tk.Entry(row,textvariable=self.tv_name_var,width=22,bg=FIELD,fg="white",insertbackground="white").pack(side="left",padx=4)
  for title,var,show in [("Servidor / URL",self.tv_url_var,None),("Usuário",self.tv_user_var,None),("Senha",self.tv_pass_var,"•"),("Chave / Token",self.tv_key_var,"•"),("MAC Stalker",self.tv_mac_var,None)]:
   r=self.row(p); self.label(r,title).pack(side="left",padx=5); tk.Entry(r,textvariable=var,show=show,width=78,bg=FIELD,fg="white",insertbackground="white").pack(side="left",fill="x",expand=True,padx=5,ipady=4)
  r=self.row(p)
  self.button(r,"SALVAR SERVIDOR",self.tv_save_profile)
  self.button(r,"CARREGAR LISTA LOCAL",self.tv_load_local)
  self.button(r,"CONECTAR / BUSCAR CANAIS",self.tv_connect)
  r=self.row(p); self.label(r,"Servidor salvo").pack(side="left",padx=5)
  self.tv_profile_combo=ttk.Combobox(r,textvariable=self.tv_profile_var,state="readonly",width=40); self.tv_profile_combo.pack(side="left",padx=5)
  self.button(r,"USAR SERVIDOR",self.tv_use_profile); self.button(r,"EXCLUIR",self.tv_delete_profile,"#9b3434")
  self.section(p,"ASSISTIR AGORA — PLAYER INTEGRADO")
  controls=self.row(p); self.button(controls,"▶ PLAY",self.tv_play); self.button(controls,"Ⅱ PAUSAR",self.tv_pause); self.button(controls,"■ PARAR",self.tv_stop); self.button(controls,"⛶ TELA CHEIA",self.tv_fullscreen); self.button(controls,"▣ PIP",self.tv_picture_in_picture)
  body=tk.Frame(p,bg=PANEL); body.pack(fill="both",expand=True,padx=10,pady=5)
  self.tv_video=tk.Frame(body,bg="black",height=330); self.tv_video.pack(side="left",fill="both",expand=True); self.tv_video.pack_propagate(False)
  self.tv_placeholder=tk.Label(self.tv_video,text="LOI TV\nConecte seu servidor e selecione um canal",bg="black",fg="#cbd5e1",font=("Segoe UI",14,"bold")); self.tv_placeholder.place(relx=.5,rely=.5,anchor="center")
  right=tk.Frame(body,bg=PANEL,width=260); right.pack(side="right",fill="y",padx=(8,0)); right.pack_propagate(False)
  self.label(right,"CANAIS E CATEGORIAS",CYAN,PANEL,font=("Segoe UI",10,"bold")).pack(anchor="w",pady=4)
  self.tv_category=tk.StringVar(value="Todos")
  self.tv_cat_combo=ttk.Combobox(right,textvariable=self.tv_category,values=["Todos"],state="readonly"); self.tv_cat_combo.pack(fill="x",pady=3); self.tv_cat_combo.bind("<<ComboboxSelected>>",lambda e:self.tv_render_channels())
  self.tv_search_entry=ttk.Entry(right,textvariable=self.tv_search_var); self.tv_search_entry.pack(fill="x",pady=(2,4)); self.tv_search_entry.insert(0, "")
  self.tv_search_entry.bind("<KeyRelease>",lambda e:self.tv_render_channels())
  self.tv_list=tk.Listbox(right,bg="#151a22",fg="white",selectbackground=BLUE,relief="flat"); self.tv_list.pack(fill="both",expand=True,pady=3); self.tv_list.bind("<Double-Button-1>",lambda e:self.tv_play())
  r=tk.Frame(right,bg=PANEL); r.pack(fill="x"); self.button(r,"ASSISTIR",self.tv_play)
  self.tv_status=self.label(p,"Status: aguardando conexão",fg="#e5b45b",wraplength=700,justify="left"); self.tv_status.pack(anchor="w",padx=14,pady=6)
  self.tv_load_profiles()

 def make_spotify(self):
  p=self.pages["Spotify"]
  self.spotify_hwnd=None; self.spotify_process=None
  self.spotify_profile_dir=Path(os.environ.get("LOCALAPPDATA",str(Path.home()))) / "LOI_CATFARM_PRO" / "SpotifyWebView2Profile"
  self.spotify_helper=Path(__file__).with_name("spotify_webview_host.py")
  self.section(p,"SPOTIFY — REPRODUÇÃO DENTRO DO LOI CATFARM PRO")
  self.label(p,"Spotify incorporado ao painel usando Microsoft Edge WebView2. Entre na sua própria conta; as regras de reprodução do Spotify continuam valendo.",fg="#e5c45d",wraplength=760,justify="left").pack(anchor="w",padx=14,pady=6)
  bar=self.row(p)
  self.button(bar,"▶ CONECTAR / ABRIR NO PAINEL",self.spotify_start_embedded,"#168b50")
  self.button(bar,"↻ RECARREGAR",self.spotify_reload)
  self.button(bar,"ABRIR NO NAVEGADOR",self.spotify_open_web,"#303b49")
  self.button(bar,"FECHAR PLAYER",self.spotify_close_embedded,"#8b3434")
  host=tk.Frame(p,bg="#05080d",highlightthickness=1,highlightbackground="#303b49",height=510)
  host.pack(fill="both",expand=True,padx=14,pady=8)
  host.pack_propagate(False)
  self.spotify_host=host
  self.spotify_placeholder=tk.Label(host,text="♫  SPOTIFY\n\nClique em CONECTAR para abrir o Spotify aqui dentro.\n\nO painel usa WebView2; não abre uma janela externa do Edge.",bg="#05080d",fg="#dce6ef",font=("Segoe UI",14,"bold"),justify="center")
  self.spotify_placeholder.place(relx=.5,rely=.5,anchor="center")
  host.bind("<Configure>",lambda e:self.spotify_resize_embedded())
  self.spotify_status=self.label(p,"Status: aguardando para abrir o Spotify no painel.",fg="#b8c5d1",wraplength=760,justify="left")
  self.spotify_status.pack(anchor="w",padx=14,pady=(0,8))

 def spotify_start_embedded(self):
  if os.name!="nt":
   self.spotify_status.config(text="O player incorporado requer Windows com WebView2."); return
  if self.spotify_process and self.spotify_process.poll() is None:
   self.spotify_resize_embedded(); self.spotify_status.config(text="Spotify WebView2 já está iniciado no painel."); return
  if not self.spotify_helper.is_file():
   self.spotify_status.config(text="Arquivo spotify_webview_host.py não encontrado na pasta do macro."); return
  try:
   self.spotify_profile_dir.mkdir(parents=True,exist_ok=True)
   pythonw=Path(sys.executable).with_name("pythonw.exe")
   executable=str(pythonw if pythonw.is_file() else Path(sys.executable))
   flags=getattr(subprocess,"CREATE_NO_WINDOW",0)
   self.spotify_process=subprocess.Popen([executable,str(self.spotify_helper),str(int(self.spotify_host.winfo_id())),str(self.spotify_profile_dir)],cwd=str(self.spotify_helper.parent),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=flags)
   self.spotify_placeholder.place_forget()
   self.spotify_status.config(text="Iniciando Spotify incorporado com WebView2... aguarde alguns segundos.")
   self.root.after(1800,self.spotify_check_embedded)
  except Exception as e:
   self.spotify_status.config(text=f"Não foi possível iniciar o WebView2: {e}")

 def spotify_check_embedded(self):
  if self.spotify_process and self.spotify_process.poll() is not None:
   err=self.spotify_profile_dir.parent / "spotify_webview_error.txt"
   detail=""
   try: detail=err.read_text(encoding="utf-8")
   except Exception: pass
   self.spotify_status.config(text="O WebView2 não iniciou. Instale o Microsoft Edge WebView2 Runtime e confirme que pywebview foi instalado. "+detail)
   self.spotify_placeholder.place(relx=.5,rely=.5,anchor="center")
  elif self.spotify_process:
   self.spotify_status.config(text="Spotify WebView2 iniciado. Se o painel ainda estiver vazio, aguarde o carregamento ou clique em RECARREGAR.")

 def spotify_resize_embedded(self):
  # O helper WebView2 é filho nativo do frame; ao redimensionar, o Windows atualiza o filho.
  if not self.spotify_process or self.spotify_process.poll() is not None:return
  try:
   self.spotify_host.update_idletasks()
   user32=ctypes.windll.user32
   hwnd_parent=self.spotify_host.winfo_id()
   # Localiza a janela filha criada pelo processo helper e ajusta ao tamanho do painel.
   found=[]
   enum_cb=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_void_p)
   def cb(hwnd,extra):
    pid=ctypes.c_ulong(); user32.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
    if pid.value==self.spotify_process.pid and user32.IsWindowVisible(hwnd):found.append(hwnd)
    return True
   user32.EnumChildWindows(hwnd_parent,enum_cb(cb),0)
   if found:
    user32.MoveWindow(found[0],0,0,max(1,self.spotify_host.winfo_width()),max(1,self.spotify_host.winfo_height()),True)
  except Exception:pass

 def spotify_reload(self):
  self.spotify_close_embedded()
  self.root.after(500,self.spotify_start_embedded)

 def spotify_close_embedded(self):
  proc=self.spotify_process; self.spotify_process=None
  if proc and proc.poll() is None:
   try:proc.terminate(); proc.wait(timeout=2)
   except Exception:
    try:proc.kill()
    except Exception:pass
  self.spotify_placeholder.place(relx=.5,rely=.5,anchor="center")
  self.spotify_status.config(text="Player Spotify fechado. O perfil local mantém a sessão quando o serviço permite.")

 def spotify_open_web(self):
  webbrowser.open("https://open.spotify.com/")
  self.spotify_status.config(text="Spotify aberto no navegador padrão.")

 def tv_store_path(self): return Path(__file__).with_name("loi_catfarm_tv.json")
 def tv_load_profiles(self):
  try: self.tv_profiles=json.loads(self.tv_store_path().read_text(encoding="utf-8"))
  except Exception: self.tv_profiles=[]
  self.tv_profile_combo["values"]=[x.get("name","Servidor") for x in self.tv_profiles]
  if self.tv_profiles: self.tv_profile_combo.current(0)
 def tv_save_profile(self):
  item={"name":self.tv_name_var.get().strip() or "Servidor","type":self.tv_type_var.get(),"url":self.tv_url_var.get().strip(),"user":self.tv_user_var.get(),"password":self.tv_pass_var.get(),"key":self.tv_key_var.get(),"mac":self.tv_mac_var.get()}
  if not item["url"] and item["type"]!="Lista local": messagebox.showwarning("TV","Informe o endereço do servidor/URL."); return
  self.tv_profiles=[x for x in self.tv_profiles if x.get("name")!=item["name"]]; self.tv_profiles.append(item)
  self.tv_store_path().write_text(json.dumps(self.tv_profiles,ensure_ascii=False,indent=2),encoding="utf-8"); self.tv_load_profiles(); self.tv_profile_var.set(item["name"]); self.tv_status.config(text="Servidor salvo neste computador.")
 def tv_use_profile(self):
  name=self.tv_profile_var.get(); item=next((x for x in self.tv_profiles if x.get("name")==name),None)
  if not item:return
  self.tv_type_var.set(item.get("type","Xtream Codes")); self.tv_name_var.set(item.get("name","")); self.tv_url_var.set(item.get("url","")); self.tv_user_var.set(item.get("user","")); self.tv_pass_var.set(item.get("password","")); self.tv_key_var.set(item.get("key","")); self.tv_mac_var.set(item.get("mac",""))
 def tv_delete_profile(self):
  name=self.tv_profile_var.get(); self.tv_profiles=[x for x in self.tv_profiles if x.get("name")!=name]; self.tv_store_path().write_text(json.dumps(self.tv_profiles,ensure_ascii=False,indent=2),encoding="utf-8"); self.tv_load_profiles()
 def tv_load_local(self):
  f=filedialog.askopenfilename(filetypes=[("Listas M3U","*.m3u *.m3u8"),("Todos os arquivos","*.*")])
  if f: self.tv_parse_m3u(Path(f).read_text(encoding="utf-8",errors="replace")); self.tv_status.config(text=f"Lista local carregada: {len(self.tv_channels)} canais.")
 def tv_connect(self):
  typ=self.tv_type_var.get(); url=self.tv_url_var.get().strip()
  if typ=="Lista local": self.tv_load_local(); return
  if typ=="Stalker Portal":
   messagebox.showinfo("Stalker Portal","Os dados do portal, MAC e token podem ser cadastrados e salvos. A busca automática de canais Stalker ainda precisa do formato/API específico fornecido pelo seu servidor."); return
  if not url: messagebox.showwarning("TV","Informe o servidor ou URL."); return
  try:
   import urllib.request, urllib.parse
   if typ=="M3U / URL":
    req=urllib.request.Request(url,headers={"User-Agent":"LOI-CATFARM-PRO/1.0"})
    data=urllib.request.urlopen(req,timeout=20).read().decode("utf-8-sig",errors="replace"); self.tv_parse_m3u(data)
   else:
    base=url.rstrip("/"); query=urllib.parse.urlencode({"username":self.tv_user_var.get(),"password":self.tv_pass_var.get()})
    req=urllib.request.Request(base+"/player_api.php?"+query,headers={"User-Agent":"LOI-CATFARM-PRO/1.0"})
    info=json.loads(urllib.request.urlopen(req,timeout=20).read().decode("utf-8",errors="replace"))
    cats={str(x.get("category_id")):x.get("category_name","Sem categoria") for x in info.get("categories",[])}
    channels=[]
    for kind,ext in [("live","ts"),("movie","mp4"),("series","mp4")]:
     req=urllib.request.Request(base+f"/player_api.php?{query}&action=get_{kind}_streams",headers={"User-Agent":"LOI-CATFARM-PRO/1.0"})
     try: arr=json.loads(urllib.request.urlopen(req,timeout=25).read().decode("utf-8",errors="replace"))
     except Exception: arr=[]
     for x in arr if isinstance(arr,list) else []:
      sid=x.get("stream_id") or x.get("series_id"); name=x.get("name") or x.get("title") or "Canal"; cat=cats.get(str(x.get("category_id")),kind.title())
      channels.append({"name":name,"group":cat,"url":f"{base}/{self.tv_user_var.get()}/{self.tv_pass_var.get()}/{sid}.{ext}"})
    self.tv_channels=channels; self.tv_refresh_categories(); self.tv_status.config(text=f"Conectado: {len(channels)} itens encontrados.")
  except Exception as e: messagebox.showerror("Falha ao conectar",str(e)); self.tv_status.config(text="Não foi possível carregar os canais. Confira URL, usuário, senha e acesso do servidor.")
 def tv_parse_m3u(self,data):
  import re
  channels=[]; name="Canal"; group="Sem categoria"
  for line in data.splitlines():
   line=line.strip()
   if line.startswith("#EXTINF"):
    name=line.split(",",1)[-1].strip() or "Canal"; m=re.search(r'group-title=["\']([^"\']+)',line); group=m.group(1) if m else "Sem categoria"
   elif line and not line.startswith("#") and line.startswith(("http://","https://","rtsp://")):
    channels.append({"name":name,"group":group,"url":line}); name="Canal"; group="Sem categoria"
  self.tv_channels=channels; self.tv_refresh_categories()
 def tv_refresh_categories(self):
  cats=["Todos"]+sorted({x.get("group","Sem categoria") for x in self.tv_channels}); self.tv_cat_combo["values"]=cats; self.tv_category.set("Todos"); self.tv_render_channels(); self.tv_status.config(text=f"Lista carregada: {len(self.tv_channels)} canais/itens.")
 def tv_render_channels(self):
  if not hasattr(self,"tv_list"):return
  self.tv_list.delete(0,"end"); cat=self.tv_category.get()
  term=self.tv_search_var.get().strip().casefold()
  self.tv_visible=[x for x in self.tv_channels if (cat=="Todos" or x.get("group")==cat) and (not term or term in x.get("name","").casefold() or term in x.get("group","").casefold())]
  for x in self.tv_visible:self.tv_list.insert("end",x.get("name","Canal"))
 def tv_selected(self):
  sel=self.tv_list.curselection(); return self.tv_visible[sel[0]] if sel and sel[0]<len(self.tv_visible) else None
 def _tv_load_vlc(self):
  """Carrega primeiro o VLC portátil distribuído junto ao LOI; usa o instalado como reserva."""
  import os
  from pathlib import Path
  if getattr(self, "_tv_vlc_dir", None) and (self._tv_vlc_dir/"libvlc.dll").is_file():
   vlc_dir=self._tv_vlc_dir
  else:
   root=Path(__file__).resolve().parent
   candidates=[root/"VLC_Portable", root/"VLC_Portable"/"vlc-3.0.24", root/"VLC"]
   # O ZIP oficial contém uma pasta-raiz versionada; procura libvlc.dll sem
   # depender do nome exato dessa pasta.
   for folder in (root/"VLC_Portable", root/"VLC"):
    if folder.is_dir():
     try: candidates.extend(p.parent for p in folder.rglob("libvlc.dll"))
     except OSError: pass
   for envname in ("ProgramFiles", "ProgramFiles(x86)"):
    base=os.environ.get(envname)
    if base: candidates.append(Path(base)/"VideoLAN"/"VLC")
   candidates.extend([Path(r"C:\Program Files\VideoLAN\VLC"), Path(r"C:\Program Files (x86)\VideoLAN\VLC")])
   vlc_dir=next((x for x in candidates if (x/"libvlc.dll").is_file()), None)
   if vlc_dir is None:
    raise RuntimeError("O VLC portátil ainda não foi preparado. Feche o macro e execute ABRIR_AQUI.bat com internet para baixar a versão oficial automaticamente.")
   self._tv_vlc_dir=vlc_dir
  # Registra DLLs nativas antes de importar python-vlc.
  if hasattr(os, "add_dll_directory"):
   try: self._tv_dll_handle=os.add_dll_directory(str(vlc_dir))
   except OSError: pass
  os.environ["PYTHON_VLC_LIB_PATH"]=str(vlc_dir/"libvlc.dll")
  os.environ["PYTHON_VLC_MODULE_PATH"]=str(vlc_dir/"plugins")
  os.environ["VLC_PLUGIN_PATH"]=str(vlc_dir/"plugins")
  # Algumas dependencias nativas do VLC procuram DLLs na pasta principal.
  os.environ["PATH"]=str(vlc_dir)+os.pathsep+os.environ.get("PATH","")
  import vlc
  return vlc

 def _tv_bind_vlc_events(self):
  """Atualiza o estado real do player; play() sozinho nao confirma que abriu o fluxo."""
  if not self.tv_player or self.tv_vlc_events:
   return
  try:
   manager=self.tv_player.event_manager()
   event_map=[
    (self._tv_load_vlc().EventType.MediaPlayerOpening,"Abrindo conexão com o canal..."),
    (self._tv_load_vlc().EventType.MediaPlayerBuffering,"Canal conectado; carregando buffer..."),
    (self._tv_load_vlc().EventType.MediaPlayerPlaying,"Reproduzindo canal ao vivo."),
    (self._tv_load_vlc().EventType.MediaPlayerEncounteredError,"Erro ao abrir o fluxo. Confira o link/servidor e o formato do canal."),
    (self._tv_load_vlc().EventType.MediaPlayerEndReached,"O fluxo terminou ou o servidor encerrou a transmissão."),
   ]
   for event_type,label in event_map:
    def callback(event, status=label):
     try: self.root.after(0,lambda value=status:self.tv_status.config(text="Status: "+value))
     except Exception: pass
    manager.event_attach(event_type,callback)
    self.tv_vlc_events.append(callback)
  except Exception:
   self.tv_vlc_events=[]

 def _tv_check_playback(self):
  """Confere depois da inicializacao se o VLC entrou em estado de erro."""
  try:
   if not self.tv_player:return
   vlc=self._tv_load_vlc()
   state=self.tv_player.get_state()
   if state==vlc.State.Error:
    self.tv_status.config(text="Status: VLC recebeu o canal, mas o fluxo retornou erro.")
    messagebox.showerror("LOI TV — falha na transmissão", "O VLC abriu o player, mas não conseguiu decodificar/reproduzir este canal.\n\nPode ser URL expirada, servidor indisponível, formato incompatível ou bloqueio do provedor. Teste outro canal da mesma lista.")
   elif state==vlc.State.Playing:
    self.tv_status.config(text="Status: Reproduzindo canal ao vivo.")
   elif state==vlc.State.Opening:
    self.tv_status.config(text="Status: Conectando ao servidor do canal...")
   elif state==vlc.State.Buffering:
    self.tv_status.config(text="Status: Canal conectado; aguardando vídeo...")
   elif state==vlc.State.Ended:
    self.tv_status.config(text="Status: O servidor encerrou o fluxo.")
   elif state==vlc.State.Stopped:
    self.tv_status.config(text="Status: VLC parou; confira o endereço do canal.")
  except Exception as e:
   try:self.tv_status.config(text="Status VLC: "+str(e)[:180])
   except Exception:pass

 def tv_play(self):
  item=self.tv_selected()
  if not item: messagebox.showinfo("LOI TV","Selecione um canal na lista."); return
  try:
   vlc=self._tv_load_vlc()
   if self.tv_vlc is None:
    plugin_dir=str(self._tv_vlc_dir/"plugins")
    self.tv_vlc=vlc.Instance("--quiet", "--no-video-title-show", "--network-caching=3000", "--live-caching=3000", "--plugin-path="+plugin_dir)
    if self.tv_vlc is None: raise RuntimeError("O VLC não conseguiu iniciar. Confira a pasta VLC_Portable e as DLLs 64-bit.")
    self.tv_player=self.tv_vlc.media_player_new()
    if self.tv_player is None: raise RuntimeError("O VLC iniciou, mas não criou o reprodutor de mídia.")
    self._tv_bind_vlc_events()
   media=self.tv_vlc.media_new(item["url"])
   if media is None: raise RuntimeError("O VLC não aceitou o endereço deste canal.")
   try: media.add_option(":network-caching=3000")
   except Exception: pass
   self.tv_player.stop()
   self.tv_player.set_media(media)
   target=self.tv_pip_frame if self.tv_pip_frame and self.tv_pip_frame.winfo_exists() else (self.tv_full_frame if self.tv_full and self.tv_full.winfo_exists() else self.tv_video)
   target.update_idletasks()
   self.tv_player.set_hwnd(target.winfo_id())
   self.tv_placeholder.place_forget()
   try:self.tv_player.audio_set_mute(False); self.tv_player.audio_set_volume(100)
   except Exception:pass
   result=self.tv_player.play()
   if result == -1: raise RuntimeError("O VLC recusou iniciar a reprodução deste canal. Confira o endereço e o acesso ao servidor.")
   self.tv_status.config(text="Status: Solicitando reprodução de "+item.get("name","Canal")+"...")
   self.root.after(4500,self._tv_check_playback)
  except Exception as e:
   self.tv_status.config(text="Status: Falha ao iniciar o player — "+str(e)[:150])
   messagebox.showerror("Player VLC",str(e))
 def tv_pause(self):
  if self.tv_player:self.tv_player.pause()
 def tv_stop(self):
  if self.tv_player:self.tv_player.stop()
  if hasattr(self,"tv_placeholder"):self.tv_placeholder.place(relx=.5,rely=.5,anchor="center")
 def _tv_rebind_video(self, target, resume_ms=0):
  """Move a saída de vídeo do VLC para outro painel/janela preservando a reprodução."""
  if not self.tv_player: return
  try:
   media=self.tv_player.get_media()
   was_playing=bool(self.tv_player.is_playing())
   self.tv_player.stop()
   target.update_idletasks()
   self.tv_player.set_hwnd(target.winfo_id())
   if media is not None:
    self.tv_player.set_media(media)
    if was_playing:
     self.tv_player.play()
     if resume_ms > 0:
      self.root.after(1100, lambda p=self.tv_player,t=resume_ms: p.set_time(t) if p else None)
  except Exception as e:
   messagebox.showerror("Player VLC",f"Não foi possível mover o vídeo: {e}")

 def tv_picture_in_picture(self):
  if not self.tv_player or not self.tv_player.get_media():
   messagebox.showinfo("Picture-in-Picture","Primeiro selecione e reproduza um canal."); return
  try:
   if self.tv_pip and self.tv_pip.winfo_exists():
    resume=max(0,self.tv_player.get_time())
    self._tv_rebind_video(self.tv_video,resume)
    self.tv_pip.destroy(); self.tv_pip=None; self.tv_pip_frame=None
    return
   if self.tv_full and self.tv_full.winfo_exists(): self.tv_exit_fullscreen()
   resume=max(0,self.tv_player.get_time())
   self.tv_pip=tk.Toplevel(self.root); self.tv_pip.title("LOI TV — Picture-in-Picture")
   self.tv_pip.geometry("520x330+80+80"); self.tv_pip.configure(bg="black")
   self.tv_pip.attributes("-topmost",True)
   bar=tk.Frame(self.tv_pip,bg="#15191d"); bar.pack(fill="x")
   tk.Label(bar,text="LOI TV • PIP",bg="#15191d",fg="#35b9e8",font=("Segoe UI",9,"bold")).pack(side="left",padx=8,pady=5)
   tk.Button(bar,text="VOLTAR AO MACRO",command=self.tv_picture_in_picture,bg="#167ba7",fg="white",relief="flat").pack(side="right",padx=5,pady=3)
   self.tv_pip_frame=tk.Frame(self.tv_pip,bg="black"); self.tv_pip_frame.pack(fill="both",expand=True)
   self.tv_pip.protocol("WM_DELETE_WINDOW",self.tv_picture_in_picture)
   self.tv_pip.bind("<Escape>",lambda e:self.tv_picture_in_picture())
   self.tv_pip.update_idletasks(); self._tv_rebind_video(self.tv_pip_frame,resume)
  except Exception as e: messagebox.showerror("Picture-in-Picture",str(e))

 def tv_fullscreen(self):
  if not self.tv_player: messagebox.showinfo("Tela cheia","Primeiro selecione e reproduza um canal."); return
  try:
   if self.tv_full and self.tv_full.winfo_exists(): self.tv_exit_fullscreen(); return
   resume_ms=max(0,self.tv_player.get_time())
   if self.tv_pip and self.tv_pip.winfo_exists():
    self.tv_pip.destroy(); self.tv_pip=None; self.tv_pip_frame=None
   self.tv_full=tk.Toplevel(self.root); self.tv_full.title("LOI TV — Tela cheia"); self.tv_full.configure(bg="black")
   self.tv_full.overrideredirect(False)
   self.tv_full.bind("<Escape>",lambda e:self.tv_exit_fullscreen()); self.tv_full.bind("<F11>",lambda e:self.tv_exit_fullscreen())
   self.tv_full_frame=tk.Frame(self.tv_full,bg="black"); self.tv_full_frame.pack(fill="both",expand=True)
   self.tv_full.update_idletasks(); self.tv_full.attributes("-fullscreen",True); self.tv_full.update_idletasks()
   self._tv_rebind_video(self.tv_full_frame,resume_ms)
  except Exception as e: messagebox.showerror("Tela cheia",str(e))
 def tv_exit_fullscreen(self):
  try:
   if self.tv_full and self.tv_full.winfo_exists():
    resume_ms=max(0,self.tv_player.get_time()) if self.tv_player else 0
    self._tv_rebind_video(self.tv_video,resume_ms)
    self.tv_full.destroy()
   self.tv_full=None
  except Exception as e:
   self.tv_full=None
   messagebox.showerror("Tela cheia",str(e))

 def make_appearance(self):
  p=self.pages["Cores"]
  self.section(p,"PERSONALIZAÇÃO VISUAL")
  self.label(p,"24 temas visuais. Escolher um tema altera somente a aparência; macros, teclas, gravações, rotas, ataques, poções, Cliques e Multicliente permanecem independentes.",fg="#c7cdd2",wraplength=590,justify="left").pack(anchor="w",padx=14,pady=6)
  self.theme_var=tk.StringVar(value="Dark Neon")
  groups={
   "TEMAS ORIGINAIS (MANTIDOS)": ["Dark Neon","Dark Red","RGB","Personalizado"],
   "NEON E GAMER": ["Cyberpunk Neon","RGB Gaming","Synthwave","Anime Gamer","Ocean Neon"],
   "FUTURISTA E DIGITAL": ["Holográfico","Glassmorphism","Transparente","Futurista Premium","Galaxy"],
   "CLÁSSICOS E PROFISSIONAIS": ["Minimalista","Neumorphism","Clean Light","Flat Design"],
   "TÁTICO, RETRÔ E PREMIUM": ["Militar Tático","Premium Dourado","Industrial","Matrix","Blue Electric","Pixel Retro"]
  }
  desc={"Dark Neon":"Azul e ciano","Dark Red":"Preto e vermelho","RGB":"Roxo e turquesa","Personalizado":"Suas próprias cores",
   "Cyberpunk Neon":"Roxo e rosa","RGB Gaming":"Multicores gamer","Holográfico":"Ciano luminoso","Minimalista":"Visual discreto",
   "Glassmorphism":"Estilo vidro","Neumorphism":"Relevos suaves","Militar Tático":"Verde operacional","Premium Dourado":"Preto e ouro",
   "Synthwave":"Retrô neon","Matrix":"Verde digital","Blue Electric":"Azul elétrico","Clean Light":"Claro moderno",
   "Industrial":"Grafite e âmbar","Galaxy":"Roxo espacial","Anime Gamer":"Rosa e ciano","Transparente":"Azul translúcido",
   "Flat Design":"Moderno simples","Pixel Retro":"Arcade retrô","Futurista Premium":"Azul futurista","Ocean Neon":"Azul oceano"}
  for group,names in groups.items():
   self.section(p,group)
   for name in names:
    r=self.row(p)
    ttk.Radiobutton(r,text=f"{name} — {desc[name]}",variable=self.theme_var,value=name,command=lambda n=name:self.apply_theme(n)).pack(side="left",padx=10,pady=4)
  self.section(p,"PERSONALIZAÇÃO MANUAL")
  r=self.row(p); self.button(r,"ESCOLHER COR PRINCIPAL",self.pick_primary)
  self.button(r,"ESCOLHER FUNDO",self.pick_background,"#596675")
  r=self.row(p); self.button(r,"SALVAR APARÊNCIA",self.save_appearance,"#20845e")
  self.button(r,"RESTAURAR TEMA ORIGINAL",self.restore_original,"#687b8c")
  self.appearance_status=self.label(p,"Tema visual: Dark Neon",fg="#aeb7bd",wraplength=590,justify="left")
  self.appearance_status.pack(anchor="w",padx=14,pady=10)
  self.custom_theme=dict(THEMES["Personalizado"])

 def apply_theme(self,name):
  palette=dict(self.custom_theme if name=="Personalizado" else THEMES.get(name,THEMES["Dark Neon"]))
  self.theme_var.set(name); self.current_theme=name; self.theme_palette=palette
  bg,panel,field=palette["bg"],palette["panel"],palette["field"]
  primary,accent=palette["primary"],palette["accent"]
  textc,muted,header=palette["text"],palette["muted"],palette["header"]
  try:
   self.root.configure(bg=bg)
   style=ttk.Style(self.root)
   style.configure("TNotebook",background=bg,borderwidth=0)
   style.configure("TNotebook.Tab",background=field,foreground=textc,padding=(12,8))
   style.map("TNotebook.Tab",background=[("selected",primary)],foreground=[("selected",textc)])
   style.configure("TCheckbutton",background=panel,foreground=textc)
   style.map("TCheckbutton",background=[("active",panel)],foreground=[("active",accent)])
   style.configure("TRadiobutton",background=panel,foreground=textc)
   style.map("TRadiobutton",background=[("active",panel)],foreground=[("active",accent)])
   style.configure("TScrollbar",background=field,troughcolor=bg,arrowcolor=textc)
  except Exception: pass
  def paint(parent):
   for w in parent.winfo_children():
    try:
     cls=w.winfo_class()
     if cls in ("Frame","Labelframe"):
      old=w.cget("bg")
      w.configure(bg=header if old=="#15191d" else (bg if old=="#202326" else panel))
     elif cls=="Label":
      old=w.cget("bg"); fg=w.cget("fg")
      newbg=header if old=="#15191d" else (bg if old=="#202326" else panel)
      if fg.lower() in ("#35b9e8","#35c9f4","#167ba7"): fg=accent
      elif fg.lower() in ("#aeb7bd","#bfc6cc","#c7cdd2"): fg=muted
      w.configure(bg=newbg,fg=fg)
     elif cls in ("Button","TButton"):
      old=w.cget("bg") if cls=="Button" else None
      if cls=="Button":
       fg=w.cget("fg"); w.configure(bg=primary,fg=textc,activebackground=accent,activeforeground=textc)
     elif cls in ("Entry","Listbox","Text"):
      w.configure(bg=field,fg=textc,insertbackground=textc,selectbackground=primary,selectforeground=textc)
     elif cls=="Canvas": w.configure(bg=panel)
    except Exception: pass
    paint(w)
  paint(self.root)
  if hasattr(self,"appearance_status"):
   self.appearance_status.config(text=f"Tema visual aplicado: {name}. Nenhuma função do macro foi alterada.",fg=muted)

 def pick_primary(self):
  color=colorchooser.askcolor(title="Cor principal do tema")
  if color and color[1]:
   self.custom_theme["primary"]=color[1]; self.custom_theme["button"]=color[1]
   self.theme_var.set("Personalizado"); self.apply_theme("Personalizado")

 def pick_background(self):
  color=colorchooser.askcolor(title="Cor de fundo do tema")
  if color and color[1]:
   self.custom_theme["bg"]=color[1]
   self.theme_var.set("Personalizado"); self.apply_theme("Personalizado")

 def appearance_path(self):
  return Path(__file__).with_name("loi_appearance.json")

 def save_appearance(self):
  try:
   data={"theme":self.theme_var.get(),"custom":self.custom_theme}
   self.appearance_path().write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
   self.appearance_status.config(text="Aparência salva. Será restaurada na próxima abertura.")
  except Exception as exc: messagebox.showerror("Aparência",f"Não foi possível salvar o tema: {exc}")

 def load_appearance(self):
  try:
   path=self.appearance_path()
   if path.exists():
    data=json.loads(path.read_text(encoding="utf-8")); self.custom_theme.update(data.get("custom",{}))
    self.apply_theme(data.get("theme","Dark Neon"))
   else: self.apply_theme("Dark Neon")
  except Exception: self.apply_theme("Dark Neon")

 def restore_original(self):
  self.custom_theme=dict(THEMES["Personalizado"])
  self.apply_theme("Personalizado")
  self.save_appearance()

 def _enable_wheel(self,canvas):
  self._wheel_canvas=canvas
  self.root.bind_all("<MouseWheel>",self._on_mousewheel)
  self.root.bind_all("<Button-4>",self._on_mousewheel_linux)
  self.root.bind_all("<Button-5>",self._on_mousewheel_linux)

 def _disable_wheel(self):
  self.root.unbind_all("<MouseWheel>")
  self.root.unbind_all("<Button-4>")
  self.root.unbind_all("<Button-5>")
  self._wheel_canvas=None

 def _on_mousewheel(self,event):
  canvas=getattr(self,"_wheel_canvas",None)
  if canvas is not None:
   canvas.yview_scroll(int(-1*(event.delta/120)), "units")
  return "break"

 def _on_mousewheel_linux(self,event):
  canvas=getattr(self,"_wheel_canvas",None)
  if canvas is not None:
   canvas.yview_scroll(-1 if event.num==4 else 1,"units")
  return "break"

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
  self.label(p,"F7 rota individual • F6 rota MGP • F5 liga/desliga • F9 pausa • O jogo precisa estar em primeiro plano.",fg="#e2c16b").pack(anchor="w",padx=14,pady=8)

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

 def make_multiclient(self):
  p=self.pages["MGP Multicliente"]
  self.section(p,"GERENCIAMENTO DE CLIENTES NEWMT2")
  self.label(p,"O MGP é independente do macro principal: F8/F9, gravação, reprodução e a aba Cliques funcionam com 1, 2 ou até 10 janelas. Somente o botão INICIAR TODOS ativa a alternância entre clientes.",fg="#e6bd70",wraplength=590,justify="left").pack(anchor="w",padx=14,pady=6)
  self.multi_mode=tk.StringVar(value="overlay")
  self.multi_config_mode=tk.StringVar(value="shared")
  r=self.row(p); self.label(r,"Posicionamento:",fg="#e8edf0").pack(side="left",padx=8)
  ttk.Radiobutton(r,text="Sobrepostas",variable=self.multi_mode,value="overlay").pack(side="left",padx=5)
  ttk.Radiobutton(r,text="Independentes",variable=self.multi_mode,value="independent").pack(side="left",padx=5)
  r=self.row(p); self.label(r,"Configurações:",fg="#e8edf0").pack(side="left",padx=8)
  ttk.Radiobutton(r,text="Geral para todos",variable=self.multi_config_mode,value="shared").pack(side="left",padx=5)
  ttk.Radiobutton(r,text="Individual por cliente",variable=self.multi_config_mode,value="individual").pack(side="left",padx=5)
  self.section(p,"JANELAS ENCONTRADAS")
  r=self.row(p)
  self.multi_list=tk.Listbox(r,selectmode="extended",height=9,bg=FIELD,fg="white",selectbackground=BLUE,relief="flat",exportselection=False)
  self.multi_list.pack(fill="both",expand=True,padx=5,pady=4)
  self.multi_window_refs=[]
  r=self.row(p); self.button(r,"↻ ATUALIZAR JANELAS",self.refresh_multi_windows); self.button(r,"SELECIONAR TODAS",self.select_all_multi); self.button(r,"ALINHAR SOBREPOSTAS",self.align_multi_windows,"#687b8c")
  self.section(p,"ALTERNÂNCIA AUTOMÁTICA DE FOCO")
  self.multi_switch_enabled=tk.BooleanVar(value=False)
  r=self.row(p)
  ttk.Checkbutton(r,text="Habilitar alternância ao usar INICIAR TODOS (não afeta F8/F9 nem a aba Cliques)",variable=self.multi_switch_enabled).pack(side="left",padx=8,pady=5)
  r=self.row(p)
  self.label(r,"Pausa após ativar cada janela (s):",fg="#e8edf0").pack(side="left",padx=8)
  self.multi_switch_delay=tk.StringVar(value="0.35")
  tk.Entry(r,textvariable=self.multi_switch_delay,width=7,bg=FIELD,fg="white",insertbackground="white",relief="flat").pack(side="left",ipady=4)
  self.button(r,"TESTAR TROCA DE FOCO",self.test_multi_focus,"#687b8c")
  self.section(p,"ROTAS INDIVIDUAIS POR CLIENTE")
  self.label(p,"F7 controla somente a rota individual. Selecione exatamente uma janela na lista acima para gravar a rota exclusiva daquele personagem. Depois, selecione vários clientes e teste: cada um executará sua própria rota.",fg="#c7cdd2",wraplength=590,justify="left").pack(anchor="w",padx=14,pady=4)
  r=self.row(p); self.button(r,"● GRAVAR ROTA DO SELECIONADO",self.record_selected_multi_route)
  self.button(r,"■ PARAR E SALVAR ROTA",self.stop_record,"#a94d45")
  self.button(r,"F7 GRAVAR / PARAR (INDIVIDUAL)",self.record_individual_hotkey,"#536675")
  r=self.row(p); self.button(r,"▶ TESTAR ROTAS INDIVIDUAIS",self.test_multi_route,"#179b60")
  self.button(r,"APAGAR ROTA DO SELECIONADO",self.clear_selected_multi_route,"#687b8c")
  self.button(r,"▶ LIGAR / DESLIGAR BOT (F5)",self.toggle,"#20b968")
  self.multi_individual_status=self.label(p,"Rotas individuais: nenhuma cadastrada.",fg="#aeb7bd",wraplength=590,justify="left")
  self.multi_individual_status.pack(anchor="w",padx=14,pady=4)
  self.section(p,"ROTA MGP — MOUSE + TECLADO (COMPARTILHADA)")
  self.label(p,"F6 controla somente esta rota compartilhada. Grave a sequência uma única vez no cliente ativo. O MGP poderá reproduzir a mesma rota, em sequência, nas janelas selecionadas. Use clientes com a mesma resolução e disposição de interface.",fg="#c7cdd2",wraplength=590,justify="left").pack(anchor="w",padx=14,pady=4)
  r=self.row(p)
  self.button(r,"● GRAVAR MOUSE + TECLADO",self.record_route)
  self.button(r,"■ PARAR GRAVAÇÃO",self.stop_record,"#a94d45")
  self.button(r,"F6 GRAVAR / PARAR (MGP)",self.record_mgp_hotkey,"#536675")
  r=self.row(p)
  self.button(r,"▶ TESTAR ROTA EM TODOS",self.test_multi_route,"#179b60")
  self.button(r,"LIMPAR ROTA",self.clear_route,"#687b8c")
  self.multi_route_status=self.label(p,"Rota MGP: nenhuma rota gravada.",fg="#aeb7bd",wraplength=590,justify="left")
  self.multi_route_status.pack(anchor="w",padx=14,pady=4)
  self.section(p,"CONTROLE MULTICLIENTE")
  r=self.row(p)
  self.button(r,"▶ INICIAR TODOS (BOTÃO)",self.start_multi,"#20b968")
  self.button(r,"Ⅱ PAUSAR TODOS (F9)",self.stop,"#247da8")
  r=self.row(p); self.button(r,"SALVAR CONFIG. MGP",self.save_multi_config); self.button(r,"CARREGAR CONFIG. MGP",self.load_multi_config)
  self.multi_status=self.label(p,"Status MGP: pronto. A alternância muda o foco visivelmente e envia cada tecla aos clientes selecionados, em sequência.",fg="#aeb7bd",wraplength=590,justify="left")
  self.multi_status.pack(anchor="w",padx=14,pady=8)
  self.label(p,"A rota MGP é reproduzida em sequência somente quando você usa INICIAR TODOS ou TESTAR ROTAS INDIVIDUAIS. O macro da aba Cliques e o F8/F9 normal não são controlados por esta aba. A troca de foco depende das permissões do Windows e do jogo.",fg="#e6bd70",wraplength=590,justify="left").pack(anchor="w",padx=14,pady=4)
  self.multi_profiles={}
  self.refresh_multi_windows()
  self.update_multi_route_status()

 def make_client_automation(self):
  p=self.pages["Clientes & Automação"]
  self.section(p,"GERENCIADOR DE CLIENTES — PRIMEIRO TESTE")
  self.label(p,"Gerenciador independente de janelas NEWMT2. A seleção desta aba não altera a seleção nem as rotas da aba MGP Multicliente.",fg="#c7cdd2",wraplength=620,justify="left").pack(anchor="w",padx=14,pady=6)
  self.section(p,"MODO DE OPERAÇÃO")
  self.client_automation_mode=tk.StringVar(value="auto")
  r=self.row(p)
  ttk.Radiobutton(r,text="Automático (recomendado)",variable=self.client_automation_mode,value="auto",command=self.update_client_mode_info).pack(side="left",padx=5)
  ttk.Radiobutton(r,text="Macro central",variable=self.client_automation_mode,value="central",command=self.update_client_mode_info).pack(side="left",padx=5)
  r=self.row(p)
  ttk.Radiobutton(r,text="Macros separados (manual)",variable=self.client_automation_mode,value="separate",command=self.update_client_mode_info).pack(side="left",padx=5)
  self.client_mode_info=self.label(p,"Automático usa o macro central e a alternância sequencial do MGP. A execução em segundo plano não é garantida.",fg="#e6bd70",wraplength=620,justify="left")
  self.client_mode_info.pack(anchor="w",padx=14,pady=5)
  self.section(p,"JANELAS E VÍNCULOS")
  r=self.row(p)
  self.button(r,"ATUALIZAR JANELAS",self.refresh_client_windows)
  self.button(r,"SELECIONAR TODAS",self.select_all_client_windows)
  self.button(r,"TESTAR JANELA SELECIONADA",self.test_selected_client_focus,"#687b8c")
  list_frame=tk.Frame(p,bg=PANEL); list_frame.pack(fill="x",padx=12,pady=4)
  self.client_list=tk.Listbox(list_frame,selectmode="extended",height=5,exportselection=False,bg=FIELD,fg="white",selectbackground=PRIMARY,relief="flat")
  self.client_list.pack(side="left",fill="both",expand=True)
  client_scroll=ttk.Scrollbar(list_frame,orient="vertical",command=self.client_list.yview); client_scroll.pack(side="right",fill="y")
  self.client_list.configure(yscrollcommand=client_scroll.set)
  self.client_window_refs=[]
  self.client_binding_status=self.label(p,"A seleção e a lista desta aba são independentes do MGP Multicliente.",fg="#aeb7bd",wraplength=620,justify="left")
  self.client_binding_status.pack(anchor="w",padx=14,pady=5)
  self.section(p,"ORGANIZAÇÃO DAS JANELAS")
  r=self.row(p)
  self.client_window_mode=tk.StringVar(value="independent")
  ttk.Radiobutton(r,text="Sobrepostas",variable=self.client_window_mode,value="overlay").pack(side="left",padx=5)
  ttk.Radiobutton(r,text="Independentes (não mover)",variable=self.client_window_mode,value="independent").pack(side="left",padx=5)
  r=self.row(p)
  self.button(r,"APLICAR ORGANIZAÇÃO",self.align_client_windows,"#687b8c")
  self.label(p,"Independentes preserva a posição atual das janelas. Sobrepostas move as janelas selecionadas para (0, 0).",fg="#c7cdd2",wraplength=620,justify="left").pack(anchor="w",padx=14,pady=4)
  self.section(p,"ESCOPO DAS CONFIGURAÇÕES")
  r=self.row(p)
  self.client_config_scope=tk.StringVar(value="shared")
  ttk.Radiobutton(r,text="Geral para todos",variable=self.client_config_scope,value="shared").pack(side="left",padx=5)
  ttk.Radiobutton(r,text="Individual por cliente",variable=self.client_config_scope,value="individual").pack(side="left",padx=5)
  self.label(p,"O escopo desta aba é independente do escopo configurado no MGP. A aplicação de parâmetros específicos por cliente continua experimental.",fg="#e6bd70",wraplength=620,justify="left").pack(anchor="w",padx=14,pady=5)
  self.section(p,"CONTROLE")
  r=self.row(p)
  self.button(r,"SALVAR CONFIG. CLIENTE",self.save_client_config,"#20845e")
  self.button(r,"CARREGAR CONFIG. CLIENTE",self.load_client_config,"#596675")
  self.label(p,"Limitação importante: macro central e macros separados ainda não executam comandos físicos simultaneamente. Windows e jogo normalmente direcionam mouse/teclado à janela em foco; por isso, o modo separado fica manual/experimental neste primeiro teste e não inicia cópias automaticamente.",fg="#e6bd70",wraplength=620,justify="left").pack(anchor="w",padx=14,pady=10)
  self.refresh_client_windows()

 def selected_client_windows(self):
  if not hasattr(self,"client_list"): return []
  return [self.client_window_refs[i] for i in self.client_list.curselection() if i < len(self.client_window_refs)]

 def refresh_client_windows(self):
  if not hasattr(self,"client_list"): return
  previous={int(getattr(w,"_hWnd",0)) for w in self.selected_client_windows()}
  self.client_list.delete(0,"end"); self.client_window_refs=[]
  if gw is None:
   self.client_list.insert("end","pygetwindow indisponível — execute instalar.bat."); return
  title=str(self.v.get("game_title",tk.StringVar(value="NEWMT2")).get()).strip().lower()
  try:
   wins=[w for w in gw.getAllWindows() if w.title and title in w.title.lower() and w.width>0 and w.height>0]
   seen=set()
   for w in wins:
    hwnd=int(getattr(w,"_hWnd",0) or 0)
    if not hwnd or hwnd in seen: continue
    seen.add(hwnd); self.client_window_refs.append(w)
    self.client_list.insert("end",f"{len(self.client_window_refs)}. {w.title}  [HWND {hwnd}]")
    if hwnd in previous: self.client_list.selection_set(len(self.client_window_refs)-1)
   self.client_binding_status.config(text=f"{len(self.client_window_refs)} janela(s) detectada(s) nesta aba. Lista e seleção independentes do MGP.")
  except Exception as exc:
   self.client_binding_status.config(text=f"Falha ao atualizar janelas: {exc}")

 def select_all_client_windows(self):
  if hasattr(self,"client_list"):
   self.client_list.selection_set(0,"end")

 def align_client_windows(self):
  targets=self.selected_client_windows()
  if not targets:
   messagebox.showinfo("Clientes & Automação","Selecione uma ou mais janelas nesta aba."); return
  if self.client_window_mode.get()=="independent":
   self.client_binding_status.config(text="Modo Independentes: nenhuma janela foi movida."); return
  moved=0
  for w in targets:
   try: w.moveTo(0,0); moved+=1
   except Exception: pass
  self.client_binding_status.config(text=f"Organização aplicada: {moved}/{len(targets)} janela(s) movidas para (0, 0).")

 def save_client_config(self):
  path=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("Configuração Clientes","*.json")],initialfile="Clientes_Automacao.json")
  if not path: return
  data={"mode":self.client_automation_mode.get(),"window_mode":self.client_window_mode.get(),
        "scope":self.client_config_scope.get(),"selected_hwnds":[int(getattr(w,"_hWnd",0)) for w in self.selected_client_windows()]}
  try:
   Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
   self.client_binding_status.config(text="Configuração desta aba salva sem alterar o MGP.")
  except Exception as exc:
   messagebox.showerror("Clientes & Automação",str(exc))

 def load_client_config(self):
  path=filedialog.askopenfilename(filetypes=[("Configuração Clientes","*.json")])
  if not path: return
  try:
   data=json.loads(Path(path).read_text(encoding="utf-8"))
   self.client_automation_mode.set(data.get("mode","auto"))
   self.client_window_mode.set(data.get("window_mode","independent"))
   self.client_config_scope.set(data.get("scope","shared"))
   self.update_client_mode_info()
   self.refresh_client_windows()
   wanted={int(x) for x in data.get("selected_hwnds",[])}
   for i,w in enumerate(self.client_window_refs):
    if int(getattr(w,"_hWnd",0)) in wanted: self.client_list.selection_set(i)
   self.client_binding_status.config(text="Configuração desta aba carregada. A seleção MGP permaneceu intacta.")
  except Exception as exc:
   messagebox.showerror("Clientes & Automação",str(exc))

 def update_client_mode_info(self):
  if not hasattr(self,"client_mode_info"): return
  mode=self.client_automation_mode.get()
  messages={
   "auto":"Automático seleciona o fluxo central seguro: usa as janelas detectadas e a alternância sequencial do MGP. Não inicia processos extras.",
   "central":"Macro central: uma instância do LOI controla as janelas selecionadas em sequência, usando o foco do Windows.",
   "separate":"Macros separados: opção experimental/manual. Abra cópias independentes por sua conta; o vínculo exclusivo por janela e a coordenação entre processos ainda não estão automatizados."
  }
  self.client_mode_info.config(text=messages.get(mode,messages["auto"]))

 def test_selected_client_focus(self):
  targets=self.selected_client_windows()
  if len(targets)!=1:
   messagebox.showinfo("Clientes & Automação","Selecione exatamente uma janela na lista desta aba.")
   return
  w=targets[0]
  hwnd=int(getattr(w,"_hWnd",0) or 0)
  if not hwnd:
   messagebox.showwarning("Clientes & Automação","A janela selecionada não forneceu um identificador HWND válido.")
   return
  def worker():
   ok=self.activate_target_window(w,allow_when_stopped=True)
   msg=(f"Vínculo testado com sucesso. HWND: {hwnd}. A janela selecionada recebeu o foco." if ok else f"Não foi possível ativar a janela selecionada. HWND: {hwnd}. O Windows/jogo pode ter bloqueado a troca de foco.")
   self.root.after(0,lambda:self.client_binding_status.config(text=msg))
  threading.Thread(target=worker,daemon=True).start()

 def make_potions(self):
  # Aba isolada: configura ate 12 poções sem alterar gravação ou Multicliente.
  p=self.pages["Poções"]
  # Barra fixa fora da área rolável: os comandos ficam sempre visíveis.
  outer=self.page_canvases["Poções"].master
  toolbar=tk.Frame(outer,bg="#15191d")
  toolbar.pack(side="top",fill="x",before=self.page_canvases["Poções"])
  tk.Button(toolbar,text="▶ TESTAR",command=self.test_potions,bg="#179b60",fg="white",relief="flat",padx=12,pady=7).pack(side="left",padx=(8,4),pady=6)
  tk.Button(toolbar,text="● LIGAR",command=self.start_potions,bg="#287ba8",fg="white",relief="flat",padx=12,pady=7).pack(side="left",padx=4,pady=6)
  tk.Button(toolbar,text="■ DESLIGAR",command=self.stop_potions,bg="#a94d45",fg="white",relief="flat",padx=12,pady=7).pack(side="left",padx=4,pady=6)
  self.label(toolbar,"Tecla:",fg="#e8edf0",bg="#15191d").pack(side="left",padx=(7,2))
  self.potion_hotkey_var=tk.StringVar(value="F11")
  tk.Entry(toolbar,textvariable=self.potion_hotkey_var,width=6,bg="#343a40",fg="white",insertbackground="white",relief="flat",justify="center").pack(side="left",ipady=4,padx=2)
  tk.Button(toolbar,text="APLICAR",command=self.apply_potion_hotkey,bg="#536675",fg="white",relief="flat",padx=7,pady=6).pack(side="left",padx=3,pady=6)
  self.label(toolbar,"Espera inventário (s):",fg="#e8edf0",bg="#15191d").pack(side="left",padx=(8,3))
  self.potion_inventory_wait=tk.StringVar(value="0.15")
  tk.Entry(toolbar,textvariable=self.potion_inventory_wait,width=7,bg="#343a40",fg="white",insertbackground="white",relief="flat").pack(side="left",ipady=4,padx=3)
  self.potion_run_status=self.label(toolbar,"Status: desligado.",fg="#aeb7bd",bg="#15191d",wraplength=300,justify="left")
  self.potion_run_status.pack(side="left",padx=10,pady=6)
  self.section(p,"RENOVAÇÃO DE POÇÕES COLORIDAS")
  self.label(p,"Configure até 12 poções do inventário. Cada uma tem ativação, coordenadas e intervalo próprios. A captura usa F12 sem consumir o item.",fg="#c7cdd2",wraplength=590,justify="left").pack(anchor="w",padx=14,pady=6)
  self.potion_enabled=[]; self.potion_names=[]; self.potion_x=[]; self.potion_y=[]
  self.potion_intervals=[]
  self.potion_capture_listeners={}; self.potion_capture_status=[]
  self.potion_stop_event=threading.Event(); self.potion_thread=None; self.potion_active=False
  for i in range(12):
   self.section(p,f"POÇÃO {i+1}")
   r=self.row(p)
   en=tk.BooleanVar(value=False); self.potion_enabled.append(en)
   ttk.Checkbutton(r,text="Ativar",variable=en).pack(side="left",padx=8)
   name=tk.StringVar(value=f"Poção {i+1}"); self.potion_names.append(name)
   tk.Entry(r,textvariable=name,width=18,bg=FIELD,fg="white",insertbackground="white",relief="flat").pack(side="left",ipady=4,padx=5)
   self.label(r,"Intervalo (s):",fg="#e8edf0").pack(side="left",padx=(8,3))
   iv=tk.StringVar(value="601"); self.potion_intervals.append(iv)
   tk.Entry(r,textvariable=iv,width=7,bg=FIELD,fg="white",insertbackground="white",relief="flat").pack(side="left",ipady=4)
   r=self.row(p)
   self.label(r,"Posição no inventário — X:",fg="#e8edf0").pack(side="left",padx=(8,3))
   xv=tk.StringVar(value=""); self.potion_x.append(xv)
   tk.Entry(r,textvariable=xv,width=7,bg=FIELD,fg="white",insertbackground="white",relief="flat").pack(side="left",ipady=4)
   self.label(r,"Y:",fg="#e8edf0").pack(side="left",padx=(8,3))
   yv=tk.StringVar(value=""); self.potion_y.append(yv)
   tk.Entry(r,textvariable=yv,width=7,bg=FIELD,fg="white",insertbackground="white",relief="flat").pack(side="left",ipady=4)
   self.button(r,"CAPTURAR POSIÇÃO",lambda idx=i:self.capture_potion_position(idx),"#287ba8")
   status=self.label(p,"Aguardando captura.",fg="#9da8b0")
   status.pack(anchor="w",padx=22,pady=(0,5))
   self.potion_capture_status.append(status)
  self.label(p,"Padrão de cada poção: 601 segundos (10 minutos e 1 segundo). Marque somente as poções que deseja configurar. Para capturar: clique em CAPTURAR POSIÇÃO, passe o cursor sobre o centro do item e pressione F12 sem clicar.",fg="#e6bd70",wraplength=590,justify="left").pack(anchor="w",padx=14,pady=8)
  self.label(p,"Os botões TESTAR, LIGAR e DESLIGAR ficam fixos no alto desta aba. O macro reconhece automaticamente se o inventário está aberto. Se estiver fechado, abre com I; se já estiver aberto, mantém aberto. Depois clica com o botão DIREITO nas poções marcadas. O cursor físico será movimentado durante os cliques. Não use junto com gravação, reprodução de rota ou Multicliente.",fg="#e6bd70",wraplength=590,justify="left").pack(anchor="w",padx=14,pady=8)

 def _selected_potion_points(self):
  points=[]
  for i,en in enumerate(self.potion_enabled):
   if not en.get(): continue
   try:
    x=int(self.potion_x[i].get().strip()); y=int(self.potion_y[i].get().strip())
    interval=float(self.potion_intervals[i].get().replace(",", "."))
    if x<0 or y<0 or interval<1: raise ValueError()
   except Exception:
    raise ValueError(f"Confira X, Y e intervalo da {self.potion_names[i].get()}.")
   points.append((i,x,y,interval,self.potion_names[i].get()))
  if not points: raise ValueError("Marque pelo menos uma poção e informe suas coordenadas.")
  return points

 def _potion_busy(self):
  return self.recording or self.running or self.multi_broadcast_active

 def _detect_inventory_open(self):
  """Reconhece o cabeçalho visual do inventário dentro da tela do jogo."""
  if cv2 is None or np is None or ImageGrab is None:
   raise RuntimeError("Falta instalar o reconhecimento visual. Feche o macro e execute ABRIR_AQUI.bat.")
  template_path=Path(__file__).resolve().with_name("inventory_header_template.png")
  template=cv2.imread(str(template_path),cv2.IMREAD_GRAYSCALE)
  if template is None:
   raise RuntimeError("Não encontrei o modelo visual do inventário (inventory_header_template.png).")
  shot=ImageGrab.grab().convert("RGB")
  screen=cv2.cvtColor(np.array(shot),cv2.COLOR_RGB2GRAY)
  # A imagem-modelo é do cabeçalho 'Inventário' do NEWMT2. Pequenas variações
  # de escala são testadas para tolerar diferenças de tamanho da janela.
  best=0.0
  h,w=template.shape[:2]
  for scale in (0.80,0.90,1.00,1.10,1.20,1.30):
   tw,th=int(w*scale),int(h*scale)
   if tw<8 or th<8 or tw>screen.shape[1] or th>screen.shape[0]:
    continue
   sample=cv2.resize(template,(tw,th),interpolation=cv2.INTER_AREA if scale<1 else cv2.INTER_CUBIC)
   result=cv2.matchTemplate(screen,sample,cv2.TM_CCOEFF_NORMED)
   _,score,_,_=cv2.minMaxLoc(result)
   best=max(best,float(score))
  return best>=0.76

 def _potion_click_cycle(self,points,inventory_was_open=None):
  if self.potion_stop_event.is_set(): return
  if pdi is None: raise RuntimeError("pydirectinput não está instalado. Execute ABRIR_AQUI.bat.")
  if not self.game_window_is_active(): raise RuntimeError("A janela NEWMT2 não está em primeiro plano. Ative o jogo e tente novamente.")
  # Detecta novamente em cada ciclo, pois o jogador pode abrir/fechar o inventário.
  inventory_is_open=self._detect_inventory_open()
  opened_by_macro = not inventory_is_open
  if opened_by_macro:
   pdi.press("i")
  try:
   # Este ajuste controla somente a espera depois de abrir/confirmar o inventário.
   wait_text=self.potion_inventory_wait.get().strip().replace(",", ".")
   inventory_wait=float(wait_text)
   if not 0.0 <= inventory_wait <= 30.0:
    raise ValueError
  except (ValueError, AttributeError):
   inventory_wait=0.15
   if hasattr(self,"potion_inventory_wait"):
    self.root.after(0,lambda:self.potion_inventory_wait.set("0.15"))
  time.sleep(inventory_wait)
  try:
   for i,x,y,interval,name in points:
    if self.potion_stop_event.is_set(): break
    if not self.game_window_is_active(): raise RuntimeError("Foco do NEWMT2 perdido; sequência interrompida por segurança.")
    # Um único clique DIREITO explícito na coordenada da poção.
    pdi.click(x=int(x), y=int(y), clicks=1, interval=0.1, button="right")
    try: pdi.mouseUp(button="right")
    except Exception: pass
    time.sleep(0.18)
  finally:
   try: pdi.mouseUp(button="right")
   except Exception: pass
   # Fecha apenas se esta execução abriu o inventário.
   if opened_by_macro and self.game_window_is_active():
    pdi.press("i")
    time.sleep(0.25)

 def _potion_worker(self,points,repeat):
  try:
   self._potion_click_cycle(points)
   self.root.after(0,lambda:self.potion_run_status.config(text="Poções marcadas aplicadas. Cursor liberado."))
   if repeat:
    due={item[0]:time.monotonic()+item[3] for item in points}
    by_index={item[0]:item for item in points}
    while not self.potion_stop_event.is_set():
     if self._potion_busy():
      self.root.after(0,lambda:self.potion_run_status.config(text="Pausado: gravação, rota ou Multicliente em andamento."))
      time.sleep(0.5)
      continue
     now=time.monotonic()
     ready=[by_index[i] for i,t in due.items() if now>=t]
     if ready:
      self._potion_click_cycle(ready)
      now=time.monotonic()
      for item in ready: due[item[0]]=now+item[3]
      self.root.after(0,lambda:self.potion_run_status.config(text="Renovação concluída. Próximos tempos individuais em contagem."))
     else:
      time.sleep(0.2)
  except Exception as exc:
   self.root.after(0,lambda msg=str(exc):self.potion_run_status.config(text="Erro: "+msg))
  finally:
   self.potion_active=False
   self.root.after(0,lambda:self.potion_run_status.config(text="Status: desligado." if not self.potion_stop_event.is_set() else "Status: desligando/concluído."))

 def _launch_potions(self,repeat):
  if self._potion_busy():
   messagebox.showwarning("Poções","Pare a gravação, a rota e o Multicliente antes de usar as poções.")
   return
  try: points=self._selected_potion_points()
  except ValueError as exc:
   messagebox.showwarning("Poções",str(exc)); return
  if cv2 is None or np is None or ImageGrab is None:
   messagebox.showerror("Reconhecimento automático","Execute ABRIR_AQUI.bat para instalar o reconhecimento visual do inventário.")
   return
  # O botão foi clicado na macro; trazer o NEWMT2 para primeiro plano automaticamente.
  if not self.activate_game_window():
   messagebox.showwarning("Poções","Não consegui ativar a janela NEWMT2. Confira se o jogo está aberto e se macro e jogo estão executando com o mesmo nível de permissão. Nenhuma tecla ou clique foi enviado.")
   return
  self.potion_stop_event.clear(); self.potion_active=True
  self.potion_run_status.config(text="Executando cliques nas poções marcadas...")
  self.potion_thread=threading.Thread(target=self._potion_worker,args=(points,repeat),daemon=True)
  self.potion_thread.start()

 def apply_potion_hotkey(self,show_errors=True):
  if not hasattr(self,"potion_hotkey_var"):
   return
  key_text=self.potion_hotkey_var.get().strip().lower()
  if not key_text:
   if show_errors: messagebox.showwarning("Tecla das poções","Digite uma tecla, por exemplo F11.")
   return
  if keyboard is None:
   if show_errors: messagebox.showerror("Tecla das poções","A biblioteca de teclas não está disponível. Execute instalar.bat.")
   return
  try:
   if self.potion_hotkey_handle is not None:
    keyboard.remove_hotkey(self.potion_hotkey_handle)
    self.potion_hotkey_handle=None
   self.potion_hotkey_handle=keyboard.add_hotkey(
    key_text,lambda:self.root.after(0,self.toggle_potions_hotkey),
    suppress=False,trigger_on_release=False)
   self.potion_hotkey_var.set(key_text.upper())
   if show_errors and hasattr(self,"potion_run_status"):
    self.potion_run_status.config(text=f"Atalho das poções: {key_text.upper()}.")
  except Exception as exc:
   if show_errors:
    messagebox.showwarning("Tecla das poções",f"Não consegui registrar '{key_text}'. Tente outra tecla.\\n\\nDetalhe: {exc}")
   self.potion_hotkey_var.set("F11")

 def toggle_potions_hotkey(self):
  if self.potion_active:
   self.stop_potions()
  else:
   self.start_potions()

 def test_potions(self):
  if self.potion_active:
   messagebox.showinfo("Poções","A renovação já está ativa. Use DESLIGAR antes de testar."); return
  self._launch_potions(False)

 def start_potions(self):
  if self.potion_active:
   messagebox.showinfo("Poções","A renovação já está ligada."); return
  self._launch_potions(True)

 def stop_potions(self):
  self.potion_stop_event.set()
  if hasattr(self,"potion_run_status"):
   self.potion_run_status.config(text="Solicitando parada segura...")

 def capture_potion_position(self,index):
  # Captura sem consumir a poção: posicionar o cursor sobre ela e pressionar F12.
  if mouse is None or pynput_keyboard is None:
   messagebox.showerror("Capturar posição","O módulo pynput não está disponível. Reinstale as dependências pelo instalador.")
   return
  old=self.potion_capture_listeners.pop(index,None)
  if old is not None:
   try: old.stop()
   except Exception: pass
  self.potion_capture_status[index].config(text="Passe o cursor sobre o centro da poção e pressione F12 (não clique).",fg="#f0c879")
  self.root.after(650,lambda idx=index:self._start_potion_mouse_capture(idx))

 def _start_potion_mouse_capture(self,index):
  if mouse is None or pynput_keyboard is None: return
  def on_press(key):
   if key == pynput_keyboard.Key.f12:
    try: x,y=mouse.Controller().position
    except Exception: return False
    self.root.after(0,lambda idx=index,px=int(x),py=int(y):self._finish_potion_capture(idx,px,py))
    listener=self.potion_capture_listeners.get(index)
    if listener is not None: self.root.after(0,listener.stop)
    return False
  try:
   listener=pynput_keyboard.Listener(on_press=on_press)
   self.potion_capture_listeners[index]=listener
   listener.start()
  except Exception as exc:
   self.potion_capture_status[index].config(text=f"Falha ao iniciar captura: {exc}",fg="#ef7777")

 def _finish_potion_capture(self,index,x,y):
  self.potion_x[index].set(str(x)); self.potion_y[index].set(str(y))
  self.potion_capture_listeners.pop(index,None)
  self.potion_capture_status[index].config(text=f"Posição capturada: X={x}  Y={y}. Clique em Salvar Configs.",fg="#69d69a")

 def get_potion_settings(self):
  return {"enabled":[v.get() for v in self.potion_enabled],"names":[v.get() for v in self.potion_names],
          "x":[v.get() for v in self.potion_x],"y":[v.get() for v in self.potion_y],
          "intervals":[v.get() for v in self.potion_intervals],"interval":"601",
          "inventory_open_wait":self.potion_inventory_wait.get(),
          "hotkey":self.potion_hotkey_var.get() if hasattr(self,"potion_hotkey_var") else "F11"}

 def set_potion_settings(self,data):
  for arr,key in ((self.potion_enabled,"enabled"),(self.potion_names,"names"),(self.potion_x,"x"),(self.potion_y,"y")):
   vals=data.get(key,[])
   for i,var in enumerate(arr):
    if i<len(vals): var.set(vals[i])
  intervals=data.get("intervals",[])
  legacy=str(data.get("interval","601"))
  for i,var in enumerate(self.potion_intervals):
   var.set(str(intervals[i]) if i<len(intervals) else legacy)
  if hasattr(self,"potion_inventory_wait"):
   self.potion_inventory_wait.set(str(data.get("inventory_open_wait","0.15")))
  if hasattr(self,"potion_hotkey_var"):
   self.potion_hotkey_var.set(str(data.get("hotkey","F11")))
   self.apply_potion_hotkey(show_errors=False)

 def selected_multi_windows(self):
  if not hasattr(self,"multi_list"):
   return []
  return [self.multi_window_refs[i] for i in self.multi_list.curselection()
          if i < len(self.multi_window_refs)]

 def multi_delay(self):
  try:
   return min(3.0,max(0.05,float(self.multi_switch_delay.get().replace(",", "."))))
  except Exception:
   return 0.35

 def test_multi_focus(self):
  targets=self.selected_multi_windows()
  if len(targets)<2:
   messagebox.showinfo("MGP Multicliente","Selecione pelo menos duas janelas NEWMT2.")
   return
  def worker():
   changed=0
   for w in targets:
    try:
     if getattr(w,"isMinimized",False):
      w.restore()
     w.activate()
     hwnd=int(getattr(w,"_hWnd",0))
     deadline=time.monotonic()+0.8
     focused=False
     while time.monotonic()<deadline:
      if int(ctypes.windll.user32.GetForegroundWindow())==hwnd:
       focused=True
       break
      time.sleep(0.02)
     if focused: changed+=1
     time.sleep(self.multi_delay())
    except Exception:
     pass
   self.root.after(0,lambda:self.multi_status.config(
    text=f"Teste de foco concluído: {changed}/{len(targets)} janelas receberam foco. Nenhuma tecla foi enviada."))
  threading.Thread(target=worker,daemon=True).start()

 def multi_route_key(self,w):
  # O título distingue as janelas; em caso de títulos repetidos, acrescenta o HWND.
  same=[x for x in self.multi_window_refs if getattr(x,"title","")==getattr(w,"title","")]
  title=str(getattr(w,"title","Cliente"))
  return title if len(same)<=1 else f"{title}::{int(getattr(w,'_hWnd',0))}"

 def update_multi_route_status(self):
  if hasattr(self,"multi_individual_status"):
   self.multi_individual_status.config(text=f"Rotas individuais cadastradas: {len(self.multi_client_routes)} cliente(s). Selecione um cliente para gravar, ou vários para testar.")

 def record_selected_multi_route(self):
  targets=self.selected_multi_windows()
  if len(targets)!=1:
   messagebox.showinfo("Rotas individuais","Selecione exatamente uma janela NEWMT2 na lista para gravar a rota desse personagem.")
   return
  if not self.activate_target_window(targets[0],allow_when_stopped=True):
   messagebox.showwarning("Rotas individuais","Não foi possível ativar a janela selecionada. Clique nela manualmente e tente gravar novamente.")
   return
  self._recording_multi_key=self.multi_route_key(targets[0])
  self._recording_target_window=targets[0]
  self._recording_target_hwnd=int(getattr(targets[0],"_hWnd",0) or 0)
  self.record_route()

 def clear_selected_multi_route(self):
  targets=self.selected_multi_windows()
  if len(targets)!=1:
   messagebox.showinfo("Rotas individuais","Selecione exatamente um cliente para apagar a rota.")
   return
  key=self.multi_route_key(targets[0])
  if key in self.multi_client_routes:
   del self.multi_client_routes[key]
  self.update_multi_route_status()

 def test_multi_route(self):
  targets=self.selected_multi_windows()
  # O teste de rotas individuais também deve funcionar com apenas um cliente.
  # A exigência de duas janelas pertence à alternância de foco/iniciar todos.
  if len(targets)<1:
   messagebox.showinfo("Rotas individuais / MGP","Selecione pelo menos uma janela NEWMT2.")
   return
  if not self.events and not self.multi_client_routes:
   messagebox.showinfo("Rota MGP","Grave uma rota compartilhada ou uma rota individual para cada cliente.")
   return
  if self.recording:
   messagebox.showwarning("Rota MGP","Pare a gravação antes de testar a rota.")
   return
  if self.running:
   messagebox.showwarning("Rota MGP","Pause o macro antes de testar a rota.")
   return
  self.multi_run_targets=list(targets)
  self.multi_broadcast_active=True
  self.playback_stop.clear()
  def worker():
   try:
    self.execute_route(bot_mode=False)
    self.root.after(0,lambda:self.multi_route_status.config(
     text=f"Teste da rota concluído nos {len(targets)} clientes selecionados (sequencialmente)."))
   finally:
    self.multi_broadcast_active=False
    self.multi_run_targets=[]
  threading.Thread(target=worker,daemon=True).start()

 def start_multi(self):
  targets=self.selected_multi_windows()
  if len(targets)<2:
   messagebox.showinfo("MGP Multicliente","Selecione pelo menos duas janelas e atualize a lista.")
   return
  # Respeita a opção da interface: não marque alternância silenciosamente.
  # O botão INICIAR TODOS executa a sequência explicitamente solicitada.
  self.multi_run_targets=list(targets)
  self.multi_broadcast_active=True
  self.start()
  if self.running:
   self.multi_status.config(text=f"Alternância automática ativa: {len(self.multi_run_targets)} clientes selecionados. O foco mudará de uma janela para outra.")

 def activate_target_window(self,w,allow_when_stopped=False):
  """Tenta ativar a janela pelo mecanismo normal do Windows; não contorna bloqueios de foco."""
  try:
   if getattr(w,"isMinimized",False):
    w.restore()
   w.activate()
   hwnd=int(getattr(w,"_hWnd",0))
   deadline=time.monotonic()+0.65
   while time.monotonic()<deadline:
    if int(ctypes.windll.user32.GetForegroundWindow())==hwnd:
     return True
    if not self.running and not allow_when_stopped: return False
    time.sleep(0.015)
  except Exception:
   return False
  return False

 def refresh_multi_windows(self):
  if not hasattr(self,"multi_list"): return
  previous={int(getattr(w,"_hWnd",0)) for w in self.selected_multi_windows()}
  self.multi_list.delete(0,"end"); self.multi_window_refs=[]
  if gw is None:
   self.multi_list.insert("end","pygetwindow indisponível — execute instalar.bat."); return
  title=str(self.v.get("game_title",tk.StringVar(value="NEWMT2")).get()).strip().lower()
  try:
   wins=[w for w in gw.getAllWindows() if w.title and title in w.title.lower() and w.width>0 and w.height>0]
   seen=set()
   for w in wins:
    hwnd=getattr(w,"_hWnd",None)
    if hwnd in seen: continue
    seen.add(hwnd); self.multi_window_refs.append(w)
    self.multi_list.insert("end",f"{len(self.multi_window_refs)}. {w.title}  [{w.width}x{w.height}]")
    if int(hwnd or 0) in previous:
     self.multi_list.selection_set(len(self.multi_window_refs)-1)
   if not wins: self.multi_list.insert("end",f"Nenhuma janela com '{title}' foi encontrada.")
  except Exception as e: self.multi_list.insert("end","Falha ao enumerar janelas: "+str(e))

 def select_all_multi(self):
  if self.multi_list.size(): self.multi_list.selection_set(0,"end")

 def align_multi_windows(self):
  if gw is None:
   messagebox.showerror("MGP Multicliente","pygetwindow não está disponível."); return
  selected=list(self.multi_list.curselection())
  windows=[self.multi_window_refs[i] for i in selected if i<len(self.multi_window_refs)]
  if len(windows)<2:
   messagebox.showinfo("MGP Multicliente","Selecione pelo menos duas janelas válidas."); return
  moved=0
  for w in windows:
   try: w.moveTo(0,0); moved+=1
   except Exception: pass
  messagebox.showinfo("MGP Multicliente",f"{moved} janela(s) posicionada(s) em (0, 0). Elas ficarão visualmente sobrepostas; isso não sincroniza comandos.")

 def save_multi_config(self):
  path=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("Configuração MGP","*.json")],initialfile="MGP_multicliente.json")
  if not path:return
  selected_titles=[self.multi_window_refs[i].title for i in self.multi_list.curselection() if i<len(self.multi_window_refs)]
  data={"version":2,"mode":self.multi_mode.get(),"config_mode":self.multi_config_mode.get(),"selected_titles":selected_titles,"profiles":self.multi_profiles,
        "switch_enabled":self.multi_switch_enabled.get(),"switch_delay":self.multi_switch_delay.get(),"client_routes":self.multi_client_routes,
        "automation_mode":getattr(self,"client_automation_mode",tk.StringVar(value="auto")).get()}
  Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
  self.status.config(text="Configuração MGP Multicliente salva.")

 def load_multi_config(self):
  path=filedialog.askopenfilename(filetypes=[("Configuração MGP","*.json")])
  if not path:return
  try:
   data=json.loads(Path(path).read_text(encoding="utf-8")); self.multi_mode.set(data.get("mode","overlay")); self.multi_config_mode.set(data.get("config_mode","shared")); self.multi_profiles=data.get("profiles",{}); self.multi_client_routes=data.get("client_routes",{})
   self.multi_switch_enabled.set(data.get("switch_enabled",False)); self.multi_switch_delay.set(data.get("switch_delay","0.18"))
   if hasattr(self,"client_automation_mode"):
    self.client_automation_mode.set(data.get("automation_mode","auto")); self.update_client_mode_info()
   self.refresh_multi_windows(); wanted=set(data.get("selected_titles",[]))
   for i,w in enumerate(self.multi_window_refs):
    if w.title in wanted:self.multi_list.selection_set(i)
   self.update_multi_route_status()
   self.status.config(text="Configuração MGP Multicliente carregada.")
  except Exception as e: messagebox.showerror("MGP Multicliente",str(e))

 def defaults(self):
  self.set_defaults()

 def set_defaults(self):
  for k,v in DEFAULT.items():
   if k in self.v:self.v[k].set(v)

 def getnum(self,k,default):
  try:return max(.03,float(self.v[k].get()))
  except:return default
 def send_one(self,key):
  if "+" in key:
   keys=[x.strip() for x in key.split("+") if x.strip()]
   pdi.hotkey(*keys)
  else:
   pdi.press(key)

 def release_client_keys(self):
  """Libera teclas no cliente atualmente em foco antes de trocar de janela."""
  if pdi is None:
   return
  keys={"space","w","a","s","d"}
  # Inclui as teclas configuradas nos módulos, inclusive ataque personalizado.
  for setting in ("attack_key","mount_key","camera_key","combo_key"):
   try:
    value=str(self.v[setting].get()).strip().lower()
    if value:
     keys.update(part.strip() for part in value.split("+") if part.strip())
   except Exception:
    pass
  for name in keys:
   try: pdi.keyUp(name)
   except Exception: pass
  for button in ("right","left","middle"):
   try: pdi.mouseUp(button=button)
   except Exception: pass

 def send(self,key):
  if pdi is None:return
  key=str(key).strip().lower()
  if not key:return
  try:
   if self.multi_broadcast_active and self.multi_run_targets:
    sent=0
    previous=None
    for w in list(self.multi_run_targets):
     if not self.running: break
     # Antes de mudar o foco, devolve ao cliente anterior e solta qualquer
     # tecla/botão que possa ter permanecido pressionado durante a troca.
     if previous is not None:
      if self.activate_target_window(previous):
       time.sleep(self.multi_delay())
       self.release_client_keys()
      previous=None
     if self.activate_target_window(w):
      time.sleep(self.multi_delay())
      hwnd=int(getattr(w,"_hWnd",0))
      if int(ctypes.windll.user32.GetForegroundWindow()) != hwnd:
       continue
      self.send_one(key)
      # Garante que o comando de ataque seja um toque, nunca um pressionamento
      # que atravesse a troca para a próxima tela/cliente.
      for part in (key.split("+") if "+" in key else [key]):
       try: pdi.keyUp(part.strip())
       except Exception: pass
      sent+=1
      previous=w
    # A última janela também recebe a soltura antes do próximo ciclo.
    if previous is not None and self.activate_target_window(previous):
     time.sleep(self.multi_delay())
     self.release_client_keys()
    if sent==0 and self.running:
     self.root.after(0,lambda:self.multi_status.config(
      text="Nenhuma janela recebeu foco. O Windows pode estar bloqueando a ativação; confira se o MGP e o jogo estão no mesmo nível de permissão."))
   else:
    self.send_one(key)
    for part in (key.split("+") if "+" in key else [key]):
     try: pdi.keyUp(part.strip())
     except Exception: pass
  except Exception as e:
   self.release_client_keys()
   self.root.after(0,lambda err=str(e):self.status.config(text="Falha ao enviar tecla: "+err))
 def start(self):
  if keyboard is None or pdi is None:
   messagebox.showerror("Dependências","Execute instalar.bat para instalar keyboard, pynput e pydirectinput."); return
  if self.running:return
  if self.multi_broadcast_active and self.v.get("mount_on") and self.v["mount_on"].get():
   self.v["mount_on"].set(False)
   if hasattr(self,"multi_status"):
    self.multi_status.config(text="MGP: Montaria automática desativada neste início para evitar o envio involuntário da tecla 1. Você pode reativá-la manualmente se desejar.")
  # IMPORTANTE: F8/F9 controlam somente o macro normal (incluindo a aba
  # Cliques), independentemente da quantidade de janelas e das opções MGP.
  # A alternância entre clientes só pode ser iniciada pelo botão dedicado
  # "INICIAR TODOS" na aba MGP Multicliente.
  if not self.multi_broadcast_active:
   self.multi_run_targets=[]
  if "loot_on" in self.v:
   self.v["loot_on"].set(False)
  self.playback_stop.clear()
  # Para rotas gravadas, o comportamento solicitado é repetir continuamente.
  # Só F9/Desligar encerra o ciclo; não parar ao concluir uma volta.
  try:
   self.v["route_repeat"].set(True)
  except Exception:
   pass
  self.running=True; self.started=time.time()
  # Não captura/bloqueia o cursor: evita sensação de mouse travado.
  self.unclip_cursor()
  threading.Thread(target=self.loop,daemon=True).start()
  self.status.config(text="Status: Ligado — volte ao jogo. F9 pausa.")
 def toggle(self):
  if self.running:
   self.stop()
   return
  # F8 deve trazer o cliente selecionado para frente antes de iniciar o macro.
  # Com vários selecionados, não inicia todos implicitamente: isso continua sendo
  # uma ação explícita do botão INICIAR TODOS na aba MGP.
  try:
   targets=self.selected_multi_windows()
   if targets and not self.activate_target_window(targets[0],allow_when_stopped=True):
    self.root.after(0,lambda:messagebox.showwarning("Foco do jogo","Não foi possível ativar a primeira janela selecionada. O macro não será iniciado."))
    return
  except Exception:
   pass
  self.start()
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
  if getattr(self,"cycle4_running",False): self.stop_cycle4()
  # Sinaliza primeiro: playback e varredura da câmera verificam self.running.
  self.running=False
  self.multi_broadcast_active=False
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
   # Mantém o macro ligado, mas não envia teclas fora da janela do Metin2.
   if not self.game_window_is_active():
    time.sleep(0.05)
    continue
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
   has_multi_routes = bool(self.multi_broadcast_active and self.multi_run_targets and self.multi_client_routes)
   if self.running and (self.events or has_multi_routes):
    # F8: executa a rota compartilhada ou as rotas individuais dos clientes
    # selecionados, sem módulos concorrentes.
    self.execute_route(bot_mode=True)
    if self.multi_broadcast_active:
     # INICIAR TODOS: cada ciclo percorre os clientes em sequência.
     # A caixa "Repetir rota continuamente" controla se outro ciclo começa.
     # A FIX6 já libera as teclas/botões de cada cliente antes da troca de foco.
     if self.running and self.v["route_repeat"].get():
      try:
       self.root.after(0,lambda:self.multi_status.config(
        text="MGP ativo: ciclo concluído; iniciando novamente as rotas dos clientes."))
      except Exception:
       pass
      pause=max(0.05,self.getnum("route_pause",1.0))
      deadline=time.monotonic()+pause
      while self.running and time.monotonic()<deadline:
       if self.playback_stop.is_set():
        break
       time.sleep(min(0.05,max(0.0,deadline-time.monotonic())))
     else:
      self.running = False
      self.playback_stop.set()
      self.release_inputs()
      self.multi_broadcast_active = False
      self.multi_run_targets = []
      try:
       self.root.after(0,lambda:self.multi_status.config(
        text="Sequência MGP concluída. Repetição desativada; comandos liberados."))
      except Exception:
       pass
    elif self.running:
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

 def activate_game_window(self):
  """Localiza e tenta ativar a janela NEWMT2 antes de enviar teclas/cliques."""
  title=str(self.v["game_title"].get()).strip().lower()
  if not title or gw is None:
   return False
  try:
   wins=[w for w in gw.getAllWindows()
         if w.title and title in w.title.lower() and w.width>0 and w.height>0]
   if not wins:
    return False
   # Prefere a maior janela visível, igual ao critério usado para localizar o jogo.
   win=max(wins,key=lambda w:w.width*w.height)
   hwnd=int(getattr(win,"_hWnd",0))
   if not hwnd:
    return False
   user32=ctypes.windll.user32
   SW_RESTORE=9
   try:
    if getattr(win,"isMinimized",False):
     user32.ShowWindow(hwnd,SW_RESTORE)
    else:
     user32.ShowWindow(hwnd,SW_RESTORE)
   except Exception:
    user32.ShowWindow(hwnd,SW_RESTORE)
   try: win.restore()
   except Exception: pass
   try: win.activate()
   except Exception: pass
   # Tentativa nativa adicional: permite a troca temporária da fila de entrada
   # entre a thread da macro e a thread proprietária da janela do jogo.
   current_hwnd=user32.GetForegroundWindow()
   current_tid=user32.GetWindowThreadProcessId(current_hwnd,None) if current_hwnd else 0
   target_tid=user32.GetWindowThreadProcessId(hwnd,None)
   attached=False
   try:
    if current_tid and target_tid and current_tid != target_tid:
     attached=bool(user32.AttachThreadInput(current_tid,target_tid,True))
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.SetActiveWindow(hwnd)
    user32.SetFocus(hwnd)
   finally:
    if attached:
     try: user32.AttachThreadInput(current_tid,target_tid,False)
     except Exception: pass
   deadline=time.monotonic()+1.8
   while time.monotonic()<deadline:
    if int(user32.GetForegroundWindow())==hwnd and self.game_window_is_active():
     return True
    # Repetir a solicitação de foco, pois o Windows pode atrasar a ativação.
    try: user32.SetForegroundWindow(hwnd)
    except Exception: pass
    time.sleep(0.05)
   return self.game_window_is_active()
  except Exception:
   return self.game_window_is_active()

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

 def record_individual_hotkey(self):
  """F7 controla exclusivamente a rota individual do cliente selecionado."""
  if self.recording:
   if self._recording_multi_key is not None:
    self.stop_record()
   return
  targets=self.selected_multi_windows()
  if len(targets)!=1:
   self.root.after(0,lambda:messagebox.showinfo("Rota individual","Selecione exatamente um cliente na lista MGP antes de usar F7."))
   return
  self.record_selected_multi_route()

 def record_mgp_hotkey(self):
  """F6 controla exclusivamente a rota compartilhada MGP."""
  if self.recording:
   if self._recording_multi_key is None:
    self.stop_record()
   return
  self._recording_multi_key=None
  targets=self.selected_multi_windows()
  if targets:
   # A rota compartilhada é gravada em um cliente selecionado e depois pode
   # ser reproduzida sequencialmente nos demais.
   if not self.activate_target_window(targets[0],allow_when_stopped=True):
    messagebox.showwarning("Rota MGP","Não foi possível dar foco ao primeiro cliente selecionado.")
    return
   self._recording_target_window=targets[0]
   self._recording_target_hwnd=int(getattr(targets[0],"_hWnd",0) or 0)
  self.record_route()

 # Compatibilidade com chamadas antigas de botões/perfis.
 def recording_hotkey(self):
  self.record_individual_hotkey()

 def _resolve_recording_target(self):
  """Resolve uma única janela NEWMT2 para esta gravação; nunca usa apenas o título no decorrer da captura."""
  if self._recording_target_window is not None and self._recording_target_hwnd:
   return self._recording_target_window, self._recording_target_hwnd
  try:
   active=gw.getActiveWindow() if gw else None
   title=str(self.v["game_title"].get()).strip().lower()
   if active and active.title and title in active.title.lower() and int(getattr(active,"_hWnd",0) or 0):
    return active, int(active._hWnd)
   wins=[w for w in gw.getAllWindows() if w.title and title in w.title.lower() and w.width>0 and w.height>0] if gw else []
   if wins:
    w=max(wins,key=lambda x:x.width*x.height)
    return w,int(getattr(w,"_hWnd",0) or 0)
  except Exception:
   pass
  return None,0

 def _recording_target_is_active(self):
  """Exige o HWND exato selecionado; outra janela do jogo ou a interface nunca contam."""
  hwnd=int(getattr(self,"_recording_target_hwnd",0) or 0)
  if not hwnd:
   return False
  try:
   return int(ctypes.windll.user32.GetForegroundWindow())==hwnd
  except Exception:
   return False

 def _begin_recording_capture(self):
  if not self.recording or self._recording_capture_started or not self._recording_target_is_active():
   return
  self._recording_waiting_focus=False
  self._recording_capture_started=True
  self.record_started=time.monotonic()
  self.mouse_listener=mouse.Listener(on_click=self.on_click)
  self.mouse_listener.start()
  self.start_raw_mouse_capture()
  try:
   self.key_hook=keyboard.hook(self.on_keyboard_event)
  except Exception as e:
   self.key_hook=None
   self.status.config(text="Mouse gravando; falha no hook do teclado: "+str(e))
  else:
   self.status.config(text="GRAVANDO somente na janela NEWMT2 selecionada. Cliques fora dela serão ignorados.")
  try:
   self.key_listener=pynput_keyboard.Listener(on_press=self.on_key_press,on_release=self.on_key_release)
   self.key_listener.start()
  except Exception as e:
   self.status.config(text="Mouse/Hook ativo; fallback de teclado indisponível: "+str(e))
  if hasattr(self,"multi_route_status"):
   self.multi_route_status.config(text="Gravando somente na janela NEWMT2 selecionada...")

 def _wait_for_recording_focus(self):
  if not self.recording or not self._recording_waiting_focus:
   return
  if self._recording_target_is_active():
   self._begin_recording_capture()
   return
  self.status.config(text="Aguardando foco da janela NEWMT2 selecionada. Nenhuma ação está sendo gravada ainda.")
  self.root.after(100,self._wait_for_recording_focus)

 def record_route(self):
  if mouse is None or pynput_keyboard is None or pdi is None or gw is None or keyboard is None:
   messagebox.showerror("Dependências","Execute ABRIR_AQUI.bat para instalar pynput, keyboard, pydirectinput e pygetwindow.")
   return
  if self.recording:
   return
  target,hwnd=self._resolve_recording_target()
  if target is None or not hwnd:
   messagebox.showerror("Janela do jogo não encontrada","Não encontrei uma janela NEWMT2 válida para vincular a gravação.")
   return
  self._recording_target_window=target
  self._recording_target_hwnd=hwnd
  try:
   self.game_rect=(int(target.left),int(target.top),int(target.width),int(target.height))
  except Exception:
   self.game_rect=self.find_game_window()
  if not self.game_rect:
   messagebox.showerror("Janela do jogo não encontrada","Não consegui obter a área da janela NEWMT2 selecionada.")
   return
  self.recording=True
  self._recording_waiting_focus=True
  self._recording_capture_started=False
  self.route_points=[]
  self.events=[]
  self.record_started=0.0
  self.pressed_keys.clear()
  self.mouse_buttons.clear()
  self.last_mouse_pos=None
  self.status.config(text="Aguardando foco da janela NEWMT2 selecionada. A gravação começará quando ela ficar ativa.")
  if hasattr(self,"multi_route_status"):
   self.multi_route_status.config(text="Aguardando foco do cliente selecionado para iniciar a gravação...")
  self.root.after(50,self._wait_for_recording_focus)
  self.root.after(0,self.render_route)

 def in_game_rect(self,x,y):
  if not self.game_rect:
   return False
  left,top,width,height=self.game_rect
  return left <= x < left+width and top <= y < top+height

 def on_click(self,x,y,button,pressed):
  if not self.recording or not self._recording_capture_started:
   return
  btn=str(button).split(".")[-1]
  # Soltura de botão já gravado é preservada mesmo se o foco mudar,
  # para evitar que a rota deixe o botão preso durante a troca de cliente.
  if btn=="right" and not pressed:
   if btn in self.mouse_buttons:
    self.mouse_buttons.discard(btn)
    self.events.append({"t":time.monotonic()-self.record_started,"type":"mouse_up","button":"right"})
    self.root.after(0,self.render_route)
   return
  # Nenhum novo clique/botão é aceito fora do HWND exato e da área do jogo.
  if not self._recording_target_is_active() or not self.in_game_rect(x,y):
   return
  if btn=="right":
   if pressed and btn not in self.mouse_buttons:
    self.mouse_buttons.add(btn)
    self.events.append({"t":time.monotonic()-self.record_started,"type":"mouse_down","button":"right"})
    self.root.after(0,self.render_route)
   return
  if not pressed:
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
  if not self.recording or not self._recording_capture_started or "right" not in self.mouse_buttons:
   return
  if not self._recording_target_is_active():
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
  if not self.recording or not self._recording_capture_started:
   return
  if not name or name in ("f6","f7","f8","f9","esc"):
   return
  # Exige o HWND exato para key_down; key_up de tecla já registrada é mantido.
  if kind == "down" and not self._recording_target_is_active():
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
  if not self.recording or not self._recording_capture_started or not self._recording_target_is_active():
   return
  name=self.normalize_key(key)
  if not name or name in ("f6","f7","f8","f9","esc") or name in self.pressed_keys:
   return
  self.pressed_keys.add(name)
  self.events.append({"t":time.monotonic()-self.record_started,"type":"key_down","key":name})

 def on_key_release(self,key):
  # A tecla pode ser solta durante uma troca rápida de foco; não descarte key_up.
  if not self.recording or not self._recording_capture_started:
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
  stop_t=(time.monotonic()-self.record_started) if self._recording_capture_started else 0.0
  for key in list(self.pressed_keys):
   self.events.append({"t":stop_t,"type":"key_up","key":key})
  for button in list(self.mouse_buttons):
   if button == "right" and self._recording_capture_started:
    self.events.append({"t":stop_t,"type":"mouse_up","button":"right"})
  self.pressed_keys.clear()
  self.recording=False
  self._recording_waiting_focus=False
  self._recording_capture_started=False
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
  if self._recording_multi_key is not None:
   self.multi_client_routes[self._recording_multi_key]=list(self.events)
   self._recording_multi_key=None
   self.update_multi_route_status()
  self._recording_target_hwnd=0
  self._recording_target_window=None
  self.status.config(text=f"Gravação encerrada: {len(self.events)} ações.")
  if hasattr(self,"multi_route_status"):
   self.multi_route_status.config(text=f"Rota MGP gravada: {len(self.events)} ações. Pronta para teste nos clientes selecionados.")
  self.render_route()
  if self._cycle4_record_slot is not None:
   self.save_cycle4_recorded_stage()

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
  if hasattr(self,"multi_route_status"):
   self.multi_route_status.config(text="Rota MGP: nenhuma rota gravada.")
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
  targets=list(self.multi_run_targets) if self.multi_broadcast_active and self.multi_run_targets else []
  # Rotas individuais podem existir mesmo quando a rota compartilhada está vazia.
  if pdi is None or (not self.events and not (targets and self.multi_client_routes)):
   return
  if targets:
   for w in targets:
    if self.playback_stop.is_set() or (bot_mode and not self.running):
     break
    if not self.activate_target_window(w,allow_when_stopped=True):
     self.root.after(0,lambda title=getattr(w,"title","cliente"):self.multi_status.config(
      text=f"Não foi possível ativar {title}; rota interrompida para evitar comandos na janela errada."))
     break
    time.sleep(self.multi_delay())
    rect=(int(w.left),int(w.top),int(w.width),int(w.height))
    route=self.multi_client_routes.get(self.multi_route_key(w),self.events)
    if not route:
     self.root.after(0,lambda title=getattr(w,"title","cliente"):self.multi_status.config(text=f"Sem rota individual ou compartilhada para {title}; cliente ignorado."))
     continue
    shared_events=self.events
    self.events=route
    try:
     ok=self.execute_route_for_rect(rect,bot_mode,expected_hwnd=int(getattr(w,"_hWnd",0)))
    finally:
     self.events=shared_events
    if not ok:
     break
    # Pequena janela neutra após a soltura total, antes de mudar o foco.
    # Evita que a próxima janela receba eventos colados à limpeza anterior.
    if not self.playback_stop.is_set() and (not bot_mode or self.running):
     time.sleep(0.12)
   return
  rect=self.find_game_window()
  if not rect:
   self.root.after(0,lambda:self.status.config(text="Janela do jogo não encontrada; rota não executada."))
   return
  # Identifica o HWND correspondente ao retângulo escolhido, mesmo que o
  # clique no botão Ligar tenha deixado a interface do macro em primeiro plano.
  target_hwnd=None
  try:
   title=str(self.v["game_title"].get()).strip().lower()
   candidates=[w for w in gw.getAllWindows() if w.title and title in w.title.lower()
               and int(w.width)>0 and int(w.height)>0
               and (int(w.left),int(w.top),int(w.width),int(w.height))==tuple(rect)]
   if candidates:
    target_hwnd=int(getattr(candidates[0],"_hWnd",0) or 0)
  except Exception:
   pass
  self.execute_route_for_rect(rect,bot_mode,expected_hwnd=target_hwnd)

 def execute_route_for_rect(self,rect,bot_mode=False,expected_hwnd=None):
  if pdi is None or not self.events:
   return
  # Salva a posição do cursor e garante a soltura de TODAS as teclas/botões,
  # inclusive se a reprodução falhar. Movimento relativo via Windows SendInput.
  held_keys=set(); held_buttons=set()
  # Registre TODAS as teclas citadas na rota, não apenas as que parecem
  # pressionadas no fim. Alguns jogos/clients podem perder um KEY_UP durante
  # troca de foco; a limpeza reforçada abaixo reaplica a soltura no dono da rota.
  route_keys={str(e.get("key", "")).strip() for e in self.events
              if e.get("type") in ("key_down", "key_up") and str(e.get("key", "")).strip()}
  # pydirectinput aplica uma pausa padrao apos CADA comando. Em rotas com
  # muitos deltas de mouse isso cria travadas artificiais. Desative-a apenas
  # durante a reproducao; os tempos gravados ja controlam o ritmo.
  old_pause=getattr(pdi,"PAUSE",0.1)
  pdi.PAUSE=0
  playback_start=time.perf_counter()
  focus_lost=False
  def target_has_focus():
   if expected_hwnd is None:
    return self.game_window_is_active()
   try:
    return int(ctypes.windll.user32.GetForegroundWindow()) == int(expected_hwnd)
   except Exception:
    return False
  def wait_until_target_returns():
   nonlocal playback_start, focus_lost
   if target_has_focus():
    return True
   focus_lost=True
   pause_started=time.perf_counter()
   self.root.after(0,lambda:self.status.config(text="Macro ligado — aguardando você voltar para a janela do Metin2."))
   while not target_has_focus():
    if self.playback_stop.is_set() or (bot_mode and not self.running):
     return False
    time.sleep(0.05)
   playback_start += time.perf_counter()-pause_started
   self.root.after(0,lambda:self.status.config(text="Metin2 reconhecido — retomando a gravação."))
   return True
  try:
   for event in sorted(list(self.events), key=lambda item:item.get("t",0)):
    # Nunca envie entrada global se outro cliente/app tomou o foco.
    if not wait_until_target_returns():
     break
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
    # O foco pode mudar durante a espera de um evento; confira novamente.
    if not wait_until_target_returns():
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
   # SendInput/pydirectinput enviam eventos globais. Antes de liberar teclas,
   # confirme que o cliente dono da rota está realmente em primeiro plano.
   # Se o foco foi roubado durante a rota, tente recuperá-lo; se não conseguir,
   # aborte a sequência e NUNCA avance para o próximo cliente.
   cleanup_focus_ok = True
   # Não rouba o foco de outro aplicativo; espera o usuário voltar ao jogo.
   if expected_hwnd is not None and not target_has_focus():
    cleanup_focus_ok = wait_until_target_returns() if (not self.playback_stop.is_set() and (not bot_mode or self.running)) else False
   # Só envie key-up/mouse-up depois de confirmar o foco do dono da rota.
   # A liberação acontece AQUI, antes de execute_route() ativar outra janela.
   if cleanup_focus_ok:
    keys_to_release=set(held_keys) | route_keys | {"space", "w", "a", "s", "d"}
    for setting in ("attack_key", "mount_key", "camera_key", "combo_key"):
     try:
      value=str(self.v[setting].get()).strip().lower()
      if value:
       keys_to_release.update(part.strip() for part in value.split("+") if part.strip())
     except Exception:
      pass
    # Duas passagens de KEY_UP reduzem o risco de o jogo manter movimento
    # preso quando um client perde foco durante a transição. Isto só é enviado
    # depois de confirmar que a janela dona da rota está em primeiro plano.
    for _release_pass in range(2):
     for key in keys_to_release:
      try:pdi.keyUp(key)
      except Exception:pass
     for btn in ("right", "left", "middle"):
      try:pdi.mouseUp(button=btn)
      except Exception:pass
     if _release_pass == 0:
      time.sleep(0.06)
   # Não reposiciona o cursor ao final: evita saltos involuntários.
   try:pdi.PAUSE=old_pause
   except Exception:pass
   if not cleanup_focus_ok:
    # Só encerre se NÃO foi possível recuperar o HWND dono da rota.
    # Perda temporária de foco, seguida de retorno ao mesmo Metin2, é uma
    # pausa normal: não pode desligar o macro nem impedir o próximo ciclo.
    self.playback_stop.set()
    if bot_mode:
     self.running=False
    msg="Rota interrompida: não foi possível confirmar o foco e liberar os comandos do cliente anterior. A sequência foi parada por segurança."
    self.root.after(0,lambda message=msg:self.multi_status.config(text=message))
   if bot_mode and not self.running:
    self.unclip_cursor()
  # Perda temporaria de foco nao significa falha: se o usuario voltou ao
  # mesmo HWND e a limpeza foi concluida, a rota pode continuar normalmente.
  # Retorne falso somente quando houve parada solicitada ou falha de seguranca.
  return cleanup_focus_ok and not self.playback_stop.is_set() and (not bot_mode or self.running)

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
   if hasattr(self,"potion_intervals"): d["potion_settings"]=self.get_potion_settings()
   if hasattr(self,"multi_mode"):
    d["mgp_multicliente"]={"mode":self.multi_mode.get(),"config_mode":self.multi_config_mode.get(),"profiles":self.multi_profiles,"client_routes":self.multi_client_routes,
      "switch_enabled":self.multi_switch_enabled.get(),"switch_delay":self.multi_switch_delay.get(),
      "selected_titles":[w.title for w in self.selected_multi_windows()]}
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
    elif k=="potion_settings" and hasattr(self,"potion_intervals"): self.set_potion_settings(val)
    elif k=="mgp_multicliente" and hasattr(self,"multi_mode"):
     self.multi_mode.set(val.get("mode","overlay"));self.multi_config_mode.set(val.get("config_mode","shared"));self.multi_profiles=val.get("profiles",{});self.multi_client_routes=val.get("client_routes",{})
     self.multi_switch_enabled.set(val.get("switch_enabled",False));self.multi_switch_delay.set(val.get("switch_delay","0.18"))
     self.refresh_multi_windows()
     self.update_multi_route_status()
     wanted=set(val.get("selected_titles",[]))
     for i,w in enumerate(self.multi_window_refs):
      if w.title in wanted:self.multi_list.selection_set(i)
    elif k in self.v:self.v[k].set(val)
   if not self.events and self.route_points:self.events=self.route_points
   self.render_route();self.status.config(text="Perfil carregado.")
  except Exception as e:messagebox.showerror("Erro",str(e))
 def tick(self):
  if self.running and self.started:
   s=int(time.time()-self.started);self.clock.config(text=f"Tempo: {s//3600:02}:{s//60%60:02}:{s%60:02}")
  self.root.after(500,self.tick)
 UPDATE_REPO = "lolprogif/lol"
 UPDATE_CURRENT = "FIX13"
 UPDATE_PACKAGE_ASSET = "LOI_UPDATE.zip"
 UPDATE_HASH_ASSET = "LOI_UPDATE.sha256"

 def check_updates(self):
  if getattr(self, "update_busy", False): return
  self.update_busy = True
  self.status.config(text="Status: verificando atualizações no GitHub...")
  threading.Thread(target=self._update_check_worker, daemon=True).start()

 def _update_check_worker(self):
  try:
   api=f"https://api.github.com/repos/{self.UPDATE_REPO}/releases/latest"
   req=urllib.request.Request(api,headers={"Accept":"application/vnd.github+json","User-Agent":"LOI-CATFARM-PRO-Updater"})
   with urllib.request.urlopen(req,timeout=20) as response: release=json.loads(response.read().decode("utf-8"))
   tag=str(release.get("tag_name","")).strip()
   assets={a.get("name"):a.get("browser_download_url") for a in release.get("assets",[])}
   pkg=assets.get(self.UPDATE_PACKAGE_ASSET); sha=assets.get(self.UPDATE_HASH_ASSET)
   if not tag or not pkg or not sha: raise RuntimeError("Release sem os assets obrigatórios LOI_UPDATE.zip e LOI_UPDATE.sha256.")
   match_latest=re.fullmatch(r"(?:v)?fix(\d+)",tag.lower())
   match_current=re.fullmatch(r"(?:v)?fix(\d+)",self.UPDATE_CURRENT.lower())
   if not match_latest or not match_current: raise RuntimeError("Tag de versão inválida. Use FIX seguido de número, por exemplo FIX14.")
   if int(match_latest.group(1))<=int(match_current.group(1)): self.root.after(0,lambda t=tag:self._update_result(f"Você já está na versão {self.UPDATE_CURRENT} (Release {t}).")); return
   self.root.after(0,lambda t=tag,u=pkg,h=sha:self._update_offer(t,u,h))
  except Exception as exc:
   self.root.after(0,lambda e=str(exc):self._update_result("Não foi possível verificar: "+e))
  finally:
   self.root.after(0,lambda:setattr(self,"update_busy",False))

 def _update_result(self,message):
  try: self.status.config(text="Status: "+message); messagebox.showinfo("LOI CATFARM PRO — Atualizações",message)
  except Exception: pass

 def _update_offer(self,tag,pkg_url,sha_url):
  # Clicar em VERIFICAR / ATUALIZAR já autoriza a instalação automática.
  self.status.config(text=f"Status: nova versão {tag}; baixando automaticamente...")
  threading.Thread(target=self._update_download_worker,args=(tag,pkg_url,sha_url),daemon=True).start()

 def _update_download_worker(self,tag,pkg_url,sha_url):
  try:
   tmp=Path(tempfile.gettempdir())/"LOI_CATFARM_PRO_update"; tmp.mkdir(parents=True,exist_ok=True)
   archive=tmp/"LOI_UPDATE.zip"; hashfile=tmp/"LOI_UPDATE.sha256"
   for url,dest in ((pkg_url,archive),(sha_url,hashfile)):
    req=urllib.request.Request(url,headers={"User-Agent":"LOI-CATFARM-PRO-Updater"})
    with urllib.request.urlopen(req,timeout=60) as r,dest.open("wb") as f: shutil.copyfileobj(r,f)
   expected=hashfile.read_text(encoding="utf-8",errors="replace").strip().split()[0].lower()
   if len(expected)!=64 or hashlib.sha256(archive.read_bytes()).hexdigest()!=expected: raise RuntimeError("Hash SHA-256 não confere. Nenhum arquivo foi alterado.")
   install=Path(sys.executable).resolve().parent; helper=install/"update_helper.exe"
   if not helper.is_file(): raise RuntimeError("Helper de atualização não instalado. Primeiro será necessário instalar a versão com o atualizador.")
   subprocess.Popen([str(helper),str(install),str(archive),str(os.getpid()),expected],cwd=str(install),close_fds=True)
   self.root.after(0,lambda t=tag:self.status.config(text=f"Status: instalando {t}; o LOI vai reiniciar."))
   self.root.after(700,self.close)
  except Exception as exc: self.root.after(0,lambda e=str(exc):self._update_result("Falha na atualização: "+e))

 def close(self):
  if getattr(self,"cycle4_running",False): self.stop_cycle4()
  try:
   self.spotify_close_embedded()
  except Exception: pass
  try:
   if self.tv_pip and self.tv_pip.winfo_exists(): self.tv_pip.destroy()
   if self.tv_full and self.tv_full.winfo_exists(): self.tv_full.destroy()
   if self.tv_player:self.tv_player.stop(); self.tv_vlc.release()
  except Exception: pass
  self.stop_potions()
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
