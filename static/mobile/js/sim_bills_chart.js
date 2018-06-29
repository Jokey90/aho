var locale = d3.timeFormatLocale({
  "dateTime": "%A, %e %B %Y г. %X",
  "date": "%d.%m.%Y",
  "time": "%H:%M:%S",
  "periods": ["AM", "PM"],
  "days": ["воскресенье", "понедельник", "вторник", "среда", "четверг", "пятница", "суббота"],
  "shortDays": ["вс", "пн", "вт", "ср", "чт", "пт", "сб"],
  "months": ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"],
  "shortMonths": ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]
});

var svg = d3.select("svg"),
    margin = {top: 50, right: 20, bottom: 20, left: 50},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;

var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
    y = d3.scaleLinear().rangeRound([height, 0]);

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var max_amount = d3.max(chart_data, function(d){return d.amount;});
var max_limit = d3.max(chart_data, function(d){return d.limit;});

var y_max = Math.max(max_amount, max_limit);

x.domain(chart_data.map(function(d){return d3.isoParse(d.date);}));
y.domain([0,y_max]);

g.append('g')
    .attr('class', 'axis axis--x')
    .attr('transform', 'translate(0,'+height+')')
    .call(d3.axisBottom(x).tickFormat(locale.format('%e %b %Y')));

g.append('g')
    .attr('class', 'axis axis--y')
    .call(d3.axisLeft(y).ticks(10));

g.selectAll('.bar').data(chart_data).enter().append('rect')
    .attr('class', 'amount-rect')
    .attr('x', function(d){return x(d3.isoParse(d.date));})
    .attr('y', function(d){return y(d.amount);})
    .attr('width', x.bandwidth())
    .attr('height', function(d){return height-y(d.amount);});


g.selectAll('.bar').data(chart_data).enter().append('text')
    .attr('class', 'amount-text')
    .attr('transform', function(d){
            return 'translate(' + (x(d3.isoParse(d.date)) + x.bandwidth() / 2 ) + ',' + (y(d.amount) - 5) + ')';
    })
    .text(function(d){return Math.round(d.amount);});

var line = d3.line()
    .x(function(d){return x(d3.isoParse(d.date));})
    .y(function(d){return y(d.limit);});

g.append('path')
    .attr('class', 'limit-line')
    .attr('d', line(chart_data))
    .attr('fill', 'none');