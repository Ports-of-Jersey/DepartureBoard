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
  var x = document.getElementById("status1");
  var y = document.getElementById("status2");
  if (x.style.display === "none") {
    x.style.display = "block";
    y.style.display = "none";
  } else {
    x.style.display = "none";
    y.style.display = "block";
  }
}