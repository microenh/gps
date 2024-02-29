from datetime import time

DIVISIONS = (
    ( 1, ord('A')),
    (10, ord('0')),
    (24, ord('a')),
    (10, ord('0')), 
    (24, ord('A'))
)
    
def grid_square(lon, lat):
    """
    lon: decimal longitude -180 .. 180 (West is negative)
    lat: decimal latitude -90 .. 90 (South is negative)
    returns 10 character string 'AA99aa99AA' (truncate for less precision)
    """
    lat += 90
    lon += 180
    lon_div = 20.0
    lat_div = 10.0

    results = []
    for div, base in DIVISIONS:
        lon_div /= div
        lat_div /= div
        results.append(chr((lo := int(lon / lon_div)) + base)
                     + chr((la := int(lat / lat_div)) + base))
        lon -= lo * lon_div
        lat -= la * lat_div
        
    return ''.join(results)

def lon_lat(grid_square):
    """
    grid_square: AA99aa99AA or any 2,4,6,8 character subset
    """
    lon = -180.0
    lat = -90.0
    lon_mult = 20.00
    lat_mult = 10.0
    for m,p in DIVISIONS:
        if len(grid_square)< 2:
            break        
        lon_mult /= m
        lat_mult /= m
        lon += lon_mult * (ord(grid_square[0]) - p)
        lat += lat_mult * (ord(grid_square[1]) - p)
        grid_square = grid_square[2:]
    return lon, lat

def try_float(f):
    try:
        return float(f)
    except ValueError:
        return 0

def timefromgps(utctime):
    utctime = try_float(utctime)
    h = int(utctime//10_000)
    utctime -= h * 10_000
    m = int(utctime//100)
    utctime -= m * 100
    s = int(utctime)
    utctime -= s
    msec = int(utctime * 1_000)
    return time(h,m,s,msec)

def todec(x,h):
    x = try_float(x)
    d = int(x//100)
    x -= d * 100
    r = d + x / 60.0
    return r if h in 'NE' else -r

    
    
