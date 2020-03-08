const express = require("express");
const bodyParser = require("body-parser");
const googleTrends = require('google-trends-api');
const yahooFinance = require('yahoo-finance');

const processDataService = require('./processDataService');
// const StatisticData = require('./models/StatisticData');
const utils = require('./utils/utils');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));

const startDate = new Date('2019-12-28');
const endDate = new Date('2019-12-31');

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

app.get('/volatilitypred/extractData/:trendWord', (req, res, next) => {

  const keyword = req.params.trendWord;
  const optionsTrend = {
    keyword: keyword,
    property: 'news',
    //resolution: 'COUNTRY',
    startTime: startDate,
    endTime: endDate
  }

  const optionsFinance = {
    symbol: keyword,
    from: startDate,
    to: endDate
  }

  let trendData;
  let financeData;
  extractGoogletrendsData(optionsTrend, function(returnValue) {
    trendData = returnValue;
  });

  extractFinanceData(optionsFinance, function(returnValue) {
    financeData = returnValue;
  });
  setTimeout(() => {
    console.log(trendData);
    res.status(201).json({trendData,financeData});
  }, 900);

  //res.status(201).json(trendData,financeData);
});

function extractGoogletrendsData(optionsObject, callback){
  googleTrends.interestOverTime(optionsObject)
  .then(function(results){
    //results = JSON.parse(results).default.timelineData.filter(r => r.hasData == "true" );
    results = JSON.parse(results).default.timelineData;
    results.forEach(function(result) {
      result.time = result.time
      result.formattedTime = utils.formatDate(result.formattedTime);
      result.formattedAxisTime = result.formattedAxisTime;
      result.value = result.value[0];
      result.formattedValue = result.formattedValue;
      result.symbol= optionsObject.keyword;
    });
    const statisticData = processDataService.generateStatisticData(results, 'value');
    const binarySeries = Object.fromEntries(processDataService.generateBinarySeries(results,
      'formattedTime', 'value', statisticData.meanPlusSigma, statisticData.meanMinusSigma));

    callback({
      gtrendsdata : results,
      statisticData: statisticData,
      binarySeries: binarySeries
    });

  })
  .catch(function(err){
    console.error('Oh no there was an error', err);
  });

}
app.get('/volatilitypred/extractFinance/:stock', (req, res, next) => {

  const optionsObject = {
    symbol: req.params.stock,
    from: startDate,
    to: endDate
  }

  yahooFinance.historical(optionsObject)
    .then(function(results){

      results.forEach(function(result) {
        result.date = utils.formatDate(result.date);
      });
      const statisticData = processDataService.generateStatisticData(results, 'open');
      const binarySeries = Object.fromEntries(processDataService.generateBinarySeries(results,
      'date', 'open', statisticData.meanPlusSigma, statisticData.meanMinusSigma));

      res.status(201).json({
        stockdata: results.reverse(),
        statisticData: statisticData,
        binarySeries: binarySeries
      });
  });

});

function extractFinanceData(optionsObject, callback){
  yahooFinance.historical(optionsObject)
    .then(function(results){

      results.forEach(function(result) {
        result.date = utils.formatDate(result.date);
      });

      const statisticData = processDataService.generateStatisticData(results, 'open');
      const binarySeries = Object.fromEntries(processDataService.generateBinarySeries(results,
      'date', 'open', statisticData.meanPlusSigma, statisticData.meanMinusSigma));

      callback({
        stockdata: results.reverse(),
        statisticData: statisticData,
        binarySeries: binarySeries
      });
  });
}

app.get('/volatilitypred/extractTrends/:trendWord', (req, res, next) => {

  const keyword = req.params.trendWord;
  const optionsObject = {
    keyword: keyword,
    property: 'news',
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
      result.formattedTime = utils.formatDate(result.formattedTime);
      result.formattedAxisTime = result.formattedAxisTime;
      result.value = result.value[0];
      result.formattedValue = result.formattedValue;
      result.symbol= keyword;
    });

    const statisticData = processDataService.generateStatisticData(results, 'value');
    const binarySeries = Object.fromEntries(processDataService.generateBinarySeries(results,
      'formattedTime', 'value', statisticData.meanPlusSigma, statisticData.meanMinusSigma));

    res.status(201).json({
      gtrendsdata : results,
      statisticData: statisticData,
      binarySeries: binarySeries
    });
  })
  .catch(function(err){
    console.error('Oh no there was an error', err);
  });

});

module.exports = app;
