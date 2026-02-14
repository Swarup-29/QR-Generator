import qrcode
from PIL import Image
import os

data = input("Enter your URL : ")
qr_size_cm = 6                     
dpi = 300                          

logo_file = ""  # Enter The path of Logo or img      


pixels = int((qr_size_cm / 2.54) * dpi)


qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)

qr.add_data(data)
qr.make()

img = qr.make_image(fill_color="black",
                    back_color="white").convert('RGB')


img = img.resize((pixels, pixels), Image.LANCZOS)


try:
    logo = Image.open(logo_file).convert("RGBA")

    logo_size = int(img.size[0] * 0.20)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    mask = Image.new("L", (logo_size, logo_size), 0)
    draw = Image.new("RGBA", (logo_size, logo_size))

    from PIL import ImageDraw
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, logo_size, logo_size), fill=255)

    circular_logo = Image.new("RGBA", (logo_size, logo_size))
    circular_logo.paste(logo, (0, 0), mask=mask)

    padding = int(logo_size * 0.25)
    bg_size = logo_size + padding

    background = Image.new("RGBA", (bg_size, bg_size), (255, 255, 255, 255))

    pos_bg = ((bg_size - logo_size) // 2,
              (bg_size - logo_size) // 2)

    background.paste(circular_logo, pos_bg, mask=circular_logo)

    pos = ((img.size[0] - bg_size) // 2,
           (img.size[1] - bg_size) // 2)

    img.paste(background, pos, mask=background)

except:
    print("Logo not found — generating QR without logo")

count = 1

file_name = f"Banner_qr{count}.png"

while os.path.exists(file_name):
    count += 1
    file_name = f"Banner_qr{count}.png"

img.save(file_name,dpi=(dpi,dpi))

print(f"Saved as {file_name}")