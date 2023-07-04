import re
import fitz
import os
from typing import Final


baseDpi: Final[int] = 72
desiredDpi: Final[int] = 300
dpiRate = desiredDpi / baseDpi

yImageOffset = 10
xLeftImageOffset = 40
xRightImageOffset = 25

def findParenthesis(page:fitz.Page):
    lst: list = page.get_text(")", clip = (340, 0, page.bound().x1, page.bound().y1))
    
    regex = re.compile("^[(]\d.\d+[a-z]?[)]$")
    words = page.get_text("words", sort=True)
    matches = [w for w in words if regex.search(w[4])]
    for match in matches:
        irect:fitz.IRect = fitz.Rect(match[0], match[1], match[2], match[3]).irect 
        #page.draw_rect(irect, width=1.5, color=(1, 0, 0))
        pix = page.get_pixmap(dpi=desiredDpi)
        irect = fitz.IRect(xLeftImageOffset * dpiRate, (irect.y0 - yImageOffset) * dpiRate, (irect.x1 - xRightImageOffset) * dpiRate, (irect.y1 + yImageOffset) * dpiRate)
        pixn = fitz.Pixmap(fitz.csGRAY, irect, 0)
        pixn.set_origin(irect.x0, irect.y0)
        pixn.copy(pix, irect)
        pixn.save(f"./imgdata/{match[4][1:-1]}.png")



def findFromFile(filepath:str):
    doc = fitz.open(filepath)
    if not os.path.exists("./imgdata"):
        os.makedirs("imgdata")
    for i, page in enumerate(doc):
        findParenthesis(page)
