import pprint
import sys

import PIL
import requests
import argparse
from PIL import Image, ImageFont, ImageDraw

if str.upper(sys.argv[1]) == "DEBUG": # modo debug para no andar llamando a la api
    names = ["MASTRITO", "JUANMA78"]
    ratings = ["23923 TR", "23751 TR"]
    ranks = [Image.open("res/x.png"), Image.open("res/d+.png")]
    images = [Image.open("res/unknown.png"), Image.open("res/unknown.png")]
else:
    ##### API CALLS
    username_left, username_right = sys.argv[1:]
    if len(sys.argv) != 3:
        raise ValueError(f"Usage: {sys.argv[0]} username1 username2")

    names = []
    ratings = []
    ranks = []
    images = []
    for username in sys.argv[1:]:

        response = requests.get(f"https://ch.tetr.io/api/users/{username}")
        player = response.json()["data"]["user"]
        names.append(str.upper(player["username"]))
        ratings.append(f'{player["league"]["rating"]:.0f} TR')
        rank = player["league"]["rank"]
        ranks.append(Image.open(f"res/{rank}.png"))

        response = requests.get(f" https://tetr.io/user-content/avatars/{player['_id']}.jpg")
        with open(f"auto_thumbnail/temp.jpg", "wb") as f:
            f.write(response.content)
        try:
            images.append(Image.open("auto_thumbnail/temp.jpg"))
        except PIL.UnidentifiedImageError:
            images.append(Image.open("res/unknown.png"))

##### PIL
background = Image.open("res/background.jpg")
vs = Image.open("res/vs.png")
background.thumbnail((1280, 720))

bg_w, bg_h = background.size
left_w, left_h = images[0].size
right_w, right_h = images[1].size
vs_w, vs_h = vs.size

# textdraw setup
draw = ImageDraw.Draw(background)
color = (255, 255, 255)
font = ImageFont.truetype("auto_thumbnail/HunDIN1451.ttf", 72)

###### toquetear este pedacito hasta que quede lindo ######
left_offset = int(1.5 * bg_w // 6)
right_offset = int(4.5 * bg_w // 6)
imag_height = 2 * bg_h // 8
name_height = 5.5 * bg_h // 8
rating_height = 6.5 * bg_h // 8

coord_rank_left = 100, 100
coord_rank_right = 900, 100
###########################################################

coord_imag_left = left_offset - left_w // 2, imag_height
coord_name_left = left_offset, name_height
coord_rating_left = left_offset, rating_height
coord_imag_right = right_offset - right_w // 2, imag_height
coord_name_right = right_offset, name_height
coord_rating_right = right_offset, rating_height

coord_vs = bg_w // 2 - vs_w // 2, bg_h // 2 - vs_h // 2

# magic
background.paste(images[0], coord_imag_left)
background.paste(images[1], coord_imag_right)
background.paste(ranks[0], coord_rank_left, ranks[0])
background.paste(ranks[1], coord_rank_right, ranks[1])
background.paste(vs, coord_vs, vs)

draw.text(coord_name_left, names[0], color, font=font, anchor="ma")
draw.text(coord_name_right, names[1], color, font=font, anchor="ma")
draw.text(coord_rating_left, ratings[0], color, font=font, anchor="ma")
draw.text(coord_rating_right, ratings[1], color, font=font, anchor="ma")

background.save("auto_thumbnail/result.png")
