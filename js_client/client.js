const loginform = document.getElementById('login-form')
const baseEndpoint = "http://localhost:8000/api"
if (loginform) {

    loginform.addEventListener('submit' , handleLogin)

}

function handleLogin(event) {
    console.log(event)
    event.preventDefault()
    const LoginEndPoint = `${baseEndpoint}/token/`

    let loginFormData = new FormData(loginform)
    let loginObjectData = Object.fromEntries(loginFormData)
    let bodyStr = JSON.stringify(loginObjectData)

    const options = {
        method : "POST",
        headers: {
            "Content-Type": "application/json"  // Fixed the typo here
        },
        body: bodyStr
    }

    fetch(LoginEndPoint , options)

    .then(response=>
        {
            console.log(response)
            return response.json
        }
        )
    
    .then(x=>{
        console.log(x)
    })

    .catch(err=>{
        console.log(err)
    })
}