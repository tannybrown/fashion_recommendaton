import math

# 겨울철
def winter(t,v) :
  v = msTokm(v)
  return 13.12 + 0.6215 * t - 11.37 * (v ** 0.16) + 0.3965 * (v ** 0.16) * t

# 단위변환
def msTokm(ms) :
  return ms * 3.6
  
# print('겨울 : ' + str(winter(10,1.3)))

# 습구온도 계산
def calculate_Tw(Ta, RH):
  Tw = Ta * math.atan(0.151977*(RH+8.313659)**(1/2)) + math.atan(Ta+RH) - math.atan(RH-1.67633) + 0.00391838*RH**(3/2)*math.atan(0.023101*RH) - 4.686035
  return Tw

# 여름철
def summer(Ta,RH) :
  Tw = calculate_Tw(Ta,RH)
  return -0.2442 + 0.55399*Tw + 0.45535*Ta - 0.0022*Tw**2 + 0.00278*Tw*Ta + 3.0


# print(summer(32,64))                                                            
