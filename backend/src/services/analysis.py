import hashlib,json
import numpy as np
from src.services.preprocessing import prepare
from src.services.fft import fft_spectrum
from src.services.lomb import lomb_scargle
from src.services.fitting import fit_sinusoids
def analyze(points,study):
 t,y,residual,meta=prepare(points,study.detrend)
 if study.min_frequency<1/meta["span_minutes"]*(1-1e-9):raise ValueError("最大搜索周期不能超过观测跨度")
 fft=fft_spectrum(t,residual,meta,study.fft_window,study.min_frequency,study.max_frequency)
 grid=np.linspace(study.min_frequency,study.max_frequency,study.frequency_points);ls=lomb_scargle(t,residual,grid)
 frequencies=[p["frequency_per_minute"] for p in ls["peaks"][:2]]
 fit=fit_sinusoids(t,y,frequencies,study.detrend)
 observations=[{"time_minutes":float(x),"jitter_ms":float(v),"residual_ms":float(r)} for x,v,r in zip(t,y,residual)]
 return {"meta":meta,"fft":fft,"ls":ls,"fit":fit,"observations":observations,"frequency_min":study.min_frequency,"frequency_max":study.max_frequency,"frequency_points":study.frequency_points,"checksum":hashlib.sha256(json.dumps(observations,sort_keys=True).encode()).hexdigest(),"assumptions":["时间单位分钟，频率为每分钟周期数，omega=2*pi*f；幅相以窗口首观测时刻t0为原点。","重复时间拒绝；数据先按时间排序。不规则或缺点不填0不静默插值，FFT不可用但浮动均值LS仍计算。","FFT为单侧PSD，除以采样率和窗能量；正频率非Nyquist项加倍，单位ms²·分钟。LS为浮动均值模型的解释方差比例，二者归一和单位不同，不能强作数值等值比较。","规则FFT的Nyquist=1/(2*dt)，频率分辨率=1/(N*dt)。不规则LS没有统一Nyquist，按显式用户频率范围与等频率网格搜索；最大搜索周期不得超过实际观测跨度。","峰值不证明网络故障原因；相近峰受有限跨度/窗泄漏/采样模式影响。幅相按两个LS候选频率联合拟合，不等于自动诊断或真实链路控制。"]}
