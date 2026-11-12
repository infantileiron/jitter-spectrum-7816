import numpy as np
from src.services.peaks import top_peaks
def lomb_scargle(t,residual,frequencies):
 relative=t-t[0];baseline=float(np.sum((residual-np.mean(residual))**2))
 if baseline<=0:raise ValueError("常量残差无法归一化LS周期谱")
 powers=[]
 for f in frequencies:
  omega=2*np.pi*f;design=np.column_stack([np.ones(len(t)),np.sin(omega*relative),np.cos(omega*relative)])
  coef=np.linalg.lstsq(design,residual,rcond=None)[0];error=residual-design@coef
  powers.append(float(np.clip((baseline-float(error@error))/baseline,0,1)))
 return {"available":True,"frequencies":[float(f) for f in frequencies],"power":powers,"peaks":top_peaks(frequencies,powers,5,1/float(t[-1]-t[0])),"units":"解释方差比例（无量纲）","normalization":"(SSE0-SSEf)/SSE0；SSE0为仅浮动均值模型，SSEf为常数+sin+cos模型","search_strategy":"显式等频率网格；不规则采样无统一Nyquist，不声称网格上限是理论Nyquist"}
