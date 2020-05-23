#  [Anoroc](https:%5C%5Canoroc.herokuapp.com) COVID-19 Explorer :fire:
* Just my simple web Dash application made with Python cuz I wanted to learn Python developing :)
* Pretty much what I have right now is on ```anoroc.herokuapp.com```
***hmm I'm not planning to work on this anymore but to focus on other stuffs like CP and AI, new features will come in hopefully once in a while***
## Version 1.0 Released (5/23): :clap:

 ##### After them heavy days working on this, here comes the Jumbo Lumbo patch   :boom:
 #### - Changes from v0.3:
 - World View   :earth_africa: now is available thanks to **Plotly**   :goat:
 - Redesigned web-interaction thanks to **Spectre CSS** framework by [Yan Zhu](https://github.com/picturepan2/spectre)
- Cleaned up codes and files 

Well there was version 0.5 also where I tried having PostgreSQL to live-update with the data sources (it's still there in older commits), but then found out it makes web-interaction slower by a lot(heroku traffics?) So I'll stick with csv files (less than 1MB total) 
*So pretty much just world view and web designs, SQL was working but it's a :snake: *


## Feature Details:
- [x] Updated data sourced from [covid19-api](covid19-api.org) with [John Hopkins CSSE](https://coronavirus.jhu.edu/map.html)
- [x] Support all countries (ISO-2 and ISO-3 combined)
- [x] Searchable bar to inspect the country you want
- [x] Total reports from **day one** and **daily** trend (updated daily)
- [x] Current status are the ones updated every 2 hours, above the charts
- [x] World View (updated daily)
- [x] Interactive country inspecting 
- [x] Flexible website design: Navigation, Tabs, Mobile responsive. 
##### *What to expect:* as said gonna be long...
- [ ] Inspect multiple countries at once.
- [ ] Infected, Recovered and Deceased rate for each country.
- [ ]  Entirely supports filtering and sorting as well as editing
- [ ]  Prediction model.
- [ ] ~~24/7 Live data.~~  *to reduce the site traffics and also due to Heroku's server issues, this will not be in anytime soon*



## Version 0.3 (05/18/20):  :older_man:(old)
* Data redone with live and updated data from JHU CSSE 
* Searchable bar with better names and country alpha-2 (ISO 3166)
* Country inspector now shows both total and daily trend
*ANOROC will check for JHU CSSE last update from the U.S. whether the data is ought to be retrieved, then retrieve. Still, it has to load a decent size JSON file so I'm looking for a request library that has nice caching.*
###### Happy quarantine!

