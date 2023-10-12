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
  var input, filter, table, article, label, i;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("articleTable");
  article = table.getElementsByClassName("article");
  for (i = 0; i < article.length; i++) {
    label = article[i].getElementsByClassName("label")[0];
    if (label) {
      txtValue = label.textContent || label.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        article[i].style.display = "";
      } else {
        article[i].style.display = "none";
      }
    }
  }
}
