//TODO Define an schema for the incoming data

const YFinanceData = function (date, open, high, low, close, symbol) {
  this.date = date;
  this.open = open;
  this.high = high;
  this.low = low;
  this.close = close;
  this.symbol = symbol;
};

module.exports = YFinanceData;
