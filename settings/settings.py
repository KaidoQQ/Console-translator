import customtkinter as ctk
import webbrowser
from abc import abstractmethod


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

GITHUB_URL = "https://github.com/KaidoQQ" 

LANGUAGES = ["Human", "Git", "Linux", "Windows CMD", "Windows PowerShell"]
LANGUAGES_CMD = ["Git", "Linux", "Windows CMD", "Windows PowerShell"]


class MainSettings(ctk.CTk):
  def __init__(self):
    super().__init__()

    self.title("Command-Translator")
    self.geometry("860x620")
    self.minsize(700, 520)
    self.resizable(True, True)

    self._build_ui()

  def _build_ui(self):
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)  

    title = ctk.CTkLabel(
      self,
      text="Command-Translater",
      font=ctk.CTkFont(family="Courier New", size=26, weight="bold"),
    )
    title.grid(row=0, column=0, pady=(20, 4))

    subtitle = ctk.CTkLabel(
      self,
      text="Any language → terminal command or exclamation",
      font=ctk.CTkFont(size=12),
      text_color="gray60",
    )
    subtitle.grid(row=1, column=0, pady=(0, 14))

    dd_frame = ctk.CTkFrame(self, fg_color="transparent")
    dd_frame.grid(row=2, column=0, sticky="ew", padx=30)
    dd_frame.grid_columnconfigure((0, 1), weight=1)


    ctk.CTkLabel(
      dd_frame, text="What to translate",
      font=ctk.CTkFont(size=12), text_color="gray60"
    ).grid(row=0, column=0, sticky="w", padx=(0, 8))

    self.from_var = ctk.StringVar(value="Human")
    self.from_dd = ctk.CTkOptionMenu(
      dd_frame,
      values=LANGUAGES,
      variable=self.from_var,
      width=200,
      fg_color="#1f538d",
      button_color="#1a4a7a",
      button_hover_color="#163d66",
      font=ctk.CTkFont(size=13),
    )
    self.from_dd.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(2, 0))

    ctk.CTkLabel(
      dd_frame, text="What should this be translated into?",
      font=ctk.CTkFont(size=12), text_color="gray60"
    ).grid(row=0, column=1, sticky="w", padx=(8, 0))

    self.to_var = ctk.StringVar(value="Linux")
    self.to_dd = ctk.CTkOptionMenu(
      dd_frame,
      values=LANGUAGES,
      variable=self.to_var,
      width=200,
      fg_color="#1f538d",
      button_color="#1a4a7a",
      button_hover_color="#163d66",
      font=ctk.CTkFont(size=13),
    )
    self.to_dd.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(2, 0))

    areas_frame = ctk.CTkFrame(self, fg_color="transparent")
    areas_frame.grid(row=3, column=0, sticky="nsew", padx=30, pady=(18, 0))
    areas_frame.grid_columnconfigure((0, 1), weight=1)
    areas_frame.grid_rowconfigure(1, weight=1)
    self.grid_rowconfigure(3, weight=1)

    ctk.CTkLabel(
      areas_frame, text="Your request",
      font=ctk.CTkFont(size=12), text_color="gray60"
    ).grid(row=0, column=0, sticky="w", pady=(0, 4))

    self.input_box = ctk.CTkTextbox(
      areas_frame,
      font=ctk.CTkFont(family="Courier New", size=13),
      wrap="word",
      border_width=1,
      border_color="#2d5a8e",
    )
    self.input_box.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
    self.input_box.insert("0.0", "For example: Find files larger than 100 MB")

    copy_input_btn = ctk.CTkButton(
      areas_frame, text="⧉ Copy query",
      width=160, height=28,
      font=ctk.CTkFont(size=11),
      fg_color="#2b2b2b", hover_color="#3a3a3a",
      command=lambda: self._copy(self.input_box),
    )
    copy_input_btn.grid(row=2, column=0, padx=(0, 10), pady=(6, 0))

    ctk.CTkLabel(
      areas_frame, text="Result",
      font=ctk.CTkFont(size=12), text_color="gray60"
    ).grid(row=0, column=1, sticky="w", pady=(0, 4))

    self.output_box = ctk.CTkTextbox(
      areas_frame,
      font=ctk.CTkFont(family="Courier New", size=13),
      wrap="word",
      border_width=1,
      border_color="#2d5a8e",
      state="disabled",
    )
    self.output_box.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

    copy_output_btn = ctk.CTkButton(
      areas_frame, text="⧉ Copy query",
      width=170, height=28,
      font=ctk.CTkFont(size=11),
      fg_color="#2b2b2b", hover_color="#3a3a3a",
      command=lambda: self._copy(self.output_box),
    )
    copy_output_btn.grid(row=2, column=1, padx=(10, 0), pady=(6, 0))

    translate_btn = ctk.CTkButton(
      self,
      text="▶  Translate",
      font=ctk.CTkFont(size=14, weight="bold"),
      height=42,
      fg_color="#1f538d",
      hover_color="#163d66",
      command=self._on_translate,
    )
    translate_btn.grid(row=4, column=0, pady=(16, 0), padx=30, sticky="ew")

    options_frame = ctk.CTkFrame(self, fg_color="transparent")
    options_frame.grid(row=5, column=0, pady=(10, 0), padx=30, sticky="ew")
    options_frame.grid_columnconfigure((0, 1), weight=1)

    explain_btn = ctk.CTkButton(
      options_frame,
      text="📖  Detailed explanation",
      font=ctk.CTkFont(size=12),
      height=36,
      fg_color="#2b2b2b", hover_color="#3a3a3a",
      command=self._on_explain,
    )
    explain_btn.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    examples_btn = ctk.CTkButton(
      options_frame,
      text="💡  3 examples of use",
      font=ctk.CTkFont(size=12),
      height=36,
      fg_color="#2b2b2b", hover_color="#3a3a3a",
      command=self._on_examples,
    )
    examples_btn.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    # ── GitHub ───────────────────────────────────────────────────────────
    github_btn = ctk.CTkButton(
      self,
      text="★  GitHub",
      font=ctk.CTkFont(size=12),
      width=120, height=30,
      fg_color="transparent",
      hover_color="#2b2b2b",
      border_width=1,
      border_color="#3a3a3a",
      text_color="gray60",
      command=lambda: webbrowser.open(GITHUB_URL),
    )
    github_btn.grid(row=6, column=0, pady=(10, 16))

  # ─────────────────────────────────────────────────────────────────────────
  @abstractmethod
  def _copy(self, textbox: ctk.CTkTextbox):
    pass

  @abstractmethod
  def _set_output(self, text: str):
    pass

  @abstractmethod
  def _on_translate(self):
    pass

  @abstractmethod
  def _on_explain(self):
    pass


  @abstractmethod
  def _on_examples(self):
    pass
