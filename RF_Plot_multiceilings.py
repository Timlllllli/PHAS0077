import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Roofline():
    
       
    
    def __init__(self, mem_roofs, cmp_roofs, achieved_performance, flag='Others'):
           
        self.mem_roofs = mem_roofs
        self.cmp_roofs = cmp_roofs
        self.achieved_performance = achieved_performance
        self.flag = flag

        
        
    def rf_plot(self):
        
        font = {'size': 13}
        plt.rc('font', **font)

        colors = ['0','tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
                  'tab:olive', 'tab:cyan','tab:blue']
        styles = ['o', 's', 'v', '^', 'D', ">", "<", "*", "h", "H", "+", "1", "2", "3", "4", "8", "p", "d", "|", "_", ".", ","]

        


        # Basic graph settings
        fig = plt.figure(1, figsize=(10.67, 6.6))
        plt.clf()
        ax = fig.gca()
        ax.set_xscale('log')
        ax.set_yscale('log')

        ax.set_xlabel('Arithmetic Intensity [FLOPs/Byte]')
        ax.set_ylabel('Performance [GFLOP/sec]')

#         Limits of axes and strides
        nx = 10000
        xmin = -2
        xmax = 2
        ymin = 10**-1
        ymax = 10**4

        ax.set_xlim(10 ** xmin, 10 ** xmax)
        ax.set_ylim(ymin, ymax)

        ixx = int(nx * 0.05)
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        scomp_x_elbow = []
        scomp_ix_elbow = []
        smem_x_elbow = []
        smem_ix_elbow = []

        

        if self.flag == 'SpMV':

            kernel_flags = [self.flag]

        elif self.flag == 'Others':
            kernel_flags = ['LBMHD', 'Stencil', 'FFT(512^3)', 'FFT(128^3)']
        elif self.flag == 'All':
            kernel_flags = ['SpMV', 'LBMHD', 'Stencil','FFT(128^3)', 'FFT(512^3)']
            
        elif self.flag == None:
            kernel_flags = None

        x = np.logspace(xmin, xmax, nx)

        # Compute machine-balance points for each system
#         for roof in self.cmp_roofs:
        for i in range(len(self.cmp_roofs)):
            roof = self.cmp_roofs[i]
            print(roof)
            for ix in range(1, nx):
                if float(self.mem_roofs[i][1] * x[ix]) > roof[1] > (self.mem_roofs[i][1] * x[ix - 1]):

                    scomp_x_elbow.append(x[ix - 1])
                    scomp_ix_elbow.append(ix - 1)
                    break


            
#         for roof in self.mem_roofs:
        for i in range(len(self.mem_roofs)):
            roof = self.mem_roofs[i]
            for ix in range(1, nx):
                if roof[1] * x[ix] > self.cmp_roofs[i][1]  > roof[1] * x[ix - 1]:
                    smem_x_elbow.append(x[ix - 1])
                    smem_ix_elbow.append(ix - 1)
                    break
#             print('balance_point_mem_x:',smem_x_elbow[-1])

        # Plot the compute bounds
        for i in range(len(self.cmp_roofs)):
            roof = self.cmp_roofs[i][1] 
            y = np.ones(len(x)) * roof
#             colors2 = colors[:2]
            cmp_lines = ax.plot(x[scomp_ix_elbow[i]:], y[scomp_ix_elbow[i]:], c=colors[i], ls='-', lw='2')
        

            
        # Plot the memory bounds
        for i in range(len(self.mem_roofs)):
            roof = self.mem_roofs[i][1]
            y = x * roof
