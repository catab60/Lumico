import pygame
import pystray
from PIL import Image, ImageDraw, ImageSequence
import threading
import ctypes
import ctypes.wintypes
import sys
import tempfile
import time
from classes import Button, Checkbox, SecondaryColor, PrimaryColor, TextEntry
import webbrowser
from tkinter import filedialog, Tk
import shutil
from win32com.client import Dispatch
import random
import string
import requests

import os


SW_HIDE = 0
SW_SHOW = 5

TENOR_API_KEY = "Tenor API KEY"

class Listing:
    def __init__(self, x, y, w, h, image_path, title, button_text, button_callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (w - 20, int(h * 0.6)))

        self.title = title
        self.font = pygame.font.SysFont("Century Gothic", 24)
        self.delete_font = pygame.font.SysFont("Century Gothic", 10)

        self.image_path = image_path


        button_width = w - 40
        button_height = 70
        button_x = x + 20
        button_y = y + h - (button_height * 2) - 30

        if button_callback == None:
            self.button = Button(
                button_x, button_y, button_width, button_height,
                button_text, self.set,
                color=(0, 130, 180),
                hovered_color=(100, 149, 237),
                fg=(255, 255, 255)
            )
        else:
            self.button = Button(
                button_x, button_y, button_width, button_height,
                button_text, button_callback,
                color=(0, 130, 180),
                hovered_color=(100, 149, 237),
                fg=(255, 255, 255)
            )


        delete_button_y = button_y + button_height + 10
        self.delete_button = Button(
            button_x, delete_button_y, button_width-220, button_height-50,
            "R", self.delete,
            color=(180, 50, 50),
            hovered_color=(220, 80, 80),
            fg=(255, 255, 255), font=self.delete_font
        )

    def draw(self, surface, y_offset=0):
        draw_rect = self.rect.move(0, y_offset)



        pygame.draw.rect(surface, (30, 30, 30), draw_rect, border_radius=12)
        pygame.draw.rect(surface, (60, 60, 60), draw_rect, width=2, border_radius=12)


        surface.blit(self.image, (draw_rect.x + 10, draw_rect.y + 10))


        title_y = draw_rect.y + self.image.get_height() + 20
        text_surf = self.font.render(self.title, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midtop=(draw_rect.centerx, title_y))
        surface.blit(text_surf, text_rect)

        btn_x = draw_rect.x + 20
        buy_btn_y = draw_rect.y + draw_rect.height - 90
        delete_btn_y = buy_btn_y - 300

        self.button.rect.topleft = (btn_x, buy_btn_y)
        self.delete_button.rect.topleft = (btn_x+230, delete_btn_y)

        self.button.draw(surface)
        self.delete_button.draw(surface)

    def delete(self):
        loaded_backgrounds.remove(self)

        shutil.rmtree(os.path.dirname(self.image_path))

        load_backgrounds()

    def set(self):
        change_wallpaper(f"{os.path.dirname(self.image_path)}/background.gif")

    def handle_event(self, event):
        self.button.handle_event(event)
        self.delete_button.handle_event(event)

