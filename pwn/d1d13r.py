
<!-- saved from url=(0045)http://d1d13r.stillhackinganyway.nl:9001/help -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body>import glob
import os
import subprocess
import tempfile

from flask import request, Flask, abort
from werkzeug.utils import secure_filename

os.chdir("/home/d1d13rp1")
app = application = Flask("d1d13rp1")
tempdir = tempfile.mkdtemp("d1d13rp1")
password = "you'll be needing this one!"

class tempfile(str):
    """Remove temporary file once the variable goes out of scope."""
    def __del__(self):
        os.unlink(self)

def save(f):
    """Store temporary file, which is wiped once the request finishes."""
    filename = os.path.basename(f.filename)
    if os.path.exists(filename):
        abort(404, "file already found")
    if ".py" in filename or ".so" in filename:
        abort(403, "filename forbidden")

    f.save(filename)
    return tempfile(filename)

def didier(*args):
    return subprocess.check_output(
        ("/usr/bin/env", "python") + args, stdin=open("/dev/null", "rb")
    )

@app.route("/help")
def help():
    return open(__file__, "rb").read()

@app.route("/oledump-process-command")
def oledump_process_command_help():
    return (
        didier("process-command.py", "--version") +
        didier("process-command.py", "--help") +
        didier("oledump.py", "--man")
    )

@app.route("/oledump-process-command", methods=["POST"])
def oledump_process_command():
    """https://blog.didierstevens.com/2017/07/22/oledump-py-vir/"""
    # Do HTTP headers include Basic Authentication?
    assert request.authorization.password == password
    filename = save(request.files["file"])
    return didier(
        "process-command.py", "-r", "oledump.py %f%", *glob.glob("*.vir")
    )

if __name__ == "__main__":
    app.run(debug=False)
</body></html>