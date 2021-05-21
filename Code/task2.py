'''
Name:Yogesh Porwal
Roll no : 20CS60R52
Email-id:yogeshporwal@kgpian.iitkgp.ac.in
Program name: task2.py
'''

#importing packages
import os
import ply.lex as lex
import ply.yacc as yacc
import unicodedata 
import urllib.request, urllib.error, urllib.parse

'''
This funtion replaces some code for charachter with charachter itself e.g. '&#39;' replaces with '(apostrophe) 
and it also change charachters of some other accents(like latin,french,italic) to normal accent
'''
def strip_accents(text):
    text = text.replace('&#39;', '\'')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '\"')
    text = text.replace('&apos;', '\'')
    
    return ''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')

#these dictionaries will contain values of extracted fields for celebrity page
profile_info={'Highest-Lowest Film':[],'Birthday':'#'}
movie_with_year={}

#tokens list
tokens = (
    'L_HIGH_LOW','L_BIRTH','P_CLOSE','WSPACE','NAME','L_YEAR','R_LINK','D_TITLE'
	)

#token(s) defination

#used to extract highest and lowest rated movies
def t_L_HIGH_LOW(t):
    r'<a\ class=\"celebrity-bio__link\"\ href=\"[A-Za-z0-9_.\~\-/]+\">\s*'
    return t

#used to extract birthday
def t_L_BIRTH(t):
    r'<p\ class=\"celebrity-bio__item\"\ data-qa=\"celebrity-bio-bday\">\s*Birthday:\s*'
    return t

#used to extract birthday
def t_P_CLOSE(t):
    r'\s*</p>'
    return t

#used to extract highest and lowest rated movies
def t_R_LINK(t):
    r'\s*</a>[,]*\s*'
    return t

#used to extract movies and year
def t_D_TITLE(t):
    r'data-title=\"\s*'
    return t

#used to extract movies and year
def t_L_YEAR(t):
    r'\s*\s.*\s*data-year=\"\s*'
    return t

#used to extract name(s)
def t_NAME(t):
	r'[a-zA-Z0-9.$\(\)\,!\&\#\@;%\'\"?:_-]+'
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
	'''start : high_low
             | birthday
             | movies
    '''

	pass

#for extracting highest and lowest rated movie-name
def p_highest_and_lowest_rated(t):
    'high_low : L_HIGH_LOW names R_LINK'
    profile_info['Highest-Lowest Film'].append(t[2])

#for extracting Birthday
def p_birthday(t):
    'birthday : L_BIRTH names P_CLOSE'
    profile_info['Birthday']=t[2]

#for extracting movies of given celibrity with year
def p_movies(t):
    'movies : D_TITLE names L_YEAR NAME '

    t[2]=t[2][:-1]  
    t[4]=t[4][:-1]
    if t[4].isnumeric():
        t[4]=int(t[4])
    movie_with_year[t[2]]=t[4]

#recursive rules for extracting name(s)
def p_names_single(t):
    'names : NAME '
    t[0] = t[1]

def p_names_multi(t):
    'names : NAME names'
    t[0] = t[1] + ' ' + t[2]
	
def p_names_ws_names(t):
    'names : NAME wspaces names'
    t[0] = t[1] + t[2] + t[3]

def p_wspaces(t):
	'''wspaces : WSPACE
			   | WSPACE wspaces'''
	t[0] = ' '

#error handling 
def p_error(t):
	pass

'''
This function will parse celebrity page which is stored in current directory and whose file name is passed as argument,
it will extract four required fields(Highest and Lowest rated film,birthday and movies) and store them 
'''
def parse_celebrity_page(filename):

    #initializing
    global profile_info
    profile_info={'Highest-Lowest Film':[],'Birthday':'#'}
    global movie_with_year
    movie_with_year={}
    
    #building parser and starting parsing

    lexer = lex.lex()
    parser = yacc.yacc()
    file_ptr=open(filename)
    txt=file_ptr.read()
    txt=strip_accents(txt)
    
    print("\nparsing started for celebrity page...")
    parser.parse(txt)
    print("\nparsing done...required fields extracted and stored!")
