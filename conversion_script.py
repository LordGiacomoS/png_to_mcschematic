from PIL import Image
import mcschematic as mcs

def hkey_get(hkey, input_, input_type=0, out_type=2):
    # type 0 == rgb
    # type 1 == name
    # type 2 == layer
    layer = hkey[input_type].index(input_)
    if out_type != 2:
        return hkey[out_type][layer]
    else:
        return layer

def heightmap_to_valmap(mapfile, height_key):
    with Image.open(mapfile) as img:
        raw_data = tuple(img.getdata())
        width, height = img.size
    pixels = [hkey_get(height_key, curr_item[:3]) for curr_item in raw_data]
    return pixels, width, height
            
concrete_rgbs = ((207, 213, 214), (125, 125, 115), (55, 58, 62), (8, 10, 15), (96, 60, 32), (142, 33, 33), (224, 97, 1), (241, 175, 21), (94, 169, 24), (73, 91, 36), (21, 119, 136), (36, 137, 199), (45, 47, 143), (100, 32, 156), (169, 48, 159), (213, 101, 143))
concrete_names = ("white", "light_gray", "gray", "black", "brown", "red", "orange", "yellow", "lime", "green", "cyan", "light_blue", "blue", "purple", "magenta", "pink")


def make_hkey(concrete_names=None): #names go lowest to highest
    if concrete_names == None:
        return (concrete_rgbs, concrete_names)
    else:
        color_dct = {
            "white": (207, 213, 214),
            "light_gray": (125, 125, 115),
            "gray": (55, 58, 62),
            "black": (8, 10, 15),
            "brown": (96, 60, 32),
            "red": (142, 33, 33),
            "orange": (224, 97, 1),
            "yellow": (241, 175, 21),
            "lime": (94, 169, 24),
            "green": (73, 91, 36),
            "cyan": (21, 119, 136),
            "light_blue": (36, 137, 199),
            "blue": (45, 47, 143),
            "purple": (100, 32, 156),
            "magenta": (169, 48, 159),
            "pink": (213, 101, 143)
        }
        rgbs = []
        names = []
        for num in range(len(concrete_names)):
            cname = concrete_names[num]
            rgbs = rgbs + [color_dct[cname]]
            names = names + [cname]
        return (tuple(rgbs), tuple(names))

def set_block(structure, material, coords):
    structure.setBlock(coords, material)
    
    
def generate_layer(structure, height_arr, layer_num, width, height, align_axis, layer_material):
    # mc N-S: Z; E-W: X
    for zpos in range(height):
        for xpos in range(width):    
            if height_arr[(zpos*width)+xpos] >= layer_num:
                coords = zpos*-1, layer_num, xpos*1 #[TBA]: filter coords based on align axis
                set_block(structure, layer_material, coords)

def generate_heightmap_structure(heightmap_png, hkey=None, use_concrete=False, base_material="stone", align_axis="z", outfile="terrain"):
    #[TBA]: align_axis names axis to align the image y coordinate to
    if hkey == None:
        hkey = make_hkey()
    
    base_material = "minecraft:"+base_material
    height_arr, img_w, img_h = heightmap_to_valmap(heightmap_png, hkey)
    struct = mcs.MCSchematic()
    
    for num in range(len(hkey[0])):
        if use_concrete:
            generate_layer(struct, height_arr, num, img_w, img_h, align_axis, hkey[1][num]+"_concrete")#BlockData(hkey[1][num]+"_concrete"))
        else:
            generate_layer(struct, height_arr, num, img_w, img_h, align_axis, base_material)
    struct.save("", outfile, mcs.Version.JE_1_20_1)
