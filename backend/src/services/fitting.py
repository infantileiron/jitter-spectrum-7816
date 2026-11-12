import numpy as np
def fit_sinusoids(t,y,frequencies,detrend):
 relative=t-t[0];columns=[np.ones(len(t))]
 if detrend=="linear":columns.append(relative)
 for f in frequencies:columns.extend([np.sin(2*np.pi*f*relative),np.cos(2*np.pi*f*relative)])
 design=np.column_stack(columns);coef,_,rank,_=np.linalg.lstsq(design,y,rcond=None)
 if rank<len(columns):raise ValueError("幅相复核设计矩阵退化，请核查频率分离")
 fitted=design@coef;start=2 if detrend=="linear" else 1;components=[]
 for i,f in enumerate(frequencies):
  a,b=coef[start+2*i:start+2*i+2];components.append({"frequency_per_minute":float(f),"period_minutes":1/float(f),"amplitude_ms":float(np.hypot(a,b)),"phase_radians":float(np.arctan2(b,a))})
 total=float(np.sum((y-np.mean(y))**2));error=float(np.sum((y-fitted)**2))
 return {"components":components,"fitted_ms":fitted.tolist(),"offset_ms":float(coef[0]),"slope_ms_per_minute":float(coef[1]) if detrend=="linear" else 0,"rmse_ms":float(np.sqrt(error/len(y))),"r_squared":1-error/total if total>0 else None,"phase_origin_minutes":float(t[0]),"phase_convention":"A*sin(2*pi*f*(t-t0)+phi)，phi=atan2(cos系数,sin系数)，t0为窗口首观测时刻"}
