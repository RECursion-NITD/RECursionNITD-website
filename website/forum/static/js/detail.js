//Comment and Question Show-Hide Button//

function answerbtnFunction() {
  var x = document.getElementById("answerDIV");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function commentbtnFunction() {
  var x = document.getElementById("commentDIV");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
