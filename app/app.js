const express = require("express");
const bodyParser = require("body-parser");
const googleTrends = require('google-trends-api');
const yahooFinance = require('yahoo-finance');

const ss = require('simple-statistics')

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));

//const startDate = new Date('2010-12-11');
//const endDate = new Date('2019-12-31');

/*Access to XMLHttpRequest at 'http://localhost:3000/api/ibex35volatilitypred' from origin 'http://localhost:8080' has
been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.*/
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept"
  );
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET, POST, PATCH, DELETE, OPTIONS"
  );
  next();
});

app.get('/volatilitypred/extractTrends/:trendWord/:startDate/:endDate', (req, res, next) => {

  const keyword = req.params.trendWord;
  const startDate = new Date(req.params.startDate);
  const endDate = new Date(req.params.endDate);

  const optionsObject = {
    keyword: keyword,
    //property: 'news',
    //resolution: 'COUNTRY',
    startTime: startDate,
    endTime: endDate
  }
  googleTrends.interestOverTime(optionsObject)
  .then(function(results){
    //results = JSON.parse(results).default.timelineData.filter(r => r.hasData == "true" );
    results = JSON.parse(results).default.timelineData;
    results.forEach(function(result) {
      result.time = result.time
      result.value = result.value[0];
    });

    res.status(201).json({
      gtrendsdata : results
    });
  })
  .catch(function(err){
    console.error('Oh no there was an error', err);
  });
});

app.get('/volatilitypred/extractFinance/:stock/:startDate/:endDate', (req, res, next) => {

  const startDate = new Date(req.params.startDate);
  const endDate = new Date(req.params.endDate);

  const optionsObject = {
    symbol: req.params.stock,
    from: startDate,
    to: endDate
  }

  yahooFinance.historical(optionsObject)
    .then(function(results){
      res.status(201).json({
        stockdata: results.reverse()
      });
  });


});

module.exports = app;
