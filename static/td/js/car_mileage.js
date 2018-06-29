var svg = d3.select("svg"),
    margin = {top: 50, right: 20, bottom: 30, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;

var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
    y = d3.scaleLinear().rangeRound([height, 0]);

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

x.domain(mileage_data.map(function(d){return d.month;}));
y.domain([0,d3.max(mileage_data, function(d){return d.diff;})]);

g.append('g')
    .attr('class', 'axis axis--x')
    .attr('transform', 'translate(0,'+height+')')
    .call(d3.axisBottom(x));

g.append('g')
    .attr('class', 'axis axis--y')
    .call(d3.axisLeft(y).ticks(10));

g.selectAll('.bar').data(mileage_data).enter().append('rect')
    .attr('class', 'mileage-rect')
    .attr('x', function(d){return x(d.month);})
    .attr('y', function(d){return y(d.diff);})
    .attr('width', x.bandwidth())
    .attr('height', function(d){return height-y(d.diff);});

g.selectAll('.bar').data(mileage_data).enter().append('text')
    .attr('class', 'mileage-comment')
    .attr('x', function(d){return x(d.month)+x.bandwidth()/2;})
    .attr('y', function(d){return y(d.diff);})
    .attr('dy', '-5')
    .text(function(d){
        if (d.value != null) {
            return d.value+' км';
        } else {
            return null;
        }
    });

g.selectAll('.bar').data(mileage_data).enter().append('text')
    .attr('class', 'mileage-text')
    .attr('x', function(d){return x(d.month)+x.bandwidth()/2;})
    .attr('y', function(d){return y(d.diff);})
    .attr('dy', '-20')
    .text(function(d){
        if (d.diff != null) {
            return d.diff+' км';
        } else {
            return null;
        }
    });

g.append('line')
    .attr('class', 'limit-line')
    .attr('x1', 0)
    .attr('x2', width)
    .attr('y1', y(1000)+0.5)
    .attr('y2', y(1000)+0.5);

d3.selectAll('.mileage-comment')
  .on('click', function (d, i) {
      document.location.href = d.link;
  });