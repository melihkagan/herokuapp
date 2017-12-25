
#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################

from bottle import route, run, default_app, debug, get, request
import copy
from csv import reader
contents = []
input_file = open("database.csv","r")
for row in reader(input_file):
    contents = contents + [row]

welcome = """
    <h1>Welcome Sinop Population Database by District</h1>
    <p>All data is shown below. Use menu to manipulate data.</p>
    <br>
"""

searchform = """
<form action="/search" method="get">
  Search for district:
  <input name="dis" type="text">
  <input type="submit">
</form>
"""
filterform = """
<form action="/filterpage" method="get">
        <fieldset>
            <legend>Filter Data by:</legend>
            <p style="font-size: 20;margin-bottom: 4px;">District:</p><br>
            <input type="checkbox" name="Ayancik" value="1">Ayancık
            <input type="checkbox" name="Boyabat" value="1">Boyabat
            <input type="checkbox" name="Dikmen" value="1">Dikmen
            <input type="checkbox" name="Duragan" value="1">Durağan
            <input type="checkbox" name="Erfelek" value="1">Erfelek
            <input type="checkbox" name="Gerze" value="1">Gerze
            <input type="checkbox" name="Merkez" value="1">Merkez
            <input type="checkbox" name="Sarayduzu" value="1">Saraydüzü
            <input type="checkbox" name="Turkeli" value="1">Türkeli<br>
            <br>
            <p style="float: left;font-size: 20;">Type:</p>
            <div style="float: left; margin-right: 80px; margin-left: 20px;">
            <select name="types" size="4" multiple style="width: 90px;" >
                <option value="Total">Total</option>
                <option value="Man">Man</option>
                <option value="Woman">Woman</option>
                <option value="Town">Town</option>
                <option value="Village">Village</option>
            </select></div>
            <p style="float: left;font-size: 20">Year:</p>
            <div style="float: left; margin-left: 20px; margin-right: 70px">
            <input type="radio" name="years" value="1111111"> All years<br>
            <input type="radio" name="years" value="1110000"> 2015-2013<br>
            <input type="radio" name="years" value="1010101"> Only odd years<br>
            </div>
            <input type="submit" value="Filter" style="float: none">
         </fieldset>
</form>
"""
def showstat(liste):
    stats = """
        <p> Here is some detail: </p>
        <p>Population rate between 2015-2014 (%%) : %s </p>
        <p> Man in total (%%) : %s </p>
        <p> Woman in total (%%) : %s </p>
        <p> Live in town  (%%) : %s </p>
        <p> Live in village (%%) : %s </p>
    """ % ( liste[0],liste[1],liste[2],liste[3],liste[4] )
    return stats

def htmlify(title,text):
    page = """
        <!doctype html>
        <html lang="en">
            <head>
                <meta charset="utf-8" />
                <title>%s</title>
                <style>
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                        }
                th, td {
                        padding: 5px;
                        text-align: left;
                }
                div.con{
                    background-color: transparent;
                    margin-left: 10px;
                    }
                body {
                    background-color: rgb(180, 211, 171);
                    }
                nav{
                    background-color: rgb(48,48,68);
                    overflow: hidden;
                    width: 100%%;
                    margin-top: 0px;
                    top: 0px;
                    left: 0px;
                    }
                nav a {
                    background-color: rgb(48,48,68);
                    float: left;
                    display: block;
                    color: rgb(79,150,67);
                    text-align: center;
                    padding: 14px 16px;
                    text-decoration: none;
                    }
                nav a:hover {
                    background-color: rgb(77,119,181);
                    color: black;
                }
                nav a:active {
                    background-color: rgb(153,180,200);
                    color: black;
                </style>
            </head>
            <body>
            <nav>
		<a href="/">Home</a>		
		<a href="/filterpage">Filter Data</a>
		<a href="/search">Search District</a>
            </nav>
            
            <div class="con">
            <br><br>
            %s
            </div>
            </body>
        </html>

    """ % (title,text)
    return page

def showalldata(data):
    table1 = "<table>"
    k = 0
    td = "<td>{}</td>"
    tdx = """<td colspan="8" style="text-align: center" >{}</td>"""
    while k < len(data) :
            table1 = table1 + "<tr>"
            m = 0
            while True :
                try:
                    if str(data[k][1]) == '' :
                        table1 = table1 + tdx.format(data[k][m])
                        m = m + 1
                        break
                    else:
                        table1 = table1 + td.format(data[k][m])
                        m = m + 1
                except IndexError :
                    break
            k = k + 1
            table1 = table1 + "</tr>"
            
    table1 = table1 + "</table>"
    return table1

