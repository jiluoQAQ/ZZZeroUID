from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw
from gsuid_core.models import Event
from gsuid_core.utils.image.image_tools import (
    crop_center_img,
    get_avatar_with_ring,
)

from .zzzero_api import zzz_api
from .name_convert import equip_id_to_sprite
from .resource.RESOURCE_PATH import SUIT_PATH
from .fonts.zzz_fonts import zzz_font_28, zzz_font_30, zzz_font_38

TEXT_PATH = Path(__file__).parent / 'texture2d'
GREY = (216, 216, 216)
BLACK_G = (40, 40, 40)
YELLOW = (255, 200, 1)
BLUE = (1, 183, 255)

ELEMENT_TYPE = {
    203: '电属性',
    205: '以太属性',
    202: '冰属性',
    200: '物理属性',
    201: '火属性',
}

prop_id = {
    '111': 'IconHpMax',
    '121': 'IconAttack',
    '131': 'IconDef',
    '122': 'IconBreakStun',
    '201': 'IconCrit',
    '211': 'IconCritDam',
    '314': 'IconElementAbnormalPower',
    '312': 'IconElementMystery',
    '231': 'IconPenRatio',
    '232': 'IconPenValue',
    '305': 'IconSpRecover',
    '310': 'IconSpGetRatio',
    '115': 'IconSpMax',
    '315': 'IconPhysDmg',
    '316': 'IconFire',
    '317': 'IconIce',
    '318': 'IconThunder',
    '319': 'IconDungeonBuffEther',
}


def get_prop_img(_id: Union[str, int], w: int = 40, h: int = 40):
    img = Image.new('RGBA', (70, 70))
    propid = str(_id)
    propid = propid[:3]
    prop_icon = prop_id.get(propid)
    if not prop_icon:
        return img.resize((w, h))

    icon = Image.open(TEXT_PATH / 'prop' / f'{prop_icon}.png')
    x, y = icon.size
    img.paste(icon, (35 - x // 2, 35 - y // 2), icon)
    return img.resize((w, h))


def get_element_img(elemet_id: Union[int, str], w: int = 40, h: int = 40):
    elemet_id = int(elemet_id)
    if elemet_id not in ELEMENT_TYPE:
        return Image.new('RGBA', (w, h), (0, 0, 0, 0))
    img = Image.open(TEXT_PATH / f'{ELEMENT_TYPE[elemet_id]}.png')
    return img.resize((w, h)).convert('RGBA')


def get_equip_img(equip_id: str, w: int = 90, h: int = 90):
    sprite_id = equip_id_to_sprite(equip_id)
    if sprite_id:
        sprite_id = sprite_id[2:]
        img = Image.open(SUIT_PATH / f'{sprite_id}.png')
        return img.resize((w, h)).convert('RGBA')
    else:
        return Image.new('RGBA', (w, h), (0, 0, 0, 0))


def get_rarity_img(rank: str, w: int = 80, h: int = 80):
    rank = rank.upper()
    if rank in ['S', 'A', 'B', 'C']:
        img = Image.open(TEXT_PATH / f'Rarity_{rank}.png')
        return img.resize((w, h)).convert('RGBA')
    else:
        return Image.new('RGBA', (w, h), (0, 0, 0, 0))


def get_rank_img(rank: str, w: int = 40, h: int = 40):
    rank = rank.upper()
    if rank in ['S', 'A', 'B']:
        img = Image.open(TEXT_PATH / f'{rank}RANK.png')
        return img.resize((w, h)).convert('RGBA')
    else:
        return Image.new('RGBA', (w, h), (0, 0, 0, 0))


def count_characters(s: str) -> float:
    count = 0
    for char in s:
        if '\u4e00' <= char <= '\u9fff':
            count += 1
        else:
            count += 0.5
    return count


async def get_player_card_min(uid: str, ev: Event, world: str = ''):
    data = await zzz_api.get_zzz_user_info_g(uid)
    if isinstance(data, int):
        return data

    user_name = data['nickname']
    world_level = data['level']
    if world:
        region_name = world
    else:
        region_name = data['region_name']
    name_len = count_characters(user_name) * 45

    player_card = Image.open(TEXT_PATH / 'player_card_min.png')
    card_draw = ImageDraw.Draw(player_card)

    avatar = await get_avatar_with_ring(ev, 129, is_ring=False)
    player_card.paste(avatar, (105, 30), avatar)

    card_draw.text((426, 120), f'UID {uid}', GREY, zzz_font_30, 'mm')
    card_draw.text((290, 64), user_name, 'white', zzz_font_38, 'lm')

    xs, ys = 290 + name_len + 20, 45
    xt, yt = xs + 90 + 12, 45
    card_draw.rounded_rectangle((xs, ys, xs + 90, ys + 35), 10, YELLOW)
    card_draw.rounded_rectangle((xt, yt, xt + 144, yt + 35), 10, BLUE)

    card_draw.text(
        (xs + 45, ys + 17),
        f'Lv{world_level}',
        BLACK_G,
        zzz_font_28,
        'mm',
    )
    card_draw.text(
        (xt + 72, yt + 17),
        region_name,
        BLACK_G,
        zzz_font_28,
        'mm',
    )
    return player_card


def get_zzz_bg(w: int, h: int) -> Image.Image:
    bg = Image.open(TEXT_PATH / 'bg.jpg').convert('RGBA')
    return crop_center_img(bg, w, h)


def add_footer(img: Image.Image) -> Image.Image:
    footer = Image.open(TEXT_PATH / 'footer.png')
    w = img.size[0]
    if w != footer.size[0]:
        footer = footer.resize(
            (w, int(footer.size[1] * w / footer.size[0])),
        )
    x, y = (
        int((img.size[0] - footer.size[0]) / 2),
        img.size[1] - footer.size[1] - 10,
    )
    img.paste(footer, (x, y), footer)
    return img
