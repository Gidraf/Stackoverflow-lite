
var question_modal =document.getElementById('question_modal')

var isopen=false;

var ask_question=document.getElementById('ask_question');

var cancel=document.getElementById('cancel');

function open_model () {
  question_modal.classList.toggle('question_modal')
}

function close_modal(){
  question_modal.classList.toggle('question_modal')
};

window.onclick= function (event) {
  if(event.target==question_modal){
    question_modal.classList.toggle('question_modal')
  }
}
