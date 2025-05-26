import qrcode

img = qrcode.make('https://theloopywhisk.com/2024/06/29/gluten-free-burger-buns/')
type(img)  # qrcode.image.pil.PilImage
img.save("QR_code.png")