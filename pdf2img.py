import re
import fitz
import os
import tarfile
from io import BytesIO
from typing import Final


baseDpi: Final[int] = 72
desiredDpi: Final[int] = 300
dpiRate: Final[int] = desiredDpi / baseDpi

yImageOffset = 70
xLeftImageOffset = 40
xRightImageOffset = 25

output: list = []


def findParenthesis(page: fitz.Page):
    regex = re.compile("^[(][\d]{1,2}.\d+[a-z]?[)]$")
    words = page.get_text("words", sort=True)
    matches = [w for w in words if regex.search(w[4])]
    for match in matches:
        irect: fitz.IRect = fitz.Rect(match[0], match[1], match[2], match[3]).irect
        # page.draw_rect(irect, width=1.5, color=(1, 0, 0))
        pix = page.get_pixmap(dpi=desiredDpi)
        irect = fitz.IRect(
            xLeftImageOffset * dpiRate,
            (irect.y0 - yImageOffset) * dpiRate,
            (irect.x1 - xRightImageOffset) * dpiRate,
            (irect.y1 + yImageOffset) * dpiRate,
        )
        pixn = fitz.Pixmap(fitz.csGRAY, irect, 0)
        pixn.set_origin(irect.x0, irect.y0)
        pixn.copy(pix, irect)
        output.append((pixn.tobytes(), f"{match[4][1:-1]}"))

def findFromFile(filepath: str, bookname: str):
    doc = fitz.open(filepath)
    if not os.path.exists("./data"):
        os.makedirs("data")
    for i, page in enumerate(doc):
        findParenthesis(page)
    directories: dict = {}
    with tarfile.open("./data/" + bookname, "w") as tar:
        for imgByte, name in output:
            name: str = name
            for index, text in enumerate(name):
                if not text.isalpha() and not text.isdecimal():
                    name = name.replace(text, '.')                 
            
            # indexOfSemiColon = name.find(".")
            # front = name[:indexOfSemiColon]
            # back = name[indexOfSemiColon + 1 :]
            # if front not in directories:
            #     directories[front] = 1
            #     dirInfo = tarfile.TarInfo(name=front)
            #     dirInfo.type = tarfile.DIRTYPE
            #     dirInfo.mode = 0o777
            #     tar.addfile(tarinfo=dirInfo)

            s = BytesIO()
            s.write(imgByte)
            s.seek(0)

            tinfo = tarfile.TarInfo(name=(name+".png"))
            tinfo.size = len(s.getbuffer())

            tar.addfile(tarinfo=tinfo, fileobj=s)
    tar.close()
