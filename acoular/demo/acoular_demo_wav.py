from pathlib import Path
from scipy.io import wavfile
import sys
path_root = Path(__file__).parents[0]
sys.path.append(str(path_root)+"\\acoular")

from pathlib import Path

from traits.api import (
    ListInt,
)

from acoular import (
    BeamformerBase,
    L_p,
    MicGeom,
    Mixer,
    PointSource,
    PowerSpectra,
    RectGrid,
    SteeringVector,
    WNoiseGenerator,
    WriteH5,
    config,
    TimeSamples,
    WriteWAV,
    WavSamples,
)


from acoular import __file__ as bpath

sfreq = 51200
duration = 1
nsamples = duration * sfreq
micgeofile = Path(bpath).parent / 'xml' / 'array_64.xml'
# h5savefile = 'three_sources.h5'
wavefile = 'three_sources.wav'

mg = MicGeom(from_file=micgeofile)

print('Processing data, this may take some time ...')

import matplotlib.pyplot as plt

ts_wavdata = WavSamples(name=str(path_root)+'\\three_sources.wav')
ps = PowerSpectra(time_data=ts_wavdata, block_size=128, window='Hanning')
rg = RectGrid(x_min=-0.2, x_max=0.2, y_min=-0.2, y_max=0.2, z=0.3, increment=0.01)
st = SteeringVector(grid=rg, mics=mg)

bb = BeamformerBase(freq_data=ps, steer=st)
pm = bb.synthetic(8000, 3)
Lm = L_p(pm)

if config.have_matplotlib:
    from pylab import axis, colorbar, figure, imshow, plot, show

    # show map
    imshow(Lm.T, origin='lower', vmin=Lm.max() - 10, extent=rg.extend(), interpolation='bicubic')
    colorbar()

# plot microphone geometry
plt.figure()
plt.plot(mg.mpos[0], mg.mpos[1], 'o')
plt.axis('equal')

plt.show()

# else:
#     print('Matplotlib not found! Please install matplotlib if you want to plot the results.')
#     print('For consolation we do an ASCII map plot of the results here.')
#     grayscale = '@%#*+=-:. '[::-1]
#     ind = ((Lm.T - Lm.max() + 9).clip(0, 9)).astype(int)[::-1]
#     print(78 * '-')
#     print('|\n'.join([' '.join(['|'] + [grayscale[i] for i in row[2:-1]]) for row in ind]) + '|')
#     print(7 * '-', ''.join([f'{grayscale[i]}={int(Lm.max())-9+i}dB ' for i in range(1, 10)]), 6 * '-')
