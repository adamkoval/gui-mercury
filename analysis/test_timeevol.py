import matplotlib.pyplot as plt

import func as fn

res_str = '21'
completed_path = '../completed_13-02-20'
sim_results = fn.MM_sim_results(completed_path, res_str)
mu1, mu2 = 0.0131, 0.00387

fn.plot_timeevol(completed_path, res_str, sim_results, mu1, mu2)
plt.show()
