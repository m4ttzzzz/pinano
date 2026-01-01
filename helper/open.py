import os
import sys

def open_file(filepath) -> tuple:
    extended_f = os.path.expanduser(filepath)
    with open(extended_f, 'rb') as f:
        line_ending_type = ""
        contents = f.read()
        if b"\r\n" in contents:
            line_ending_type = "Windows (CRLF)"
        elif b"\n" in contents:
            line_ending_type = "Unix (LF)"
        elif b"\r" in contents:
            line_ending_type = "Macintosh (CR)"
        else:
            line_ending_type = "undefined"
        return (line_ending_type, contents.decode(errors='ignore'))

def save_file(filepath, contents: str) -> str:
    extended_f = os.path.expanduser(filepath)
    if sys.platform == 'win32': extended_f = extended_f.replace("/", "\\")
    os.makedirs(os.path.dirname(extended_f), exist_ok=True)
    with open(extended_f, 'w', newline="\n") as f:
        f.write(contents)
    return extended_f

def optimize_path(tfp: str) -> str:
    tfp = os.path.expanduser(tfp)
    user = os.path.expanduser('~')
    ffp = tfp.replace(user, "~").replace("\\", "/")
    return ffp