
import pylab
import numpy as np

import task as T

def plot_task(task):
    task = np.array( task )
    labels = list(set( map(str, task[:,2]) ))
    labels.sort()
    pylab.hold( True )
    pylab.plot( task[:,0], task[:,1], "k" )
    cols = "rgw"
    for i in range(len(labels)):
        coords = np.array([st[:2] for st in task if str(st[2]) == labels[i]])
        pylab.plot( coords[:,0], coords[:,1], "o"+cols[i] )

if __name__ == "__main__":
    trainargs = {"stacked": False, 
                 "ngrid": 0, 
                 "nlab": 40,
                 "ntest": 0, 
                 "axisBal": "size",
                 "anglerotBal": 101, 
                 "cornerBal": 1,
                 "identity": 1 }
    pylab.subplot( 131 )
    task = T.build_task( ** trainargs )
    print "First 3 trials:"
    print task[:3]
    plot_task(task[:,4:])
    
    # Test phase
    print "Test phase"
    pylab.subplot( 132 )
    testargs = trainargs
    testargs["nlab"] = 0
    testargs["ntest"] = 50
    task = T.build_task( **testargs )
    print "First 3 trials:"
    print task[:3]
    plot_task(task[:,4:])
    
    # Preview examples
    print "Preview examples"
    pylab.subplot( 133 )
    demoargs = trainargs
    demoargs["nlab"] = 0
    demoargs["ngrid"] = 80
    task = T.build_task( **demoargs )
    print "First 3 trials:"
    print task[:3]
    plot_task(task[:,4:])
    pylab.show()



