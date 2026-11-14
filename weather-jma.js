/* weather-jma.js — 気象庁の天気予報 (福岡県) をコースページに表示する (2026-11)
 * データ: https://www.jma.go.jp/bosai/forecast/data/forecast/400000.json (CORS 許可)
 * 天気コード表: 気象庁 forecast_const.js の TELOPS (アイコン番号・日本語表記) を転記
 * 使い方: <div class="jma-weather" data-area="400020" data-area-name="北九州地方" data-city="82056" data-city-name="八幡"></div>
 */
(function () {
  var TELOPS = {"100":["100","晴"],"101":["101","晴時々曇"],"102":["102","晴一時雨"],"103":["102","晴時々雨"],"104":["104","晴一時雪"],"105":["104","晴時々雪"],"106":["102","晴一時雨か雪"],"107":["102","晴時々雨か雪"],"108":["102","晴一時雨か雷雨"],"110":["110","晴後時々曇"],"111":["110","晴後曇"],"112":["112","晴後一時雨"],"113":["112","晴後時々雨"],"114":["112","晴後雨"],"115":["115","晴後一時雪"],"116":["115","晴後時々雪"],"117":["115","晴後雪"],"118":["112","晴後雨か雪"],"119":["112","晴後雨か雷雨"],"120":["102","晴朝夕一時雨"],"121":["102","晴朝の内一時雨"],"122":["112","晴夕方一時雨"],"123":["100","晴山沿い雷雨"],"124":["100","晴山沿い雪"],"125":["112","晴午後は雷雨"],"126":["112","晴昼頃から雨"],"127":["112","晴夕方から雨"],"128":["112","晴夜は雨"],"130":["100","朝の内霧後晴"],"131":["100","晴明け方霧"],"132":["101","晴朝夕曇"],"140":["102","晴時々雨で雷を伴う"],"160":["104","晴一時雪か雨"],"170":["104","晴時々雪か雨"],"181":["115","晴後雪か雨"],"200":["200","曇"],"201":["201","曇時々晴"],"202":["202","曇一時雨"],"203":["202","曇時々雨"],"204":["204","曇一時雪"],"205":["204","曇時々雪"],"206":["202","曇一時雨か雪"],"207":["202","曇時々雨か雪"],"208":["202","曇一時雨か雷雨"],"209":["200","霧"],"210":["210","曇後時々晴"],"211":["210","曇後晴"],"212":["212","曇後一時雨"],"213":["212","曇後時々雨"],"214":["212","曇後雨"],"215":["215","曇後一時雪"],"216":["215","曇後時々雪"],"217":["215","曇後雪"],"218":["212","曇後雨か雪"],"219":["212","曇後雨か雷雨"],"220":["202","曇朝夕一時雨"],"221":["202","曇朝の内一時雨"],"222":["212","曇夕方一時雨"],"223":["201","曇日中時々晴"],"224":["212","曇昼頃から雨"],"225":["212","曇夕方から雨"],"226":["212","曇夜は雨"],"228":["215","曇昼頃から雪"],"229":["215","曇夕方から雪"],"230":["215","曇夜は雪"],"231":["200","曇海上海岸は霧か霧雨"],"240":["202","曇時々雨で雷を伴う"],"250":["204","曇時々雪で雷を伴う"],"260":["204","曇一時雪か雨"],"270":["204","曇時々雪か雨"],"281":["215","曇後雪か雨"],"300":["300","雨"],"301":["301","雨時々晴"],"302":["302","雨時々止む"],"303":["303","雨時々雪"],"304":["300","雨か雪"],"306":["300","大雨"],"308":["308","雨で暴風を伴う"],"309":["303","雨一時雪"],"311":["311","雨後晴"],"313":["313","雨後曇"],"314":["314","雨後時々雪"],"315":["314","雨後雪"],"316":["311","雨か雪後晴"],"317":["313","雨か雪後曇"],"320":["311","朝の内雨後晴"],"321":["313","朝の内雨後曇"],"322":["303","雨朝晩一時雪"],"323":["311","雨昼頃から晴"],"324":["311","雨夕方から晴"],"325":["311","雨夜は晴"],"326":["314","雨夕方から雪"],"327":["314","雨夜は雪"],"328":["300","雨一時強く降る"],"329":["300","雨一時みぞれ"],"340":["400","雪か雨"],"350":["300","雨で雷を伴う"],"361":["411","雪か雨後晴"],"371":["413","雪か雨後曇"],"400":["400","雪"],"401":["401","雪時々晴"],"402":["402","雪時々止む"],"403":["403","雪時々雨"],"405":["400","大雪"],"406":["406","風雪強い"],"407":["406","暴風雪"],"409":["403","雪一時雨"],"411":["411","雪後晴"],"413":["413","雪後曇"],"414":["414","雪後雨"],"420":["411","朝の内雪後晴"],"421":["413","朝の内雪後曇"],"422":["414","雪昼頃から雨"],"423":["414","雪夕方から雨"],"425":["400","雪一時強く降る"],"426":["400","雪後みぞれ"],"427":["400","雪一時みぞれ"],"450":["400","雪で雷を伴う"]};
  var URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/400000.json";
  var ICON = "https://www.jma.go.jp/bosai/forecast/img/";
  var WD = ["日", "月", "火", "水", "木", "金", "土"];

  function jstToday() { return new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10); }
  function md(d) { /* d は "YYYY-MM-DD" (日本時間の日付) */ return (+d.slice(5, 7)) + "/" + (+d.slice(8, 10)) + "（" + WD[new Date(Date.UTC(+d.slice(0, 4), +d.slice(5, 7) - 1, +d.slice(8, 10))).getUTCDay()] + "）"; }
  function clean(s) { return (s || "").replace(/\u3000/g, " ").replace(/\s+/g, " ").trim(); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function icon(code, alt) {
    var t = TELOPS[code];
    return t ? '<img src="' + ICON + t[0] + '.svg" alt="' + esc(alt || t[1]) + '" width="44" height="33" loading="lazy">' : "";
  }
  function pick(areas, code) { for (var i = 0; i < areas.length; i++) if (areas[i].area.code === code) return areas[i]; return null; }

  function render(el, data) {
    var area = el.getAttribute("data-area"), city = el.getAttribute("data-city");
    var areaName = el.getAttribute("data-area-name"), cityName = el.getAttribute("data-city-name");
    var today = jstToday(), short = data[0], week = data[1];
    var ts0 = short.timeSeries[0], ts1 = short.timeSeries[1], ts2 = short.timeSeries[2];
    var a0 = pick(ts0.areas, area), a1 = pick(ts1.areas, area), a2 = pick(ts2.areas, city);
    if (!a0) throw new Error("area");
    var days = [], seen = {};
    ts0.timeDefines.forEach(function (t, i) {
      var d = t.slice(0, 10);
      if (d < today || seen[d]) return;
      seen[d] = 1;
      var pops = [];
      if (a1) a1.pops.forEach(function (p, j) {
        var tt = ts1.timeDefines[j];
        if (tt.slice(0, 10) === d && p !== "") pops.push([tt.slice(11, 13), p]);
      });
      var mx = "", mn = "";
      if (a2) a2.temps.forEach(function (v, j) {
        var tt = ts2.timeDefines[j];
        if (tt.slice(0, 10) !== d) return;
        if (tt.slice(11, 13) === "09") mx = v; else if (d !== today) mn = v;
      });
      days.push({ d: d, code: a0.weatherCodes[i], text: clean(a0.weathers && a0.weathers[i]), wind: clean(a0.winds && a0.winds[i]), pops: pops, mx: mx, mn: mn });
    });
    var h = '<div class="jw-days">';
    days.forEach(function (x, k) {
      h += '<div class="jw-day"><div class="jw-date">' + (k === 0 && x.d === today ? "今日 " : k <= 1 ? "明日 " : "") + md(x.d) + "</div>";
      h += '<div class="jw-main">' + icon(x.code, x.text) + '<div class="jw-text">' + esc(x.text || (TELOPS[x.code] || [0, ""])[1]) + "</div></div>";
      if (x.mx || x.mn) h += '<div class="jw-temp">' + (x.mx ? '<span class="jw-hi">' + esc(x.mx) + "℃</span>" : "") + (x.mn ? ' / <span class="jw-lo">' + esc(x.mn) + "℃</span>" : "") + ' <small>（' + esc(cityName) + "）</small></div>";
      if (x.pops.length) h += '<div class="jw-pop">降水確率 ' + x.pops.map(function (p) { return '<span>' + (+p[0]) + "時〜 <b>" + esc(p[1]) + "%</b></span>"; }).join("") + "</div>";
      if (x.wind) h += '<div class="jw-wind">風 ' + esc(x.wind) + "</div>";
      h += "</div>";
    });
    h += "</div>";
    // 週間予報 (福岡県・気温は福岡市)
    var w0 = week.timeSeries[0], wa = w0.areas[0], wt = week.timeSeries[1] && week.timeSeries[1].areas[0];
    var cells = "";
    w0.timeDefines.forEach(function (t, i) {
      var d = t.slice(0, 10);
      if (d < today || seen[d]) return;
      var mn = wt && wt.tempsMin[i], mx = wt && wt.tempsMax[i], tel = TELOPS[wa.weatherCodes[i]];
      cells += '<div class="jw-w"><div class="jw-date">' + md(d) + "</div>" + icon(wa.weatherCodes[i]) + '<div class="jw-wtext">' + esc(tel ? tel[1] : "") + "</div>" +
        (wa.pops[i] !== "" ? '<div class="jw-wpop">' + esc(wa.pops[i]) + "%</div>" : "") +
        (mx ? '<div class="jw-wtemp"><span class="jw-hi">' + esc(mx) + '</span>/<span class="jw-lo">' + esc(mn) + "</span></div>" : "") + "</div>";
    });
    if (cells) h += '<div class="jw-week-head">週間予報（福岡県・気温は福岡市）</div><div class="jw-week">' + cells + "</div>";
    var rep = short.reportDatetime, r = new Date(rep);
    var stamp = rep.slice(0, 4) + "年" + (+rep.slice(5, 7)) + "月" + (+rep.slice(8, 10)) + "日 " + (+rep.slice(11, 13)) + "時";
    h += '<p class="jw-src">' + esc(areaName) + "の予報です（コースの地点の予報ではありません）。出典：気象庁ホームページ（" + esc(short.publishingOffice) + " " + stamp + "発表）を加工して作成。</p>";
    el.innerHTML = h;
    el.setAttribute("data-loaded", "1");
  }

  function run() {
    var els = document.querySelectorAll(".jma-weather");
    if (!els.length || !window.fetch) return;
    fetch(URL, { cache: "no-store" }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (data) {
      Array.prototype.forEach.call(els, function (el) {
        try { render(el, data); } catch (e) { el.querySelector(".jw-fallback") && (el.querySelector(".jw-fallback").style.display = "block"); }
      });
    }).catch(function () {
      Array.prototype.forEach.call(els, function (el) { var f = el.querySelector(".jw-fallback"); if (f) f.style.display = "block"; });
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run); else run();
})();
