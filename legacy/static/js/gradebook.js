// gradebook.js - старий JavaScript для JS -> TS (ЛР10, крок 4)
function average(grades) {
  var sum = 0;
  for (var i = 0; i < grades.length; i++) {
    if (grades[i] != null) sum += grades[i];
  }
  return grades.length ? Math.round(sum / grades.length * 10) / 10 : 0;
}

function lateBadge(days) {
  if (days == 0) return "";
  if (days > 5) return "Не приймається";
  return "Запізно на " + days + " д.";
}

function formatScore(x) {
  return x == null ? "–" : String(x);
}

module.exports = { average: average, lateBadge: lateBadge, formatScore: formatScore };
