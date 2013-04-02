#!/usr/bin/R -q --no-save < rtest2.R
# from "R in Action"
png("rtest2.png")
x <- pretty(c(-3,3), 30)
y <- dnorm(x)
plot(x, y,
	type = "l",
	xlab = "Normal Deviate",
	ylab = "Density",
	yaxs = "i"
)