#             colors2 = colors[:2]
            mem_lines = ax.plot(x[:smem_ix_elbow[i] ], y[:smem_ix_elbow[i] ], c=colors[i], ls='-', lw='2')
            #, label='BW = %s GB/s'% str(self.mem_roofs[i][1])
            
            

        # Label the compute bounds and memory bounds
        for roof in self.cmp_roofs:
            ax.text(x[-ixx], roof[1]*1.1 ,
                    '%s - %d GFlops/s'%(roof[0],roof[1]) ,
                    horizontalalignment='right',
                    verticalalignment='bottom')
            
        for roof in self.mem_roofs:
            for i in range(len(self.mem_roofs)):

                ang = np.arctan(np.log10(xlim[1] / xlim[0]) / np.log10(ylim[1] / ylim[0])
                                * fig.get_size_inches()[1] / fig.get_size_inches()[0])

    #             if x[ixx] * roof[1] > ymin:
                if x[ixx] * self.mem_roofs[i][1] > ymin:

                    ax.text(x[ixx+i*1100], x[ixx+i*1100] * self.mem_roofs[i][1] * (1 + 0.5 * np.sin(ang) ** 2),
                            'BW - %d GBytes/s'%(np.round(self.mem_roofs[i][1])) ,
                            horizontalalignment='left',
                            verticalalignment='bottom',
                            rotation=180 / np.pi * ang, fontsize=10)

                else:
                    ymin_ix_elbow = list()
                    ymin_x_elbow = list()
                    for ix in range(1, nx):
                        if roof[1] * x[ix] >= ymin > roof[1] * x[ix - 1]:
                            ymin_x_elbow.append(x[ix - 1])
                            ymin_ix_elbow.append(ix - 1)
                            break
                    ax.text(x[ixx + ymin_ix_elbow[0]], x[ixx + ymin_ix_elbow[0]] * roof[1] * (1 + 0.1 * np.sin(ang)),
                             'BW - %d GBytes/s'%(np.round(self.mem_roofs[i][1])) ,
                            horizontalalignment='left',
                            verticalalignment='bottom',
                            rotation=180 / np.pi * ang)


#         # Draw the measured performance points
        if len(self.achieved_performance) != 0:
            for i in range(len(self.achieved_performance)):
#                 point_color = colors[i]
#  
                achieved_performance = self.achieved_performance[i]
                for j in range(len(achieved_performance)):
#                     color = colors[j]
#                     colors2 = ['tab:orange', 'tab:orange','tab:green', 'tab:green','tab:red','tab:red']
#                     colors2 = ['0','0','0','0','tab:orange']
                    plt.plot( achieved_performance[j][0], achieved_performance[j][1], 'x' , color=colors[j], markersize=8)
        
                    nub = [0,1,2]
                    z = nub[j]
                    print('z',z)
                    if achieved_performance[j][0]*self.mem_roofs[z][1] < self.cmp_roofs[z][1]:
                        ceiling = achieved_performance[j][0]*self.mem_roofs[z][1]
                        print(ceiling)
                        point = achieved_performance[j][1]
                            #mupltiplier = [16,32,64]

#                         cores = [16,32,16,32,16,32]
#                         nodes = [2,2,4,4,8,8]
                        cores = [32,32,32]
                        nodes = [2,4,8]
#                         cores = [1,2,3,4,8]
#                         nodes = [1,1,1,1,2]
#                         n = ['node','node','node','node','nodes']
#                         gpu = ['GPU','GPUs','GPUs','GPUs','GPUs']
                        plt.vlines(x=achieved_performance[j][0], color=colors[j], ymin=point, ymax=ceiling, ls='--', 
                                       label= '%f %s - %d cores/node - %d nodes'%(((ceiling-point)/ceiling*100),'%',cores[j], nodes[j]))
                    else:
                        ceiling = self.cmp_roofs[z][1]
                        point = achieved_performance[j][1]
                        plt.vlines(x=achieved_performance[j][0], color=colors[j], ymin=point, ymax=ceiling, ls='--', 
                                       label= '%f %s - %d cores/node - %d nodes'%(((ceiling-point)/ceiling*100),'%',cores[j], nodes[j]))
        
        # Draw the dotted line of machine-balance point
        for i in range(len(smem_x_elbow)):

            plt.vlines(x=smem_x_elbow[i], ymin=ylim[0], ymax=self.cmp_roofs[i][1], color=colors[i], ls='--',
                       label='(%f,%f)'%(smem_x_elbow[i],self.cmp_roofs[i][1]))



        # Put the legend to the proper position of the graph
        plt.legend(loc='lower right',  fontsize=12)

        # The string here is the text that will be displayed on your plot.
        
        ax.text(xlim[0] * 1.1, ylim[1] / 1.1, 'Peta4 ', horizontalalignment='left',
                verticalalignment='top')
#         ax.text(xlim[0] * 1.1, ylim[1] / 1.1, 'Wilkes3 ', horizontalalignment='left',
#                 verticalalignment='top')

        plt.grid(linestyle='--')
        #plt.savefig("Roofline models_Skylake_multinodes.jpg",dpi=1000, bbox_inches='tight')
        plt.show()
        
        print('-----------')
        for line in ax.lines:
            print(line.get_xdata().tolist()[-1])
        
        return ax.lines
    
    
    