from math import cos, pi, sin
from pathlib import Path
from random import Random

from PIL import Image, ImageDraw, ImageFont


SIZE = 1200
FONT_DIR = Path('/usr/share/fonts/truetype/noto')
INK = '#211131'
CREAM = '#fff3d2'
PINK = '#ff539d'
GOLD = '#ffbd74'
image = Image.new('RGB', (SIZE, SIZE))
draw = ImageDraw.Draw(image)


def gradient(top, bottom, stops):
    for row in range(top, bottom + 1):
        fraction = (row - top) / (bottom - top) * (len(stops) - 1)
        segment = min(int(fraction), len(stops) - 2)
        blend = fraction - segment
        color = tuple(round(start + (end - start) * blend)
                      for start, end in zip(stops[segment], stops[segment + 1]))
        draw.line((0, row, SIZE, row), fill=color)


def title(text, center, limit, size, color, face='CondensedBlack', stroke=0):
    while True:
        font = ImageFont.truetype(str(FONT_DIR / f'NotoSansDisplay-{face}.ttf'), size)
        if font.getlength(text) + 2 * stroke <= limit:
            break
        size -= 1
    draw.text(center, text, font=font, anchor='mm', fill=color,
              stroke_width=stroke, stroke_fill=INK)


def star(center, outer, inner, points, color, outline=None):
    center_x, center_y = center
    vertices = []
    for index in range(points * 2):
        angle = pi * index / points - pi / 2
        radius = outer if index % 2 == 0 else inner
        vertices.append((center_x + cos(angle) * radius, center_y + sin(angle) * radius))
    draw.polygon(vertices, fill=color, outline=outline, width=3 if outline else 1)


def shape(start, curves, fill, outline=None, width=1):
    vertices = [start]
    for control_a, control_b, end in curves:
        origin = vertices[-1]
        for step in range(1, 25):
            ratio = step / 24
            reverse = 1 - ratio
            vertices.append(tuple(reverse**3 * origin[axis]
                                  + 3 * reverse**2 * ratio * control_a[axis]
                                  + 3 * reverse * ratio**2 * control_b[axis]
                                  + ratio**3 * end[axis] for axis in range(2)))
    draw.polygon(vertices, fill=fill)
    if outline:
        draw.line(vertices + [start], fill=outline, width=width, joint='curve')


def skyline():
    rng = Random(62013)
    for left in range(-20, 1200, 56):
        height = rng.randrange(32, 148)
        roof = 590 - height
        width = rng.randrange(38, 64)
        draw.rectangle((left, roof, left + width, 602), fill='#623161')
        draw.rectangle((left + 7, roof - 8, left + width - 7, roof), fill='#623161')
        for window_y in range(roof + 13, 582, 19):
            for window_x in range(left + 8, left + width - 6, 14):
                if rng.random() < .43:
                    draw.rectangle((window_x, window_y, window_x + 5, window_y + 4), fill='#f897a4')


def palm(base, crown, scale, color):
    base_x, base_y = base
    crown_x, crown_y = crown
    shape((base_x - 11, base_y), [((base_x - 4, base_y - 100),
          (crown_x - 41, crown_y + 80), crown), ((crown_x - 15, crown_y + 75),
          (base_x + 15, base_y - 100), (base_x + 12, base_y))], color)
    branches = [(-125, 22, -95, -72), (-115, -50, -50, -94), (-50, -91, 5, -100),
                (58, -88, 53, -102), (116, -55, 100, -85), (132, 20, 107, -69), (71, 67, 103, -22)]
    for tip_x, tip_y, high_x, high_y in branches:
        def point(offset_x, offset_y):
            return crown_x + offset_x * scale, crown_y + offset_y * scale

        tip = point(tip_x, tip_y)
        shape(crown, [(point(high_x * .48, high_y * .65), point(high_x, high_y), tip),
                      (point(tip_x * .78, tip_y - 8), point(high_x * .38, high_y * .28), crown)], color)


def backdrop():
    gradient(0, 614, [(31, 15, 52), (116, 41, 104), (221, 83, 138), (255, 168, 119)])
    draw.ellipse((412, 236, 788, 608), fill='#ffbf80')
    for row, width in [(433, 6), (455, 8), (481, 10), (512, 13), (553, 17)]:
        draw.rectangle((425, row, 775, row + width), fill='#f99285')
    skyline()
    draw.rectangle((0, 590, SIZE, 607), fill='#ffafad')
    gradient(607, 890, [(106, 57, 104), (72, 40, 83), (40, 24, 62)])
    draw.polygon([(0, 670), (600, 600), (1200, 670), (1200, 898), (0, 898)], fill='#39254e')
    draw.line([(0, 695), (600, 609), (1200, 695)], fill='#d37c9b', width=4)
    draw.polygon([(65, 813), (266, 768), (358, 768), (179, 813)], fill='#9d637e')
    draw.polygon([(1023, 775), (1169, 809), (1200, 808), (1200, 793), (1112, 775)], fill='#9d637e')
    palm((78, 671), (146, 389), 1.21, '#321940')
    palm((1141, 675), (1076, 380), 1.14, '#321940')


