# PHAS0077
Roofline model plot


For the use of my .py files, I will show two examples to understand the simple principle.

For beth .py files, you need to input:

1. the memory-bound ceilings,
2. the compute-bound ceilings,
3. the data points you want to draw up.

First example according to RF_plot.py,
"
mem_roofs_PCIe = [('Peak GPU Memory Bandwidth', 1.935*1000)]
cmp_roofs_SXM = [('Peak FP64', 4*9.7*1000)]
Achieved_performance_Icelake = [(0.537, 2.2), (0.771, 3.16), (0.951, 3.9), (1.49, 6.09), (1.85, 7.58), (3.06, 12.6), (3.87, 15.9), (6.10, 25.0), (7.89, 32.4)]
Achieved_points = [Achieved_performance_GPU]
rf1 = Roofline(mem_roofs_SXM, cmp_roofs_SXM, Achieved_points)
rf1.rf_plot()
"

Second Example according to RF_multiceilings.py:
mem_roofs_SXM = [('Peak RAM BW', 4*2.039*1000), ('Peak RAM BW', 2*4*2.039*1000)]
cmp_roofs_SXM = [('Peak FP64 - one node', 4*9.7*1000), ('Peak FP64 - two nodes', 2*4*9.7*1000),]
Achieved_performance_GPU = [(3.5, 15.7), (7.0, 31.5), (10.5, 47.2), (14.0, 63.0), (18.7, 84.4)]
Achieved_performance = [Achieved_performance_GPU]
rf = Roofline(mem_roofs_SXM, cmp_roofs_SXM, Achieved_performance)
rf.rf_plot()
