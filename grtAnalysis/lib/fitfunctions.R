
# {{{1 Statistics
bic.model <- function(fitobj, numrows) AIC( fitobj, k=log(numrows) )
# }}}1

# {{{1 Translation functions
radiens2degrees <- function( rad ) 180 * rad / pi

xy2angle <- function(xyvec) {
        # For a unit vector of x/y coordinates, finds their angle 
        # TODO: catch the case where xyvec is not a unit vector.
        if (xyvec[2] > 0) { 
                    theta.rad <- acos( xyvec[1] )  }
    else { 
                theta.rad <- 2*pi - acos( xyvec[1] ) }
        radiens2degrees( theta.rad )
}
# }}}1

# {{{1 GRT model functions
null.model.loglik <- function( df ) {
    # code the responses
    same  <- 0
    n <- 0
    for (resp in df$Resp){
        n <- n + 1
        if ( resp==df$Resp[1] ) {
            same  <- same + 1
        }
    }
    bias <- same / n
    (likelihood <- (log(bias)*same + log(1-bias) * (n-same)))
}
# }}}1

# vim: foldmethod=marker
