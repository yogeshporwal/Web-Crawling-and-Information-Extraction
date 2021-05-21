'''
Name:Yogesh Porwal
Roll no : 20CS60R52
Email-id:yogeshporwal@kgpian.iitkgp.ac.in
Program name: task1.py
'''

#importing packages
import urllib.request, urllib.error, urllib.parse
import sys
import ply.lex as lex
import ply.yacc as yacc
import unicodedata 

#importing task2.py so that we can use function(s) from this program to integrate functionalities of second task with task1
import task2

#these dictionaries will contain values of extracted fields for movie page
extracted_fields={'Movie Name':'#','Director':[],'Genre':'#','Writers':'#','Producer':'#','Original Language':'#','Cast & Charachter':[],'Storyline':'#','Box Office Collection':'#','Runtime':'#','WHERE TO WATCH':[]}
recommended_movies={}
cast_and_pagelink={}
urls=[]
count=0

#tokens list
tokens = (
	'LDIR','NAME','END','RLINK','LLINK','WSPACE','WRITER_TAG','PRODUCER_TAG','L_WATCH','R_WATCH',
    'LANGTAG','LLANG','LSPAN','STORY_TAG','BOX_TAG','L_TITLE','R_TITLE','LINK','L_GENRE',
    'RSPAN','LCAST','BR','TIME_TAG','TIME','END_TIME','HREF','E_LINK','L_LIKE','WSPAN',
	)

#token(s) defination

#used to extract movie-name
def t_L_TITLE(t):
    r'<title>\s*'
    return t

#used to extract movie-name
def t_R_TITLE(t):
    r'\s*-\ Rotten\ Tomatoes</title>'
    return t

#used to extract director(s) name
def t_LDIR(t):
    r'data-qa=\"movie-info-director\">\s*'
    return t

#used to extract director name
def t_RLINK(t):
    r'\s*</a>[,]*\s*'
    return t

#used to extract genre
def t_L_GENRE(t):
    r'<div\ class=\"meta-value\ genre"\ data-qa=\"movie-info-item-value\">'

#used to extract genre and storyline
def t_END(t):
    r'\s*</div>'
    return t

#used to extract storyline
def t_STORY_TAG(t):
    r'data-qa=\"movie-info-synopsis\">\s*'
    return t

#used to extract original language of movie
def t_LANGTAG(t):
    r'>Original\ Language:</div>\s*'
    return t

#used to extract writer(s) name
def t_WRITER_TAG(t):
    r'>Writer:</div>\s*<div\ class=\"meta-value\"\ data-qa=\"movie-info-item-value\">\s*'
    return t

#used to extract original language of movie
def t_LLANG(t):
    r'<div\ class=\"meta-value\"\ data-qa=\"movie-info-item-value\">\s*'
    return t

#used to extract writer(s) and producer(s) name
def t_LLINK(t):
    r'<a\ href=\"/celebrity/[a-zA-Z0-9_\s~.$\(\)\,!\&\#\@\'\":_-]+\">\s*'
    return t

#used to extract producer(s) name
def t_PRODUCER_TAG(t):
    r'>Producer:</div>\s*<div\ class=\"meta-value\"\ data-qa=\"movie-info-item-value\">\s*'
    return t

#used to extract writer(s) and producer(s) name
def t_LSPAN(t):
    r'\s*\"\ class=\"unstyled\ articleLink\"\ data-qa=\"cast-crew-item-link\">\s*<span\ title=\"[A-Za-z0-9\s.$\(\)\,!\&\#\@;%\'\":_-]+\">\s*'
    return t

#used to extract writer(s) and producer(s) name
def t_WSPAN(t):
    r'<span\ title=\"[A-Za-z0-9\s.$\(\)\,!\&\#\@;%\'\":_-]+\">\s*'
    return t

#used to extract writer(s) and producer(s) name
def t_RSPAN(t):
    r'\s*</span>\s+ [</a>]*\s*<span\ '
    return t

#used to extract cast and charachter
def t_LCAST(t):
    r'class=\"characters\ subtle\ smaller\"\ title=\"[A-Za-z0-9\s.$\(\)\,!\&\#\@;%\'\":_-]+\">\s* <br/>\s*'
    return t

