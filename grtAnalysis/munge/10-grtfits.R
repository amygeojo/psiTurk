
labels <- c( "Unimodal", "Bimodal", "2D", "Null" ) 
oned.labels <- c( "Unimodal", "Bimodal", "Null" ) 

fits.table <- function(df, withplot=F) {
    axis <- unique(df$axis)
    anglerange <- unique(df$anglerange)
    subj <- unique( df$subjid )
    if (length( unique ( df$resp ) ) < 2) {
        warning( paste("Subject",subj,"always gave the same response.") )
        return (data.frame())
    }
    twod <- glc( resp ~ bimod + unimod, data=df )
    bimod <- glc( resp ~ bimod, data=df )
    unimod <- glc( resp ~  unimod, data=df )
    
    # Either of these nulls is legit:
    null1loglik <- null.model.loglik( df )
    null1bic <- log( nrow( df ) ) - 2 * null1loglik
    null2loglik <- log(.5)*nrow(df)
    null2bic <- -2 * null2loglik
    nullbic <- min( null1bic, null2bic )
    
    bics <- c(laply( list( unimod, bimod, twod ), bic.model, numrows=nrow(df) ), nullbic)
    winner <- labels[which.min( bics )]
    
    # Plot if we're doing that
    if (withplot) {
        subj <- unique(df$subjid)
        title <- paste("#", subj, "Bestfit:", winner )
        plot( twod, main=title )
    }
    
    # Record the twod coeffs
    twodcoeffs <- twod$par$coeffs
    twod.angle <- xy2angle( twodcoeffs )
    twod.bimod <- twodcoeffs[1] 
    twod.noise <- twod$par$noise
    twod.bias <- twod$par$bias
    
    # Now choose the 1d winner
    unimodcoeff <- unimod$par$coeffs
    bimodcoeff <- bimod$par$coeffs
    oned.index <- which.min( c(bics[1:2], bics[4]) )
    winnercoeff <- c( unimodcoeff, bimodcoeff, 0 )[oned.index]
    onedwinner <- oned.labels[oned.index]
    
    used.index <- which.min( bics[1:2] )
    used <- labels[used.index]
    
    data.frame(BestFit=winner, BestFitOne=onedwinner, Used=used,
               unimodcoeff=unimodcoeff, bimodcoeff=bimodcoeff,
               winnercoeff=winnercoeff, twodAngle=twod.angle,
               twodBimod=twod.bimod, twodNoise=twod.noise, twodBias=twod.bias,
               axis=axis, anglerange=anglerange )
}

fits <- ddply( testtrials, ~ subjid, fits.table, .parallel=T)

