import customtkinter as ctk
import tkinter as tk
import functools

# --- LOGIC CORE (PRESERVED) ---
ZWJ = '\u200D'
standalone_vowels = {'aa': 'ආ', 'aae': 'ඈ', 'ae': 'ඇ', 'a': 'අ', 'ii': 'ඊ', 'i': 'ඉ', 'uu': 'ඌ', 'u': 'උ', 'ee': 'ඒ', 'e': 'එ', 'oo': 'ඕ', 'o': 'ඔ', 'au': 'ඖ', 'ai': 'ඓ'}
consonants = {'k': 'ක', 'kh': 'ඛ', 'g': 'ග', 'gh': 'ඝ', 'ng': 'ඞ', 'nng': 'ඟ', 'ch': 'ච', 'chh': 'ඡ', 'j': 'ජ', 'jh': 'ඣ', 'ny': 'ඤ', 'jny': 'ඥ', 'ndg': 'ඦ', 't': 'ට', 'th': 'ඨ', 'd': 'ඩ', 'dh': 'ඪ', 'n': 'ණ', 'nd': 'ඬ', 'th': 'ත', 'd': 'ද', 'dh': 'ධ', 'n': 'න', 'nd': 'ඳ', 'p': 'ප', 'ph': 'ඵ', 'b': 'බ', 'bh': 'භ', 'm': 'ම', 'mb': 'ඹ', 'y': 'ය', 'r': 'ර', 'l': 'ල', 'w': 'ව', 'v': 'ව', 'sh': 'ශ', 'shh': 'ෂ', 's': 'ස', 'h': 'හ', 'f': 'ෆ', 'L': 'ළ', 'lh': 'ළ'}
vowel_signs = {'aa': 'ා', 'aae': 'ෑ', 'ae': 'ැ', 'a': '', 'ii': 'ී', 'i': 'ි', 'uu': 'ූ', 'u': 'ු', 'ee': 'ේ', 'e': 'ෙ', 'oo': 'ෝ', 'o': 'ො', 'au': 'ෞ', 'ai': 'ෛ'}
special_mappings = {'ru': 'රු', 'ruu': 'රූ', 'lu': 'ලු', 'luu': 'ලූ', 'ksha': 'ක්ෂ', 'hra': 'හ්‍ර', 'ri': 'රි', 'rii': 'රී'}

full_dict = {}
full_dict.update(standalone_vowels)
for c_eng, c_sin in consonants.items():
    full_dict[c_eng] = c_sin + '්'
    for v_eng, v_sign in vowel_signs.items():
        if v_eng == 'a': full_dict[c_eng + 'a'] = c_sin + v_sign
        else: full_dict[c_eng + v_eng] = c_sin + v_sign
    full_dict[c_eng + 'r' + 'a'] = c_sin + '්' + ZWJ + 'ර'
    full_dict[c_eng + 'y' + 'a'] = c_sin + '්' + ZWJ + 'ය'
full_dict.update(special_mappings)
sorted_keys = sorted(full_dict.keys(), key=len, reverse=True)

def convert_singlish(text):
    converted_text = ""
    i = 0
    while i < len(text):
        match_found = False
        for key in sorted_keys:
            if text.startswith(key, i):
                converted_text += full_dict[key]
                i += len(key)
                match_found = True
                break
        if not match_found:
            converted_text += text[i]
            i += 1
    return converted_text


# --- Unicode -> FM Abhaya Logic ---
TOKEN_REPHA = 'ƒ'
TOKEN_RAKARA = '`'
TOKEN_YANSAYA = 'H'

fm_abhaya_map = {
    # --- HIGH PRIORITY LIGATURES ---
    'ව්': 'õ', 
    'ම්': 'ï', 
    'ච්': 'É', 
    'ඬ්': 'å', 
    'ධ්': 'è', 
    'ට්‍': 'Ü', 
    'ඕ': '´', 
    'ඩ්': 'â', 
    'බ්': 'í',

    # --- Vowels & Modifiers ---
    '්': 'a', 'ා': 'd', 'ැ': 'e', 'ෑ': 'E',
    'ි': 's', 'ී': 'S', 'ු': 'q', 'ූ': 'Q',
    'ෙ': 'f', 
    'ෛ': 'I', 'ං': 'x', 'ඃ': 'H',
    'ෘ': 'D', 

    # --- Consonants (Lower Case) ---
    'ක': 'l', 'ඛ': 'L',
    'ග': '.', 'ඝ': '>',
    'ච': 'p', 'ඡ': 'P',
    'ජ': 'c', 'ඣ': 'C',
    'ට': 'g', 'ඨ': 'G',
    'ඩ': 'v', 'ඪ': 'V',
    'ණ': 'K', 
    'ත': ';', 'ථ': ':',
    'ද': 'o', 'ධ': 'O',
    'න': 'k', 'ඳ': 'K', 
    'ප': 'm', 'ඵ': ']',
    'බ': 'n', 'භ': 'N', 
    'ම': 'u', 'ඹ': 'U',
    'ය': 'h', 'ර': 'r',
    'ල': ',', 
    'ව': 'j', 
    'ශ': 'M', 
    'ෂ': '/', 
    'ස': 'i', 'හ': 'y',
    'ළ': '<', 
    'ෆ': 'Z', 
    'ඥ': '{', 
    'ඤ': '}', 
    'ඞ': 'W', 
    'ඟ': '\\', 

    # --- Initial Vowels ---
    'අ': 'w', 'ආ': 'W', 
    'ඇ': 'A', 'ඈ': 'A', 
    'ඉ': 'b', 'ඊ': 'B',
    'උ': 'L', 'ඌ': '|', 
    'එ': 't', 'ඒ': 'T',
    'ඔ': 'T', 
    'ඖ': 'Tw', 
    
    # Pre-mapped Tokens
    TOKEN_REPHA: TOKEN_REPHA,
    TOKEN_RAKARA: TOKEN_RAKARA,
    TOKEN_YANSAYA: TOKEN_YANSAYA
}