#used to extract 'you might also like' movies
def t_L_LIKE(t):
    r'<span\ slot=\"title\"\ class=\"recommendations-panel__poster-title\">'
    return t

#used to extract 'you might also like' movies
def t_BR(t):
    r'\s*<(br\/|\/span)>'
    return t

#used to extract 'where to watch' platforms
def t_L_WATCH(t):
    r'<affiliate-icon\ name=\"'
    return t

#used to extract 'where to watch' platforms
def t_R_WATCH(t):
    r'\ alignicon=\"left\ center\"></affiliate-icon>'
    return t

#used to extract box office collection
def t_BOX_TAG(t):
    r'>Box\ Office\ \(Gross\ USA\):</div>\s*'
    return t

#used to extract runtime
def t_TIME_TAG(t):
    r'>Runtime:</div>\s*'
    return t

#used to extract runtime
def t_TIME(t):
    r'<time\ datetime=\"[A-Za-z0-9\s.$\(\)\,!\&\#\@;%\'\":_-]+">\s*'
    return t

#used to extract runtime
def t_END_TIME(t):
    r'\s*</time>'
    return t

#used to extract urls
def t_HREF(t):
    r'<a\ href=\"\s*'
    return t

#used to extract urls
def t_E_LINK(t):
    r'\"\ class=\"recommendations-panel__poster-link\">\s*'
    return t

#used to extract name(s)
def t_NAME(t):
	r'[a-zA-Z0-9.$\(\)\,!\&\#\@;%\'\"?:_-]+'
	return t

#used to extract urls
def t_LINK(t):
    r'[A-Za-z0-9_.\~\-/]+'
    return t

#for spaces and tabs
t_WSPACE = r'[\ \t]+'

#rule for Error Handling
def t_error(t):
	t.lexer.skip(1)

'''
Parsing Rules
'''

def p_start(t):
	'''start : director
             | language
             | title
             | writer
             | producer
             | cast
             | cast_char
             | cast_no_link
             | storyline
             | collection
             | runtime
             | url
             | might_like
             | genre
             | watch
    '''

	pass

#for extracting movie-name
def p_title(t):
    'title : L_TITLE names R_TITLE'
    extracted_fields['Movie Name'] = t[2]

#for extracting genre
def p_genre(t):
    'genre : L_GENRE names END'
    extracted_fields['Genre'] = t[2]

#for extracting 'WHERE TO WATCH' fields
def p_watch(t):
    'watch : L_WATCH names R_WATCH'
    platform_to_watch=t[2][:-1]
    extracted_fields['WHERE TO WATCH'].append(platform_to_watch)

#for extracting director(s) name
def p_director(t):
    'director : LDIR names RLINK'
    extracted_fields['Director'].append(t[2])

#for extracting original language
def p_language(t):
    'language : LANGTAG LLANG names END'
    extracted_fields['Original Language'] = t[3]

#for extracting cast and charachter
def p_cast_char(t):
    'cast_char : HREF LINK LSPAN names RSPAN LCAST names BR'
    string=t[4]+' as '+t[7]
    extracted_fields['Cast & Charachter'].append(string)
    cast_and_pagelink[string]=t[2]

#for extracting cast and charachter when role is not mentioned
def p_cast_(t):
    'cast : HREF LINK LSPAN names RSPAN LCAST BR'
    string=t[4]+'(no role mentioned)'
    extracted_fields['Cast & Charachter'].append(string)
    cast_and_pagelink[string]=t[2]

#for extracting cast and charachter
def p_cast_no_link(t):
    'cast_no_link : WSPAN names RSPAN LCAST names BR'
    string=t[2]+' as '+t[5]
    extracted_fields['Cast & Charachter'].append(string)
    cast_and_pagelink[string]='#'

#for extracting cast and charachter when role is not mentioned
def p_cast_no_role(t):
    'cast_no_link : WSPAN names RSPAN LCAST BR'
    string=t[2]+'(no role mentioned)'
    extracted_fields['Cast & Charachter'].append(string)
    cast_and_pagelink[string]='#'

#for extracting story-line
def p_storyline(t):
    'storyline : STORY_TAG names END'
    extracted_fields['Storyline'] = t[2]

#for extracting boxoffice-collection
def p_collection(t):
    'collection : BOX_TAG LLANG names END'
    extracted_fields['Box Office Collection'] = t[3]

