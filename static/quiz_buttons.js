var audioElement
var timer_button = false

function create_question(JSON_data,correct_answers){
    if(audioElement != null){
        clear_answers();
        audioElement.pause(audioElement);
        audioElement.currentTime = 0;
    }
    var question_number = parseInt(document.getElementById("question_number").innerHTML)
    document.getElementById("question_number").innerHTML = String(question_number+1);

    answers=get_possible_answers(correct_answers[question_number],JSON_data)
    console.log(correct_answers);

    create_timer()

    var table = document.createElement("table");
    table.id = "quiz_table"

    var tr = document.createElement("tr");
    var tr1 = document.createElement("tr");

    button_0 = create_question_button("button_0")
    button_1 = create_question_button("button_1")
    button_2 = create_question_button("button_2")
    button_3 = create_question_button("button_3")

    button_0.onclick = function() {button_press(correct_answers[question_number],"button_0")}
    button_1.onclick = function() {button_press(correct_answers[question_number],"button_1")}
    button_2.onclick = function() {button_press(correct_answers[question_number],"button_2")}
    button_3.onclick = function() {button_press(correct_answers[question_number],"button_3")}


    table.appendChild(tr);
        tr.appendChild(button_0)
        tr.appendChild(button_1)
    table.appendChild(tr1);
        tr1.appendChild(button_2)
        tr1.appendChild(button_3)

    document.body.appendChild(table);

    for( var i=0; i< answers.length; i++){
    button = document.getElementById("button_" + String(i))
    button.innerHTML = answers[i]["name"]
    }

    audioElement = new Audio(correct_answers[question_number]["preview_url"]);
    audioElement.play(audioElement);

    timer_button = false
}

function create_question_button(button_id){
    var td = document.createElement("td");
    var button = document.createElement("button");

    td.className = "quiz_td"
    button.id = button_id
    button.classList.add("answer_button")

    button.onmouseover = function() {document.getElementById(button_id).style.opacity = "0.5"}
    button.onmouseout = function() {document.getElementById(button_id).style.opacity = "1"}
    td.appendChild(button)


    return td
    }

function button_press(correct_answer,button_id){
timer_button = true
console.log(button_id)
if (document.getElementById(button_id).textContent == correct_answer["name"]){
        document.body.style.backgroundColor = "green";
        var text = document.createTextNode("answer is correct");

        var questions_right = parseInt(document.getElementById("questions_right").innerHTML)
        document.getElementById("questions_right").innerHTML = String(questions_right+1);

        var time_score = parseInt(document.getElementById("time_score").innerHTML)
        var this_time_score = parseInt(document.getElementById("curent_time_score").innerHTML)
        document.getElementById("time_score").innerHTML = String(time_score+this_time_score);

}
else {    document.body.style.backgroundColor = "red";
    var text = document.createTextNode("answer is incorrect");
}

var answerdiv = document.createElement("div");
answerdiv.id = "answerdiv"
answerdiv.className = "center_in_div"

var text_box = document.createElement("p");

var Button_for_next = document.createElement("button");
Button_for_next.id = "Button_for_next";
    if (document.getElementById("question_number").innerHTML == 10) {
         Button_for_next.onclick = function() {ending()};
     }
     else{
     Button_for_next.onclick = function() {create_question(JSON_data,correct_answers)};
     }
    var text_for_button = document.createTextNode("Click for next Question");

answerdiv.appendChild(text_box);
text_box.appendChild(text);

answerdiv.appendChild(Button_for_next);
Button_for_next.appendChild(text_for_button);

document.body.appendChild(answerdiv);

clear_table()

}

function create_timer(){
    var conainer = document.getElementById("container");
    var animate_bar = document.createElement("div");

    animate_bar.id = "animate"

    conainer.appendChild(animate_bar);
    document.getElementById("curent_time_score").textContent = 1001

  var elem = document.getElementById("animate");
  var pos = 100;
  var Interval = setInterval(frame, 30);
  function frame() {
    if (pos <= 0.0 || timer_button == true) {
      clearInterval(Interval);
    } else {
      pos = pos-0.1;
      document.getElementById("curent_time_score").textContent = Math.round(pos*10)+1
      elem.style.width = pos + "%";
    }
  }

}

function clear_table(){
    var quiz_table = document.getElementById("quiz_table");
    var quiz_header = document.getElementById("animate");

    quiz_header.remove();
    quiz_table.remove();
}

function clear_answers(){
    document.body.style.backgroundColor = 'rgba(0,0,0,0)';
    var answerdiv = document.getElementById("answerdiv");
    answerdiv.remove()

}

function ending(){
    clear_answers();
    document.getElementById("timer").remove();
    audioElement.pause(audioElement);

    document.getElementById("container").style.height = "100%";

    var btn = document.createElement("BUTTON");
    var text_for_btn = document.createTextNode("Click to play again");
    btn.appendChild(text_for_btn);
    btn.onclick = function() {window.location = "/select_type"}

    document.getElementById("score_box").appendChild(btn);
}