echo Calculate $1
python indices_calculation.py --loop --index=$1 --rcp=rcp45 &&
python indices_calculation.py --loop --index=$1 --rcp=rcp85 &&
#
python indices_calculation.py --merge=all --index=$1 --rcp=rcp45 &&
python indices_calculation.py --merge=all --index=$1 --rcp=rcp85  &&
#
python indices_calculation.py --graph=map --index=$1 --rcp=rcp45 &&
python indices_calculation.py --graph=map --index=$1 --rcp=rcp85 &&
python indices_calculation.py --graph=ts --index=$1 --rcp=rcp45

 #python indices_calculation.py --loop --index=tnny --rcp=rcp45
 #python indices_calculation.py --loop --index=tnny --rcp=rcp85
 #python indices_calculation.py --merge=all --index=tnny --rcp=rcp45
 #python indices_calculation.py --merge=all --index=tnny --rcp=rcp85

# python indices_calculation.py --graph=ts --index=txny --rcp=rcp45
# python indices_calculation.py --graph=ts --index=tnxy --rcp=rcp45
# python indices_calculation.py --graph=ts --index=txxy --rcp=rcp45
# python indices_calculation.py --graph=ts --index=tnny --rcp=rcp45
#
# python indices_calculation.py --graph=map --index=txny --rcp=rcp45
# python indices_calculation.py --graph=map --index=tnxy --rcp=rcp45
# python indices_calculation.py --graph=map --index=txxy --rcp=rcp45
# python indices_calculation.py --graph=map --index=tnny --rcp=rcp45
#
#
# python indices_calculation.py --graph=map --index=txny --rcp=rcp85
# python indices_calculation.py --graph=map --index=tnxy --rcp=rcp85
# python indices_calculation.py --graph=map --index=txxy --rcp=rcp85
# python indices_calculation.py --graph=map --index=tnny --rcp=rcp85



#python indices_calculation.py --loop --index=$1 --rcp=rcp45
#python indices_calculation.py --loop --index=$1 --rcp=rcp85
#
#python indices_calculation.py --merge=all --index=$1 --rcp=rcp45
#python indices_calculation.py --merge=all --index=$1 --rcp=rcp85
#
# python indices_calculation.py --graph=map --index=$1 --rcp=rcp45
# python indices_calculation.py --graph=map --index=$1 --rcp=rcp85
#python indices_calculation.py --graph=ts --index=$1 --rcp=rcp45

# python indices_calculation.py --loop --index=tx10p --rcp=rcp45
# python indices_calculation.py --loop --index=tx10p --rcp=rcp85
#
# python indices_calculation.py --merge=all --index=tx10p --rcp=rcp45
# python indices_calculation.py --merge=all --index=tx10p --rcp=rcp85
#
# python indices_calculation.py --graph=map --index=tx10p --rcp=rcp45
# python indices_calculation.py --graph=map --index=tx10p --rcp=rcp85
# python indices_calculation.py --graph=ts --index=tx10p --rcp=rcp45

# python indices_calculation.py --loop --index=tx90p --rcp=rcp45
# python indices_calculation.py --loop --index=tx90p --rcp=rcp85
#
# python indices_calculation.py --merge=all --index=tx90p --rcp=rcp45
# python indices_calculation.py --merge=all --index=tx90p --rcp=rcp85
#
# python indices_calculation.py --graph=map --index=tx90p --rcp=rcp45
# python indices_calculation.py --graph=map --index=tx90p --rcp=rcp85
# python indices_calculation.py --graph=ts --index=tx90p --rcp=rcp45
#
# python indices_calculation.py --loop --index=tn90p --rcp=rcp45
# python indices_calculation.py --loop --index=tn90p --rcp=rcp85
#
# python indices_calculation.py --merge=all --index=tn90p --rcp=rcp45
# python indices_calculation.py --merge=all --index=tn90p --rcp=rcp85
#
# python indices_calculation.py --graph=map --index=tn90p --rcp=rcp45
# python indices_calculation.py --graph=map --index=tn90p --rcp=rcp85
# python indices_calculation.py --graph=ts --index=tn90p --rcp=rcp45
