from pycbc.waveform import get_td_waveform
import numpy as np

hp, hc = get_td_waveform(approximant='SEOBNRv4_opt', 
                         mass1=10, mass2=10,
                         delta_t=1.0/4096, f_lower=30)

# 直接保存到当前目录（软链接至Windows)
np.save('waveform_hp.npy', hp)
np.save('waveform_hc.npy', hc)
print('波形已保存到：', np.__file__)