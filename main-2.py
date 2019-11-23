
import re
import json
import requests as req
from bs4 import BeautifulSoup

from flask import Flask
from flask import request

from urllib import request as reques

import nltk
nltk.download('punkt')
from nltk import word_tokenize




app= Flask(__name__)


@app.route('/get_file', methods= ['POST', 'GET'])
def flask_resume():
    url = request.args.get('files')
    get_url = req.get(url)
    input_resume = reques.urlopen(url).read().decode('utf8')
   
    raw = BeautifulSoup(input_resume, 'html.parser').get_text()
    tokens = word_tokenize(raw)
    a = print (tokens)
    context = {}
    re_email = re.findall(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-z A-Z]{1,4}',str(a))
    re_phone = re.findall(r'((?:\(?\+34\)?)?\d{12})',str(a)) or (r'((?:\(?\+34\)?)?\d{10})',str(a))
    for i,w in enumerate(tokens):
        if w.startswith("develop"):
            if w.startswith("develop"):
                try:
                    context[w] = tokens[i:i+10]
                except:pass
            elif w.startswith("Develop"):
                try:
                    context[w] = tokens[i:i+10]
                except:pass
            elif w.startswith("Work"):
                try:
                    context[w] = tokens[i:i+10]
                except:pass
            elif w.startswith("Hands"):
                try:
                    context[w] = tokens[i:i+10]
                except:pass
            elif w.startswith("Design"):
                try:
                    context[w] = tokens[i:i+10]
                except:pass
            fp = open('star.txt','w')
            fp.write('Word'+'\t\t'+'PreviousContext\n')
            for word in context:
                fp.write(word+'\t\t'+' '.join(context[word])+'\n')
            fp.close()
            fp = open('star.txt','r')
            with open('star.txt', 'r+',encoding='latin-1') as final_file:
        
                content = final_file.readlines()
    
    

    with open('get_file_from_url.txt', 'w+') as f:
        f.write(get_url.text)

    with open('get_file_from_url.txt','r', encoding='latin-1')as file1:
        with open('Details.txt','r',encoding='latin-1' )as file2:
            same = set(file1).intersection(file2)
            
    same.discard('\n')
    words_list = []

    for line in same:
        words_list.append(line)
        
    words_list = list(map(str.strip,words_list))
    print ('words_list', words_list)

    #extracting other titles
    with open('get_file_from_url.txt','r', encoding='latin-1')as file3:
        with open('other_details.txt','r',encoding='latin-1' )as file4:
            same1 = set(file3).intersection(file4)
                    
    same1.discard('\n')
    words_extract = []

    for f in same1:
        words_extract.append(f)
        
    words_extract = list(map(str.strip,words_extract))
    print ('words_extract', words_extract)
            
    #function to replace extracted titles        
    def multiwordReplace(text, wordDic):
        rc = re.compile('|'.join(map(re.escape, wordDic)))
        def translate(match):
            return wordDic[match.group(0)]
        return rc.sub(translate, text)


    str1 = open('get_file_from_url.txt','r', encoding='latin-1')
    str1 = str1.read()

    wordDic1 = dict((k,'Summary') for k in words_list)
    wordDic2 = dict((k,'xyz') for k in words_extract)
    wordDic = dict(wordDic1, **wordDic2)
    print(wordDic)

    with open ('se.txt','w', encoding='latin-1') as infile:
        str2 = multiwordReplace(str1,wordDic)
        infile.write(str2)
        
    #extracting summary paragraphs
    with open("se.txt", encoding='latin-1')as infile,open("fgh1.txt",'w', encoding='latin-1')as outfile:
        copy = False
        for word in words_extract:
            for line in infile:
                if line.strip() == "Summary":
                    copy = True
           
                elif line.strip() == "xyz":
                    copy = False
                elif copy:
                    outfile.write(line)

    with open('fgh1.txt', 'r+') as final_file:
        parse_output = final_file.readlines()

    return json.dumps({'Project_details':[line.strip('\n') for line in parse_output if line != '\n'],'Email':[line.strip('\n') for line in re_email if line != '\n'],'Context':[line.strip('\n') for line in content if line != '\n'],
                                 'phone':[line.strip('\n') for line in re_phone if line != '\n']})

 
    

if __name__ == "__main__":
    
    
    app.run(debug=True)