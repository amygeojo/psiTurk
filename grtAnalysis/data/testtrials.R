
alldata.rawstring <- smash$datastring
tmp <- tempfile()


# Read in the original file. 
# This didn't have a column for alllabeled.
testpipe1 <- pipe( paste("awk -F, 'NF==26 {if ($16==2) { print $0 }}' >", tmp)  )
cat(alldata.rawstring, file=testpipe1)
close(testpipe1)

columns1 <- c('subjid',
              'anglerange', 
              'angleoffset', 
              'testdist',
              'lengthrange', 
              'lengthoffset',
              'swapidentity', 
              'axis', 
              'nbasis',
              'swapcorners', 
              'ntest', 
              'nlab', 
              'order',
              'respondtrain',
              'trial',
              'block',
              'respmode',
              'bimod',
              'unimod',
              'abstractlabel',
              'box',
              'length',
              'angle',
              'label',
              'resp',
              'RT'
              )

testtrials1 <- read.csv(tmp,
                       header = F,
                       col.names = columns1)
# Add in the column it's missing:
testtrials1$alllab <- 'false'

testpipe2 <- pipe( paste("awk -F, 'NF==27 {if ($17==2) { print $0 }}' >", tmp)  )
cat(alldata.rawstring, file=testpipe2)

columns2 <- c('subjid',
              'alllab', 
              'anglerange', 
              'angleoffset', 
              'testdist',
              'lengthrange', 
              'lengthoffset',
              'swapidentity', 
              'axis', 
              'nbasis',
              'swapcorners', 
              'ntest', 
              'nlab', 
              'order',
              'respondtrain',
              'trial',
              'block',
              'respmode',
              'bimod',
              'unimod',
              'abstractlabel',
              'box',
              'length',
              'angle',
              'label',
              'resp',
              'RT'
              )

testtrials2 <- read.csv(tmp,
                       header=F,
                       col.names=columns2)

testtrials <- rbind( testtrials1, testtrials2 )