fm_abhaya_map['ෙ'] = 'f'
fm_sorted_keys = sorted(fm_abhaya_map.keys(), key=len, reverse=True)

def unicode_to_fm_abhaya(text):
    text = text.replace('ේ', 'ෙ' + '්')
    text = text.replace('ො', 'ෙ' + 'ා')
    text = text.replace('ෝ', 'ෙ' + 'ා' + '්')
    text = text.replace('\u0DBB\u0DCA\u200D', TOKEN_REPHA)
    text = text.replace('\u0DCA\u200D\u0DBB', TOKEN_RAKARA)
    text = text.replace('\u0DCA\u200D\u0DBA', TOKEN_YANSAYA)
    
    legacy_output = ""
    i = 0
    length = len(text)
    
    base_consonants = set()
    for k in fm_abhaya_map:
        if len(k) == 1 and k not in ['්', 'ා', 'ැ', 'ෑ', 'ි', 'ී', 'ු', 'ූ', 'ෙ', 'ෛ', 'ං', 'ඃ', 'ෘ', TOKEN_REPHA, TOKEN_RAKARA, TOKEN_YANSAYA]:
            if ord(k) > 128: 
                base_consonants.add(k)
    base_consonants.add('ඳ')
    base_consonants.add('ඦ')
    
    pre_movable = ['ෙ', 'ෛ']
    
    while i < length:
        match_found = False
        for key in fm_sorted_keys:
            if len(key) > 1 and text.startswith(key, i):
                legacy_output += fm_abhaya_map[key]
                i += len(key)
                match_found = True
                break
        
        if match_found:
            continue
            
        char = text[i]
        
        if char in base_consonants:
            cluster = char
            j = i + 1
            temp_cluster_tokens = ""
            while j < length and text[j] in [TOKEN_RAKARA, TOKEN_YANSAYA]:
                temp_cluster_tokens += text[j]
                j += 1
            
            if j < length and text[j] in pre_movable:
                pre_char = text[j]
                legacy_output += fm_abhaya_map.get(pre_char, pre_char)
                legacy_output += fm_abhaya_map.get(char, char)
                for tok in temp_cluster_tokens:
                    legacy_output += fm_abhaya_map.get(tok, tok)
                i = j + 1
            else:
                legacy_output += fm_abhaya_map.get(char, char)
                i += 1
        else:
            legacy_output += fm_abhaya_map.get(char, char)
            i += 1
            
    return legacy_output


