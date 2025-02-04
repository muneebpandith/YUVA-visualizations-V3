!/**
 * Highcharts Gantt JS v12.1.2 (2025-01-09)
 * @module highcharts/modules/static-scale
 * @requires highcharts
 *
 * StaticScale
 *
 * (c) 2016-2024 Torstein Honsi, Lars A. V. Cabrera
 *
 * License: www.highcharts.com/license
 */function(t,e){"object"==typeof exports&&"object"==typeof module?module.exports=e(require("highcharts")):"function"==typeof define&&define.amd?define("highcharts/modules/static-scale",[["highcharts/highcharts"]],e):"object"==typeof exports?exports["highcharts/modules/static-scale"]=e(require("highcharts")):t.Highcharts=e(t.Highcharts)}(this,function(t){return function(){"use strict";var e={944:function(e){e.exports=t}},i={};function r(t){var a=i[t];if(void 0!==a)return a.exports;var o=i[t]={exports:{}};return e[t](o,o.exports,r),o.exports}r.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return r.d(e,{a:e}),e},r.d=function(t,e){for(var i in e)r.o(e,i)&&!r.o(t,i)&&Object.defineProperty(t,i,{enumerable:!0,get:e[i]})},r.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)};var a={};r.d(a,{default:function(){return p}});var o=r(944),n=r.n(o),s=n().addEvent,h=n().defined,c=n().isNumber,u=n().pick;function l(){var t=this.chart.options.chart;!this.horiz&&c(this.options.staticScale)&&(!t.height||t.scrollablePlotArea&&t.scrollablePlotArea.minHeight)&&(this.staticScale=this.options.staticScale)}function d(){if("adjustHeight"!==this.redrawTrigger){for(var t=0,e=this.axes||[];t<e.length;t++)!function(t){var e=t.chart,i=!!e.initiatedScale&&e.options.animation,r=t.options.staticScale;if(t.staticScale&&h(t.min)){var a=u(t.brokenAxis&&t.brokenAxis.unitLength,t.max+t.tickInterval-t.min)*r,o=(a=Math.max(a,r))-e.plotHeight;!e.scrollablePixelsY&&Math.abs(o)>=1&&(e.plotHeight=a,e.redrawTrigger="adjustHeight",e.setSize(void 0,e.chartHeight+o,i)),t.series.forEach(function(t){var i=t.sharedClipKey&&e.sharedClips[t.sharedClipKey];i&&i.attr(e.inverted?{width:e.plotHeight}:{height:e.plotHeight})})}}(e[t]);this.initiatedScale=!0}this.redrawTrigger=null}var f=n();({compose:function(t,e){var i=e.prototype;i.adjustHeight||(s(t,"afterSetOptions",l),i.adjustHeight=d,s(e,"render",i.adjustHeight))}}).compose(f.Axis,f.Chart);var p=n();return a.default}()});