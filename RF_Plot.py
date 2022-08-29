import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Roofline():
    
    
    
    def __init__(self, mem_roofs, cmp_roofs, achieved_performance):
           
        self.mem_roofs = mem_roofs
        self.cmp_roofs = cmp_roofs
        self.achieved_performance = achieved_performance

        
        
    def rf_plot(self):
        
        font = {'size': 13}
        plt.rc('font', **font)

        colors = ['0', 'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
                  'tab:olive', 'tab:cyan']
        styles = ['o', 's', 'v', '^', 'D', ">", "<", "*", "h", "H", "+", "1", "2", "3", "4", "8", "p", "d", "|", "_", ".", ","]

        # Validations
        if not self.mem_roofs or not self.cmp_roofs:
            print('Input bounds can not be empty!')
            return

        for roof in self.mem_roofs:
            if len(roof) != 2:
                print('Wrong information input of memory bounds')
                return
            if type(roof[0]) != str:
                print('Wrong data type input of memory bounds')
                return
            if type(roof[1]) not in [float, int]:
                print('Wrong data type input of memory bounds')
                return

        for roof in self.cmp_roofs:
            if len(roof) != 2:
                print('Wrong information provided in compute bounds')
                return
            if type(roof[0]) != str:
                print('Wrong data type input of compute bounds')
                return
            if type(roof[1]) not in [float, int]:
                print('Wrong data type input of compute bounds')
                return



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
        xmin = -3
        xmax = 3
        ymin = 10**0
        ymax = 10**5

        ax.set_xlim(10 ** xmin, 10 ** xmax)
        ax.set_ylim(ymin, ymax)

        ixx = int(nx * 0.02)
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        scomp_x_elbow = []
        scomp_ix_elbow = []
        smem_x_elbow = []
        smem_ix_elbow = []


        x = np.logspace(xmin, xmax, nx)

        # Compute the coordinate of machine-balance point(s)
        for roof in self.cmp_roofs:
            for ix in range(1, nx):
                if float(self.mem_roofs[0][1] * x[ix]) > roof[1] > (self.mem_roofs[0][1] * x[ix - 1]):

                    scomp_x_elbow.append(x[ix - 1])
                    scomp_ix_elbow.append(ix - 1)
                    break

            
        for roof in self.mem_roofs:
            for ix in range(1, nx):
                if roof[1] * x[ix] > self.cmp_roofs[-1][1]  > roof[1] * x[ix - 1]:
                    smem_x_elbow.append(x[ix - 1])
                    smem_ix_elbow.append(ix - 1)
                    break


        # Plot the compute bounds
        for i in range(len(self.cmp_roofs)):
            roof = self.cmp_roofs[i][1] 
            y = np.ones(len(x)) * roof
            
            #ax.plot(x[scomp_ix_elbow[i]:], y[scomp_ix_elbow[i]:], c=colors[i], ls='-', lw='2')
            cmp_lines = ax.plot(x[scomp_ix_elbow[i]:], y[scomp_ix_elbow[i]:], c=colors[i], ls='-', lw='2')#label='Peak CP = %s GFlops/s'%(str(self.cmp_roofs[i][1])))
        

        # Plot the memory bounds if there are more than one memory bounds
        for i in range(len(self.mem_roofs)):
            roof = self.mem_roofs[i][1]
            y = x * roof
        
            mem_lines = ax.plot(x[:smem_ix_elbow[i] ], y[:smem_ix_elbow[i] ], c=colors[i], ls='-', lw='2')
        
        
        # Label the compute bounds 
        for roof in self.cmp_roofs:
            ax.text(x[-ixx], roof[1] ,
                    '%s - %f GFlops/s'%(str(roof[0]), roof[1]) ,
                    horizontalalignment='right',
                    verticalalignment='bottom')
            
        # Calculate the angle of the BW bound and label the BW bounds
        for roof in self.mem_roofs:

            ang = np.arctan(np.log10(xlim[1] / xlim[0]) / np.log10(ylim[1] / ylim[0])
                            * fig.get_size_inches()[1] / fig.get_size_inches()[0])

            if x[ixx] * roof[1] > ymin:

                ax.text(x[ixx], x[ixx] * roof[1] * (1 + 0.7 * np.sin(ang) ** 2),
                         '%s - %f GFlops/s'%(str(roof[0]), roof[1]) ,
                        horizontalalignment='left',
                        verticalalignment='bottom',
                        rotation=180 / np.pi * ang)

            else:
                ymin_ix_elbow = list()
                ymin_x_elbow = list()
                for ix in range(1, nx):
                    if roof[1] * x[ix] >= ymin > roof[1] * x[ix - 1]:
                        ymin_x_elbow.append(x[ix - 1])
                        ymin_ix_elbow.append(ix - 1)
                        break
                ax.text(x[ixx + ymin_ix_elbow[0]], x[ixx + ymin_ix_elbow[0]] * roof[1] * (1 + 0.5 * np.sin(ang)**2),
                         '%s - %f GFlops/s'%(str(roof[0]), roof[1]) ,
                        horizontalalignment='left',
                        verticalalignment='bottom',
                        rotation=180 / np.pi * ang)


         # Draw the measured performance points
        if len(self.achieved_performance) != 0:
            for i in range(len(self.achieved_performance)):
                colors = ['tab:cyan', '0']
                point_color = colors[i]
                print('Color:',point_color)
                achieved_performance = self.achieved_performance[i]
                for j in range(len(achieved_performance)):
                    
                    plt.plot( achieved_performance[j][0], achieved_performance[j][1], 'x' , color=point_color, markersize=8)
#                     if self.achieved_performance[i][0]*self.mem_roofs[0][1] < self.cmp_roofs[0][1]:
#                         plt.vlines(x=self.achieved_performance[i][0], color=colors[i],ymin=ylim[0], ymax=self.achieved_performance[i][0]*self.mem_roofs[0][1], ls='--')
#                     else:
#                         plt.vlines(x=self.achieved_performance[i][0], color=colors[i],ymin=ylim[0], ymax=self.cmp_roofs[0][1], ls='--')

        # Put the legend to the proper position of the graph
        plt.legend(loc=4, fontsize=12)

        # The string here is the text that will be displayed on your plot.
        ax.text(xlim[0] * 1.1, ylim[1] / 1.1, 'NVIDIA A100 TENSOR CORE GPU 80GB SXM', horizontalalignment='left',
                verticalalignment='top')

        plt.grid(linestyle='--')
#         plt.savefig("Roofline models_Peta4_GPU_SXM.jpg", dpi=1000, bbox_inches='tight')
        plt.show()
        
        print('-----------')
        for line in ax.lines:
            print(line.get_xdata().tolist()[-1])
        
        return ax.lines
    
    
    