#13-07-2026
import os
#get Current Working Folder
print('Get Current Working Dir')
current_dir=os.getcwd()
print(current_dir)
#change Folder
print('Change Dir')
os.chdir('D:/Github/Python/Pratice')
#list all the files and folder in selected Dir
print(os.listdir())
#creating new folder in selected dir
print('Creating a New Folder')
os.mkdir('File Handling')
print(os.listdir())
#removing dir if empty
print('Removing a Folder')
print(os.rmdir('File Handling'))
print(os.listdir())
#check path exist
print('Check Path Exist or Not')
print(os.path.exists('D:\Github\Remote_Github'))
print('Get File or Folder Size')
print(os.path.getsize('D:\Github\Remote_Github\Python-Pratice-Project\Abstraction\CloudStorageProviderAPISimulator.py'))
print('Check is Folder or not')
print(os.path.isdir('D:\Github\Remote_Github\Python-Pratice-Project\Abstraction'))
print('Check is File or not')
print(os.path.isfile('D:\Github\Remote_Github\Python-Pratice-Project\Abstraction\CloudStorageProviderAPISimulator.py'))
print(os.listdir())
os.chdir('D:/Github/Python/Pratice/Abstraction')
print(os.getcwd())
print(os.listdir())
print('Rename File')
os.rename('D:/Github/Python/Pratice/Abstraction/CloudStorageInterface.py','D:/Github/Python/Pratice/Abstraction/CloudStorageInterface.py')
print(os.listdir())
os.chdir('D:/Github/Python/Pratice')
print(os.listdir())
print('Rename Folder')
os.rename('D:/Github/Python/Pratice/Classes, Objects & Variables','D:/Github/Python/Pratice/Classes_Objects_Variables')
print(os.listdir())