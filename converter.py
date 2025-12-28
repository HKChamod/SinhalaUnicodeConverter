import tkinter as tk
from tkinter import ttk, messagebox
import functools

# --- Dictionary Generation Logic (Singlish -> Unicode) ---
# Keeping this robust logic from previous versions
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


# --- Unicode -> FM Abhaya (Final Polished) ---

TOKEN_REPHA = 'ƒ'      # Special Repha Key
TOKEN_RAKARA = '`'     # Grave Key
TOKEN_YANSAYA = 'H'    # H Key

# Final Polished Map (including Ligatures)
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

# Override explicit characters if they exist in text
fm_abhaya_map['ෙ'] = 'f'

# Sorted keys for greedy matching (High Priority)
fm_sorted_keys = sorted(fm_abhaya_map.keys(), key=len, reverse=True)

def unicode_to_fm_abhaya(text):
    # PHASE 2: ALGORITHM
    
    # 1. DECOMPOSE COMPLEX VOWELS
    text = text.replace('ේ', 'ෙ' + '්')
    text = text.replace('ො', 'ෙ' + 'ා')
    text = text.replace('ෝ', 'ෙ' + 'ා' + '්')
    
    # 2. TOKENIZATION
    text = text.replace('\u0DBB\u0DCA\u200D', TOKEN_REPHA)
    text = text.replace('\u0DCA\u200D\u0DBB', TOKEN_RAKARA)
    text = text.replace('\u0DCA\u200D\u0DBA', TOKEN_YANSAYA)
    
    # 3. PROCESSING (Ligatures checks + Kombuwa Reordering)
    legacy_output = ""
    i = 0
    length = len(text)
    
    # Base Consonants for Swapping Check
    base_consonants = set()
    for k in fm_abhaya_map:
        if len(k) == 1 and k not in ['්', 'ා', 'ැ', 'ෑ', 'ි', 'ී', 'ු', 'ූ', 'ෙ', 'ෛ', 'ං', 'ඃ', 'ෘ', TOKEN_REPHA, TOKEN_RAKARA, TOKEN_YANSAYA]:
            # Basic heuristic: non-vowels are consonants
            if ord(k) > 128: 
                base_consonants.add(k)
    base_consonants.add('ඳ')
    base_consonants.add('ඦ')
    
    pre_movable = ['ෙ', 'ෛ']
    
    while i < length:
        # A. Priority Check: Multi-Char Ligatures (Greedy Match)
        match_found = False
        for key in fm_sorted_keys:
            if len(key) > 1 and text.startswith(key, i):
                # Found a multi-char ligature (e.g., 'ව්' or 'ධ්')
                # Check for Kombuwa logic? 
                # Ligatures like 'ව්' (Hal) generally don't take vowel signs like 'e'.
                # So we can safely map them directly.
                legacy_output += fm_abhaya_map[key]
                i += len(key)
                match_found = True
                break
        
        if match_found:
            continue
            
        # B. Standard Character Logic (Single Char)
        char = text[i]
        
        # Check if Start of Consonant Cluster for Reordering
        if char in base_consonants:
            cluster = char
            # Look ahead for cluster components (Rakara, Yansaya)
            j = i + 1
            temp_cluster_tokens = ""
            while j < length and text[j] in [TOKEN_RAKARA, TOKEN_YANSAYA]:
                temp_cluster_tokens += text[j]
                j += 1
            
            # Check for Pre-Movable Vowels (Kombuwa) immediately following the cluster
            if j < length and text[j] in pre_movable:
                pre_char = text[j]
                
                # REORDERING HAPPENS HERE
                # Output: PreChar + Base + Tokens
                legacy_output += fm_abhaya_map.get(pre_char, pre_char) # PreChar
                legacy_output += fm_abhaya_map.get(char, char)      # Base
                for tok in temp_cluster_tokens:                     # Tokens
                    legacy_output += fm_abhaya_map.get(tok, tok)
                
                # Skip processed chars (Base + Tokens + PreChar)
                i = j + 1
            else:
                # No swap needed, just output current char (and next iteration will handle tokens/modifiers naturally)
                # Actually, if we identified tokens here, we could output them, but simpler to just map char and let tokens be mapped in next loop?
                # YES, because single char mapping handles Token mapping correctly.
                # AND tokens are in base_consonants exclusion list? No tokens are in map.
                # So next loop iteration will hit Token, not base_cons logic, and map it.
                legacy_output += fm_abhaya_map.get(char, char)
                i += 1
        
        else:
            # Not a base consonant
            legacy_output += fm_abhaya_map.get(char, char)
            i += 1
            
    return legacy_output


class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sinhala Converter Support Suite - Polished")
        self.root.geometry("700x550")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Singlish to Unicode')
        self.setup_singlish_tab()
        
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Unicode to Legacy (FM Abhaya)')
        self.setup_legacy_tab()

    def setup_singlish_tab(self):
        container = self.tab1
        tk.Label(container, text="Singlish Input", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=(15, 5))
        self.s_input = tk.Text(container, height=8, font=("Segoe UI", 12))
        self.s_input.pack(fill="x", padx=20)
        self.s_input.bind("<KeyRelease>", self.update_singlish_conversion)
        
        tk.Label(container, text="Sinhala Unicode Output", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=(15, 5))
        self.s_output = tk.Text(container, height=8, font=("Iskoola Pota", 14))
        self.s_output.pack(fill="x", padx=20)
        
        btn_frame = tk.Frame(container)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Clear", command=lambda: self.clear(self.s_input, self.s_output), width=15).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Copy Output", command=lambda: self.copy(self.s_output), width=20, bg="#ddffdd").pack(side="left", padx=10)

    def setup_legacy_tab(self):
        container = self.tab2
        tk.Label(container, text="Sinhala Unicode Input", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=(15, 5))
        self.l_input = tk.Text(container, height=8, font=("Iskoola Pota", 12))
        self.l_input.pack(fill="x", padx=20)
        
        tk.Label(container, text="Legacy Font Output (FM Abhaya)", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=(15, 5))
        self.l_output = tk.Text(container, height=8, font=("Courier New", 12)) 
        self.l_output.pack(fill="x", padx=20)
        
        btn_frame = tk.Frame(container)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Convert", command=self.convert_unicode_legacy, width=20, bg="#ddddff").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Clear", command=lambda: self.clear(self.l_input, self.l_output), width=15).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Copy Output", command=lambda: self.copy(self.l_output), width=20, bg="#ddffdd").pack(side="left", padx=10)

    def update_singlish_conversion(self, event):
        content = self.s_input.get("1.0", tk.END).strip()
        converted = convert_singlish(content)
        self.s_output.delete("1.0", tk.END)
        self.s_output.insert("1.0", converted)

    def convert_unicode_legacy(self):
        content = self.l_input.get("1.0", tk.END).strip()
        converted = unicode_to_fm_abhaya(content)
        self.l_output.delete("1.0", tk.END)
        self.l_output.insert("1.0", converted)

    def clear(self, input_widget, output_widget):
        input_widget.delete("1.0", tk.END)
        output_widget.delete("1.0", tk.END)

    def copy(self, widget):
        content = widget.get("1.0", tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Copied", "Text copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
