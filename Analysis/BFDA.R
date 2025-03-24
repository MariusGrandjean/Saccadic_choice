#### Bayesian Factor Design Analysis : BFDA ####

library(devtools)
library(BFDA)

# Simulate many hypothetical studies, both under H1 and under H0, using the function "BFDA.sim"

sim.H1 <- BFDA.sim(expected.ES=0.572, type="t.paired",
                   prior=list("Cauchy",list(prior.location=0, prior.scale=sqrt(2)/2)),
                   n.min=30, n.max=70, alternative="greater", boundary=Inf, B=1000, design = 'sequential',
                   verbose=TRUE, cores=4, stepsize = 5)

sim.H0 <- BFDA.sim(expected.ES=0, type="t.paired",
                   prior=list("Cauchy",list(prior.location=0, prior.scale=sqrt(2)/2)),
                   n.min=30, n.max=55, alternative="greater", boundary=c(1/6,6), B=1000, design = 'sequential',
                   verbose=TRUE, cores=4, stepsize = 5)

# Analyze the simulated studies, using the function "BFDA.analyze"

BFDA.analyze(sim.H1, design="sequential", n.min=30, n.max=70, boundary=c(1/6,6))
BFDA.analyze(sim.H0, design="sequential", n.min=30, n.max=55, boundary=c(1/6,6))

# Plot the simulated studies (plot, SSD, evDens)

plot(sim.H1, n.min=30, n.max=55, boundary=c(1/6, 6))
plot(sim.H0, n.min=30, n.max=55, boundary=c(1/6, 6), forH1 = FALSE)

# Tune your design in a way that you achieve the desired goals with adequate probability (SSD)

SSD(sim.H1, power=.57, boundary=c(1/6, 6))
SSD(sim.H0)