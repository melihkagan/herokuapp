
#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################

from bottle import route, run, default_app, debug
import copy
from csv import reader
contents = []
input_file = open("database.csv","r")
for row in reader(input_file):
    contents = contents + [row]

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
</style>
            </head>
            <body>
            %s
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


key1 = {'Ayancik':0,'Boyabat':0,'Dikmen':1,'Duragan':1,'Erfelek':1,'Gerze':0,'Merkez':1,'Sarayduzu':0,'Turkeli': 1}
key2 = {'Total':1,'Man':1,'Woman':0,'Town':1,'Village':0}
print( key1['Duragan'] )
abcc = 'Boyabat'
print( key1[abcc] )
def index():
    return htmlify("My lovely website",
                   showalldata(contents))

def aabb():
    return htmlify("Myy lovely website",
                   showalldata(filterbydis(key1,key2,contents)))



route('/', 'GET', index)
route('/aabb', 'GET', aabb)


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