#for extracting runtime
def p_runtime(t):
    'runtime : TIME_TAG LLANG TIME names END_TIME'
    extracted_fields['Runtime'] = t[4]

#for extracting urls for 'you might also like' movies
def p_get_url(t):
    'url : HREF LINK E_LINK'
    urls.append(t[2])
    
#for extracting you might like part
def p_might_like(t):
    'might_like : L_LIKE names BR'
    global count
    recommended_movies[count]=t[2]
    count+=1

#for extracting writer-name
def p_writer(t):
    'writer : WRITER_TAG statements END'
    extracted_fields['Writers']=t[2]  

#for extracting producer-name
def p_producer(t):
    'producer : PRODUCER_TAG statements END'
    extracted_fields['Producer']=t[2]  

#recursive rules 
def p_names_one(t):
    'names : NAME'
    t[0] = t[1]

def p_names_mid(t):
    'names : NAME names'
    t[0] = t[1] + ' ' + t[2]
	
def p_names_multi(t):
    'names : NAME wspaces names'
    t[0] = t[1] + t[2] + t[3]

def p_wspaces(t):
	'''wspaces : WSPACE
			   | WSPACE wspaces'''
	t[0] = ' '

def p_statements_multi(t):
    'statements : statements statement'
    t[0]=t[1]+' , '+t[2]
    
def p_statements_single(t):
    'statements : statement '
    t[0]=t[1]
	
def p_statement(t):
    'statement : LLINK names RLINK'
    t[0]=t[2]

#error handling
def p_error(t):
	pass

'''
This function will parse movie page which is stored in current directory and whose file name is passed as argument,
it will extract all 11 required fields and store them 
'''
def parsing(filename):

    #building parser and starting parsing
    lexer = lex.lex()
    parser = yacc.yacc()
    file_ptr=open(filename)
    txt=file_ptr.read()
    txt=task2.strip_accents(txt)

    #initializing
    global extracted_fields
    extracted_fields={'Movie Name':'#','Director':[],'Genre':'Not Available!','Writers':'#','Producer':'#','Original Language':'#','Cast & Charachter':[],'Storyline':'#','Box Office Collection':'#','Runtime':'#','WHERE TO WATCH':[]}
    global recommended_movies
    recommended_movies={}
    global urls
    urls=[]
    global cast_and_pagelink
    cast_and_pagelink={}
    global count
    count=0

    print("\nparsing started...")
    parser.parse(txt)
    print("\nparsing done...required fields extracted and stored!")

#list of generes
genres=["Action &Adventure","Animation","Drama","Comedy","Mystery & Suspense","Horror","Sci-Fi","Documentary","Romance","Classics"]
#list to hold 100 movie-names
movies=[]

def main():

    content=None
    count=0

    #opening file
    file_ptr=open("rottentomatoes movie genre link.txt")
    source_code={}
    webContent=None
    code=[]
    print("\ncrawling started...")

    for line in file_ptr:

        if line[:5]!='https':
            continue

        url = line.strip()
        response = urllib.request.urlopen(url)
        webContent = response.read().decode('utf-8')
        content=webContent
        source_code[genres[count]]= webContent
        count+=1
    file_ptr.close()
    print("crawling completed!")
    
    #listing 10 genres to choose one
    print("\nChoose one of the following genres(1-10),to choose option enter corresponding digit mentioned before genre name:")

    print("%d\t%s" % (0,"EXIT"))    
    num=1
    for genre in genres:
        print("%d\t%s" % (num,genre))
        num+=1

    while(1):

        choice=input("\nenter your choice: ")
        flag=0
        if choice.isnumeric() and int(choice)>=1 and int(choice)<=10:
            flag=1
            break
        elif choice.isnumeric() and int(choice)==0 :
            flag=0
            break
        else:
            print("please choose correct option!")


    if flag==1:
        #if user choosed one of the 10 listed genres

        genre=genres[int(choice)]
        choice=int(choice)-1
        x=0
        #crawling again to find movie list
        for line in source_code[genres[int(choice)]].split('\n'):

            if x==1:
                title=line.split('</a>')[0]
                if title!='</div>':
                    movies.append(title)
                x=0

            if '$0' and 'class="unstyled articleLink">' in line:
                x=1
        
        #listing 100 movies to choose one
        print("\nChoose one of the following movies(1-100),to choose option enter corresponding number mentioned before movie name:")
        print("%d\t%s" % (0,"EXIT"))    
        num=1
        for movie in movies:
            if(num<=100):
                movie=movie.strip()
                print("%d\t%s" % (num,movie))
            num+=1

        while(1):

            movie_choice=input("\nenter your choice: ")
            flag=0
            if movie_choice.isnumeric() and int(movie_choice)>=1 and int(movie_choice)<=100:
                flag=1
                break
            elif movie_choice.isnumeric() and int(movie_choice)==0 :
                flag=0
                break
            else:
                print("please choose correct option!")

        movie_name=""
        url=None

        if flag==1:
            #if user selects one of the 100 movies from the  list

            print("\ngetting url and downloading...")
            x=0
            movie_choice=int(movie_choice)-1
            for line in source_code[genres[int(choice)]].split('\n'):

                if x==1:
                    title=line.split('</a>')[0]
                    if title==movies[int(movie_choice)]:
                        movie_name=title
                        break
                    x=0

                if 'class="unstyled articleLink">' in line:
                    url=line.split('"')[1]
                    x=1

            queries(movie_name,url,genre)
        
        else:
            print("Invalid choice!") 
            print("closing...")  

    else:
        print("closing...")  
        print("\nThank you!") 