def filterbydis(key,key2,table):
    ndatab = []
    ndatab = ndatab + [table[0]]
    i=1
    while i < len(table):
        if key[table[i][0]] == 1:
            ndatab = ndatab + [table[i]]
            for k in range(1,6):
                if key2[table[i+k][0]] == 1:
                    ndatab = ndatab + [table[i+k]]   
            i=i+6
        elif key[table[i][0]] == 0:
            i=i+6
        else:
            ndatab[0][0]="Error"
            break
    return ndatab

def filterbytype(key,table):
    ndatab = []
    ndatab = ndatab + [table[0]]
    i=1
    while i < len(table):
        if str(table[i][1]) == '' :
            ndatab = ndatab + [table[i]]
        elif key[table[i][0]] == 1 :
            ndatab = ndatab + [table[i]]
        i=i+1
    return ndatab

def filterbyyear(key,table):
    ndatab = []
    liste = list(key.keys())
    z= 0
    while z< len(table):
        m=1
        row = [] 
        row = row + [str(table[z][0])]
        for name in liste:
            if key[name] == 1 :
                row = row + [str(table[z][m])]
            m = m + 1
        ndatab = ndatab + [row]
        z = z + 1
    return ndatab

def finddis(disname,table):
    disname = disname.lower()
    p=0
    dis = []
    dis= dis + [table[0]]
    while p < len(table):
        if disname.capitalize() == str(table[p][0]):
            k=0
            while k<6 :
                dis = dis + [table[p+k]]
                k=k+1
        p= p + 1
    return dis

def disstat(dis):
    poprate = str( ((int(dis[2][1])-int(dis[2][2]))/int(dis[2][2]))*100)
    man = str( (int(dis[3][1])/int(dis[2][1]))*100)
    woman = str( (int(dis[4][1])/int(dis[2][1]))*100)
    town = str( (int(dis[5][1])/int(dis[2][1]))*100)
    village = str( (int(dis[6][1])/int(dis[2][1]))*100)
    stat= [poprate,man,woman,town,village]
    return stat

key1 = {'Ayancik':0,'Boyabat':0,'Dikmen':0,'Duragan':0,'Erfelek':0,'Gerze':0,'Merkez':0,'Sarayduzu':0,'Turkeli': 0}
key2 = {'Total':0,'Man':0,'Woman':0,'Town':0,'Village':0}
key3 = {'2015':0,'2014':0,'2013':0,'2012':0,'2011':0,'2010':0,'2009':0}
disnlist = list(key1.keys())

def resetkey(akey):
    liste = list(akey.keys())
    for name in liste:
        akey[name] = 0
    return akey

def nkey2(alist):
    keym = resetkey(key2.copy())
    for name in alist:
        keym[name] = 1
    return keym


def filterpage():
    skey1 = key1.copy()
    diclist1 = list(skey1.keys())
    for name in diclist1:
        if request.GET.get(name) != None :
            skey1[name]= int(request.GET.get(name))
        else :
            skey1[name] = 0

    typelist = request.GET.getall("types")
    skey2= nkey2(typelist)

    yearfil = list(str(request.GET.get("years")))
    skey3 = key3.copy()
    diclist2 = list(skey3.keys())
    if len(yearfil) > 5 :
        a=0
        for name in diclist2:
            skey3[name] = int(yearfil[a])
            a = a + 1
    
    return htmlify("Filter Data",filterform + showalldata(filterbydis(skey1,skey2,filterbyyear(skey3,contents))))

def search():
    disname=request.GET.get("dis")
    if disname == None :
        return htmlify("Search",searchform)
    elif (str(disname).lower()).capitalize() in disnlist :
        return htmlify(str(disname).lower(),showstat(disstat(finddis(str(disname),contents)))+"<br>"+showalldata(finddis(str(disname),contents)))
    else :
        return htmlify("Error","<h3>Try again:</h3>"+searchform)
    

def index():
    
    return htmlify("Sinop Population Database",welcome+showalldata(contents))


route('/search', 'GET' , search)
route('/filterpage', 'GET', filterpage)
route('/', 'GET', index)


#####################################################################
### Don't alter the below code.
### It allows this website to be hosted on Heroku
### OR run on your computer.
#####################################################################

# This line makes bottle give nicer error messages
debug(True)
# This line is necessary for running on Heroku
app = default_app()
# The below code is necessary for running this bottle app standalone on your computer.
if __name__ == "__main__":
  run()

