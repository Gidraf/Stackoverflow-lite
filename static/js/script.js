
//this module is intented to run web js script

//init ask_question modal
var question_modal =document.getElementById('question_modal')
// init downvote button
var downvote_btn = document.getElementById("votes");
var isopen=false;
// init ask questio button
var ask_question=document.getElementById('ask_question');

// init answers votes
var votes=0

// initialize the cancel button
var cancel=document.getElementById('cancel');

// display the question_modal when clicked
function open_model () {
  question_modal.classList.toggle('question_modal')
}

function vote_downvote()
{
  votes--
  downvote_btn.textContent=votes + " votes";

}

function vote_upvote(){
  votes++
  downvote_btn.textContent=votes + " votes";
}


//closes the question_modal on cancel clicked

function close_modal(){
  question_modal.classList.toggle('question_modal')
};

//close the question_modal if the user closes otside the question_modal
window.onclick= function (event) {
  if(event.target==question_modal){
    question_modal.classList.toggle('question_modal')
  }
}
