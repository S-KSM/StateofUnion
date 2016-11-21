
# coding: utf-8

# In[1]:

def myrun(args):
    """python Dave2nd.py --m="all" or python Dave2nd.py --m="pair". The Default option is all"""
    mode = args.m
    if mode == "pair":
        print("Preparing...")
        #import glob
        import pandas as pd
        import csv
        import argparse
        import sys
        import re

        print("Reading Keywords")
        ### Reads Keywords from your file
        df_input = pd.read_csv("input.dat",sep = ",",header=None)
        df_input.columns = ["Keyword","filename"]

        keyword_file=df_input.T.to_dict()

        print("Let's get started.")
        total = {}
        dict_top100 = {}
        final_wordfrequency = {}

        for i in range(len(keyword_file)):
            file = keyword_file[i]["filename"]
            total[file]={}
            key = keyword_file[i]["Keyword"]
            #print(key)
            total[file][key]=[]    
            #print("Analyzing:%s" %file)

            try:

                f = open(file,"r",errors = "surrogateescape") # In case there is an error with the formatting, it tries to handle
                mystring = f.read() #Reads the file
                #print(len(mystring))
                mystring = re.sub(r'\s+'," ",mystring,flags=re.IGNORECASE)
                #print(len(mystring))
                mystring = re.sub(r'\n'," ",mystring,flags=re.IGNORECASE)
                mystring = (mystring.encode("ascii",errors="ignore")).decode("utf-8",errors="ignore")

                for  i in re.finditer(key,mystring,re.IGNORECASE):
                    #print("hey")
                    if i.span()[0]> 50 and  i.span()[1]+50 < len(mystring): 
                        total[file][key].append(mystring[i.span()[0]-50:i.span()[1]+50])
                    elif i.span()[1]+50 < len(mystring):
                        total[file][key].append(mystring[0:i.span()[1]+50].strip("\n"))
                    else:
                        total[file][key].append(mystring[i.span()[0]-50:len(mystring)].strip("\n"))

            except:
                pass
                print("File: %s doesn't exist. Please check %s-%s pair in the input file." %(file,file,key))
        df = pd.DataFrame(total)
        with open('finaloutput2.csv', 'w', newline='') as csvfile:
            csvWriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow(['FileName', 'Keyword', 'Sentence'])

            for column in df.keys():
                col_file = column
                for keyword in total[col_file].keys():
                    col_key = keyword
                    for i in range(len(total[column][keyword])):
                        sentence = str(total[column][keyword][i])

                        csvWriter.writerow([col_file,col_key,sentence])

        df_temp = pd.read_csv("finaloutput2.csv", encoding="utf-8", error_bad_lines=False,delimiter=",")
        grouped = df_temp.groupby(['Keyword','FileName'])
        df_temp2 = grouped.count()
        df_temp2.columns = ['Frequency']
        df_temp2.to_csv("Frequency_updated2.csv")

        print("All Done!")
    
    else:

        print("Preparing...")
        import glob
        import pandas as pd

        from collections import Counter
        import re

        path_documents = r"C:\Users\Shobeir\Desktop\Playground\Python\StateoftheUnion\*.txt"
        path_inp = r"C:\Users\Shobeir\Desktop\Playground\Python\StateoftheUnion\input.dat"


        print("Reading Keywords")
        ### Reads Keywords from your file
        #for file in glob.glob(path_inp):
        f = open(path_inp,"r", errors="ignore", encoding='utf-8')
        inp = f.read()
        keywords = [line for line in inp.splitlines()] # makes a list of keywords

        print("Let's get started.")
        total = {}
        dict_top100 = {}
        final_wordfrequency = {}

        for file in glob.glob(path_documents):
            total[file]={}
            print("Analyzing: " + str(file))
            f = open(file,"r",errors = "surrogateescape") # In case there is an error with the formatting, it tries to handle
            mystring = f.read() #Reads the file
            #print(len(mystring))
            mystring = re.sub(r'\s+'," ",mystring,flags=re.IGNORECASE)
            #print(len(mystring))
            mystring = re.sub(r'\n'," ",mystring,flags=re.IGNORECASE)
            mystring = (mystring.encode("ascii",errors="ignore")).decode("utf-8",errors="ignore")
            #print(len(mystring))
            for key in keywords:
                total[file][key]=[]
                for  i in re.finditer(key,mystring,re.IGNORECASE):
                    #print("hey")
                    if i.span()[0]> 50 and  i.span()[1]+50 < len(mystring): 
                        total[file][key].append(mystring[i.span()[0]-50:i.span()[1]+50])
                    elif i.span()[1]+50 < len(mystring):
                        total[file][key].append(mystring[0:i.span()[1]+50].strip("\n"))
                    else:
                        total[file][key].append(mystring[i.span()[0]-50:len(mystring)].strip("\n"))

        df = pd.DataFrame(total)

        final_output = open(r"C:\Users\Shobeir\Desktop\Playground\Python\StateoftheUnion\finaloutput2.csv","w", encoding="utf-8")
        final_output.write("FileName, Keyword, Sentence\n")
        for keyword in keywords:
            col_key = keyword
            for column in df.columns:
                col_file = column
                for i in range(len(total[column][keyword])):
                    sentence = str(total[column][keyword][i]).replace(","," ")
                    final_output.write(col_file + ", " + col_key + ", " + sentence + "\n")
        final_output.close()

        df_temp = pd.read_csv(r"C:\Users\Shobeir\Desktop\Playground\Python\StateoftheUnion\finaloutput2.csv", encoding="utf-8", error_bad_lines=False)
        grouped = df_temp.groupby([' Keyword','FileName'])
        df_temp2 = grouped.count()
        df_temp2.columns = ['Frequency']
        df_temp2.to_csv(r"C:\Users\Shobeir\Desktop\Playground\Python\StateoftheUnion\Frequency_updated2.csv")

        print("All Done!")




# In[4]:

def main():
    """python Dave2nd.py --m="all" or python Dave2nd.py --m="pair". The Default option is "all" """
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--m',type = str,default = "all",
                       help = '''to read from keyword-filename
                        pair use "pair"''')
    args = parser.parse_args()
    sys.stdout.write(str(myrun(args)))
    
if __name__=='__main__':
    main()



