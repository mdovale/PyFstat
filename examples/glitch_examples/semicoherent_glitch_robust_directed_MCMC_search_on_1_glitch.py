import numpy as np
import matplotlib.pyplot as plt
import pyfstat
from make_simulated_data import tstart, duration, tref, F0, F1, F2, Alpha, Delta, outdir

plt.style.use('paper')

label = 'semicoherent_glitch_robust_directed_MCMC_search_on_1_glitch'

Nstar = 1000
F0_width = np.sqrt(Nstar)*np.sqrt(12)/(np.pi*duration)
F1_width = np.sqrt(Nstar)*np.sqrt(180)/(np.pi*duration**2)

theta_prior = {
    'F0': {'type': 'unif',
           'lower': F0-F0_width/2.,
           'upper': F0+F0_width/2.},
    'F1': {'type': 'unif',
           'lower': F1-F1_width/2.,
           'upper': F1+F1_width/2.},
    'F2': F2,
    'delta_F0': {'type': 'unif',
                 'lower': 0,
                 'upper': 1e-5},
    'delta_F1': 0,
    'tglitch': {'type': 'unif',
                'lower': tstart+0.1*duration,
                'upper': tstart+0.9*duration},
    'Alpha': Alpha,
    'Delta': Delta,
    }

ntemps = 3
log10beta_min = -0.5
nwalkers = 100
nsteps = [500, 500]

mcmc = pyfstat.MCMCGlitchSearch(
    label=label, sftfilepattern='data/*1_glitch*sft', theta_prior=theta_prior,
    tref=tref, minStartTime=tstart, maxStartTime=tstart+duration,
    nsteps=nsteps, nwalkers=nwalkers, ntemps=ntemps,
    log10beta_min=log10beta_min, nglitch=1)

mcmc.transform_dictionary['F0'] = dict(
    subtractor=F0, symbol='$f-f^\mathrm{s}$')
mcmc.transform_dictionary['F1'] = dict(
    subtractor=F1, symbol='$\dot{f}-\dot{f}^\mathrm{s}$')

mcmc.run()
mcmc.plot_corner()
mcmc.print_summary()