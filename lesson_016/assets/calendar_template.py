header = """
    <html>
      <head>
        <meta charset="utf-8">
      </head>
    
      <body>
"""
footer = """
    </body>
  </html>
"""
css = """

    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;500&display=swap');

      # @font-face {
      #   font-family: 'Weather Icons';
      #   src: url('assets/weathericons-regular-webfont.woff') format('woff'),
      #   url('assets/weathericons-regular-webfont.ttf') format('truetype');
      # }

      @font-face {
      font-family: 'Weather Icons'; 
      url('https://erikflowers.github.io/weather-icons/font/weathericons-regular-webfont.woff') format('woff'), 
      url('https://erikflowers.github.io/weather-icons/font/weathericons-regular-webfont.ttf') format('truetype'), 
      font-weight: normal;
      font-style: normal;
    }

      body {
        color: rgb(51, 51, 51);
        font-family: "Roboto Slab";
        width: 857px;
      }

      .wrapper {
        width: 857px;
      }

      table {
        border-collapse: collapse;
      }

      .month_name {
        font-size: 30;
        text-align: left;
        padding-left: 12;
        padding-bottom: 6;
      }
      th.city {
        font-size: 30;
        text-align: right;
         padding-right: 12;
        padding-bottom: 6;
      }

      tr:nth-child(2) {
        line-height: 1.5;
        font-size: 20;
      }

      .noday {
        height: 142px;
        width: 120px;
      }

      .day {
        height: 142px;
        width: 120px;
        border: 1px solid rgb(51, 51, 51);
      }    

      .sat > .date,  .sun > .date, th.sat, th.sun { 
        color: #ff4949;
      }

      .sun.day, .sat.day { 
        border-color: #ff4949;
      }

      .fri {
        border-right-width: 0;
      }

      .fri + .noday {
        border-left: 1px solid rgb(51 51 51);
      }

      .date {
        margin-top: -10px;
        padding-right: 10px;
        font-size: 24px;
        line-height: 1.528;
        text-align: right;
      }

      .icon {
        padding-top: 10px;
        font-size: 34px;
        font-family: "Weather Icons";
        line-height: 0.809;
        text-align: center;
      }

      .descr {
        font-size: 14.667px;
        line-height: 2.5;
        text-align: center;
      }

      .temp {
        font-size: 20px;
        line-height: 1.2;
        text-align: center;
        left: 17.625px;
        top: 102.17px;
        z-index: 4;
      }

    </style>
    """

month_header = '<tr><th colspan="3" class="month_name">{month}</th>' \
               '<th colspan="4" class="city">{city}</th></tr>'

day = """
  <td class="{weekday} day">
    <div class="date">{day}</div>
    <div class="icon">{weather_icon}</div>
    <div class="descr">{descr}</div>
    <div class="temp">{temp_day}{temp_units}  {temp_night}{temp_units}</div>
  </td>
"""
