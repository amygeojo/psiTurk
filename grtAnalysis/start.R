library(ProjectTemplate)
load.project()


plot( glc(resp ~ bimod + unimod, data=subset( testtrials, subjid==4 )))
