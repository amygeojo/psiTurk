
import numpy as np
import numpy.random as nprand

def gen_rects():
    leftfatx = [0, .2]
    leftskinnyx = [0, .1]
    rightfatx = [.8, 1]
    rightskinnyx = [.9, 1]
    
    ys = zip( np.arange(0, 1, .2), np.arange(.2,1.2,.2) )
    
    leftrects = zip( [leftfatx, leftskinnyx, leftskinnyx, leftskinnyx, leftfatx], ys )
    rightrects = zip( [rightfatx, rightskinnyx, rightskinnyx, rightskinnyx, rightfatx], ys )
    
    return leftrects + rightrects

def gen_coords_in_rect(rect, n):
    return zip(nprand.uniform( rect[0][0], rect[0][1], n ),
               nprand.uniform( rect[1][0], rect[1][1], n ))

def build_abstract_task(stacked=False, 
                        ngrid=0,
                        nlab=0,
                        ntest=0
                        #order='i',  # not supported in this version.
                       ):
    if ngrid:
        rect = [[0,1], [0,1]]
        coords = gen_coords_in_rect( rect, ngrid )
        return np.column_stack([coords, [np.nan]*ngrid, [np.nan]*ngrid])
    
    rects = gen_rects()
    defaultreps = 10  # number of times the layout is repeated.
    
    if stacked:
        layout = [5, 3, 4, 3, 2,
                  2, 3, 4, 3, 5]
    else:
        layout = [2, 3, 4, 3, 2,
                  2, 3, 4, 3, 2]
    
    if ntest > 0:
        reps = sum( sum(layout) * (np.arange(1, defaultreps)) < ntest ) + 1
    else:
        reps = defaultreps
    
    stims = []
    for i in range(10):
        n = layout[i] * reps
        coords = gen_coords_in_rect( rects[i], n )
        labels = [np.nan for _ in xrange(n)]
        if i == 0:
            assert (nlab/2) <= len(labels), "Too many labels for the labeled box!"
            labels[:(nlab/2)] = [ 0 for _ in xrange( nlab/2 ) ]
        elif i == 9:
            labels[:(nlab/2)] = [ 1 for _ in xrange( nlab/2 ) ]
        
        for j in xrange(len(coords)):
            stims.append( list(coords[j]) + [labels[j], i] )
    
    # Make sure last 10 are unlabeled and evenly chosen from the two sides.
    nprand.shuffle(stims)
    unlab1 = [ stim for stim in stims if np.isnan( stim[2] ) and stim[3]<5 ]
    unlab2 = [ stim for stim in stims if np.isnan( stim[2] ) and stim[3]>=5 ]
    labeled = [ stim for stim in stims if not np.isnan( stim[2] ) ]
    if not ntest:
        lastten = unlab1[:5] + unlab2[:5]
        rest = unlab1[5:] + unlab2[5:] + labeled
        nprand.shuffle( rest )
        nprand.shuffle( lastten )
        
        return rest + lastten
    else:
        nprand.shuffle( unlab1 )
        nprand.shuffle( unlab2 )
        assert ntest % 2 == 0
        ret = unlab1[:ntest/2] + unlab2[:ntest/2]
        nprand.shuffle( ret )
        return ret

def generate_stims( task, axisBal='size', anglerotBal=0, cornerBal=0, identity=0 ):
    assert (axisBal in ['size', 'angle']), "Invalid axisbal: %s" % axisbal
    axisBal = axisBal == 'angle'
    print axisBal
    sizerange  = 230
    sizeoffset = 50
    angleoffset = anglerotBal
    anglerange = 60
    bounds = [[ sizeoffset, sizerange+sizeoffset ], [angleoffset, angleoffset+anglerange]]
    
    def transform_size(size_val):
        thesebounds = bounds[0]
        return (size_val*(thesebounds[1] - thesebounds[0])) + thesebounds[0]
    # y is angle
    def transform_angle(angle_val):
        thesebounds = bounds[1]
        return (angle_val*(thesebounds[1] - thesebounds[0])) + thesebounds[0]
    def transformstim( stim ):
        ret = np.array(stim)
        stimflip = stim
        if cornerBal:
            stimflip[1] = 1 - stim[1]
        if axisBal:
            ret[0] = transform_size( stimflip[1] )
            ret[1] = transform_angle( stimflip[0] )
        else:
            ret[0] = transform_size( stimflip[0] )
            ret[1] = transform_angle( stimflip[1] )
        if not identity:
            ret[2] = 1-stim[2]
        return ret
    
    return [ transformstim(item) for item in task ]

def build_task(stacked=False, ngrid=False, nlab=0, ntest=0, axisBal=0,
               anglerotBal=0, cornerBal=0, identity=0):
    assert nlab % 2 == 0, "nlab must be even!"
    
    abstract_task = np.array(build_abstract_task(stacked, ngrid, nlab, ntest))
    stims = np.array(generate_stims(abstract_task, axisBal, anglerotBal,
                                    cornerBal, identity))
    stims = stims[:,:-1] # Pinch off the rectangle identifier here.
    
    return np.hstack([abstract_task, stims])

class tvexp:
    pass