'''
This function takes movie name and url and download that HTML page in current directory and then call 'parsing" function
to parse that page and extract required fields,then give options to user and according to choice of user it show results 
or call some functions(again itself or function from task2.py)
'''

def queries(movie_name,url,genre):

    url="https://www.rottentomatoes.com"+url
    #print(url)
    response = urllib.request.urlopen(url)
    webContent = response.read()
    movie_name=movie_name.strip()
    filename=movie_name+".html"
    myfile = open(filename, 'wb')
    print("\nRequested HTML page has been downloaded with the name \""+filename+"\" in current directory!")
    myfile.write(webContent)
    myfile.close

    #calling function to parse downloaded html file
    parsing(filename)
    
    #list of queries that user can ask
    query=['Movie Name','Director','Writers','Producer','Original Language','Cast & Charachter','Storyline','Box Office Collection','Runtime','YOU MIGHT ALSO LIKE','WHERE TO WATCH']

    if extracted_fields['Genre']!='Not Available!' and genre=='Not Available!':
        genre=extracted_fields['Genre']

    
    while(True):
        #listing queries before user
        print("\nFollowing queries you may ask, to ask query enter corresponding digit mentioned before option:")
        num=1
        for choice in query:
            print("%d\t%s" % (num,choice))
            num+=1

        choice=input("\nenter a digit to choose query:")

        #if user selects 'Director' or 'WHERE TO WATCH'
        if choice=='2' or choice=='11':
            if not extracted_fields[query[int(choice)-1]]:
                print("Data Unavailable!")                      
            else:
                for name in extracted_fields[query[int(choice)-1]]:
                    print(name)

        #if user selects 'Cast and Charachter'
        elif choice=='6' :
            if not extracted_fields[query[int(choice)-1]]:
                print("Data Unavailable!")                    
            else:
                x=1
                for name in extracted_fields[query[int(choice)-1]]:
                    print(x,name)
                    x+=1
    
                #showing list of cast and charachter
                print("\n choose option from the above list by entering corresponding number(1-{}),enter 0 to move to previous menu:".format(x-1))
                val=input("\n enter your choice:")

                if val.isnumeric() and int(val)>=1 and int(val)<x:
    
                    #if valid option is selected

                    if cast_and_pagelink[extracted_fields[query[int(choice)-1]][int(val)-1]]=='#':
                        print("\nURL is not available for page of this celebrity")
                        continue

                    url="https://www.rottentomatoes.com"+cast_and_pagelink[extracted_fields[query[int(choice)-1]][int(val)-1]]
                    #print(url)
                    print("\nDownloading...")
                    response = urllib.request.urlopen(url)
                    webContent = response.read()
                    celebrity_name=extracted_fields[query[int(choice)-1]][int(val)-1].split('as')
                    celebrity_name=celebrity_name[0].strip()
                    filename=celebrity_name+".html"
                    myfile = open(filename, 'wb')
                    print("\nRequested HTML page has been downloaded with the name \""+filename+"\" in current directory!")
                    myfile.write(webContent)
                    myfile.close

                    task2.parse_celebrity_page(filename)

                    c_query=['Highest Rated Film','Lowest Rated Film','Birthday','His/Her Other Movies']
                    
                    while(True):
                        #listing queries which can be asked about celebrity page
                        print("\nFollowing queries you may ask, to ask query enter corresponding digit mentioned before option,enter any other key to go to previous menu:")
                        num=1
                        print("%s\t%s" % ("\n0","Go to previous menu"))
                        for choice in c_query:
                            print("%d\t%s" % (num,choice))
                            num+=1

                        received=input("\nenter a digit to choose query:")

                        #if user selects 'Highest Rated Film'
                        if received=='1':
                            if len(task2.profile_info['Highest-Lowest Film'])>=1:
                                print(task2.profile_info['Highest-Lowest Film'][0])
                            else:
                                print("Not Available!")

                        #if user selects 'Lowest Rated Film'
                        elif received=='2':
                            if len(task2.profile_info['Highest-Lowest Film'])>=2:
                                print(task2.profile_info['Highest-Lowest Film'][1])
                            else:
                                print("Not Available!")

                        #if user selects 'Birthday'
                        elif received=='3':
                            if task2.profile_info['Birthday']!='#':
                                print(task2.profile_info['Birthday'])
                            else:
                                print("Not Available!")

                        #if user selects 'His/Her Movies'
                        elif received=='4':
                
                            filter_year=input("\nenter year(in \'yyyy\' format) to filter movie list(movies of that or after that year will be shown): ")
                    
                            if filter_year.isnumeric():
                                filter_year=int(filter_year)
                                flag=1
                                print("Year","  ","Movie")
                                for movie,year in task2.movie_with_year.items():
                                    if year>=filter_year:
                                        print(year,"    ",movie)
                                        flag=0

                                if flag:
                                    print("No movie found of this year(or afer that year)")
                            else:
                                print("Invalid input!,please enter numeric values only")
                        else:
                            print("\nWrong choice..going to previous menu!")
                            break
                else:
                    print("\nWrong choice..going to previous menu!")

        #if user selects 'Storyline'
        elif choice=='7':
            if extracted_fields[query[int(choice)-1]]=='#':
                print("Data Unavailable!")
            else:
                print(extracted_fields[query[int(choice)-1]])

        #if user selects 'Movie Name' or 'Writer' or 'Producer' or 'Original Language' or 'Box Office Collection' or 'Runtime'
        elif choice=='1' or choice=='3' or choice=='4' or choice=='5' or choice=='8' or choice=='9' :
            if extracted_fields[query[int(choice)-1]]=='#':
                print("Data Unavailable!")
            else:
                names=extracted_fields[query[int(choice)-1]].split(',')
                for name in names:
                    print(name)

        #if user selects 'YOU MIGHT ALSO LIKE'
        elif choice=='10':

            #showing list of movies 
            print("\nChoose one of the recommended movies(1-5),to choose option enter corresponding number mentioned before movie name:")
            val=0
            print("%d\t%s" % (-1,"Go to previous menu"))   
            print("%d\t%s" % (0,"EXIT"))

            for num,movie in recommended_movies.items():
                print(num+1,'   ',movie)
                val=num+1

            while(1):

                option=input("\nenter your choice: ")
                flag=0
                flag=0
                if option.isnumeric() and int(option)>=1 and int(option)<=val:
                    flag=1
                    break
                elif option.isnumeric() and int(option)==0 :
                    flag=0
                    break
                elif option=='-1' :
                    flag=-1
                    break
                else:
                    print("please choose correct option!")


            if flag==1 :
                #if correct option chosen then again recursively calling this function with for chosen movie
                print("\ngetting url and downloading...")
                queries(recommended_movies[int(option)-1],urls[int(option)-1],extracted_fields['Genre'])
                return
            elif flag==-1:
                pass
            else:
                print("\nclosing...!")
                print("\nThank you!")
                break

        else:
            print("invalid choice!")

        choice = input("\nEnter \"y\" (without quotes) to exit,any other key to continue: ")
            
        if choice == 'y':
            print("\nThank you!")
            break
            


if __name__ == '__main__':
	main()