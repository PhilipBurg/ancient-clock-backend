from PIL import Image, ImageFont, ImageDraw

OLED_WIDTH = 128
OLED_HEIGHT = 64

class ImageGenerator:
    def __init__(self, font="DejaVuSans.ttf", size=12):
        try:
            self.font = ImageFont.truetype(font, size)
        except OSError:
            self.font = ImageFont.load_default(size)

    def generate_text_image(self, text):
        img = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
        draw = ImageDraw.Draw(img)

        _, _, w, h = draw.textbbox((0, 0), text=text, font=self.font)
        x = (OLED_WIDTH - w) * 0.5
        y = (OLED_HEIGHT - h) * 0.5
        draw.text((x, y), text, font=self.font, fill="white")
        return img

ImageGenerator().generate_text_image("Hallo Welt").show()