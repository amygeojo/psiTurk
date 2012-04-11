
perpage <- c(3,3)

plotcond <- function(df) {
    axis <- unique(df$axis)
    pdf( paste("graphs/", axis, ".pdf", sep=""))
    par(mfrow=perpage)
    d_ply( df, .(subjid), fits.table, withplot=T )
    dev.off()
}

d_ply(testtrials, .(axis), plotcond)
