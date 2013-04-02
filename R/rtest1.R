#!/usr/bin/R -q --no-save << rtest1.R
# from "R in Action"

png("rtest1.png")
curve(cos(x), from=-10, to=10)
curve(exp(x) - 1, add=TRUE, col="red")
curve(sin(x / 2) / 2, add=TRUE, col="blue")

#plot()
#dev.off()
