from textual.app import App
from textual.widgets import TextArea, Header, Footer, Input
from helper.open import open_file, save_file, optimize_path
import sys

class pinano(App):
    CSS_PATH = 'style.tcss'
    BINDINGS = [
        ('ctrl+s', 'save_file', "Saves the current file.")
    ]
    def __init__(self, path: str = ""):
        self.contents = ""
        self.is_new_file = True
        self.path = path
        self.line_ending = "New file"

        if self.path:
            self.line_ending, self.contents = open_file(path)
            self.is_new_file = False
        
        self.text_area = TextArea(show_line_numbers=True)
        self.footer = Footer()
        self.header = Header(show_clock=True)
        self.file_input = Input(type="text", disabled=True)
        super().__init__()
    
    # Base pinano class
    def compose(self):
        yield self.text_area
        yield self.header
        yield self.footer
        yield self.file_input
    
    def on_mount(self):
        self.title = f'pinano — "{optimize_path(self.path)}"' if self.path else "pinano"
        self.sub_title = self.line_ending
        self.text_area.load_text(self.contents)
    
    def action_save_file(self):
        if self.path:
            save_file(self.path, self.text_area.text)
            self.line_ending, self.contents = open_file(self.path)
            self.on_mount()
        else:
            self.file_input.disabled = False
            self.file_input.focus()
    
    def on_input_submitted(self, message: Input.Submitted):
        value = message.value
        input_ins = message.input

        if input_ins == self.file_input:
            self.path = save_file(value, self.text_area.text)
            self.line_ending, self.contents = open_file(self.path)
            self.on_mount()
            self.file_input.disabled = True



if __name__ == "__main__":
    pinano_ins = pinano(sys.argv[1] if len(sys.argv) > 1 else "")
    pinano_ins.run()