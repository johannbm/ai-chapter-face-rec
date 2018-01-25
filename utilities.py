import pickle
from PIL import ImageDraw, ImageFont


def convert_bounds_to_pil_format(location):
    top, right, bottom, left = location
    return [left, top, right, bottom]


def save_pickle_encodings(encodings, names):
    file_name = "people_encodings"
    with open(file_name, 'wb') as f:
        pickle.dump((encodings, names), f)


def load_pickle_encodings(file_name='people_encodings'):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


def draw_rect(pil_image, bounds, color=(255, 0, 0)):
    draw = ImageDraw.Draw(pil_image)
    draw.rectangle(convert_bounds_to_pil_format(bounds), outline=color)


def draw_name(pil_image, bounds, names):
    colors = [(255,0,0), (50,200,200), (200,200,50)]
    for i in range(len(names)):
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 45)
        draw.text((bounds[3], bounds[2] + 50*i), names[i], font=font, fill=colors[i])

