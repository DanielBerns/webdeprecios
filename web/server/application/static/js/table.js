function w3_open(elementId) {
  document.getElementById(elementId).style.display = "block";
}

function w3_close(elementId) {
  document.getElementById(elementId).style.display = "none";
}

window.onscroll = function() {myFunction()};

var header = document.getElementById("myHeader");
var sticky = header.offsetTop;

function myFunction() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
}

function searchArticleTable() {
  var input, filter, table, row, searchThis, i;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("articleTable");
  row = table.getElementsByClassName("row");
  for (i = 0; i < row.length; i++) {
    searchThis = row[i].getElementsByClassName("searchThis")[0];
    if (searchThis) {
      txtValue = searchThis.textContent || searchThis.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        row[i].style.display = "";
      } else {
        row[i].style.display = "none";
      }
    }
  }
}
