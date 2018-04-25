from flask import Flask, render_template, request
import json

w = json.load(open("worldl.json"))
for c in w:
	c['tld'] = c['tld'][1:]
letter= sorted(list(set([c['name'][0] for c in w])))
page_size = 20
app = Flask(__name__)

@app.route('/')
def mainPage():
	return render_template('index.html',
		w = w[0:page_size],
                page_number=0,
                page_size=page_size,
                letter = letter)

@app.route('/navigate/<b>')
def navigatePage(b):
	bn = int(b)
	return render_template('index.html',
		w = w[bn:bn+page_size],
		page_number = bn,
		page_size = page_size,
		letter = letter)
				
@app.route('/continent/<a>')
def continentPage(a):
	cl = [c for c in w if c['continent']==a]
	return render_template(
		'continent.html',
		length_of_cl = len(cl),
		cl = cl,
		a = a,)

@app.route('/alphacontinent/<a>')
def alphacontinentPage(a):
	cl = [c for c in w if c['name'][0]==a]
	return render_template(
		'alphacontinent.html',
		length_of_cl = len(cl),
		cl = cl,
		a = a,letter=letter
		)

@app.route('/country/<i>')
def countryPage(i):
	return render_template(
		'country.html',
		c = w[int(i)])

@app.route('/countryByName/<n>')
def countryByNamePage(n):
	c = None
	for x in w:
		if x['name'] == n:
			c = x
	return render_template(
		'country.html',
		c = c)

@app.route('/editCountryByName/<n>')
def editCountryByNamePage(n):
	c = None
	for x in w:
		if x['name'] == n:
			c = x
	return render_template(
		'countryedit.html',
		c = c)

@app.route('/updateCountryByName')
def updateCountryByNamePage(	):
	n = request.args.get('name')
	c = None
	for x in w:
		if x['name'] == n:
			c = x
	c['capital'] = request.args.get('capital')
	c['continent'] = request.args.get('continent')
	c['population']  = int(request.args.get('population'))
	c['area'] = int(request.args.get('area'))
	c['gdp']  = float(request.args.get('gdp'))
	c['tld']  = request.args.get('tld')
	return render_template(
		'country.html',
		c = c) 

@app.route('/createCountry')
def createPage(	):
	return render_template(
		'createcountry.html',
		c = c) 

@app.route('/newCountryByName')
def newCountryByNamePage(	):
	c =  {}
	c['name']= request.args.get('name')
	c['capital'] = request.args.get('capital')
	c['continent'] = request.args.get('continent')
	c['population'] = int(request.args.get('population'))
	c['area'] = int(request.args.get('area'))
	c['gdp']  = float(request.args.get('gdp'))
	c['tld']  = request.args.get('tld')
	w.append(c)
	w.sort(key = lambda c: c['name'])
	return render_template(
		'country.html',
		c = c)
	
@app.route('/delete/<n>')
def deleteCountry(n):
        i = 0
        for c in w:
                if c['name'] == n:
                        break
                i = i+1
        del w[i]
        return render_template('index.html',
		w = w[0:page_size],
		page_number = 0,
		page_size = page_size,
		letter = letter
		)
		
if __name__ == '__main__':
	app.run( debug=True)
