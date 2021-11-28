from pyconll import  load_from_string
def loadSentences(n,file):
    """
    :param n:  n sentence
    :param file:
    :return:
    """
    count=0
    text=""
    line=file.readline()
    while(line and count<n):
        text+=line
        if(line=="\n"):
            count+=1
        line=file.readline()
    not_empty=True if line else False
    return  load_from_string(text),not_empty