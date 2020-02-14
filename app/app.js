const express = require("express");
const bodyParser = require("body-parser");
const googleTrends = require('google-trends-api');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));

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

//app.get('/volatilitypred/extractdata/:trendWord', (req, res, next) => {
app.get('/volatilitypred/extractdata', (req, res, next) => {

  const startDate = new Date();
  //startDate.setHours(startDate.getHours() - 2);
  startDate.setDate(startDate.getDay() - 2);

  const optionsObject = {
    keyword: 'another',//req.params.trendWord,//'ibex35',
    property: 'web search',
    //resolution: 'COUNTRY',
    startTime: startDate,
    //endTime:
    //granularTimeResolution: true
  }
  googleTrends.interestOverTime(optionsObject)
  .then(function(results){
    results = JSON.parse(results).default.timelineData.filter(r => r.hasData == "true" );
    res.status(201).json({
      stockdata : null,
      gtrendsdata : results
    });
  })
  .catch(function(err){
    console.error('Oh no there was an error', err);
  });
});

module.exports = app;