def convertible():
    draw.ellipse((112, 735, 1091, 858), fill='#281731')
    for center_x in (336, 907):
        draw.ellipse((center_x - 75, 680, center_x + 75, 838), fill=INK)
        draw.ellipse((center_x - 49, 705, center_x + 49, 815), fill='#52345d', outline='#e1a4cc', width=6)
        draw.ellipse((center_x - 22, 738, center_x + 22, 782), fill='#ebb0d4')
    shape((208, 638), [((351, 579), (672, 570), (818, 615)),
          ((878, 640), (910, 673), (928, 687)), ((666, 720), (367, 727), (208, 638))], '#49213f', INK, 11)
    draw.rounded_rectangle((495, 521, 585, 675), 30, fill='#452039', outline=INK, width=8)
    draw.rounded_rectangle((487, 529, 560, 597), 21, fill='#389a9a', outline=INK, width=7)
    draw.arc((496, 542, 548, 585), 195, 355, fill='#85e0cd', width=4)


def ghost_driver():
    shape((494, 570), [((462, 579), (459, 603), (471, 627)), ((484, 658), (525, 661), (550, 641)),
          ((573, 631), (586, 607), (574, 586)), ((558, 563), (527, 582), (494, 570))], '#62c2b7', INK, 8)
    draw.arc((481, 581, 549, 639), 100, 270, fill='#c3f5db', width=4)
    draw.line([(483, 620), (493, 616), (503, 626)], fill='#388b88', width=4, joint='curve')
    shape((537, 638), [((552, 605), (553, 572), (552, 536)), ((549, 478), (581, 431), (634, 426)),
          ((690, 418), (729, 461), (731, 514)), ((729, 559), (750, 584), (767, 610)),
          ((760, 644), (719, 655), (689, 636)), ((664, 660), (636, 664), (610, 641)),
          ((582, 663), (550, 658), (537, 638))], '#fff6ec', INK, 9)
    shape((561, 557), [((574, 584), (607, 601), (642, 604)), ((694, 610), (722, 587), (729, 565)),
          ((734, 582), (751, 597), (762, 613)), ((746, 641), (717, 651), (689, 632)),
          ((658, 656), (633, 655), (610, 637)), ((585, 655), (556, 652), (542, 635)),
          ((550, 616), (560, 586), (561, 557))], '#edd3f0')
    star((612, 513), 29, 9, 4, INK)
    star((684, 510), 26, 8, 4, INK)
    draw.arc((630, 527, 660, 550), 12, 165, fill=INK, width=5)
    draw.ellipse((578, 537, 603, 547), fill='#f4b0cb')
    draw.ellipse((696, 535, 717, 545), fill='#f4b0cb')
    draw.ellipse((600, 561, 685, 646), fill='#a82578', outline=INK, width=6)
    draw.ellipse((602, 559, 679, 632), fill='#ef50a4', outline='#ffb5e0', width=4)
    star((640, 595), 25, 12, 5, CREAM)
    draw.ellipse((705, 563, 753, 603), fill='#fff6ec', outline=INK, width=6)


def bodywork():
    draw.line([(735, 607), (773, 536), (826, 543), (878, 623)], fill=INK, width=18, joint='curve')
    draw.line([(735, 607), (773, 536), (826, 543), (878, 623)], fill='#9de6e0', width=6, joint='curve')
    shape((126, 691), [((139, 664), (175, 632), (229, 623)), ((326, 628), (370, 647), (508, 647)),
          ((672, 646), (765, 621), (860, 613)), ((962, 621), (1020, 640), (1075, 668)),
          ((1095, 689), (1080, 748), (1048, 773)), ((1024, 780), (1002, 782), (982, 782)),
          ((980, 678), (831, 677), (828, 792)), ((698, 813), (542, 815), (412, 801)),
          ((417, 682), (254, 681), (252, 784)), ((188, 779), (117, 759), (126, 691))], '#ec568e', INK, 11)
    draw.line([(158, 684), (252, 668), (485, 683), (655, 678), (853, 649), (991, 655), (1060, 678)],
              fill='#ffb6c6', width=8, joint='curve')
    draw.line([(435, 780), (612, 789), (801, 773)], fill='#932b68', width=8, joint='curve')
    draw.rounded_rectangle((139, 704, 206, 725), 9, fill='#a02d60')
    draw.rounded_rectangle((1007, 685, 1075, 708), 9, fill='#ffe8a9', outline=INK, width=4)
    title('make.fun', (620, 731), 325, 81, CREAM, stroke=4)


def lettering():
    title('13 YEARS WAITING FOR', (600, 64), 990, 58, CREAM)
    title('GTA VI', (600, 174), 1050, 178, CREAM, 'BlackItalic', 6)


def wanted_meter(star):
    for index in range(5):
        star((456 + index * 72, 293), 31, 14, 5, GOLD, INK)


def hud_star(center, outer, inner, points, color, outline):
    center_x, center_y = center
    star((600 + (center_x - 600) * .82, 854 + center_y - 293),
         outer * .74, inner * .74, points, color, outline)


def punchline():
    gradient(860, 1199, [(46, 25, 60), (30, 16, 47), (24, 13, 40)])
    draw.rounded_rectangle((424, 825, 776, 879), 27, fill=INK, outline='#845779', width=3)
    wanted_meter(hud_star)
    draw.rounded_rectangle((450, 882, 750, 958), 38, fill=GOLD)
    title('WANTED', (600, 920), 252, 60, INK)
    title('LUMBAR SUPPORT', (600, 1038), 1094, 141, CREAM, 'CondensedBlackItalic')


def main():
    backdrop()
    convertible()
    ghost_driver()
    bodywork()
    lettering()
    punchline()
    image.save(Path(__file__).with_name('meme.png'), optimize=True)


if __name__ == '__main__':
    main()
