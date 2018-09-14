// this script will handle scripts for users
const register_url = "https://stackoverflowgidraf.herokuapp.com/auth/register";

function register_user(e,form)
{
  e.preventDefault();  // prevent form from submiting

  fetch(register_url,{
    method: 'POST',
    body : {"username": form.username, "useremail":form.email,"password":form.password},
    Access-Control-Allow-Origin:*,
    Access-Control-Allow-Methods: 'HEAD, GET, POST, PUT, PATCH, DELETE',
    Access-Control-Allow-Headers: 'Origin, Content-Type, X-Auth-Token',
    headers : {"content-type":"application/json; charset = UTF-8"}
  }).then(function (response){
    console.log(response.json())
  })
}
