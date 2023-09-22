from conversion_script import generate_heightmap_structure as gen_schem

small_hkey = make_hkey(("white", "light_gray", "gray", "black", "brown"))
gen_schem("examples/small_heightmap.png", small_hkey, use_concrete=True, outfile="small_heightmap")
large_hkey = make_hkey(("red", "orange", "yellow", "lime", "green", "light_blue", "magenta", "pink"))    
gen_schem("examples/large_heightmap.png", large_hkey, use_concrete=True, outfile="large_heightmap")