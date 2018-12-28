from PIL import Image, ImageDraw, ImageFont
import codecs

DPI = 300

if DPI == 300:
    PAGE_SIZE = (2480, 3508)
    FONT_SIZE = 27 * 2
    TEXT_PADDING = 6
    PLACEHOLDER_DIMENSIONS = 222
    PLACEHOLDER_SIZE = (PLACEHOLDER_DIMENSIONS, PLACEHOLDER_DIMENSIONS)
    PLACEHOLDER_PADDING = 13
    OUTLINE_IN_PIXELS = 2
    TOP_PADDING = 50
    LEFT_PADDING = 50
    RIGHT_PADDING = 30
    NUMBER_IN_ROW = (2480 - LEFT_PADDING - RIGHT_PADDING) / (PLACEHOLDER_PADDING + PLACEHOLDER_DIMENSIONS)
    DPI = (300, 300)
else:
    PAGE_SIZE = (1240, 1754)
    FONT_SIZE = 27
    TEXT_PADDING = 3
    PLACEHOLDER_DIMENSIONS = 111
    PLACEHOLDER_SIZE = (PLACEHOLDER_DIMENSIONS, PLACEHOLDER_DIMENSIONS)
    PLACEHOLDER_PADDING = 14
    OUTLINE_IN_PIXELS = 1
    TOP_PADDING = 50
    LEFT_PADDING = 50
    RIGHT_PADDING = 30
    NUMBER_IN_ROW = (1240 - LEFT_PADDING - RIGHT_PADDING) / (PLACEHOLDER_PADDING + PLACEHOLDER_DIMENSIONS)
    DPI = (150, 150)

background_color = (256, 256, 256)
font_color = (0, 0, 0)
shadow_color = (255, 255, 255)

main_image = Image.new('RGB', PAGE_SIZE, background_color)

font = ImageFont.truetype("impact.ttf", FONT_SIZE)


def draw_outlined_text(draw, x, y, line, font, font_color):
    # move right
    draw.text((x - OUTLINE_IN_PIXELS, y), line, font=font, fill=shadow_color)
    # move left
    draw.text((x + OUTLINE_IN_PIXELS, y), line, font=font, fill=shadow_color)
    # move up
    draw.text((x, y + OUTLINE_IN_PIXELS), line, font=font, fill=shadow_color)
    # move down
    draw.text((x, y - OUTLINE_IN_PIXELS), line, font=font, fill=shadow_color)
    # diagnal left up
    draw.text((x - OUTLINE_IN_PIXELS, y + OUTLINE_IN_PIXELS), line, font=font, fill=shadow_color)
    # diagnal right up
    draw.text((x + OUTLINE_IN_PIXELS, y + OUTLINE_IN_PIXELS), line, font=font, fill=shadow_color)
    # diagnal left down
    draw.text((x - OUTLINE_IN_PIXELS, y - OUTLINE_IN_PIXELS), line, font=font, fill=shadow_color)
    # diagnal right down
    draw.text((x + OUTLINE_IN_PIXELS, y - OUTLINE_IN_PIXELS), line, font=font, fill=shadow_color)
    # main text
    draw.text((x, y), line, font=font, fill=font_color)



def put_text_on_lense_image(im_obj, lines_array, font):
    imgDrawer = ImageDraw.Draw(im_obj)
    line_w, line_h = imgDrawer.textsize('W', font=font)
    line_count = len(lines_array)
    if line_count == 3:
        t_padding = TEXT_PADDING/3
        initial_v_offset = 24
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

        draw_outlined_text(imgDrawer, h_offset, v_offset, stripped_line, font, font_color)


counter = 0
config = codecs.open('config.txt', 'r', 'utf-8')
for item in config.readlines():
    if item:
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
        for i in range(number):
            v_offset, h_offset = 0, 0
            v_offset = counter / NUMBER_IN_ROW * (PLACEHOLDER_DIMENSIONS + PLACEHOLDER_PADDING) + TOP_PADDING
            h_offset = counter % NUMBER_IN_ROW * (PLACEHOLDER_DIMENSIONS + PLACEHOLDER_PADDING) + LEFT_PADDING
            try:
                lense_image = Image.open('./images/'+name+'.png')
                resized_image = lense_image.resize(PLACEHOLDER_SIZE, Image.ANTIALIAS)
                lines_array = list(text.split(';'))
            except:
                resized_image = Image.new("RGB", PLACEHOLDER_SIZE, color='red')
                lines_array = ['image', 'not', 'found']
            put_text_on_lense_image(resized_image, lines_array, font)
            main_image.paste(resized_image, (h_offset, v_offset))
            counter += 1

main_image.show()
main_image.save('output.png', dpi=DPI)
