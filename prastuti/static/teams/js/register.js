
function emailField(){

    var lst = parseInt(document.getElementById("size").value)
    var emails = document.getElementById("emails")
    while (emails.firstChild) {
        emails.removeChild(emails.lastChild);
    }
    if (lst == 0)return;
    var lab = document.createElement("label")
    lab.innerHTML = "Team Name"
    var name = document.createElement("input")
    name.setAttribute("type",'text')
    name.setAttribute("name","team_name")
    emails.appendChild(lab)
    emails.appendChild(name)
    for(var i = 1; i <= lst; i++){
        var node = document.createElement("div")
        var label = document.createElement("label")
        label.innerHTML = "Email ID of Member #" + i;
        var field = document.createElement("input")
        field.setAttribute('type',"email");
        field.setAttribute('name','email' + i);
        field.required = true
        node.appendChild(label);
        node.appendChild(field);
        emails.appendChild(node);
    }

    {% if event.event_name == 'Codigo' or event.event_name == 'Recognizance' %}
      var node = document.createElement("div")
      var label = document.createElement("label")
      {% if event.event_name == 'Codigo' %}
      label.innerHTML = "Hackerrank id of the user"
      {% endif %}
      {% if event.event_name == 'Recognizance' %}
      label.innerHTML = "kaggle id of the team"
      {% endif %}
      var field = document.createElement("input")
      field.setAttribute('type',"text");
      field.setAttribute('name','team_id');
      node.appendChild(label);
      node.appendChild(field);
      emails.appendChild(node);
    {% endif %}
    var but = document.createElement("button")
    but.setAttribute("value","Submit")
    but.innerHTML = "Submit"
    emails.appendChild(but)
}
