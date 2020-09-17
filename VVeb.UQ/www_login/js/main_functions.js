function start_new_session()
{
  username = document.getElementById("username").value;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", "php/login_session.php?FROM_WEB_FRONT=yes&username="+username, false);
  xmlhttp.send();
  reply = xmlhttp.responseText;
  document.getElementById("new_session_comments").innerHTML = reply;
}

