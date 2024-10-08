import qrcode
from PIL import Image
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=25,
    border=5)
qr.add_data("https://github.com/Abu-Bakar-Rakib")
qr.make(fit=True)
ig = qr.make_image(fill_color="black", back_color="white")
ig.save("Github.png")
