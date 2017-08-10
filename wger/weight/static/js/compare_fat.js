/*
 This file is part of wger Workout Manager.

 wger Workout Manager is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 wger Workout Manager is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 */
'use strict';

function modifyTimePeriod(data, pastNumberDays) {
  var filtered;
  var date;
  if (data.length) {
    if (pastNumberDays !== 'all') {
      date = new Date();
      date.setDate(date.getDate() - pastNumberDays);
      filtered = MG.clone(data).filter(function (value) {
        return value.date >= date;
      });
      return filtered;
    }
  }
  return data;
}

$(document).ready(function () {
  var username;
  var url;
  var chartParams;
  var weightChart;
  weightChart = {};
  chartParams = {
    title: 'Fat Intake (g)',
    animate_on_load: true,
    full_width: true,
    top: 10,
    left: 50,
    right: 20,
    show_secondary_x_label: true,
    xax_count: 10,
    target: '#fat_diagram',
    x_accessor: 'date',
    y_accessor: 'fat',
    min_y_from_data: true,
    colors: ['#CCCCFF', '#3465a4', 'blue', 'rgb(255,100,43)'],
  };

  username = $('#fat').data('currentUsername');
  url = '/weight/api/get_nutritional_data/' + username;
  d3.json(url, function (json) {
    var data = [];
    var legend = [];
    Object.keys(json).forEach(function(key,index) {
      data[index] = MG.convert.date(json[key], 'date');
      legend.push(key);
    });

    if (data.length) {
      weightChart.data = data;
      chartParams.data = data;
      chartParams.legend = legend;
      chartParams.legend_target = '#fat_legend';
      MG.data_graphic(chartParams);
    }
  });

  $('.modify-time-period-controls button').click(function () {
    var pastNumberDays = $(this).data('time_period');
    var data = modifyTimePeriod(weightChart.data, pastNumberDays);

    // change button state
    $(this).addClass('active').siblings().removeClass('active');
    if (data.length) {
      chartParams.data = data;
      MG.data_graphic(chartParams);
    }
  });
});