# --- UI LAYER (CUSTOMTKINTER) ---
class SinhalaConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- THEME SETUP ---
        ctk.set_appearance_mode("Dark")
        self.title("Sinhala Converter Modern")
        self.geometry("900x650")
        
        # Define Colors
        self.color_bg_main = "#121212"    # Deep Black
        self.color_sidebar = "#0d0d0d"   # Slightly darker or same
        self.color_red = "#E50914"       # Vibrant Red
        self.color_white = "#FFFFFF"
        self.color_trans = "transparent"
        
        self.configure(fg_color=self.color_bg_main)

        # --- LAYOUT CONFIG ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar()
        self.create_main_area()
        
        # Default View
        self.show_singlish()

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=self.color_sidebar)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo = ctk.CTkLabel(self.sidebar_frame, text="SINHALA\nCONVERTER", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.color_red)
        self.logo.grid(row=0, column=0, padx=20, pady=(40, 30))
        
        self.btn_menu_singlish = ctk.CTkButton(self.sidebar_frame, text="Singlish to Unicode", 
                                             command=self.show_singlish, 
                                             fg_color=self.color_trans, hover_color="#2c2c2c", 
                                             height=40, anchor="w", font=ctk.CTkFont(size=14))
        self.btn_menu_singlish.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        self.btn_menu_legacy = ctk.CTkButton(self.sidebar_frame, text="Unicode to Legacy", 
                                           command=self.show_legacy, 
                                           fg_color=self.color_trans, hover_color="#2c2c2c",
                                           height=40, anchor="w", font=ctk.CTkFont(size=14))
        self.btn_menu_legacy.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=0) # Title
        self.main_frame.grid_rowconfigure(1, weight=1) # Content
        
        self.content_title = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=22, weight="bold"))
        self.content_title.grid(row=0, column=0, sticky="w", pady=(10, 20))
        
        self.content_area = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_area.grid(row=1, column=0, sticky="nsew")
        self.content_area.grid_columnconfigure(0, weight=1)

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def set_active_button(self, btn):
        self.btn_menu_singlish.configure(fg_color=self.color_trans, text_color="gray90")
        self.btn_menu_legacy.configure(fg_color=self.color_trans, text_color="gray90")
        btn.configure(fg_color=self.color_red, text_color="white")

    # --- VIEWS ---
    def show_singlish(self):
        self.set_active_button(self.btn_menu_singlish)
        self.content_title.configure(text="Singlish to Unicode")
        self.clear_content()
        
        # Input
        lbl_in = ctk.CTkLabel(self.content_area, text="Singlish Input", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_in.pack(anchor="w", pady=(0, 5))
        self.s_input = ctk.CTkTextbox(self.content_area, height=150, font=ctk.CTkFont(size=14))
        self.s_input.pack(fill="x", pady=(0, 20))
        self.s_input.bind("<KeyRelease>", self.run_singlish_logic)
        
        # Output
        lbl_out = ctk.CTkLabel(self.content_area, text="Sinhala Unicode Output", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_out.pack(anchor="w", pady=(0, 5))
        self.s_output = ctk.CTkTextbox(self.content_area, height=150, font=ctk.CTkFont(family="Iskoola Pota", size=16))
        self.s_output.pack(fill="x", pady=(0, 20))
        
        # Buttons
        btn_row = ctk.CTkFrame(self.content_area, fg_color="transparent")
        btn_row.pack(fill="x")
        
        ctk.CTkButton(btn_row, text="Clear", fg_color=self.color_red, hover_color="#b3000b", 
                      command=lambda: self.clear_boxes(self.s_input, self.s_output)).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_row, text="Copy Output", fg_color="#222222", hover_color="#333333", border_width=1, border_color="gray30",
                      command=lambda: self.copy_text(self.s_output)).pack(side="left")

    def show_legacy(self):
        self.set_active_button(self.btn_menu_legacy)
        self.content_title.configure(text="Unicode to Legacy (FM Abhaya)")
        self.clear_content()
        
        # Input
        lbl_in = ctk.CTkLabel(self.content_area, text="Sinhala Unicode Input", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_in.pack(anchor="w", pady=(0, 5))
        self.l_input = ctk.CTkTextbox(self.content_area, height=150, font=ctk.CTkFont(family="Iskoola Pota", size=14))
        self.l_input.pack(fill="x", pady=(0, 20))
        
        # Output
        lbl_out = ctk.CTkLabel(self.content_area, text="Legacy Output (FM Abhaya)", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_out.pack(anchor="w", pady=(0, 5))
        
        # CRITICAL FONT SETUP
        legacy_font = ctk.CTkFont(family="FMAbhaya", size=18)
        # Note: If font not installed, it falls back. CTkFont handles family properly.
        
        self.l_output = ctk.CTkTextbox(self.content_area, height=150, font=legacy_font)
        self.l_output.pack(fill="x", pady=(0, 20))
        
        # Buttons
        btn_row = ctk.CTkFrame(self.content_area, fg_color="transparent")
        btn_row.pack(fill="x")
        
        ctk.CTkButton(btn_row, text="Convert", fg_color=self.color_red, hover_color="#b3000b",
                      command=self.run_legacy_logic).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_row, text="Clear", fg_color="#222222", hover_color="#333333", border_width=1, border_color="gray30",
                      command=lambda: self.clear_boxes(self.l_input, self.l_output)).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_row, text="Copy Output", fg_color="#222222", hover_color="#333333", border_width=1, border_color="gray30",
                      command=lambda: self.copy_text(self.l_output)).pack(side="left")

    # --- ACTIONS ---
    def run_singlish_logic(self, event):
        text = self.s_input.get("1.0", "end-1c")
        res = convert_singlish(text)
        self.s_output.delete("1.0", "end")
        self.s_output.insert("1.0", res)
    
    def run_legacy_logic(self):
        text = self.l_input.get("1.0", "end-1c")
        res = unicode_to_fm_abhaya(text)
        self.l_output.delete("1.0", "end")
        self.l_output.insert("1.0", res)

    def clear_boxes(self, t1, t2):
        t1.delete("1.0", "end")
        t2.delete("1.0", "end")

    def copy_text(self, widget):
        text = widget.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(text)
        # Optional toast or separate window? CTk doesn't have builtin toast.
        # Minimal feedback via button text logic or ignored.
        
if __name__ == "__main__":
    app = SinhalaConverterApp()
    app.mainloop()
