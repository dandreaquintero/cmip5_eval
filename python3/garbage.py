
start = '_'
end = '-'
s = 'pr_day_FGOALS-s2_rcp45_r1i1p1_20060101-21001231_Andes.nc'
print((s.split(start))[-2].split(end)[0])
print((s.split(start))[-2].split(end)[1])
