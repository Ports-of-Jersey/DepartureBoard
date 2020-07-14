// sets the date
var date = new Date();

function setDate() {
  let date = new Date();
  date = date.toLocaleString('en-GB', { timeZoneName: 'short' });
  let dateElement = document.getElementById('footer-date');
  dateElement.innerHTML = date;
}

setDate();

// alternates between status messages
var altStatus = setInterval(switchStatus, 4000);

function switchStatus() {
  var x = document.getElementsByClassName("status1");
  var y = document.getElementsByClassName("status2");
  var i = 0
  while (i < x.length) {
    if (x[i].style.display === "none") {
      x[i].style.display = "block";
      y[i].style.display = "none";
    } else {
      x[i].style.display = "none";
      y[i].style.display = "block";
    }
    i ++;
  }
}