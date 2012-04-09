
import pylab
import numpy as np

import task as T

def plot_task(task):
    abstract = np.array( [x[1:4] for x in task] )
    actual = np.array( [x[5:7] + [x[3]] for x in task] )
    labels = list(set( map(str, [x[3] for x in task] ) ) )
    labels.sort()
    pylab.hold( True )
    pylab.plot( actual[:,0], actual[:,1], "k" )
    cols = "rgw"
    for i in range(len(labels)):
        coords = np.array([st[:2] for st in actual if str(st[2]) == labels[i]])
        pylab.plot( coords[:,0], coords[:,1], "o"+cols[i] )

if __name__ == "__main__":
    taskparams = T.condition_builder(0, 1)
    taskobject = T.tvTask( ** taskparams )
    
    pylab.subplot( 121 )
    train = taskobject.train
    print "First 3 trials:"
    print train[:3]
    plot_task(train)
    
    # Test phase
    print "Test phase"
    pylab.subplot( 122 )
    test = taskobject.test
    print "First 3 trials:"
    print test[:3]
    plot_task(test)
    
    pylab.show()



