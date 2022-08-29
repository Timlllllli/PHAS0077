import matplotlib.pyplot as plt

def plot_timeagainstcores(time_2021, time_2022, no_hardwares):
    
    y1 = time_2021
    y2 = time_2022
    x = no_hardwares
    

    # The basic figure set-up
    font = {'size': 10}
    plt.rc('font', **font)
    fig = plt.figure(1, figsize=(10.67, 6.6))
    plt.clf()
    ax = fig.gca()
    

#     ax1 = plt.subplot(1, 2, 1)
#     ax.plot(x, y2, color='r', markerfacecolor='blue', marker='o')
#     ax.plot(x, y2, color='b', markerfacecolor='0', marker='o')
    # plot the two lines in on axes and label them
    ax.plot(x, y1, color='r', label= '2021')
    ax.plot(x, y2, color='c', label= '2022')
    
    # set the log-log scale
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.xlabel('Nodes - Cores per node')
    plt.ylabel('Total time cost / s')
    plt.legend(loc=1, fontsize=16)
#     ax.plot(x, y2, color='b', markerfacecolor='black', marker='o')
#     ax2 = plt.subplot(1, 2, 2)
#     ax2.plot(x, y2, color='r', markerfacecolor='blue', marker='o')
#     plt.xlabel('No. nodes')
#     plt.title("2022")
    
#     ax1.set_xscale('log')
#     ax1.set_yscale('log')
    
#     ax2.set_xscale('log')
#     ax2.set_yscale('log')
    
#     ax1.axes.xaxis.set_visible(False)
#     ax2.axes.xaxis.set_visible(False)
    #text = ['1n-16cpn', '1n-32cpn', '1n-64cpn', '2n-32cpn', '2n-64cpn', '4n-32cpn', '4n-64cpn', '8n-32cpn', '8n-64cpn']

    # To set the xticks shown on the plot
    core = [8, 16, 32, 32*2, 32*4, 32*8]
    node = [1, 1, 1, 2, 4, 8]
    text = [0]*6
    for i in range(len(core)):
        text[i] = '%d n - %d cpn'%((node[i],(core[i])))
#     text = ['8','16','32','64','128','256']
#     text = [16, 32, 64, 32*2, 64*2, 32*4, 64*4, 32*8, 64*8]
#     for i in range(len(text)):
#         text[i] = str(text[i])
    
    # To set the real xticks 
    ax.set_xticks([8, 16, 32, 32*2, 32*4, 32*8])
    ax.set_xticklabels(text,rotation=45)
    
#     ax2.set_xticks([8, 16, 32, 32*2, 32*4, 32*8])
#     ax2.set_xticklabels(text,rotation=45)
#     for a, b in zip(x, y2):  
#         ax.text(a, b, (b), ha='left', va='bottom', fontsize=16)
#     for a, b in zip(x, y2):  
#         ax2.text(a, b, (b), ha='left', va='bottom', fontsize=12)
    
    
#     plt.xlabel('Time Consuming/s')
#     plt.subplots_adjust(wspace =0.4)
#     plt.title("Time consuming vs No. cores - Skylake cores - 2022 ")
    #plt.savefig("Sky_times_two_years.jpg",dpi=100, bbox_inches='tight')
    

    
    plt.show()

    