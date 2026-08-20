# mySprite = sprites.create(img("""
#         . . . . . . . . . . . . . . . .
#         . . . 3 3 3 . . . . . . . . . .
#         . . . . . . 3 . . . . . . . . .
#         . . . . . . 3 . . . . 1 1 . . .
#         . . . . . 3 . . . . 1 1 . . . .
#         . 2 . . 3 3 . . . . 1 . . . . .
#         . 2 . . 3 3 3 3 3 1 . . . . . .
#         . 2 . . . . . . . . 1 . . . . .
#         . 2 . . . . . . . . 1 1 . . . .
#         . 2 . . . . . . . . . 1 . . . .
#         . . 2 . . . . . . . . 1 . . . .
#         . . 2 2 . . . . . . . . 1 . . .
#         . . . . 2 2 . . . . . . . . . .
#         . . . . . . 2 2 2 . . . . . . .
#         . . . . . . . . . 2 2 . . . . .
#         . . . . . . . . . . . . . . . .
#         """),
#     SpriteKind.player)
#e_pet_bounce01.pbm bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\x01\x80\x00\x00\x00\xe0\x03\xc0\x00\x00\x01\xb0\x06\xc0\x00\x00\x01\x9f\xfc\xc0\x00\x00\x01\x9f\xf8\xc0\x00\x00\x01\xb0\x0c\xc0\x00\x00\x01\xa4G\x80\x00\x00\x01\xa2#\x80\x00\x00\x00\xc1\x11\x00\x00\x00\x01\x80\x01\x80\x00\x00\x01\x830\xc0\x00\x00\x01\x830\xc0\x00\x00\x01\x80\x00\xc0\x00\x00\x01\x80\x00\xc0\x00\x00\x01\x80\x80\xc0\x00\x00\x00\xc1@\xc0\x00\x00\x00\xc0\x01\x80\x00\x00\x00`\x03\xc0\x00\x00\x00\xff\xff\xe0\x00\x00\x01\xff\xfe`\x00\x00\x01\x86\x18 \x00\x00\x01\x8c\x8c0\x00\x00\x01\xcd\xdcp\x00\x00\x01\xee\x9c\xf0\x00\x00\x00\xff\xff\xe0\x00\x00\x00\x7fs\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
def img(img_string):
    #mapping = 1 #use a lookup for each color that can define what each symbol gets translated to
    new_img = []
    lit_up_mask = []
    unlit_mask = []
    bg_color_layer=''
    fg_color_layer=''
    zero_one_string = ''
    lines = [x.strip() for x in img_string.split('\n')]
    for line in lines:
        
        if line == '':
            pass
        else:
            new_img_line = []
            lit_up_line = []
            unlit_line = []
            for char in line:
                if char in ['.']: # . => transparent
                    new_img_line.append('.')
                    lit_up_line.append('.')
                    unlit_line.append('.')
                    bg_color_layer += '1'
                    #1 in bg is transparent
                    fg_color_layer += '0'
                    #0's in fg image are transparent
                elif char in ['f']: #f => off
                    new_img_line.append('f')
                    unlit_line.append('0')
                    lit_up_line.append('.')
                    bg_color_layer += '0'
                    #1 in bg is transparent
                    fg_color_layer += '0'
                    #0's in fg image are transparent
                elif char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd','e']:
                    new_img_line.append('9')
                    lit_up_line.append('1')       #9 => lit up, default all others for now
                    unlit_line.append('.')
                    bg_color_layer += '1'
                    #1 in bg is transparent
                    fg_color_layer += '1'
            new_img.append(new_img_line)
            lit_up_mask.append(lit_up_line)
            unlit_mask.append(unlit_line)
    for row in new_img:
        print (' '.join(row))
        for char in row:
            zero_one_string+=char
    print(zero_one_string)#Draw bg color layer down first.  1's in the pbm show up as black on gimp.  Those ultimately are transparent in the final sprite
    
    #b=bytearray(int(zero_one_string, 2).to_bytes((len(zero_one_string) + 7) // 8, 'big'))
    #print(b)
    print()
    bg_color_image = bytearray(int(bg_color_layer, 2).to_bytes((len(bg_color_layer) + 7) // 8, 'big'))
    print(bg_color_layer)
    print(bg_color_image)
    print()
    fg_color_image = bytearray(int(fg_color_layer, 2).to_bytes((len(fg_color_layer) + 7) // 8, 'big'))
    print(fg_color_layer)
    #f is black, 9 is light blue
a = img("""
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . f f . . . . . . f . .
        . . . . f 9 9 f . . . . f f . .
        . . . f 9 f f 9 f . . f 9 9 f .
        . . f 9 f f f f 9 f . 9 9 9 f .
        . . 9 f f f f f f 9 f 9 f 9 9 f
        . f 9 f f f f f f f 9 f f f f 9
        f 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
        """)
