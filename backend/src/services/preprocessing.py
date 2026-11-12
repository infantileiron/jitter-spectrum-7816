import numpy as np
def prepare(points,detrend="mean"):
 if len(points)<16:raise ValueError("窗口内至少16个观测点，不对不足样本造周期")
 ordered=sorted(points,key=lambda p:p["time_minutes"]);t=np.array([p["time_minutes"] for p in ordered],dtype=float);y=np.array([p["jitter_ms"] for p in ordered],dtype=float)
 if not np.all(np.isfinite(t)) or not np.all(np.isfinite(y)):raise ValueError("时间与抖动值必须有限")
 dt=np.diff(t)
 if np.any(dt<=0):raise ValueError("时间戳重复或非递增，不允许静默去重")
 relative=t-t[0];median=float(np.median(dt));regular=bool(np.allclose(dt,median,rtol=1e-6,atol=1e-9))
 if detrend=="linear":design=np.column_stack([np.ones(len(t)),relative])
 elif detrend=="mean":design=np.ones((len(t),1))
 else:raise ValueError("去趋势方式只能为mean或linear")
 coefficients=np.linalg.lstsq(design,y,rcond=None)[0];baseline=design@coefficients;residual=y-baseline;variance=float(np.mean(residual**2))
 if variance<=1e-20*max(1,float(np.mean(y**2))):raise ValueError("原序列或去趋势后为常量，没有可分析的周期波动")
 return t,y,residual,{"n":len(t),"start_minutes":float(t[0]),"end_minutes":float(t[-1]),"span_minutes":float(t[-1]-t[0]),"median_interval_minutes":median,"min_interval_minutes":float(np.min(dt)),"max_interval_minutes":float(np.max(dt)),"regular":regular,"fft_nyquist":1/(2*median) if regular else None,"detrend":detrend,"removed_offset_ms":float(coefficients[0]),"removed_slope_ms_per_minute":float(coefficients[1]) if detrend=="linear" else 0.0,"residual_variance_ms2":variance,"phase_origin_minutes":float(t[0])}
def sampling_meta(points):
 if len(points)<16:raise ValueError("窗口内至少16个观测点")
 t=np.array(sorted(p["time_minutes"] for p in points),dtype=float);d=np.diff(t)
 if np.any(d<=0):raise ValueError("时间戳重复，不允许静默去重")
 median=float(np.median(d));regular=bool(np.allclose(d,median,rtol=1e-6,atol=1e-9))
 return {"span":float(t[-1]-t[0]),"regular":regular,"nyquist":1/(2*median) if regular else None}
