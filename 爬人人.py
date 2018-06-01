import urllib.request  
import re  
  
  
def get_links(url, name='yyets'):  
    data = urllib.request.urlopen(url).read().decode()  
    pattern = '"(magnet:.*\=wss\:\/\/tracker\.fastcast\.nz)"'  
    linksfind = set(re.findall(pattern, data))  
    linksdict = {}  
    total = len(linksfind)  
    for i in linksfind:
        print (i,end='\n')
        #linksdict[int(i[1][1:3]) * 100 + int(i[2][1:3])] = i  
#    with open(name + '.txt', 'w') as f:   
#        for i in sorted(list(linksdict.keys())):  
#            f.write(linksdict[i][0] + '\n')  
#            print(linksdict[i][0])  
    print("Get download links of: ", name, str(total))  
  
  
if __name__ == '__main__':  
    #---------- 将要下载的网址粘到下面，多个就用多个get---------------------------  
    get_links('http://zmz003.com/Gk7St3')
    
    print('All is okay!') 
