
ggplot( fits, aes( x=axis, fill=BestFit )) + geom_bar(width=.7) + facet_grid( ~ labcond )
ggsave( "graphs/strategies_fillplot.pdf")

# Condition breakdown for each fit type
#ggplot( fits, aes( x=BestFit, fill=axis )) + geom_bar(width=.7, position="dodge") + theme_bw()
ggplot( fits, aes( x=axis, fill=BestFit )) + geom_bar(width=.7, position="dodge") + facet_grid( ~ labcond )
ggsave( "graphs/fitbycond.pdf" )

