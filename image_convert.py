from PIL import Image

INPUT='LogoFull.png'
OUTPUT='Logo.png'
ICON='Icon.ico'

def resize(f):
    i = Image.open(INPUT)
    ir=i.resize((i.width//f, i.height//f), Image.LANCZOS)
    ir.save(OUTPUT)
    i.save(ICON)


if __name__ == '__main__':
    resize(3)
