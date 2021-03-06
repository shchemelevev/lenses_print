import json
import math
import configparser
import codecs
from PIL import Image, ImageDraw, ImageFont


TOP_PADDING = 50
LEFT_PADDING = 50
RIGHT_PADDING = 30

BACKGROUND_COLOR = (256, 256, 256)
PAGE_SIZE = (2480, 3508)

PLACEHOLDER_DIMENSIONS = 222
PLACEHOLDER_PADDING = 13
PLACEHOLDER_SIZE = (PLACEHOLDER_DIMENSIONS, PLACEHOLDER_DIMENSIONS)

NUMBER_IN_ROW = 10  #(2480 - LEFT_PADDING - RIGHT_PADDING - 100) / (PLACEHOLDER_PADDING +
                    #                                            PLACEHOLDER_DIMENSIONS)

TEXT_PADDING = 6


def draw_outlined_text(draw, x, y, line, font, config):
    outline_size = config.getint('FONT', 'outline_size')
    outline_color = tuple(json.loads(config.get('FONT', 'outline_color')))
    color = tuple(json.loads(config.get('FONT', 'color')))
    # move right
    draw.text((x - outline_size, y), line, font=font, fill=outline_color)
    # move left
    draw.text((x + outline_size, y), line, font=font, fill=outline_color)
    # move up
    draw.text((x, y + outline_size), line, font=font, fill=outline_color)
    # move down
    draw.text((x, y - outline_size), line, font=font, fill=outline_color)
    # diagnal left up
    draw.text((x - outline_size, y + outline_size), line, font=font, fill=outline_color)
    # diagnal right up
    draw.text((x + outline_size, y + outline_size), line, font=font, fill=outline_color)
    # diagnal left down
    draw.text((x - outline_size, y - outline_size), line, font=font, fill=outline_color)
    # diagnal right down
    draw.text((x + outline_size, y - outline_size), line, font=font, fill=outline_color)
    # main text
    draw.text((x, y), line, font=font, fill=color)


def get_font(text, config):
    im_obj = Image.new('RGBA', (222, 222), (255, 255, 255))
    imgDrawer = ImageDraw.Draw(im_obj)
    max_radius = PLACEHOLDER_DIMENSIONS / 2 - 10
    current_font_size = config.getint('FONT', 'text_max_size')
    font = ImageFont.truetype(config.get('FONT', 'filename'), current_font_size)

    line_w, line_h = imgDrawer.textsize(text, font)
    current_radius = int(math.sqrt((line_w/2.0) * (line_w/2.0) + (line_h) * (line_h)))
    counter = 1
    while current_radius > max_radius:
        counter +=1
        current_font_size -= 1
        font = ImageFont.truetype(config.get('FONT', 'filename'), current_font_size)
        line_w, line_h = imgDrawer.textsize(text, font)
        current_radius = int(math.sqrt((line_w/2.0) * (line_w/2.0) + (line_h) * (line_h)))
    return font


def put_text_on_lense_image(im_obj, lines_array, config):
    imgDrawer = ImageDraw.Draw(im_obj)

    first_line = lines_array[0]
    font = get_font(first_line, config)
    line_w, line_h = imgDrawer.textsize(first_line, font=font)
    v_offset = PLACEHOLDER_DIMENSIONS / 2 - line_h
    h_offset = PLACEHOLDER_DIMENSIONS/ 2 - line_w / 2
    draw_outlined_text(imgDrawer, h_offset, v_offset, first_line.strip(), font, config)

    second_line = lines_array[1].strip()
    font = ImageFont.truetype(config.get('FONT', 'filename'), config.getint("FONT", 'power_size'))
    if '-' in second_line:
        w, h = imgDrawer.textsize(second_line+'-', font=font)
    else:
        w, h = imgDrawer.textsize(second_line, font=font)
    v_offset = PLACEHOLDER_DIMENSIONS / 2 + 5
    h_offset = (PLACEHOLDER_DIMENSIONS / 2.0 - w / 2.0)
    draw_outlined_text(imgDrawer, h_offset, v_offset, second_line, font, config)


def load_image(filename_without_ext):
    for ext in ['.png', '.jpg', 'jpeg']:
        try:
            lense_image = Image.open('./images/'+filename_without_ext+ext).convert('RGBA')
            return lense_image.resize(PLACEHOLDER_SIZE, Image.ANTIALIAS)
        except:
            pass
    raise ValueError('file not found')


def get_image_offset(image_number):
    v_offset = int(image_number / NUMBER_IN_ROW) * (PLACEHOLDER_DIMENSIONS + PLACEHOLDER_PADDING)\
               + TOP_PADDING
    h_offset = image_number % NUMBER_IN_ROW * (PLACEHOLDER_DIMENSIONS + PLACEHOLDER_PADDING) + LEFT_PADDING
    return (int(h_offset), int(v_offset))


def parse_input_attrs(line):
    try:
        name, number, text  = item.split('|')
        try:
            number = int(number)
        except:
            number = 1
    except:
        name = item.strip()
        number = 1
        text = ''
    return name, number, text


def get_print_config(config_filename):
    f = open(config_filename, 'r')
    result = dict()
    for item in f.readlines():
        name, value = item.strip().split('=')
        try:
            value = int(value)
        except:
            pass
        try:
            value = json.loads(value)
        except:
            pass
        result[name] = value
    return result


if __name__ == '__main__':
    counter = 0
    lenses_list_for_print = codecs.open('lenses_list_for_print.txt', 'r', 'utf-8')
    config = configparser.RawConfigParser()
    config.read('config.txt')



    main_image = Image.new('RGB', PAGE_SIZE, BACKGROUND_COLOR)

    for item in lenses_list_for_print.readlines():
        if item.strip():
            name, number, text = parse_input_attrs(item)
            for i in range(number):
                try:
                    resized_image = load_image(name)
                    lines_array = list(text.split(';'))
                except:
                    resized_image = Image.new("RGBA", PLACEHOLDER_SIZE, color='red')
                    lines_array = ['image', 'not', 'found']
                put_text_on_lense_image(resized_image, lines_array, config)
                # main_image.alpha_composite(resized_image, get_image_offset(counter))
                main_image.paste(resized_image, get_image_offset(counter), resized_image)
                counter += 1

    main_image.show()
    main_image.save('output.png', dpi=(300,300))
