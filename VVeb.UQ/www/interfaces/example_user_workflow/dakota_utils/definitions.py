# Definitions of DAKOTA settings and variables used by other modules

from copy import deepcopy

# Settings Information
# What settings DAKOTA expects to read from the netcdf file
allowed_settings = ['sample_type','samples','seed']

# Variable Type Information
# Required and optional data for different variables
# Currently only supporting simple aleatory uncertain variable distributions
# and only the required variables 

allowed_variable_types = {}

# Normal uncertain variables
vartype = 'normal'
allowed_variable_types[vartype] = {}
allowed_variable_types[vartype]['name']     = 'normal_uncertain'
allowed_variable_types[vartype]['required'] = [ 'means', 'std_deviations' ]
allowed_variable_types[vartype]['optional'] = [ 'lower_bounds', 'upper_bounds', 'initial_point' ]

# Log Normal uncertain variables
allowed_variable_types['lognormal'] = deepcopy(allowed_variable_types['normal'])
allowed_variable_types['lognormal']['name']     = 'lognormal_uncertain'

# Uniform uncertain variables
vartype = 'uniform'
allowed_variable_types[vartype] = {}
allowed_variable_types[vartype]['name']     = 'uniform_uncertain'
allowed_variable_types[vartype]['required'] = [ 'lower_bounds', 'upper_bounds' ]
allowed_variable_types[vartype]['optional'] = [ 'initial_point' ]

# Log uniform uncertain variables
allowed_variable_types['loguniform']         = deepcopy(allowed_variable_types['uniform'])
allowed_variable_types['loguniform']['name'] = 'loguniform_uncertain'

# Triangular uncertain variables
vartype = 'triangular'
allowed_variable_types[vartype] = {}
allowed_variable_types[vartype]['name']     = 'triangular_uncertain'
allowed_variable_types[vartype]['required'] = [ 'modes', 'lower_bounds', 'upper_bounds' ]
allowed_variable_types[vartype]['optional'] = [ 'initial_point' ]

# Exponential uncertain variables
vartype = 'exponential'
allowed_variable_types[vartype] = {}
allowed_variable_types[vartype]['name']     = 'exponential_uncertain'
allowed_variable_types[vartype]['required'] = [ 'betas' ]
allowed_variable_types[vartype]['optional'] = [ 'initial_point' ]

# Beta uncertain variables
vartype = 'beta'
allowed_variable_types[vartype] = {}
allowed_variable_types[vartype]['name']     = 'beta_uncertain'
allowed_variable_types[vartype]['required'] = [ 'alphas', 'betas', 'lower_bounds', 'upper_bounds' ]
allowed_variable_types[vartype]['optional'] = [ 'initial_point' ]

# Gamma uncertain variables
vartype = 'gamma'
allowed_variable_types[vartype] = {}
allowed_variable_types[vartype]['name']     = 'gamma_uncertain'
allowed_variable_types[vartype]['required'] = [ 'alphas', 'betas' ]
allowed_variable_types[vartype]['optional'] = [ 'initial_point' ]

# Gumbel uncertain variables
allowed_variable_types['gumbel']         = deepcopy(allowed_variable_types['gamma'])
allowed_variable_types['gumbel']['name'] = 'gumbel_uncertain'

# Frechet uncertain variables
allowed_variable_types['frechet']         = deepcopy(allowed_variable_types['gamma'])
allowed_variable_types['frechet']['name'] = 'frechet_uncertain'

# Weibull uncertain variables
allowed_variable_types['weibull']         = deepcopy(allowed_variable_types['gamma'])
allowed_variable_types['weibull']['name'] = 'weibull_uncertain'

# Poisson uncertain variables
vartype = 'poisson'
allowed_variable_types[vartype] = {}
allowed_variable_types[vartype]['name']     = 'poisson_uncertain'
allowed_variable_types[vartype]['required'] = [ 'lambdas' ]
allowed_variable_types[vartype]['optional'] = [ 'initial_point' ]

# Binomial uncertain variables
vartype = 'binomial'
allowed_variable_types[vartype] = {}
allowed_variable_types[vartype]['name']     = 'binomial_uncertain'
allowed_variable_types[vartype]['required'] = [ 'probability_per_trial', 'num_trials' ]
allowed_variable_types[vartype]['optional'] = [ 'initial_point' ]

# Negative binomial uncertain variables
allowed_variable_types['negative_binomial'] = deepcopy(allowed_variable_types['binomial'])
allowed_variable_types['negative_binomial']['name'] = 'negative_binomial_uncertain'

# Geometric uncertain variables
vartype = 'geometric'
allowed_variable_types[vartype] = {}
allowed_variable_types[vartype]['name']     = 'geometric_uncertain'
allowed_variable_types[vartype]['required'] = [ 'probability_per_trial']
allowed_variable_types[vartype]['optional'] = [ 'initial_point' ]

# Hypergeometric uncertain variables
vartype = 'hypergeometric'
allowed_variable_types[vartype] = {}
allowed_variable_types[vartype]['name']     = 'hypergeometric_uncertain'
allowed_variable_types[vartype]['required'] = [ 'total_population', 'selected_population', 'num_drawn' ]
allowed_variable_types[vartype]['optional'] = [ 'initial_point' ]

# Continuous design variables used for parameter scans
vartype = 'scan'
allowed_variable_types[vartype] = {}
allowed_variable_types[vartype]['name']     = 'continuous_design'
allowed_variable_types[vartype]['required'] = [ 'lower_bounds', 'upper_bounds', 'partitions' ]

# Continuous design variables used for correlated parameter scans
allowed_variable_types['scan_correlated']   = deepcopy(allowed_variable_types['scan'])
