

def ipv4_to_int(str):
    blocks = list(map(int, str.split(".")))
    val = (blocks[0] << 24) | (blocks[1] << 16) | (blocks[2] << 8) | blocks[3]
    return val

def ipv6_to_int(str):  
    if "::" in str:
        parts = str.split("::")
        left = [p for p in parts[0].split(":") if p]
        right = [p for p in parts[1].split(":") if p]
        missing = 8 - (len(left) + len(right))
        blocks = left + ["0"] * missing + right
    else:
        blocks = str.split(":")
    
    val = 0
    for block in blocks:
        val = (val << 16) | int(block, 16)
    return val