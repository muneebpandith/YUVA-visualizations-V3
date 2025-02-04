!/**
 * Highstock JS v12.1.2 (2025-01-09)
 * @module highcharts/modules/heikinashi
 * @requires highcharts
 * @requires highcharts/modules/stock
 *
 * HeikinAshi series type for Highcharts Stock
 *
 * (c) 2010-2024 Karol Kolodziej
 *
 * License: www.highcharts.com/license
 */function(t,i){"object"==typeof exports&&"object"==typeof module?module.exports=i(require("highcharts"),require("highcharts").SeriesRegistry):"function"==typeof define&&define.amd?define("highcharts/modules/heikinashi",[["highcharts/highcharts"],["highcharts/highcharts","SeriesRegistry"]],i):"object"==typeof exports?exports["highcharts/modules/heikinashi"]=i(require("highcharts"),require("highcharts").SeriesRegistry):t.Highcharts=i(t.Highcharts,t.Highcharts.SeriesRegistry)}(this,function(t,i){return function(){"use strict";var e,r,o={512:function(t){t.exports=i},944:function(i){i.exports=t}},n={};function a(t){var i=n[t];if(void 0!==i)return i.exports;var e=n[t]={exports:{}};return o[t](e,e.exports,a),e.exports}a.n=function(t){var i=t&&t.__esModule?function(){return t.default}:function(){return t};return a.d(i,{a:i}),i},a.d=function(t,i){for(var e in i)a.o(i,e)&&!a.o(t,e)&&Object.defineProperty(t,e,{enumerable:!0,get:i[e]})},a.o=function(t,i){return Object.prototype.hasOwnProperty.call(t,i)};var s={};a.d(s,{default:function(){return S}});var h=a(944),p=a.n(h),u=a(512),c=a.n(u),f=(e=function(t,i){return(e=Object.setPrototypeOf||({__proto__:[]})instanceof Array&&function(t,i){t.__proto__=i}||function(t,i){for(var e in i)i.hasOwnProperty(e)&&(t[e]=i[e])})(t,i)},function(t,i){function r(){this.constructor=t}e(t,i),t.prototype=null===i?Object.create(i):(r.prototype=i.prototype,new r)}),l=c().seriesTypes,y=l.candlestick.prototype.pointClass;l.hlc.prototype.pointClass;var d=function(t){function i(){return null!==t&&t.apply(this,arguments)||this}return f(i,t),i}(y),g={dataGrouping:{groupAll:!0}},v=(r=function(t,i){return(r=Object.setPrototypeOf||({__proto__:[]})instanceof Array&&function(t,i){t.__proto__=i}||function(t,i){for(var e in i)Object.prototype.hasOwnProperty.call(i,e)&&(t[e]=i[e])})(t,i)},function(t,i){if("function"!=typeof i&&null!==i)throw TypeError("Class extends value "+String(i)+" is not a constructor or null");function e(){this.constructor=t}r(t,i),t.prototype=null===i?Object.create(i):(e.prototype=i.prototype,new e)}),k=p().composed,_=c().seriesTypes.candlestick,m=p().addEvent,D=p().merge,O=p().pushUnique;function b(){this.series.forEach(function(t){t.is("heikinashi")&&(t.heikiashiData.length=0,t.getHeikinashiData())})}function x(){for(var t=this.points,i=this.heikiashiData,e=this.cropStart||0,r=0;r<t.length;r++){var o=t[r],n=i[r+e];o.open=n[0],o.high=n[1],o.low=n[2],o.close=n[3]}}function P(){this.heikiashiData.length&&(this.heikiashiData.length=0)}var j=function(t){function i(){var i=null!==t&&t.apply(this,arguments)||this;return i.heikiashiData=[],i}return v(i,t),i.compose=function(t,e){_.compose(t),O(k,"HeikinAshi")&&(m(e,"postProcessData",b),m(i,"afterTranslate",x),m(i,"updatedData",P))},i.prototype.getHeikinashiData=function(){var t=this.allGroupedTable||this.dataTable,i=t.rowCount,e=this.heikiashiData;if(!e.length&&i){this.modifyFirstPointValue(t.getRow(0,this.pointArrayMap));for(var r=1;r<i;r++)this.modifyDataPoint(t.getRow(r,this.pointArrayMap),e[r-1])}this.heikiashiData=e},i.prototype.init=function(){t.prototype.init.apply(this,arguments),this.heikiashiData=[]},i.prototype.modifyFirstPointValue=function(t){var i=(t[0]+t[1]+t[2]+t[3])/4,e=(t[0]+t[3])/2;this.heikiashiData.push([i,t[1],t[2],e])},i.prototype.modifyDataPoint=function(t,i){var e=(i[0]+i[3])/2,r=(t[0]+t[1]+t[2]+t[3])/4,o=Math.max(t[1],r,e),n=Math.min(t[2],r,e);this.heikiashiData.push([e,o,n,r])},i.defaultOptions=D(_.defaultOptions,g),i}(_);j.prototype.pointClass=d,c().registerSeriesType("heikinashi",j);var w=p();j.compose(w.Series,w.Axis);var S=p();return s.default}()});