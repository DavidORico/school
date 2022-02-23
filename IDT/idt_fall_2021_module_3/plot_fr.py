import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

plt.figure()
plt.title('5.8GHz video downlink in meters')
ax = plt.gca()

ellipse = Ellipse(xy=(0.0, 0.0), width=10, height=0.35943654, 
                        edgecolor='r', fc='None', lw=2)
ax.add_patch(ellipse)
plt.xlim([-6, 6])
plt.ylim([-0.5, 0.5])
plt.savefig('fr_5_8GHz.png')
