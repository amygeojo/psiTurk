
alldata.rawstring <- smash$datastring

istesttrial <- function( trialstring ) {
    fields <- str_split( trialstring, sep=",")
    return( length(fields) == 26 && fields[16]=="2" )
}

tmp <- tempfile()
testpipe <- pipe( paste("awk -F, 'NF==26 {if ($16==2) { print $0 }}' >", tmp)  )
cat(alldata.rawstring, file=testpipe)
close(testpipe)

testtrials <- read.csv(tmp,
                       header=F,
                       col.names=c('subjid',
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
                       )

