import matplotlib.pyplot as plt

kur = [7.962212461251134, 4.60629649252467, 26.028273983847164, 3.939605241101096, 1.5343252073010714, 2.432164607242037]
ill = [3.458421392856332, 2.293519353496849, 1.7361889643523247, 6.278359263392159, 3.2127358151933567, 0.6307410060496121]
kur_micron = [aa*0.055 for aa in kur]
ill_micron = [bb*0.055 for bb in ill]


plt.hist(kur_micron, 10, histtype = 'step', label='KUR dataset',lw=1,
                              ec="red", alpha=0.3)
plt.hist(ill_micron, 10, histtype = 'step', label='ILL dataset',lw=1,
                              ec="black", alpha=0.3)
plt.xlabel('Dist. root point and fit point [$\mu$m]')
plt.ylabel('Counts')
plt.xlim(0,1.8)
plt.ylim(0,3)
plt.legend()
plt.show()