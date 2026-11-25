# Janela auxiliar WebView2 para hospedar Spotify como controle filho do painel Tkinter.
# Requer pywebview + Microsoft Edge WebView2 Runtime no Windows.
import os
import sys
import time
import ctypes
from pathlib import Path


def main():
    if os.name != 'nt' or len(sys.argv) < 3:
        return 2
    parent_hwnd = int(sys.argv[1])
    profile_dir = Path(sys.argv[2])
    profile_dir.mkdir(parents=True, exist_ok=True)
    os.environ['WEBVIEW2_USER_DATA_FOLDER'] = str(profile_dir)

    try:
        import webview
    except Exception as exc:
        try:
            (profile_dir.parent / 'spotify_webview_error.txt').write_text(
                'Não foi possível importar pywebview: ' + repr(exc), encoding='utf-8')
        except Exception:
            pass
        return 3

    user32 = ctypes.WinDLL('user32', use_last_error=True)
    GWL_STYLE = -16
    WS_CHILD = 0x40000000
    WS_VISIBLE = 0x10000000
    WS_POPUP = 0x80000000
    WS_CAPTION = 0x00C00000
    WS_THICKFRAME = 0x00040000
    WS_SYSMENU = 0x00080000
    WS_MINIMIZEBOX = 0x00020000
    WS_MAXIMIZEBOX = 0x00010000

    get_long = getattr(user32, 'GetWindowLongPtrW', user32.GetWindowLongW)
    set_long = getattr(user32, 'SetWindowLongPtrW', user32.SetWindowLongW)
    get_long.argtypes = [ctypes.c_void_p, ctypes.c_int]
    get_long.restype = ctypes.c_ssize_t
    set_long.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_ssize_t]
    set_long.restype = ctypes.c_ssize_t
    user32.SetParent.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    user32.SetParent.restype = ctypes.c_void_p
    user32.SetWindowPos.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                                    ctypes.c_int, ctypes.c_int, ctypes.c_uint]
    user32.SetWindowPos.restype = ctypes.c_bool

    window = webview.create_window(
        'Spotify — LOI CATFARM PRO',
        'https://open.spotify.com/',
        width=1000,
        height=650,
        min_size=(480, 320),
        resizable=True,
        on_top=False,
        background_color='#10151c',
    )

    def attach_when_ready():
        # pywebview expõe a janela nativa depois que o backend EdgeChromium cria o Form.
        for _ in range(120):
            try:
                native = window.native
                hwnd = int(native.Handle.ToInt64())
                if hwnd and user32.IsWindow(hwnd):
                    old = get_long(hwnd, GWL_STYLE)
                    new = (old & ~(WS_POPUP | WS_CAPTION | WS_THICKFRAME | WS_SYSMENU |
                                   WS_MINIMIZEBOX | WS_MAXIMIZEBOX)) | WS_CHILD | WS_VISIBLE
                    set_long(hwnd, GWL_STYLE, new)
                    user32.SetParent(hwnd, parent_hwnd)
                    user32.SetWindowPos(hwnd, 0, 0, 0, 1, 1, 0x0020 | 0x0004 | 0x0010)
                    return
            except Exception:
                pass
            time.sleep(0.15)
        try:
            (profile_dir.parent / 'spotify_webview_error.txt').write_text(
                'O WebView2 iniciou, mas não foi possível anexar o painel nativo ao LOI CATFARM PRO. '
                'Verifique a instalação do Microsoft Edge WebView2 Runtime.', encoding='utf-8')
        except Exception:
            pass

    window.events.shown += attach_when_ready
    try:
        webview.start(gui='edgechromium', debug=False)
    except Exception as exc:
        try:
            (profile_dir.parent / 'spotify_webview_error.txt').write_text(
                'Falha ao iniciar WebView2: ' + repr(exc), encoding='utf-8')
        except Exception:
            pass
        return 4
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
