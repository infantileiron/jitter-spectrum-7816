def top_peaks(frequencies,powers,count=5,min_spacing=0):
 if len(frequencies)!=len(powers):raise ValueError("频率与功率长度不匹配")
 candidates=[i for i,p in enumerate(powers) if (i==0 or p>=powers[i-1]) and (i==len(powers)-1 or p>=powers[i+1])]
 chosen=[]
 for i in sorted(candidates,key=lambda j:-powers[j]):
  f=float(frequencies[i])
  if f<=0 or any(abs(f-p["frequency_per_minute"])<min_spacing for p in chosen):continue
  chosen.append({"frequency_per_minute":f,"period_minutes":1/f,"power":float(powers[i])})
  if len(chosen)>=count:break
 return chosen
