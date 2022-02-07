import os

# for i in open('data1/Client/','r'):
#     print(i)


# os.path.join()
# subdirname = os.path.basename(os.path.dirname('data1/Client/'))
# print(subdirname)

# import required module
import os
 
# assign directory
directory = 'data1/Client/'
 
# iterate over files in
# that directory
li =[]
for filename in os.scandir(directory):
    
    li.append(filename.path.split('/')[-1])

print( max(li) )