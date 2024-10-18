WHITE = (0,0,0)
Dark =(73, 36, 62)
Light =(219, 175, 160)
 

def colonizer(col1,col2):
    Dark =col1   
    Light =(219, 175, 160)
    Light =col2
 

    num_squares = 12
    cl = []
    for i in range(num_squares + 2): 
        ratio = i / (num_squares + 1)
        r = int((1 - ratio) * Dark[0] + ratio * Light[0])
        g = int((1 - ratio) * Dark[1] + ratio * Light[1])
        b = int((1 - ratio) * Dark[2] + ratio * Light[2])
        cl.append((r, g, b))
    print(cl)
    
def diffuser(col1,col2):
    Dark =col1   
    Light =(219, 175, 160)
    Light =col2
 
    num_squares = 30
    cl = []
    for i in range(num_squares + 2): 
        ratio = i / (num_squares + 1)
        r = int((1 - ratio) * Dark[0] + ratio * Light[0])
        g = int((1 - ratio) * Dark[1] + ratio * Light[1])
        b = int((1 - ratio) * Dark[2] + ratio * Light[2])
        cl.append((r, g, b))
    return cl    
    