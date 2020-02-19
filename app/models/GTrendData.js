//TODO Define an schema for the incoming data

const GTrendData = function (date, value, symbol) {
  this.date = date;
  this.value = value;
  this.symbol = symbol;
};

module.exports = GTrendData;
