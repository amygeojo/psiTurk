
import numpy as np
import numpy.random as nprand

VERSION = 1.0
NCONDS = 1
NCOUNTERS = 2

def bounded(x, bounds=[0,1]):
    return x >= bounds[0] and x <= bounds[1]

def random_coords_in_rect(rect, n):
    return zip(nprand.uniform( rect[0][0], rect[0][1], n ),
               nprand.uniform( rect[1][0], rect[1][1], n ))

def gen_rects():
    leftfatx = [0, .2]
    leftskinnyx = [0, .2]; rightfatx = [.8, 1]
    rightskinnyx = [.8, 1]
    
    ys = zip( np.arange(0, 1, .2), np.arange(.2,1.2,.2) )
    
    leftrects = zip( [leftfatx, leftskinnyx, leftskinnyx, leftskinnyx, leftfatx], ys )
    rightrects = zip( [rightfatx, rightskinnyx, rightskinnyx, rightskinnyx, rightfatx], ys )
    
    return leftrects + rightrects

class tvTask:
    def __init__(self,
                 order = "interspersed",
                 nbasis = 280,
                 nlab = 0,
                 ntest = 50,
                 testform = "bimodal",
                 respondtrain = False,
                 axis = None,
                 swapcorners = None, 
                 swapidentity = None,
                 angleoffset = None,
                 lengthoffset = 50,
                 anglerange = 60,
                 lengthrange = 120):
        
        # These params need to not take default values:
        assert axis != None
        assert angleoffset != None
        assert swapcorners != None
        assert swapidentity != None
        
        self.order = order
        self.respondtrain = respondtrain
        self.nlab = nlab
        self.nbasis = nbasis
        self.ntest = ntest
        self.testform = testform
        self.axis = axis
        self.swapcorners = swapcorners
        self.swapidentity = swapidentity
        self.angleoffset = angleoffset
        self.lengthoffset = lengthoffset
        self.anglerange = anglerange
        self.lengthrange = lengthrange
        
        self.checkinputs()
        
        # Inferred parameters
        self.bounds = {'length': [self.lengthoffset, self.lengthrange+self.lengthoffset], 
                       'angle': [self.angleoffset, self.anglerange+self.angleoffset]}
        self.stacked = self.nlab > (self.nbasis / 7)
        
        trainAbstract, testAbstract = self.build_abstract_task()
        self.train = [ self.transform_stim(stim) for stim in trainAbstract ]
        self.test = [ self.transform_stim(stim) for stim in testAbstract ]
    
    # Check various properties of the inputs
    def checkinputs(self):
        assert self.nbasis % 28 == 0
        assert self.order in ["interspersed"]  # I'm sure I'll try out more in the future
        assert self.testform in ["bimodal", "grid", "mixed"] 
        assert self.axis in ["length", "angle"]
        assert ((self.angleoffset+self.anglerange)<=90 and self.angleoffset<=90) or ((self.angleoffset+self.anglerange)>=90 and self.angleoffset>=90)
        assert self.angleoffset <= (180 - self.anglerange)
        assert self.anglerange <= 90
        assert self.swapcorners in [False, True]
        assert self.swapidentity in [False, True]
    
    # Methods to find 'actual' stims given abstract stims.
    def transform_length(self, length_val):
        assert bounded(length_val, [0,1])
        lengthbounds = self.bounds['length']
        return (length_val*(lengthbounds[1] - lengthbounds[0])) + lengthbounds[0]
    
    # y is angle
    def transform_angle(self, angle_val):
        assert bounded(angle_val, [0,1])
        anglebounds = self.bounds['angle']
        return (angle_val*(anglebounds[1] - anglebounds[0])) + anglebounds[0]
    
    def transform_stim(self, stim):
        ret = stim
        stimflip = stim
        if self.swapcorners:
            stim[2] = 1 - stim[2]
        if self.axis == "length":
            length_abstract = stimflip[1]
            angle_abstract = stimflip[2]
        elif self.axis == "angle":
            length_abstract = stimflip[2]
            angle_abstract = stimflip[1]
        ret.append(self.transform_length( length_abstract ))
        ret.append(self.transform_angle( angle_abstract ))
        ret = list(ret)
        
        label = stim[3]
        if self.swapidentity:
            label = 1 - label
        if np.isnan( label ):
            ret.append( "broken")
        else:
            ret.append( {0: "ch1", 1: "ch2"}[label] )
        return ret
    
    def build_abstract_task(self):
        """
        Returns stims for both a test phase and a training phase.
        """
        rects = gen_rects()
        
        regularlayout = [2, 3, 4, 3, 2,
                         2, 3, 4, 3, 2]
        stackedlayout = [5, 3, 4, 3, 2,
                         2, 3, 4, 3, 5]
        
        if self.stacked:
            layout = [5, 3, 4, 3, 2,
                      2, 3, 4, 3, 5]
        else:
            layout = [2, 3, 4, 3, 2,
                      2, 3, 4, 3, 2]
        
        reps = self.nbasis / sum(regularlayout)  # number of times the layout is repeated.
        
        testreps = sum( sum(layout) * (np.arange(1, reps)) < self.ntest ) + 1
        trainreps = reps
        
        teststims = []
        trainstims = []
        # DISCUSS: should we make all the rectangles squares?
        # There are 10 
        for i in range(len(layout)):
            ntrain = layout[i] * trainreps
            ntest = layout[i] * testreps
            traincoords = random_coords_in_rect( rects[i], ntrain )
            testcoords = random_coords_in_rect( rects[i], ntest )
            
            # Most TVs are unlabeled, so we start with those and then add the others
            trainlabels = [np.nan for _ in xrange(ntrain)]
            testlabels = [np.nan for _ in xrange(ntest)]
            # Add in labels to training if we're in a labeled area
            if i == 0:
                assert (self.nlab/2) <= len(trainlabels), "Too many labels for the labeled box!"
                trainlabels[:(self.nlab/2)] = [ 0 for _ in xrange( self.nlab/2 ) ]
            elif i == 9:
                trainlabels[:(self.nlab/2)] = [ 1 for _ in xrange( self.nlab/2 ) ]
            
            for j in xrange(len(traincoords)):
                trainstims.append( list(traincoords[j]) + [trainlabels[j], i] )
            for j in xrange(len(testcoords)):
                teststims.append( list(testcoords[j]) + [testlabels[j], i] )
        
        nprand.shuffle( trainstims )
        nprand.shuffle( teststims )
        
        # Removed the last-ten thing.
        # Make sure last 10 training items are unlabeled items drawn evenly
        # from both groups
        #unlab1 = [ stim for stim in trainstims if np.isnan( stim[2] ) and stim[3]<5 ]
        #unlab2 = [ stim for stim in trainstims if np.isnan( stim[2] ) and stim[3]>=5 ]
        #labeled = [ stim for stim in trainstims if not np.isnan( stim[2] ) ]
        #lastten = unlab1[:5] + unlab2[:5]
        #rest = unlab1[5:] + unlab2[5:] + labeled
        #nprand.shuffle( rest )
        #nprand.shuffle( lastten )
        #trainstims = rest + lastten
        
        unlab1 = [ stim for stim in teststims if np.isnan( stim[2] ) and stim[3]<5 ]
        unlab2 = [ stim for stim in teststims if np.isnan( stim[2] ) and stim[3]>=5 ]
        nprand.shuffle( unlab1 )
        nprand.shuffle( unlab2 )
        assert self.ntest % 2 == 0, "Number of test items must be even"
        teststims = unlab1[:self.ntest/2] + unlab2[:self.ntest/2]
        nprand.shuffle( teststims )
        if self.respondtrain == "no":
            trainstims = [ ["obs"] + row for row in trainstims ]
            teststims = [ ["choice"] + row for row in teststims ]
        return trainstims, teststims

def condition_builder(condnum, counternum):
    maxlength = 120
    maxangle = 90
    #anglerange = [70, 90][condnum // 2]
    #lengthrange = [70, 100][condnum % 2]
    anglerange = 70
    lengthrange = 120
    angleoffset = nprand.randint(0, maxangle-anglerange+1) + maxangle*nprand.randint(2)
    lengthoffset = 30
    swapcorners = [False, True][nprand.randint(2)]
    swapidentity = [False, True][nprand.randint(2)]
    axis = ["length", "angle"][counternum]
    return dict(
         order = "interspersed",
         nbasis = 112,
         nlab = 0,
         ntest = 50,
         testform = "bimodal",
         respondtrain = "no",
         axis = axis,
         swapcorners = swapcorners, 
         swapidentity = swapidentity,
         angleoffset = angleoffset,
         lengthoffset = lengthoffset,
         anglerange = anglerange,
         lengthrange = lengthrange)

