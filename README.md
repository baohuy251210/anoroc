*Update: currently in maintenance, stay tuned for the new design, new databases and new applications I'll try 
to have version 1.0 up this week :shipit: * 
#  Anoroc COVID-19 Monitor 
* Just my simple web Dash application made with Python cuz I wanted to learn Python developing :)
* Pretty much what I have right now is on ```anoroc.herokuapp.com```
## Features Summary:
- [x] Live updated Covid-19 monitor on [Anoroc](https:%5C%5Canoroc.herokuapp.com)
- [x] Data is sourced from [covid19-api](covid19-api.org) which is live with [John Hopkins CSSE](https://coronavirus.jhu.edu/map.html)
- [x] Support ~188 countries
- [x] Searchable bar to inspect the country you want
- [x] Total reports from **day one** and Daily reports model
- [x] Table with last updated reports
- [x] Materialized Design :) 
##### *What to expect:*
- [ ] Interactive options with country inspecting (Histogram, Scatter, Bar charts)
- [ ] Inspect multiple countries at once.
- [ ] Infected, Recovered and Deceased rate for each country.
- [ ]  Entire table supports filtering and sorting as well as editing
- [ ]  More flexible website design: Navigation, Tabs, Mobile responsive. 
- [ ]  Prediction model.
- [ ] 24/7 Live data. *Since it's running on a free Heroku server, the site will sleep after a ~2hrs without access or changes. Hence the new data is loaded every time someone wakes it up(e.g. with an access)*
## Version 0.3 (05/18/20):
* Data redone with live and updated data from JHU CSSE 
* Searchable bar with better names and country alpha-2 (ISO 3166)
* Country inspector now shows both total and daily trend
*ANOROC will check for JHU CSSE last update from the U.S. whether the data is ought to be retrieved, then retrieve. Still, it has to load a decent size JSON file so I'm looking for a request library that has nice caching.*
###### Happy quarantine!


