from justwatch import JustWatch
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

just_watch = JustWatch(country='Canada')
        
movies = open("Unwatched.txt", "r")
textFile = open("Results.txt", "w+")
line = movies.readline()
textFile.write("Movie Title,Stream,Rent,Buy\n")

while line:
    textFile.write("%s" % line.rstrip())
    results = just_watch.search_for_item(query=line)
    result = results.get("items")
    isResult = False
    stream = list()
    rent = list()
    buy = list()

    for x in range(len(result)):
        for y in result[x]:
            if y == 'title':
                searchTitle = ''.join(line.split()).lower()
                resultTitle = ''.join(result[x][y].split()).lower()
                if fuzz.ratio(searchTitle,resultTitle) >= 80:
                    foundTitle = str(result[x][y])
                    ratio = str(fuzz.ratio(searchTitle,resultTitle))
                    isResult = True
                else:
                    isResult = False
            if isinstance(result[x][y], list) and isResult is True:
                for z in range(len(result[x][y])):
                    try:
                        if result[x][y][z]["monetization_type"] == "flatrate":
                            for v in result[x][y][z]["urls"].values():
                                if 'http' in v and 'intent' not in v:
                                    stream.append(v)
                        elif result[x][y][z]["monetization_type"] == "rent":
                            for v in result[x][y][z]["urls"].values():
                                if 'http' in v and 'intent' not in v:
                                    rent.append(v)   
                        elif result[x][y][z]["monetization_type"] == "buy":
                            for v in result[x][y][z]["urls"].values():
                                if 'http' in v and 'intent' not in v:
                                    buy.append(v)
                    except KeyError:
                        pass

    maxValue = max(len(stream), len(rent))
    maxValue = max(len(buy), maxValue)
    #textFile.write("MaxValue: %i" % maxValue)
    #textFile.write(",Stream: %i" % len(stream))
    #textFile.write(",Rent: %i" % len(rent))
    #textFile.write(",Buy: %i\n" % len(buy))
    

    for x in range(maxValue):
        try:
            textFile.write(",%s" % stream[x])
        except:
            textFile.write(",") 
        try:
            textFile.write(",%s" % rent[x])
        except:
            textFile.write(",") 
        try:
            textFile.write(",%s" % buy[x])
        except:
            textFile.write(",") 
        textFile.write("\n") 
    '''
    textFile.write("Stream:\n")                
    for item in stream:
        textFile.write(",%s\n" % item)  
    
    textFile.write("Rent:\n") 
    for item in rent:
        textFile.write(",,%s\n" % item)    
    
    textFile.write("Buy:\n") 
    for item in buy:
        textFile.write(",,,%s\n" % item)           
    textFile.write("\n")
    '''
    textFile.write("\n")
    line = movies.readline()
    

textFile.close()
movies.close()
