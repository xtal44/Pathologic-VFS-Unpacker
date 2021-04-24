import io
import argparse
import os


#Parsing the arguments (getting the file name)

parser = argparse.ArgumentParser(description = 'Unpack a specified VFS file')
parser.add_argument('VFSfilename', metavar = 'fName', type = str, nargs ='+', help = 'path to the file to unpack')

parsedArgs = parser.parse_args()

print(parsedArgs.VFSfilename[0]+":")

#Open the VFS for reading as a binary stream
archive = open (parsedArgs.VFSfilename[0],"rb",buffering = 0)



header = archive.read(4) #4 byte header
header = header.decode("UTF-8")

if header == "LP1C":


    subdirectories = archive.read(4) #uint32
    subdirectories = int.from_bytes(subdirectories, byteorder = 'little',signed = False)

    numberOfFiles = archive.read(4) #uint32
    numberOfFiles = int.from_bytes(numberOfFiles, byteorder = 'little',signed = False)

    #Initializing lists, probably not necessary in Python, easier for me to remember the list names this way tho
    fileNames = []
    fileOffsets = []
    fileLengths = []
    fileNameLengths = []
    UIDs = []

    #Reading filename lengths, filenames, file offsets and UIDs in a loop
    for i in range(numberOfFiles):
        fileNameLength = archive.read(1) #1 byte for the filename size
        fileNameLength = int.from_bytes(fileNameLength, byteorder = 'little',signed = False)
        fileNameLengths.append(fileNameLength)
        fileName = archive.read(fileNameLength)
        print(fileName)
        fileName = fileName.decode("cp1251")
        print(fileName)
        fileNames.append(fileName)
        fileLength = archive.read(4)
        fileLength = int.from_bytes(fileLength, byteorder = 'little',signed = False)
        fileLengths.append(fileLength)
        fileOffset = archive.read(4)
        fileOffset = int.from_bytes(fileOffset, byteorder = 'little',signed = False)
        fileOffsets.append(fileOffset)
        UID = archive.read(8)
        UIDs.append(UID)

    #Create a directory for writing the files
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    archiveSub = (parsedArgs.VFSfilename[0])[0:-4]
    path = os.path.join(scriptDirectory, archiveSub)
    try:
        os.mkdir(path)
    except OSError as error:
        print("Subdirectory already existed")

    #Writing out files, could be done in the loop above, separated for easier debugging for now
    for i in range(numberOfFiles):

        fileAbs = os.path.join(path,fileNames[i])
        if (os.path.isfile(fileAbs)):
            overwriteCheck = input("File " + fileNames[i] + " already exists! Overwrite? Y/N: ")
            if overwriteCheck == "N":
                continue

        outputFile = open(fileAbs,"wb",buffering = 0)
        archive.seek(fileOffsets[i])
        outputFile.write(archive.read(fileLengths[i]))
        outputFile.close()

else:
    print ("Not a proper VFS file (check header)")

archive.close()