def fetch_gifs(search_term="random", limit=20):
    url = "https://tenor.googleapis.com/v2/search"
    params = {
        "q": search_term,
        "key": TENOR_API_KEY,
        "limit": limit,
        "random": True,
        "media_filter": "gif"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        gif_urls = [result['media_formats']['gif']['url'] for result in data.get('results', [])]
        return gif_urls
    else:
        print(f"Error fetching GIFs: {response.status_code}")
        return []

def DisplaySearch(query):


    def SaveOnlineGif(path):
        name = "Community GIF"
        gif_path = path
        existing_titles = [bg.title for bg in loaded_backgrounds]
        

        if name in existing_titles:
            suffix = 1
            new_name = f"{name} {suffix}"
            while new_name in existing_titles:
                suffix += 1
                new_name = f"{name} {suffix}"
            name = new_name


        folder_path = f"wallpapers/{name}"
        os.makedirs(folder_path, exist_ok=True)


        new_gif_path = os.path.join(folder_path, "background.gif")
        shutil.copy(gif_path, new_gif_path)


        with Image.open(new_gif_path) as img:
            first_frame = next(ImageSequence.Iterator(img))
            cover_path = os.path.join(folder_path, "cover.png")
            first_frame.save(cover_path, format="PNG")

        load_backgrounds()
        ShowHome()
    def subproccess():
        global loaded_search
        global total_scroll_region_Download
        total_scroll_region_Download = 55 + 414
        loaded_search = []
        
        g = fetch_gifs(query, limit=22)

        
        shutil.rmtree("temp", ignore_errors=True)
        os.makedirs("temp", exist_ok=True)

        cols_list = 4
        start_x_list = 14 + 5
        start_y_list = 150
        w_list, h_list = 280, 400
        gap_list = 14


        for idx, gif in enumerate(g):

            response = requests.get(gif)
            if response.status_code == 200:
                with open(f"temp/{gif.split('/')[-1]}", "wb") as f:
                    f.write(response.content)


                row_list = idx // cols_list
                col_list = idx % cols_list

                x_list = start_x_list + col_list * (w_list + gap_list)
                y_list = start_y_list + row_list * (h_list + gap_list)


                filePath = f"temp/{gif.split('/')[-1]}"

                listing = Listing(
                    x=x_list,
                    y=y_list,
                    w=w_list,
                    h=h_list,
                    image_path=filePath,
                    title="",
                    button_text="Save",
                    button_callback=lambda x=filePath:SaveOnlineGif(x),
                )
                loaded_search.append(listing)
                if len(loaded_search)%4==0:
                    total_scroll_region_Download = total_scroll_region_Download + 414


    threading.Thread(target=subproccess).start()
    







        





ButtonColor = (100, 100, 100)


titlebarH = 50


tempdir = tempfile.mkdtemp()
Restart = False


window_visible = True

def get_hwnd():
    return pygame.display.get_wm_info()['window']

def hide_pygame_window():
    hwnd = get_hwnd()
    ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)

def show_pygame_window():
    hwnd = get_hwnd()
    ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)

def create_tray_image():
    logo = Image.open("assets/logo.png").convert("RGBA")

    image = logo.resize((64, 64))
    return image


def setup_tray():
    icon = pystray.Icon("pygame_tray", create_tray_image(), "Lumico")

    def toggle_window(icon, item):
        global window_visible
        if window_visible:
            hide_pygame_window()
            window_visible = False
        else:
            show_pygame_window()
            window_visible = True

    def on_quit(icon, item):
        icon.stop()
        pygame.quit()
        sys.exit()

    icon.menu = pystray.Menu(
        pystray.MenuItem(lambda item: "Show Window", toggle_window),
        pystray.MenuItem('Quit', on_quit)
    )
    icon.run()


def extract_gif_frames(gif_path):
    img = Image.open(gif_path)
    frames = []
    frame_count = 0
    try:
        while True:
            frame = img.convert("RGB")
            frame_path = os.path.join(tempdir, f"frame_{frame_count}.bmp")
            frame.save(frame_path, "BMP")
            frames.append(frame_path)
            img.seek(img.tell() + 1)
            frame_count += 1
    except EOFError:
        pass
    return frames

def set_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)


def sub_proccess(delay):
    global frames
    global Restart
    while True:
        for frame in frames:
            set_wallpaper(frame)
            time.sleep(delay)
            if Restart:
                Restart = False
                break

def main(gif_path=None, delay=1):
    global frames
    if gif_path:
        frames = extract_gif_frames(gif_path)
    
    if not hasattr(main, 'thread'):
        main.thread = threading.Thread(target=sub_proccess, args=(delay,), daemon=True)
        main.thread.start()

def change_wallpaper(path):
    global frames
    global Restart

    with open("data", "w") as f:
        f.write(path)

    frames = extract_gif_frames(path)
    Restart = True




pygame.init()
flags = pygame.NOFRAME
screen = pygame.display.set_mode((1200, 800), flags)
pygame.display.set_caption("Lumico")
icon = pygame.image.load("assets/logo.png").convert_alpha()
pygame.display.set_icon(icon)






