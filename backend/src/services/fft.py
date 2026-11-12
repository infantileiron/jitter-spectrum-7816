import numpy as np
from src.services.peaks import top_peaks
def fft_spectrum(t,residual,meta,window,min_frequency,max_frequency):
 if not meta["regular"]:return {"available":False,"reason":"时间间隔不规则或存在缺采样，FFT不可用；未填0、未重采样，LS仍可计算","frequencies":[],"power":[],"peaks":[],"units":"ms²·分钟","nyquist":None}
 n=len(t);dt=meta["median_interval_minutes"];fs=1/dt
 if max_frequency>fs/2*(1+1e-9):raise ValueError("规则采样搜索上限不能超过Nyquist频率")
 w=np.hanning(n) if window=="hann" else np.ones(n) if window=="boxcar" else None
 if w is None:raise ValueError("FFT窗只能为hann或boxcar")
 energy=float(np.sum(w*w));spectrum=np.fft.rfft(residual*w);power=np.abs(spectrum)**2/(fs*energy)
 if n%2==0:power[1:-1]*=2
 else:power[1:]*=2
 frequencies=np.fft.rfftfreq(n,d=dt);spacing=fs/n;selected=(frequencies>=min_frequency)&(frequencies<=max_frequency)
 f=frequencies[selected];p=power[selected]
 return {"available":True,"reason":"等间隔单侧FFT功率谱密度","frequencies":f.tolist(),"power":p.tolist(),"peaks":top_peaks(f,p,5,1/meta["span_minutes"]),"units":"ms²·分钟","nyquist":fs/2,"frequency_spacing":spacing,"window":window,"window_energy":energy,"full_psd_integral_ms2":float(np.sum(power)*spacing),"window_normalized_mean_square_ms2":float(np.sum((residual*w)**2)/energy)}
