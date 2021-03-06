background = 'ticket_template_cp/background.png'
font_regular = 'ticket_template_cp/BlenderPro-Medium.ttf'
font_bold = 'ticket_template_cp/BlenderPro-Bold.ttf'

fields = [
    # main fields
    {'data_type': 'name', 'pos': (162, 162), 'font': font_regular, 'font_size': 20, 'capital': True, 'width': 260},
    {'data_type': 'origin', 'pos': (162, 238), 'font': font_regular, 'font_size': 20, 'capital': True, 'width': 260},
    {'data_type': 'dest', 'pos': (162, 313), 'font': font_regular, 'font_size': 20, 'capital': True, 'width': 260},
    {'data_type': 'date', 'pos': (465, 162), 'font': font_regular, 'font_size': 20, 'capital': True, 'width': 128},
    {'data_type': 'flight', 'pos': (634, 162), 'font': font_regular, 'font_size': 20, 'capital': True, 'width': 128},
    {'data_type': 'fare_code', 'pos': (465, 238), 'font': font_regular, 'font_size': 20, 'capital': True, 'width': 128},
    {'data_type': 'seat', 'pos': (634, 238), 'font': font_regular, 'font_size': 20, 'capital': True, 'width': 128},
    {'data_type': 'gate', 'pos': (493, 312), 'font': font_bold, 'font_size': 46, 'capital': True, 'width': 0},
    {'data_type': 'brd_time', 'pos': (662, 312), 'font': font_bold, 'font_size': 46, 'capital': True, 'width': 0},
    # tear-off coupon
    {'data_type': 'name', 'pos': (859, 159), 'font': font_regular, 'font_size': 16, 'capital': False, 'width': 200},
    {'data_type': 'origin', 'pos': (899, 199), 'font': font_regular, 'font_size': 16, 'capital': False, 'width': 158},
    {'data_type': 'dest', 'pos': (880, 218), 'font': font_regular, 'font_size': 16, 'capital': False, 'width': 177},
    {'data_type': 'date', 'pos': (930, 274), 'font': font_regular, 'font_size': 16, 'capital': False, 'width': 127},
    {'data_type': 'seat', 'pos': (859, 274), 'font': font_regular, 'font_size': 16, 'capital': False, 'width': 60},
    {'data_type': 'gate', 'pos': (858, 340), 'font': font_bold, 'font_size': 25, 'capital': False, 'width': 62},
    {'data_type': 'brd_time', 'pos': (930, 340), 'font': font_bold, 'font_size': 25, 'capital': False, 'width': 104},
    # Barcode rotation: don't rotate - 0, 90 deg - 2, 180 deg - 3, 270 deg - 4
    {'data_type': 'barcode', 'pos': (52, 139), 'size': (51, 223), 'rotate': 2},
]