show_pygame_window()


t = threading.Thread(target=setup_tray, daemon=True)
t.start()


drag = False
offset_x = 0
offset_y = 0

global_tab = 1


def resetButtons():
    HomePageButton.hovered_color = ButtonColor
    HomePageButton.color = SecondaryColor
    DownloadButton.hovered_color = ButtonColor
    DownloadButton.color = SecondaryColor
    CreateButton.hovered_color = ButtonColor
    CreateButton.color = SecondaryColor
    SettingsButton.hovered_color = ButtonColor
    SettingsButton.color = SecondaryColor
def ShowHome():
    global global_tab
    global scroll_y
    scroll_y = 0
    resetButtons()
    global_tab = 1
    HomePageButton.hovered_color = SecondaryColor
    HomePageButton.color = SecondaryColor
    


def ShowDownload():
    global global_tab
    global scroll_y
    scroll_y = 0
    resetButtons()
    global_tab = 2
    DownloadButton.hovered_color = SecondaryColor
    DownloadButton.color = SecondaryColor

def ShowCreate():
    global global_tab
    resetButtons()
    global_tab = 3
    CreateButton.hovered_color = SecondaryColor
    CreateButton.color = SecondaryColor

def ShowSettings():
    global global_tab
    resetButtons()
    global_tab = 4
    SettingsButton.hovered_color = SecondaryColor
    SettingsButton.color = SecondaryColor


def UploadGIF():
    root = Tk()
    global UploadText
    global UploadText_rect
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a GIF file",
        filetypes=[("GIF files", "*.gif")]
    )
    if file_path:
        file_name = os.path.basename(file_path)
        global UploadText
        UploadText = UploadFont.render(f"File selected: {file_name}", True, (230, 230, 230))
        UploadText_rect = UploadText.get_rect()
        UploadText_rect.centerx = 1200 // 2
        UploadText_rect.y = 500
        return file_path
    else:
        return None
    
def GenerateBackground():
    name = EntryName.text
    gif_path = gifuploaded
    existing_titles = [bg.title for bg in loaded_backgrounds]
    

    if name in existing_titles:
        suffix = 1
        new_name = f"{name} {suffix}"
        while new_name in existing_titles:
            suffix += 1
            new_name = f"{name} {suffix}"
        name = new_name


    folder_path = f"wallpapers/{name}"
    os.makedirs(folder_path, exist_ok=True)


    new_gif_path = os.path.join(folder_path, "background.gif")
    shutil.copy(gif_path, new_gif_path)

    with Image.open(new_gif_path) as img:
        first_frame = next(ImageSequence.Iterator(img))
        cover_path = os.path.join(folder_path, "cover.png")
        first_frame.save(cover_path, format="PNG")

    load_backgrounds()
    ShowHome()

    

def UploadGIF_MAIN():
    global gifuploaded
    gif_path = UploadGIF()
    if gif_path:
        gifuploaded = gif_path




def create_startup_shortcut():
    startup_folder = os.path.join(
        os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup'
    )
    shortcut_path = os.path.join(startup_folder, "main.lnk")


    python_exe = sys.executable


    script_path = os.path.abspath("main.py")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = python_exe
    shortcut.Arguments = f'"{script_path}"'
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.IconLocation = python_exe
    shortcut.save()

def remove_startup_shortcut():
    startup_folder = os.path.join(
        os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup'
    )
    shortcut_path = os.path.join(startup_folder, "main.lnk")
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)

gifuploaded = None

HomePageButton = Button(10, 60, 150, 30, "Home", ShowHome, color=SecondaryColor,hovered_color=ButtonColor, fg=(230,230,230))
DownloadButton = Button(170, 60, 150, 30, "Browse", ShowDownload, color=SecondaryColor,hovered_color=ButtonColor, fg=(230,230,230))
CreateButton = Button(330, 60, 150, 30, "Create", ShowCreate, color=SecondaryColor,hovered_color=ButtonColor, fg=(230,230,230))
SettingsButton = Button(880, 60, 150, 30, "Settings", ShowSettings, color=SecondaryColor,hovered_color=ButtonColor, fg=(230,230,230))
GithubPage = Button(1040, 60, 150, 30, "Credits", lambda:webbrowser.open("https://github.com/catab60"), color=SecondaryColor,hovered_color=ButtonColor, fg=(230,230,230))

