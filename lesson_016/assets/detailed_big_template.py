import cv2
import cmapy

CMAPS = {'ясно': cmapy.cmap('Wistia_r'),
         'дождь': cv2.COLORMAP_BONE,
         'дождь/гроза': cmapy.cmap('bone_r'),
         'облачно': cmapy.cmap('PuBu_r'),
         'осадки': cv2.COLORMAP_OCEAN,  # снег с дождём
         'снег': cv2.COLORMAP_WINTER,
         'метель': cv2.COLORMAP_OCEAN,
         'дождь/град': cv2.COLORMAP_OCEAN,
}

ICONS = {'ясно': '\uF00D',
         'дождь': '\uF018',
         'дождь/гроза': '\uF01D',
         'облачно': '\uF013',
         'осадки': '\uF06C',
         'снег': '\uF01B',
         'метель': '\uF082',
         'дождь/град': '\uF017',
         'press': '\uF079',
         'humidity': '\uF078',
         'wind': '\uF050',
}


BACKGROUND_IM = 'assets/big_bg.png'
FONT_REGULAR = 'assets/RobotoSlab-Regular.ttf'
FONT_BOLD = 'assets/RobotoSlab-Medium.ttf'
FONT_ICONS = 'assets/weathericons-regular-webfont.ttf'

WHITE = (255, 255, 255)

fields = [
    # data
    {'text': '{city}', 'pos': (46, 31), 'font': FONT_REGULAR, 'font_size': 30, 'color': WHITE},
    {'text': '{date:%d %b %Y}', 'pos': (46, 74), 'font': FONT_REGULAR, 'font_size': 23, 'color': WHITE},
    {'text': '{temp_day}{temp_units}  {temp_night}{temp_units}',
        'pos': (46, 112), 'font': FONT_BOLD, 'font_size': 70, 'color': WHITE},
    {'text': '{descr}', 'pos': (46, 200), 'font': FONT_REGULAR, 'font_size': 32, 'color': WHITE},
    {'text': '{press} {press_units}', 'pos': (73, 260), 'font': FONT_REGULAR, 'font_size': 24, 'color': WHITE},
    {'text': '{humidity} {humidity_units}', 'pos': (262, 260), 'font': FONT_REGULAR, 'font_size': 24, 'color': WHITE},
    {'text': '{wind_speed} {wind_speed_units}',
        'pos': (450, 260), 'font': FONT_REGULAR, 'font_size': 24, 'color': WHITE},

    # icons
    {'text': ICONS['press'], 'pos': (46, 260), 'font': FONT_ICONS, 'font_size': 24, 'color': WHITE},
    {'text': ICONS['humidity'], 'pos': (240, 260), 'font': FONT_ICONS, 'font_size': 24, 'color': WHITE},
    {'text': ICONS['wind'], 'pos': (412, 260), 'font': FONT_ICONS, 'font_size': 24, 'color': WHITE},
    # TODO Придумать способ выводить большую иконку погоды
    # {'text': ICONS['дождь'], 'pos': (334, 25), 'font': FONT_ICONS, 'font_size': 160, 'color': WHITE},
]
