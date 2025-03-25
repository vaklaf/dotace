import csv





def fixer():
    with open(r'..\outputs\web_crawler_output_plk\plk_individualni-zadosti_20250320_032541.csv','r',encoding='utf-8') as inFile:
        reader = csv.reader(inFile,delimiter=";")
        with open(r'..\outputs\web_crawler_output_plk\plk_individualni-zadosti_20250320_032541f.csv','w',newline='\n',encoding='utf-8') as outFile:
            writer = csv.writer(outFile,delimiter=";")
            
            i = 0
            for row in reader:
                r = row
                if i >=1:
                    r[5] = r[5].replace(".",",")[:-2]
                writer.writerow(r)
                i +=1
            


if __name__=="__main__":
    fixer()