UploadButton = Button(350, 200, 500, 200, "Upload .gif", UploadGIF_MAIN, color=SecondaryColor,hovered_color=ButtonColor, fg=(230,230,230), font_size=60)
UploadFont = pygame.font.SysFont("Century Gothic", 20)
UploadText = UploadFont.render("File selected: None", True, (230, 230, 230))
UploadText_rect = UploadText.get_rect()
UploadText_rect.centerx = 1200 // 2
UploadText_rect.y = 450
GenerateButton = Button(20, 680, 1160, 100, "Generate", GenerateBackground, color=(51,111,71),hovered_color=(73,159,102), fg=(230,230,230))

temp = pygame.font.SysFont("Century Gothic", 40)
temp = temp.render("Name:", True, (230, 230, 230))

EntryName = TextEntry((170, 610, 1010, 40))
SearchEntry = TextEntry((20, 100, 1010, 40))
EnterButton = Button(1040, 100, 150, 40, "Search", lambda:DisplaySearch(searchResult), color=SecondaryColor,hovered_color=ButtonColor, fg=(230,230,230))



StartCheckbox = Checkbox(20,100, 50, 1, "Start on startup")
previous_state = StartCheckbox.active
if os.path.exists("state"):
    with open("state", "r") as f:
        line = f.readline().strip()
        if line in ["True", "False"]:
            StartCheckbox.active = (line == "True")
            previous_state = StartCheckbox.active



HomeFrame = pygame.rect.Rect(10,90,1180,700)
DownloadFrame = pygame.rect.Rect(10,90,1180,700)
CreateFrame = pygame.rect.Rect(10,90,1180,700)
SettingsFrame = pygame.rect.Rect(10,90,1180,700)

InnerHome = pygame.Rect(
        HomeFrame.x,
        HomeFrame.y + 10,
        HomeFrame.width,
        HomeFrame.height - 20
    )

InnerDownload = pygame.Rect(
        DownloadFrame.x,
        DownloadFrame.y + 10,
        DownloadFrame.width,
        DownloadFrame.height - 20
)

global_font = pygame.font.Font("assets/font.ttf", 48)
titlebarLabel = global_font.render("Lumico", True, (230, 230, 230))

ShowHome()

loaded_search = []
def load_backgrounds():
    global loaded_backgrounds
    loaded_backgrounds = []

    cols_list = 4
    start_x_list = 14 + 5
    start_y_list = 100
    w_list, h_list = 280, 400
    gap_list = 14

    folders = sorted(
        f for f in os.listdir("wallpapers")
        if os.path.isdir(os.path.join("wallpapers", f))
    )

    for idx, folder in enumerate(folders):
        row_list = idx // cols_list
        col_list = idx % cols_list

        x_list = start_x_list + col_list * (w_list + gap_list)
        y_list = start_y_list + row_list * (h_list + gap_list)

        image_path = os.path.join("wallpapers", folder, "cover.png").replace("\\", "/")
        title = folder

        listing = Listing(
            x=x_list,
            y=y_list,
            w=w_list,
            h=h_list,
            image_path=image_path,
            title=title,
            button_text="Set",
            button_callback=None)
        loaded_backgrounds.append(listing)


load_backgrounds()



total_scroll_region_Home = 5

for i in range(len(loaded_backgrounds)):
    if i%4==0:
        total_scroll_region_Home = total_scroll_region_Home + 414




scroll_y = 0

if os.path.exists("data"):
    with open("data", "r") as f:
        saved_path = f.read().strip()
    main(saved_path, 0)
else:
    main("wallpapers/space/background.gif", 0)

searchResult = ""
prev_search = ""  



