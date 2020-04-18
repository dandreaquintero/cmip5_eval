# #creating a DataFrame using a dictionary
# import pandas as pd
# dictionary={'fruits':['apples', 'banana','mangoes'], 'count':[10,20,15]}
# df= pd.DataFrame(dictionary)
# print (df)

#creating a DataFrame using series
import pandas as pd
series= pd.series([6,12], index =['a','b'])
df= pd.DataFrame(series)
print (df)

# # MERGE OPERATION
# import pandas as pd
# player=['player1', 'player2','player3']
# point =[8,5,6]
# title= ['game1','game2','game3']
# df1  = pd.DataFrame(['Player':player, 'Points':point, 'Title':title])
