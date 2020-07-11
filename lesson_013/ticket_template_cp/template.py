background = 'ticket_template_cp/background.png'
font_regular = 'ticket_template_cp/BlenderPro-Medium.ttf'
font_bold = 'ticket_template_cp/BlenderPro-Bold.ttf'

fields = [
    # main fields
    {'data_type': 'name', 'pos': (162, 162), 'font': font_regular, 'font_size': 20, 'capital': True, 'max_length': 26},
    {'data_type': 'from', 'pos': (162, 238), 'font': font_regular, 'font_size': 20, 'capital': True, 'max_length': 26},
    {'data_type': 'to', 'pos': (162, 313), 'font': font_regular, 'font_size': 20, 'capital': True, 'max_length': 26},
    {'data_type': 'date', 'pos': (465, 162), 'font': font_regular, 'font_size': 20, 'capital': True, 'max_length': 11},
    {'data_type': 'flight', 'pos': (634, 162), 'font': font_regular, 'font_size': 20, 'capital': True, 'max_length': 11},
    {'data_type': 'class', 'pos': (465, 238), 'font': font_regular, 'font_size': 20, 'capital': True, 'max_length': 11},
    {'data_type': 'seat', 'pos': (634, 238), 'font': font_regular, 'font_size': 20, 'capital': True, 'max_length': 11},
    {'data_type': 'gate', 'pos': (493, 312), 'font': font_bold, 'font_size': 46, 'capital': True, 'max_length': 3},
    {'data_type': 'brd_time', 'pos': (662, 312), 'font': font_bold, 'font_size': 46, 'capital': True, 'max_length': 5},
    # tear-off coupon
    {'data_type': 'name', 'pos': (859, 159), 'font': font_regular, 'font_size': 16, 'capital': False, 'max_length': 26},
    {'data_type': 'from', 'pos': (899, 199), 'font': font_regular, 'font_size': 16, 'capital': False, 'max_length': 26},
    {'data_type': 'to', 'pos': (880, 218), 'font': font_regular, 'font_size': 16, 'capital': False, 'max_length': 26},
    {'data_type': 'date', 'pos': (930, 274), 'font': font_regular, 'font_size': 16, 'capital': False, 'max_length': 11},
    {'data_type': 'seat', 'pos': (859, 274), 'font': font_regular, 'font_size': 16, 'capital': False, 'max_length': 11},
    {'data_type': 'gate', 'pos': (858, 340), 'font': font_bold, 'font_size': 25, 'capital': False, 'max_length': 3},
    {'data_type': 'brd_time', 'pos': (930, 340), 'font': font_bold, 'font_size': 25, 'capital': False, 'max_length': 5},
    {'data_type': 'barcode', 'pos': (52, 139), 'size': (51, 223)},
]
