from settings.settings import MainSettings
from settings.settings import LANGUAGES_CMD

import customtkinter as ctk
import pyperclip

from pathlib import Path

from google import genai

from dotenv import load_dotenv 
import os


load_dotenv(Path(__file__).parent / "info" / "tokens.env")

API_KEY = os.getenv("GEMINI")

client = genai.Client(api_key=API_KEY)

class CMD_Translator(MainSettings):
  def __init__(self):
    super().__init__()
    self._build_ui()

  def _copy(self, textbox: ctk.CTkTextbox):
    text = textbox.get("0.0", "end").strip()
    if text:
      pyperclip.copy(text)

  def _set_output(self, text: str):
    self.output_box.configure(state="normal")
    self.output_box.delete("0.0", "end")
    self.output_box.insert("0.0", text)
    self.output_box.configure(state="disabled")

  def _on_translate(self):
    request  = self.input_box.get("0.0", "end").strip()
    from_env = self.from_var.get()
    to_env   = self.to_var.get()


    if from_env == "Human" and to_env in LANGUAGES_CMD:
      request = self.input_box.get("0.0", "end").strip()
      task_file = client.files.upload(file="prompts/to_console.txt")

      response = client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        contents = [task_file,
        f"{request}, Your task is to complete the assignment described in the file"]
      )

    if from_env in LANGUAGES_CMD and to_env == "Human":
      request = self.input_box.get("0.0", "end").strip()
      task_file = client.files.upload(file="prompts/from_console.txt")

      response = client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        contents = [task_file,
        f"{request}, Your task is to complete the assignment described in the file"]
      )

    if from_env in LANGUAGES_CMD and to_env in LANGUAGES_CMD:
      request = self.input_box.get("0.0", "end").strip()
      task_file = client.files.upload(file="prompts/from_any.txt")

      response = client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        contents = [task_file,
        f"{request}, Your task is to complete the assignment described in the file"]
      )


    self._set_output(response.text)

  def _on_explain(self):
    request = self.input_box.get("0.0", "end").strip()
    task_file = client.files.upload(file="prompts/explanation.txt")

    response = client.models.generate_content(
      model = "gemini-2.5-flash-lite",
      contents = [task_file,
      f"{request}, Your task is to complete the assignment described in the file"]
    )

    self._set_output(response.text)

  def _on_examples(self):
    request = self.input_box.get("0.0", "end").strip()
    task_file = client.files.upload(file="prompts/3_examples.txt")

    response = client.models.generate_content(
      model = "gemini-2.5-flash-lite",
      contents = [task_file,
      f"{request}, Your task is to complete the assignment described in the file"]
    )

  
    self._set_output(response.text)


if __name__ == "__main__":
  app = CMD_Translator()
  app.mainloop()