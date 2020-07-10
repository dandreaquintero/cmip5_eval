echo Calculate $1
# python indices_calculation.py --loop --index=$1 --rcp=rcp45 &&
# python indices_calculation.py --loop --index=$1 --rcp=rcp85 &&
#
# python indices_calculation.py --merge=all --index=$1 --rcp=rcp45 &&
# python indices_calculation.py --merge=all --index=$1 --rcp=rcp85  &&
#
python indices_calculation.py --graph=map --index=$1 --rcp=rcp45
python indices_calculation.py --graph=map --index=$1 --rcp=rcp85
#python indices_calculation.py --graph=ts --index=$1 --rcp=rcp45
