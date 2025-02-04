!/**
 * Highcharts JS v12.1.2 (2025-01-09)
 * @module highcharts/modules/color-axis
 * @requires highcharts
 *
 * ColorAxis module
 *
 * (c) 2012-2024 Pawel Potaczek
 *
 * License: www.highcharts.com/license
 */function(t,e){"object"==typeof exports&&"object"==typeof module?module.exports=e(require("highcharts"),require("highcharts").Axis,require("highcharts").Color,require("highcharts").LegendSymbol,require("highcharts").SeriesRegistry,require("highcharts").SVGElement,require("highcharts").SVGRenderer):"function"==typeof define&&define.amd?define("highcharts/modules/heatmap",[["highcharts/highcharts"],["highcharts/highcharts","Axis"],["highcharts/highcharts","Color"],["highcharts/highcharts","LegendSymbol"],["highcharts/highcharts","SeriesRegistry"],["highcharts/highcharts","SVGElement"],["highcharts/highcharts","SVGRenderer"]],e):"object"==typeof exports?exports["highcharts/modules/heatmap"]=e(require("highcharts"),require("highcharts").Axis,require("highcharts").Color,require("highcharts").LegendSymbol,require("highcharts").SeriesRegistry,require("highcharts").SVGElement,require("highcharts").SVGRenderer):t.Highcharts=e(t.Highcharts,t.Highcharts.Axis,t.Highcharts.Color,t.Highcharts.LegendSymbol,t.Highcharts.SeriesRegistry,t.Highcharts.SVGElement,t.Highcharts.SVGRenderer)}(this,function(t,e,i,r,o,s,a){return function(){"use strict";var n,l,h,c,p,d,u,f={532:function(t){t.exports=e},620:function(t){t.exports=i},500:function(t){t.exports=r},28:function(t){t.exports=s},540:function(t){t.exports=a},512:function(t){t.exports=o},944:function(e){e.exports=t}},g={};function y(t){var e=g[t];if(void 0!==e)return e.exports;var i=g[t]={exports:{}};return f[t](i,i.exports,y),i.exports}y.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return y.d(e,{a:e}),e},y.d=function(t,e){for(var i in e)y.o(e,i)&&!y.o(t,i)&&Object.defineProperty(t,i,{enumerable:!0,get:e[i]})},y.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)};var m={};y.d(m,{default:function(){return tD}});var v=y(944),x=y.n(v),b=y(532),C=y.n(b),A=y(620),w=y.n(A),M=w().parse,k=x().addEvent,L=x().extend,I=x().merge,O=x().pick,P=x().splat;!function(t){var e;function i(){var t=this,i=this.userOptions;this.colorAxis=[],i.colorAxis&&(i.colorAxis=P(i.colorAxis),i.colorAxis.map(function(i){return new e(t,i)}))}function r(t){var e,i,r=this,o=this.chart.colorAxis||[],s=function(e){var i=t.allItems.indexOf(e);-1!==i&&(r.destroyItem(t.allItems[i]),t.allItems.splice(i,1))},a=[];for(o.forEach(function(t){(e=t.options)&&e.showInLegend&&(e.dataClasses&&e.visible?a=a.concat(t.getDataClassLegendSymbols()):e.visible&&a.push(t),t.series.forEach(function(t){(!t.options.showInLegend||e.dataClasses)&&("point"===t.options.legendType?t.points.forEach(function(t){s(t)}):s(t))}))}),i=a.length;i--;)t.allItems.unshift(a[i])}function o(t){t.visible&&t.item.legendColor&&t.item.legendItem.symbol.attr({fill:t.item.legendColor})}function s(t){var e;null===(e=this.chart.colorAxis)||void 0===e||e.forEach(function(e){e.update({},t.redraw)})}function a(){(this.chart.colorAxis&&this.chart.colorAxis.length||this.colorAttribs)&&this.translateColors()}function n(){var t=this.axisTypes;t?-1===t.indexOf("colorAxis")&&t.push("colorAxis"):this.axisTypes=["colorAxis"]}function l(t){var e=this,i=t?"show":"hide";e.visible=e.options.visible=!!t,["graphic","dataLabel"].forEach(function(t){e[t]&&e[t][i]()}),this.series.buildKDTree()}function h(){var t=this,e=this.getPointsCollection(),i=this.options.nullColor,r=this.colorAxis,o=this.colorKey;e.forEach(function(e){var s=e.getNestedProperty(o),a=e.options.color||(e.isNull||null===e.value?i:r&&void 0!==s?r.toColor(s,e):e.color||t.color);a&&e.color!==a&&(e.color=a,"point"===t.options.legendType&&e.legendItem&&e.legendItem.label&&t.chart.legend.colorizeItem(e,e.visible))})}function c(){this.elem.attr("fill",M(this.start).tweenTo(M(this.end),this.pos),void 0,!0)}function p(){this.elem.attr("stroke",M(this.start).tweenTo(M(this.end),this.pos),void 0,!0)}t.compose=function(t,d,u,f,g){var y,m=d.prototype,v=u.prototype,x=g.prototype;m.collectionsWithUpdate.includes("colorAxis")||(e=t,m.collectionsWithUpdate.push("colorAxis"),m.collectionsWithInit.colorAxis=[m.addColorAxis],k(d,"afterCreateAxes",i),y=d.prototype.createAxis,d.prototype.createAxis=function(t,i){if("colorAxis"!==t)return y.apply(this,arguments);var r=new e(this,I(i.axis,{index:this[t].length,isX:!1}));return this.isDirtyLegend=!0,this.axes.forEach(function(t){t.series=[]}),this.series.forEach(function(t){t.bindAxes(),t.isDirtyData=!0}),O(i.redraw,!0)&&this.redraw(i.animation),r},v.fillSetter=c,v.strokeSetter=p,k(f,"afterGetAllItems",r),k(f,"afterColorizeItem",o),k(f,"afterUpdate",s),L(x,{optionalAxis:"colorAxis",translateColors:h}),L(x.pointClass.prototype,{setVisible:l}),k(g,"afterTranslate",a,{order:1}),k(g,"bindAxes",n))},t.pointSetVisible=l}(p||(p={}));var S=p,E=w().parse,T=x().merge;(n=d||(d={})).initDataClasses=function(t){var e,i,r,o=this.chart,s=this.legendItem=this.legendItem||{},a=this.options,n=t.dataClasses||[],l=o.options.chart.colorCount,h=0;this.dataClasses=i=[],s.labels=[];for(var c=0,p=n.length;c<p;++c)e=T(e=n[c]),i.push(e),(o.styledMode||!e.color)&&("category"===a.dataClassColor?(o.styledMode||(l=(r=o.options.colors||[]).length,e.color=r[h]),e.colorIndex=h,++h===l&&(h=0)):e.color=E(a.minColor).tweenTo(E(a.maxColor),p<2?.5:c/(p-1)))},n.initStops=function(){for(var t=this.options,e=this.stops=t.stops||[[0,t.minColor||""],[1,t.maxColor||""]],i=0,r=e.length;i<r;++i)e[i].color=E(e[i][1])},n.normalizedValue=function(t){var e=this.max||0,i=this.min||0;return this.logarithmic&&(t=this.logarithmic.log2lin(t)),1-(e-t)/(e-i||1)},n.toColor=function(t,e){var i,r,o,s,a,n,l=this.dataClasses,h=this.stops;if(l){for(n=l.length;n--;)if(r=(a=l[n]).from,o=a.to,(void 0===r||t>=r)&&(void 0===o||t<=o)){s=a.color,e&&(e.dataClass=n,e.colorIndex=a.colorIndex);break}}else{for(i=this.normalizedValue(t),n=h.length;n--&&!(i>h[n][0]););r=h[n]||h[n+1],i=1-((o=h[n+1]||r)[0]-i)/(o[0]-r[0]||1),s=r.color.tweenTo(o.color,i)}return s};var D=d,V=y(500),_=y.n(V),z=y(512),R=y.n(z),G=(l=function(t,e){return(l=Object.setPrototypeOf||({__proto__:[]})instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var i in e)e.hasOwnProperty(i)&&(t[i]=e[i])})(t,e)},function(t,e){function i(){this.constructor=t}l(t,e),t.prototype=null===e?Object.create(e):(i.prototype=e.prototype,new i)}),j=x().defaultOptions,q=R().series,N=x().defined,W=x().extend,H=x().fireEvent,K=x().isArray,X=x().isNumber,F=x().merge,U=x().pick,Y=x().relativeLength;j.colorAxis=F(j.xAxis,{lineWidth:0,minPadding:0,maxPadding:0,gridLineColor:"#ffffff",gridLineWidth:1,tickPixelInterval:72,startOnTick:!0,endOnTick:!0,offset:0,marker:{animation:{duration:50},width:.01,color:"#999999"},labels:{distance:8,overflow:"justify",rotation:0},minColor:"#e6e9ff",maxColor:"#0022ff",tickLength:5,showInLegend:!0});var Z=function(t){function e(e,i){var r=t.call(this,e,i)||this;return r.coll="colorAxis",r.visible=!0,r.init(e,i),r}return G(e,t),e.compose=function(t,i,r,o){S.compose(e,t,i,r,o)},e.prototype.init=function(e,i){var r=e.options.legend||{},o=i.layout?"vertical"!==i.layout:"vertical"!==r.layout;this.side=i.side||o?2:1,this.reversed=i.reversed||!o,this.opposite=!o,t.prototype.init.call(this,e,i,"colorAxis"),this.userOptions=i,K(e.userOptions.colorAxis)&&(e.userOptions.colorAxis[this.index]=i),i.dataClasses&&this.initDataClasses(i),this.initStops(),this.horiz=o,this.zoomEnabled=!1},e.prototype.hasData=function(){return!!(this.tickPositions||[]).length},e.prototype.setTickPositions=function(){if(!this.dataClasses)return t.prototype.setTickPositions.call(this)},e.prototype.setOptions=function(e){var i=F(j.colorAxis,e,{showEmpty:!1,title:null,visible:this.chart.options.legend.enabled&&!1!==e.visible});t.prototype.setOptions.call(this,i),this.options.crosshair=this.options.marker},e.prototype.setAxisSize=function(){var t,i=this.chart,r=null===(t=this.legendItem)||void 0===t?void 0:t.symbol,o=this.getSize(),s=o.width,a=o.height;r&&(this.left=+r.attr("x"),this.top=+r.attr("y"),this.width=s=+r.attr("width"),this.height=a=+r.attr("height"),this.right=i.chartWidth-this.left-s,this.bottom=i.chartHeight-this.top-a,this.pos=this.horiz?this.left:this.top),this.len=(this.horiz?s:a)||e.defaultLegendLength},e.prototype.getOffset=function(){var i,r=null===(i=this.legendItem)||void 0===i?void 0:i.group,o=this.chart.axisOffset[this.side];if(r){this.axisParent=r,t.prototype.getOffset.call(this);var s=this.chart.legend;s.allItems.forEach(function(t){t instanceof e&&t.drawLegendSymbol(s,t)}),s.render(),this.chart.getMargins(!0),this.chart.series.some(function(t){return t.isDrilling})||(this.isDirty=!0),this.added||(this.added=!0,this.labelLeft=0,this.labelRight=this.width),this.chart.axisOffset[this.side]=o}},e.prototype.setLegendColor=function(){var t=this.horiz,e=this.reversed,i=e?1:0,r=e?0:1,o=t?[i,0,r,0]:[0,r,0,i];this.legendColor={linearGradient:{x1:o[0],y1:o[1],x2:o[2],y2:o[3]},stops:this.stops}},e.prototype.drawLegendSymbol=function(t,e){var i,r=e.legendItem||{},o=t.padding,s=t.options,a=this.options.labels,n=U(s.itemDistance,10),l=this.horiz,h=this.getSize(),c=h.width,p=h.height,d=U(s.labelPadding,l?16:30);this.setLegendColor(),r.symbol||(r.symbol=this.chart.renderer.symbol("roundedRect").attr({r:null!==(i=s.symbolRadius)&&void 0!==i?i:3,zIndex:1}).add(r.group)),r.symbol.attr({x:0,y:(t.baseline||0)-11,width:c,height:p}),r.labelWidth=c+o+(l?n:U(a.x,a.distance)+(this.maxLabelLength||0)),r.labelHeight=p+o+(l?d:0)},e.prototype.setState=function(t){this.series.forEach(function(e){e.setState(t)})},e.prototype.setVisible=function(){},e.prototype.getSeriesExtremes=function(){var t,e,i,r,o=this.series,s=o.length;for(this.dataMin=1/0,this.dataMax=-1/0;s--;){e=(r=o[s]).colorKey=U(r.options.colorKey,r.colorKey,r.pointValKey,r.zoneAxis,"y"),i=r[e+"Min"]&&r[e+"Max"];for(var a=0,n=[e,"value","y"];a<n.length;a++){var l=n[a];if((t=r.getColumn(l)).length)break}if(i)r.minColorValue=r[e+"Min"],r.maxColorValue=r[e+"Max"];else{var h=q.prototype.getExtremes.call(r,t);r.minColorValue=h.dataMin,r.maxColorValue=h.dataMax}N(r.minColorValue)&&N(r.maxColorValue)&&(this.dataMin=Math.min(this.dataMin,r.minColorValue),this.dataMax=Math.max(this.dataMax,r.maxColorValue)),i||q.prototype.applyExtremes.call(r)}},e.prototype.drawCrosshair=function(e,i){var r,o=this.legendItem||{},s=i&&i.plotX,a=i&&i.plotY,n=this.pos,l=this.len;i&&((r=this.toPixels(i.getNestedProperty(i.series.colorKey)))<n?r=n-2:r>n+l&&(r=n+l+2),i.plotX=r,i.plotY=this.len-r,t.prototype.drawCrosshair.call(this,e,i),i.plotX=s,i.plotY=a,this.cross&&!this.cross.addedToColorAxis&&o.group&&(this.cross.addClass("highcharts-coloraxis-marker").add(o.group),this.cross.addedToColorAxis=!0,this.chart.styledMode||"object"!=typeof this.crosshair||this.cross.attr({fill:this.crosshair.color})))},e.prototype.getPlotLinePath=function(e){var i=this.left,r=e.translatedValue,o=this.top;return X(r)?this.horiz?[["M",r-4,o-6],["L",r+4,o-6],["L",r,o],["Z"]]:[["M",i,r],["L",i-6,r+6],["L",i-6,r-6],["Z"]]:t.prototype.getPlotLinePath.call(this,e)},e.prototype.update=function(e,i){var r=this.chart.legend;this.series.forEach(function(t){t.isDirtyData=!0}),(e.dataClasses&&r.allItems||this.dataClasses)&&this.destroyItems(),t.prototype.update.call(this,e,i),this.legendItem&&this.legendItem.label&&(this.setLegendColor(),r.colorizeItem(this,!0))},e.prototype.destroyItems=function(){var t=this.chart,e=this.legendItem||{};if(e.label)t.legend.destroyItem(this);else if(e.labels)for(var i=0,r=e.labels;i<r.length;i++){var o=r[i];t.legend.destroyItem(o)}t.isDirtyLegend=!0},e.prototype.destroy=function(){this.chart.isDirtyLegend=!0,this.destroyItems(),t.prototype.destroy.apply(this,[].slice.call(arguments))},e.prototype.remove=function(e){this.destroyItems(),t.prototype.remove.call(this,e)},e.prototype.getDataClassLegendSymbols=function(){var t,e=this,i=e.chart,r=e.legendItem&&e.legendItem.labels||[],o=i.options.legend,s=U(o.valueDecimals,-1),a=U(o.valueSuffix,""),n=function(t){return e.series.reduce(function(e,i){return e.push.apply(e,i.points.filter(function(e){return e.dataClass===t})),e},[])};return r.length||e.dataClasses.forEach(function(o,l){var h=o.from,c=o.to,p=i.numberFormatter,d=!0;t="",void 0===h?t="< ":void 0===c&&(t="> "),void 0!==h&&(t+=p(h,s)+a),void 0!==h&&void 0!==c&&(t+=" - "),void 0!==c&&(t+=p(c,s)+a),r.push(W({chart:i,name:t,options:{},drawLegendSymbol:_().rectangle,visible:!0,isDataClass:!0,setState:function(t){for(var e=0,i=n(l);e<i.length;e++)i[e].setState(t)},setVisible:function(){this.visible=d=e.visible=!d;for(var t=[],r=0,o=n(l);r<o.length;r++){var s=o[r];s.setVisible(d),s.hiddenInDataClass=!d,-1===t.indexOf(s.series)&&t.push(s.series)}i.legend.colorizeItem(this,d),t.forEach(function(t){H(t,"afterDataClassLegendClick")})}},o))}),r},e.prototype.getSize=function(){var t=this.chart,i=this.horiz,r=this.options,o=r.height,s=r.width,a=t.options.legend;return{width:U(N(s)?Y(s,t.chartWidth):void 0,null==a?void 0:a.symbolWidth,i?e.defaultLegendLength:12),height:U(N(o)?Y(o,t.chartHeight):void 0,null==a?void 0:a.symbolHeight,i?12:e.defaultLegendLength)}},e.defaultLegendLength=200,e.keepProps=["legendItem"],e}(C());W(Z.prototype,D),Array.prototype.push.apply(C().keepProps,Z.keepProps);var B=x();B.ColorAxis=B.ColorAxis||Z,B.ColorAxis.compose(B.Chart,B.Fx,B.Legend,B.Series);var J=y(28),Q=y.n(J),$=R().seriesTypes.column.prototype,tt=x().addEvent,te=x().defined;!function(t){function e(t){var e=this.series,i=e.chart.renderer;this.moveToTopOnHover&&this.graphic&&(e.stateMarkerGraphic||(e.stateMarkerGraphic=new(Q())(i,"use").css({pointerEvents:"none"}).add(this.graphic.parentGroup)),(null==t?void 0:t.state)==="hover"?(this.graphic.attr({id:this.id}),e.stateMarkerGraphic.attr({href:""+i.url+"#".concat(this.id),visibility:"visible"})):e.stateMarkerGraphic.attr({href:""}))}t.pointMembers={dataLabelOnNull:!0,moveToTopOnHover:!0,isValid:function(){return null!==this.value&&this.value!==1/0&&this.value!==-1/0&&(void 0===this.value||!isNaN(this.value))}},t.seriesMembers={colorKey:"value",axisTypes:["xAxis","yAxis","colorAxis"],parallelArrays:["x","y","value"],pointArrayMap:["value"],trackerGroups:["group","markerGroup","dataLabelsGroup"],colorAttribs:function(t){var e={};return te(t.color)&&(!t.state||"normal"===t.state)&&(e[this.colorProp||"fill"]=t.color),e},pointAttribs:$.pointAttribs},t.compose=function(t){return tt(t.prototype.pointClass,"afterSetState",e),t}}(u||(u={}));var ti=u,tr=(h=function(t,e){return(h=Object.setPrototypeOf||({__proto__:[]})instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var i in e)Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i])})(t,e)},function(t,e){if("function"!=typeof e&&null!==e)throw TypeError("Class extends value "+String(e)+" is not a constructor or null");function i(){this.constructor=t}h(t,e),t.prototype=null===e?Object.create(e):(i.prototype=e.prototype,new i)}),to=R().seriesTypes.scatter.prototype.pointClass,ts=x().clamp,ta=x().defined,tn=x().extend,tl=x().pick,th=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return tr(e,t),e.prototype.applyOptions=function(e,i){return(this.isNull||null===this.value)&&delete this.color,t.prototype.applyOptions.call(this,e,i),this.formatPrefix=this.isNull||null===this.value?"null":"point",this},e.prototype.getCellAttributes=function(){for(var t=this.series,e=t.options,i=(e.colsize||1)/2,r=(e.rowsize||1)/2,o=t.xAxis,s=t.yAxis,a=this.options.marker||t.options.marker,n=t.pointPlacementToXValue(),l=tl(this.pointPadding,e.pointPadding,0),h={x1:ts(Math.round(o.len-o.translate(this.x-i,!1,!0,!1,!0,-n)),-o.len,2*o.len),x2:ts(Math.round(o.len-o.translate(this.x+i,!1,!0,!1,!0,-n)),-o.len,2*o.len),y1:ts(Math.round(s.translate(this.y-r,!1,!0,!1,!0)),-s.len,2*s.len),y2:ts(Math.round(s.translate(this.y+r,!1,!0,!1,!0)),-s.len,2*s.len)},c=0,p=[["width","x"],["height","y"]];c<p.length;c++){var d=p[c],u=d[0],f=d[1],g=f+"1",y=f+"2",m=Math.abs(h[g]-h[y]),v=a&&a.lineWidth||0,x=Math.abs(h[g]+h[y])/2,b=a&&a[u];if(ta(b)&&b<m){var C=b/2+v/2;h[g]=x-C,h[y]=x+C}l&&(("x"===f&&o.reversed||"y"===f&&!s.reversed)&&(g=y,y=f+"1"),h[g]+=l,h[y]-=l)}return h},e.prototype.haloPath=function(t){if(!t)return[];var e=this.shapeArgs||{},i=e.x,r=void 0===i?0:i,o=e.y,s=void 0===o?0:o,a=e.width,n=void 0===a?0:a,l=e.height,h=void 0===l?0:l;return[["M",r-t,s-t],["L",r-t,s+h+t],["L",r+n+t,s+h+t],["L",r+n+t,s-t],["Z"]]},e.prototype.isValid=function(){return this.value!==1/0&&this.value!==-1/0},e}(to);tn(th.prototype,{dataLabelOnNull:!0,moveToTopOnHover:!0,ttBelow:!1});var tc=x().isNumber,tp={animation:!1,borderRadius:0,borderWidth:0,interpolation:!1,nullColor:"#f7f7f7",dataLabels:{formatter:function(){var t=this.series.chart.numberFormatter,e=this.point.value;return tc(e)?t(e,-1):""},inside:!0,verticalAlign:"middle",crop:!1,overflow:"allow",padding:0},marker:{symbol:"rect",radius:0,lineColor:void 0,states:{hover:{lineWidthPlus:0},select:{}}},clip:!0,pointRange:null,tooltip:{pointFormat:"{point.x}, {point.y}: {point.value}<br/>"},states:{hover:{halo:!1,brightness:.2}},legendSymbol:"rectangle"},td=y(540),tu=y.n(td),tf=x().doc,tg=x().defined,ty=x().pick,tm=function(t){var e=t.canvas,i=t.context;return e&&i?(i.clearRect(0,0,e.width,e.height),i):(t.canvas=tf.createElement("canvas"),t.context=t.canvas.getContext("2d",{willReadFrequently:!0})||void 0,t.context)},tv=(c=function(t,e){return(c=Object.setPrototypeOf||({__proto__:[]})instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var i in e)Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i])})(t,e)},function(t,e){if("function"!=typeof e&&null!==e)throw TypeError("Class extends value "+String(e)+" is not a constructor or null");function i(){this.constructor=t}c(t,e),t.prototype=null===e?Object.create(e):(i.prototype=e.prototype,new i)}),tx=function(){return(tx=Object.assign||function(t){for(var e,i=1,r=arguments.length;i<r;i++)for(var o in e=arguments[i])Object.prototype.hasOwnProperty.call(e,o)&&(t[o]=e[o]);return t}).apply(this,arguments)},tb=R().series,tC=R().seriesTypes,tA=tC.column,tw=tC.scatter,tM=tu().prototype.symbols,tk=x().addEvent,tL=x().extend,tI=x().fireEvent,tO=x().isNumber,tP=x().merge,tS=x().pick,tE=function(t,e){var i=e.series.colorAxis;if(i){var r=i.toColor(t||0,e).split(")")[0].split("(")[1].split(",").map(function(t){return ty(parseFloat(t),parseInt(t,10))});return r[3]=255*ty(r[3],1),tg(t)&&e.visible||(r[3]=0),r}return[0,0,0,0]},tT=function(t){function e(){var e=null!==t&&t.apply(this,arguments)||this;return e.valueMax=NaN,e.valueMin=NaN,e.isDirtyCanvas=!0,e}return tv(e,t),e.prototype.drawPoints=function(){var t=this,e=t.options,i=e.interpolation,r=e.marker||{};if(i){var o=t.image,s=t.chart,a=t.xAxis,n=t.yAxis,l=a.reversed,h=a.len,c=n.reversed,p=n.len,d={width:h,height:p};if(!o||t.isDirtyData||t.isDirtyCanvas){var u=tm(t),f=t.canvas,g=t.options,y=g.colsize,m=g.rowsize,v=t.points,x=t.points.length,b=s.colorAxis&&s.colorAxis[0];if(f&&u&&b){var C=a.getExtremes(),A=C.min,w=C.max,M=n.getExtremes(),k=M.min,L=M.max,I=w-A,O=L-k,P=Math.round(I/(void 0===y?1:y)/8*8),S=Math.round(O/(void 0===m?1:m)/8*8),E=[[P,P/I,void 0!==l&&l,"ceil"],[S,S/O,!(void 0!==c&&c),"floor"]].map(function(t){var e=t[0],i=t[1],r=t[2],o=t[3];return r?function(t){return Math[o](e-i*t)}:function(t){return Math[o](i*t)}}),T=E[0],D=E[1],V=f.width=P+1,_=V*(f.height=S+1),z=(x-1)/_,R=new Uint8ClampedArray(4*_);t.buildKDTree();for(var G=0;G<_;G++){var j=v[Math.ceil(z*G)],q=j.x,N=j.y;R.set(tE(j.value,j),4*Math.ceil(V*D(N-k)+T(q-A)))}u.putImageData(new ImageData(R,V),0,0),o?o.attr(tx(tx({},d),{href:f.toDataURL("image/png",1)})):(t.directTouch=!1,t.image=s.renderer.image(f.toDataURL("image/png",1)).attr(d).add(t.group))}t.isDirtyCanvas=!1}else(o.width!==h||o.height!==p)&&o.attr(d)}else(r.enabled||t._hasPointMarkers)&&(tb.prototype.drawPoints.call(t),t.points.forEach(function(e){e.graphic&&(e.graphic[t.chart.styledMode?"css":"animate"](t.colorAttribs(e)),null===e.value&&e.graphic.addClass("highcharts-null-point"))}))},e.prototype.getExtremes=function(){var t=tb.prototype.getExtremes.call(this,this.getColumn("value")),e=t.dataMin,i=t.dataMax;return tO(e)&&(this.valueMin=e),tO(i)&&(this.valueMax=i),tb.prototype.getExtremes.call(this)},e.prototype.getValidPoints=function(t,e){return tb.prototype.getValidPoints.call(this,t,e,!0)},e.prototype.hasData=function(){return!!this.dataTable.rowCount},e.prototype.init=function(){t.prototype.init.apply(this,arguments);var e=this.options;e.pointRange=tS(e.pointRange,e.colsize||1),this.yAxis.axisPointRange=e.rowsize||1,tM.ellipse=tM.circle,e.marker&&tO(e.borderRadius)&&(e.marker.r=e.borderRadius)},e.prototype.markerAttribs=function(t,e){var i=t.shapeArgs||{};if(t.hasImage)return{x:t.plotX,y:t.plotY};if(e&&"normal"!==e){var r=t.options.marker||{},o=this.options.marker||{},s=o.states&&o.states[e]||{},a=r.states&&r.states[e]||{},n=(a.width||s.width||i.width||0)+(a.widthPlus||s.widthPlus||0),l=(a.height||s.height||i.height||0)+(a.heightPlus||s.heightPlus||0);return{x:(i.x||0)+((i.width||0)-n)/2,y:(i.y||0)+((i.height||0)-l)/2,width:n,height:l}}return i},e.prototype.pointAttribs=function(t,e){var i=tb.prototype.pointAttribs.call(this,t,e),r=this.options||{},o=this.chart.options.plotOptions||{},s=o.series||{},a=o.heatmap||{},n=t&&t.options.borderColor||r.borderColor||a.borderColor||s.borderColor,l=t&&t.options.borderWidth||r.borderWidth||a.borderWidth||s.borderWidth||i["stroke-width"];if(i.stroke=t&&t.marker&&t.marker.lineColor||r.marker&&r.marker.lineColor||n||this.color,i["stroke-width"]=l,e&&"normal"!==e){var h=tP(r.states&&r.states[e],r.marker&&r.marker.states&&r.marker.states[e],t&&t.options.states&&t.options.states[e]||{});i.fill=h.color||w().parse(i.fill).brighten(h.brightness||0).get(),i.stroke=h.lineColor||i.stroke}return i},e.prototype.translate=function(){var t=this.options,e=t.borderRadius,i=t.marker,r=i&&i.symbol||"rect",o=tM[r]?r:"rect",s=-1!==["circle","square"].indexOf(o);this.generatePoints();for(var a=0,n=this.points;a<n.length;a++){var l=n[a],h=l.getCellAttributes(),c=Math.min(h.x1,h.x2),p=Math.min(h.y1,h.y2),d=Math.max(Math.abs(h.x2-h.x1),0),u=Math.max(Math.abs(h.y2-h.y1),0);if(l.hasImage=0===(l.marker&&l.marker.symbol||r||"").indexOf("url"),s){var f=Math.abs(d-u);c=Math.min(h.x1,h.x2)+(d<u?0:f/2),p=Math.min(h.y1,h.y2)+(d<u?f/2:0),d=u=Math.min(d,u)}l.hasImage&&(l.marker={width:d,height:u}),l.plotX=l.clientX=(h.x1+h.x2)/2,l.plotY=(h.y1+h.y2)/2,l.shapeType="path",l.shapeArgs=tP(!0,{x:c,y:p,width:d,height:u},{d:tM[o](c,p,d,u,{r:tO(e)?e:0})})}tI(this,"afterTranslate")},e.defaultOptions=tP(tw.defaultOptions,tp),e}(tw);tk(tT,"afterDataClassLegendClick",function(){this.isDirtyCanvas=!0,this.drawPoints()}),tL(tT.prototype,{axisTypes:ti.seriesMembers.axisTypes,colorKey:ti.seriesMembers.colorKey,directTouch:!0,getExtremesFromAll:!0,keysAffectYAxis:["y"],parallelArrays:ti.seriesMembers.parallelArrays,pointArrayMap:["y","value"],pointClass:th,specialGroup:"group",trackerGroups:ti.seriesMembers.trackerGroups,alignDataLabel:tA.prototype.alignDataLabel,colorAttribs:ti.seriesMembers.colorAttribs,getSymbol:tb.prototype.getSymbol}),ti.compose(tT),R().registerSeriesType("heatmap",tT);/**
 * @license Highmaps JS v12.1.2 (2025-01-09)
 * @module highcharts/modules/heatmap
 * @requires highcharts
 *
 * (c) 2009-2024 Torstein Honsi
 *
 * License: www.highcharts.com/license
 */var tD=x();return m.default}()});