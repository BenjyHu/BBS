import random
from PIL import Image,ImageDraw,ImageFont,ImageFilter

def check_code(width=150,height=30,char_length=5,font_size=28,font_file='kumo.ttf'):
    code = []
    # 生成图像
    img = Image.new(mode='RGB',size=(width,height),color=(255,255,255))
    # 生成画笔
    draw = ImageDraw.Draw(img,mode='RGB')

    def ran_char():
        '''
        随机生成字母
        :return:
        '''
        return chr(random.randint(65,90))

    def ran_color():
        '''
        随机生成颜色
        :return:
        '''
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    # 写入文本
    font = ImageFont.truetype(font_file,font_size)
    for i in range(char_length):
        char = ran_char()
        code.append(char)
        color = ran_color()
        draw.text([i*width/char_length,random.randint(0,4)],char,font=font,fill=color)

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0,width),random.randint(0,height)],fill=ran_color())

    # 画线
    for i in range(char_length):
        x1 = random.randint(0,width)
        x2 = random.randint(0,width)
        y1 = random.randint(0,height)
        y2 = random.randint(0,height)
        draw.line((x1,y1,x2,y2),fill=ran_color())

    # 画圆
    for i in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x,y,x+4,y+4),0,90,fill=ran_color())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    return img,''.join(code)
