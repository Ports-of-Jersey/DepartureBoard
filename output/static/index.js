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
  var messageX = document.getElementsByClassName("status1");
  var messageY = document.getElementsByClassName("status2");
  var row = 0
  while (row < messageX.length) {
    if (messageX[row].style.display === "none") {
      messageX[row].style.display = "block";
      messageY[row].style.display = "none";
    } else {
      messageX[row].style.display = "none";
      messageY[row].style.display = "block";
    }
    row ++;
  }
}