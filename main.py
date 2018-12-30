import json
import ConfigParser
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

NUMBER_IN_ROW = (2480 - LEFT_PADDING - RIGHT_PADDING) / (PLACEHOLDER_PADDING + PLACEHOLDER_DIMENSIONS)

TEXT_PADDING = 6


def draw_outlined_text(draw, x, y, line, font):
    # move right
    draw.text((x - font.outline_size, y), line, font=font, fill=font.outline_color)
    # move left
    draw.text((x + font.outline_size, y), line, font=font, fill=font.outline_color)
    # move up
    draw.text((x, y + font.outline_size), line, font=font, fill=font.outline_color)
    # move down
    draw.text((x, y - font.outline_size), line, font=font, fill=font.outline_color)
    # diagnal left up
    draw.text((x - font.outline_size, y + font.outline_size), line, font=font, fill=font.outline_color)
    # diagnal right up
    draw.text((x + font.outline_size, y + font.outline_size), line, font=font, fill=font.outline_color)
    # diagnal left down
    draw.text((x - font.outline_size, y - font.outline_size), line, font=font, fill=font.outline_color)
    # diagnal right down
    draw.text((x + font.outline_size, y - font.outline_size), line, font=font, fill=font.outline_color)
    # main text
    draw.text((x, y), line, font=font, fill=font.color)


def put_text_on_lense_image(im_obj, lines_array, font):
    imgDrawer = ImageDraw.Draw(im_obj)
    line_w, line_h = imgDrawer.textsize('W', font=font)
    line_count = len(lines_array)
    if line_count == 3:
        t_padding = TEXT_PADDING/3
        initial_v_offset = 10
    else:
        t_padding = TEXT_PADDING
        initial_v_offset = (PLACEHOLDER_DIMENSIONS - line_count * (line_w + t_padding) - t_padding) / 2

    for index, line in enumerate(lines_array):
        stripped_line = line.strip()
        if '-' in line:
            w, h = imgDrawer.textsize(stripped_line+'-', font=font)
        else:
            w, h = imgDrawer.textsize(stripped_line, font=font)
        h_offset = (PLACEHOLDER_DIMENSIONS - w) / 2
        v_offset = initial_v_offset + index * (h + t_padding)

        draw_outlined_text(imgDrawer, h_offset, v_offset, stripped_line, font)


def load_image(filename_without_ext):
    for ext in ['.png', '.jpg', 'jpeg']:
        try:
            lense_image = Image.open('./images/'+filename_without_ext+ext).convert('RGBA')
            return lense_image.resize(PLACEHOLDER_SIZE, Image.ANTIALIAS)
        except:
            pass
    raise ValueError('file not found')


def get_image_offset(image_number):
    v_offset = image_number / NUMBER_IN_ROW * (PLACEHOLDER_DIMENSIONS + PLACEHOLDER_PADDING) + TOP_PADDING
    h_offset = image_number % NUMBER_IN_ROW * (PLACEHOLDER_DIMENSIONS + PLACEHOLDER_PADDING) + LEFT_PADDING
    return (h_offset, v_offset)


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
    config = ConfigParser.RawConfigParser()
    config.read('config.txt')

    font = ImageFont.truetype(config.get('FONT', 'filename'), config.getint('FONT','size'))
    font.outline_size = config.getint('FONT', 'outline_size')
    font.outline_color = tuple(json.loads(config.get('FONT', 'outline_color')))
    font.color = tuple(json.loads(config.get('FONT', 'color')))

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
                put_text_on_lense_image(resized_image, lines_array, font)
                # main_image.alpha_composite(resized_image, get_image_offset(counter))
                main_image.paste(resized_image, get_image_offset(counter), resized_image)
                counter += 1

    main_image.show()
    main_image.save('output.png', dpi=(300,300))