running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            hide_pygame_window()
            window_visible = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if mx >= screen.get_width() - 30 - 10 and my <= titlebarH:
                hide_pygame_window()
                window_visible = False
            elif my <= titlebarH:
                drag = True
                cursor = ctypes.wintypes.POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
                rect = ctypes.wintypes.RECT()
                hwnd = get_hwnd()
                ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                offset_x = cursor.x - rect.left
                offset_y = cursor.y - rect.top

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drag = False

        elif event.type == pygame.MOUSEMOTION and drag:

            cursor = ctypes.wintypes.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
            new_x = cursor.x - offset_x
            new_y = cursor.y - offset_y
            hwnd = get_hwnd()
            ctypes.windll.user32.SetWindowPos(hwnd, None, new_x, new_y, 0, 0, 0x0001)

        elif event.type == pygame.MOUSEWHEEL:
            if global_tab ==1:
                if HomeFrame.collidepoint(pygame.mouse.get_pos()):
                    scroll_y += event.y * 30
                    max_scroll = 0
                    min_scroll = min(0, HomeFrame.height - total_scroll_region_Home)
                    scroll_y = max(min_scroll, min(max_scroll, scroll_y))
            elif global_tab == 2:
                if DownloadFrame.collidepoint(pygame.mouse.get_pos()):
                    scroll_y += event.y * 30
                    max_scroll = 0
                    min_scroll = min(0, DownloadFrame.height - total_scroll_region_Download)
                    scroll_y = max(min_scroll, min(max_scroll, scroll_y))
            
        HomePageButton.handle_event(event)
        DownloadButton.handle_event(event)
        CreateButton.handle_event(event)
        SettingsButton.handle_event(event)
        GithubPage.handle_event(event)
        if global_tab == 4:
            StartCheckbox.handle_event(event)
        if global_tab == 1:
            for listing in loaded_backgrounds:
                listing.handle_event(event)
        if global_tab == 3:
            UploadButton.handle_event(event)
            GenerateButton.handle_event(event)
            EntryName.handle_event(event)
        if global_tab == 2:
            EnterButton.handle_event(event)
            SearchEntry.handle_event(event)
            searchResult = SearchEntry.text
            if searchResult != prev_search:
                prev_search = searchResult
            for listing in loaded_search:
                listing.handle_event(event)



    screen.fill(PrimaryColor)

    if StartCheckbox.active != previous_state:
        with open("state", "w") as f:
            f.write(str(StartCheckbox.active))

        if StartCheckbox.active:
            create_startup_shortcut()
        else:
            remove_startup_shortcut()
        previous_state = StartCheckbox.active

    HomePageButton.draw(screen)
    DownloadButton.draw(screen)
    CreateButton.draw(screen)
    SettingsButton.draw(screen)
    GithubPage.draw(screen)

    

    if global_tab == 1:

        pygame.draw.rect(screen, SecondaryColor, HomeFrame)

        screen.set_clip(InnerHome)

        for listing in loaded_backgrounds:
            listing.draw(screen, y_offset=scroll_y)
        screen.set_clip(None)
    
    elif global_tab == 2:
        
        pygame.draw.rect(screen, SecondaryColor, DownloadFrame)
        SearchEntry.draw(screen)
        EnterButton.draw(screen)

        screen.set_clip(InnerDownload)
        for listing in loaded_search:
            listing.draw(screen,y_offset=scroll_y)
        screen.set_clip(None)
    elif global_tab == 3:
        pygame.draw.rect(screen, SecondaryColor, CreateFrame)
        UploadButton.draw(screen)
        GenerateButton.draw(screen)
        EntryName.draw(screen)

        screen.blit(UploadText, UploadText_rect)
        screen.blit(temp, (20, 600))
        
    elif global_tab == 4:
        pygame.draw.rect(screen, SecondaryColor, SettingsFrame)
        StartCheckbox.draw(screen)


    pygame.draw.rect(screen, SecondaryColor, (0, 0, screen.get_width(), titlebarH))
    screen.blit(titlebarLabel, (10, 5))


    close_rect = pygame.Rect(screen.get_width() - 30 - 10,
                             (titlebarH - 30) // 2,
                             30, 30)
    pygame.draw.rect(screen, (200, 50, 50), close_rect)

    pygame.display.update()




pygame.quit()
