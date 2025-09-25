from PIL import Image, ImageFont, ImageDraw

OLED_WIDTH = 128
OLED_HEIGHT = 64

CLEAR = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))


HIEROGLYPHS = {
    "Man_standing": "𓀀",
    "Seated_woman": "𓀁",
    "Seated_deity": "𓀭",
    "Owl": "𓅓",
    "Quail_chick": "𓅪",
    "Horned_ox": "𓃜",
    "Lion": "𓃭",
    "Cobra": "𓆗",
    "Reed_leaf": "𓇋",
    "Sun_disk": "𓇳",
    "Water": "𓈗",
    "Placenta": "𓐍",
    "Sickle": "𓌳",
    "Penis": "𓂸",
    "Elephant": "𓃰",
    "Scarab": "𓆣",
    "Hand": "𓂧",
    "Eye": "𓂀",
    "Pillar": "𓊽",
    "Ankh": "𓋹",
    "Fish": "𓆛",
    "Goose": "𓅭",
    "Turtle": "𓆉",
    "Falcon": "𓅃",
    "Star": "𓇼"
}


def generate_image(text, font):
    img = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
    draw = ImageDraw.Draw(img)

    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
    text_width = x1 - x0
    text_height = y1 - y0

    target_x = (OLED_WIDTH - text_width) / 2 - x0
    target_y = (OLED_HEIGHT - text_height) / 2 - y0

    draw.text((target_x, target_y), text, font=font, fill="white")

    return img


class ImageGenerator:
    def __init__(self, font="DejaVuSans.ttf", small_size=12, large_size=40):
        try:
            self.latin_small = ImageFont.truetype(font, small_size)
        except OSError:
            self.latin_small = ImageFont.load_default()

        try:
            self.glyph_font = ImageFont.truetype("NotoSansEgyptianHieroglyphs-Regular.ttf", 40)
        except OSError:
            self.glyph_font = ImageFont.load_default()

        try:
            self.latin_large = ImageFont.truetype(font, large_size)
        except OSError:
            self.latin_large = ImageFont.load_default()

    def generate_text_image(self, text):
        if len(text) == 1:
            return generate_image(text, self.latin_large)
        else:
            return generate_image(text, self.latin_small)

    def generate_hieroglyph(self, glyph):
        return generate_image(HIEROGLYPHS[glyph], self.glyph_font)
