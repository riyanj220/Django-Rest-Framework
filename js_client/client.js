const contentContainer = document.getElementById('content-container')

const loginform = document.getElementById('login-form');
const baseEndpoint = "http://localhost:8000/api";
if (loginform) {
    loginform.addEventListener('submit', handleLogin);
}

function handleLogin(event) {
    event.preventDefault();
    const LoginEndPoint = `${baseEndpoint}/token/`; // Fixed string interpolation

    let loginFormData = new FormData(loginform);
    let loginObjectData = Object.fromEntries(loginFormData);
    let bodyStr = JSON.stringify(loginObjectData);

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"  // Content type is set to JSON
        },
        body: bodyStr
    };

    fetch(LoginEndPoint, options)
        .then(response => response.json())  // Call .json() to parse the response
        .then(authData=>{
            handleAuthData(authData , getProductList)})
        .catch(err => {
            console.log(err);
        });
}

function handleAuthData(authData , callback) {
    // Check if authData contains access and refresh tokens
    if (authData.access && authData.refresh ) {
        localStorage.setItem('access', authData.access);
        localStorage.setItem('refresh', authData.refresh);
        callback()
    } else {
        console.error('No tokens received', authData);
    }
}

function writeToContainer(data) {
    if(contentContainer){
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data,null,4) + "</pre>"
    }
}

function getFetchOptions(method,body){
    return {
        method: method === null? "GET": method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('access')}`
        },
        body: body? body:null
    }
}

function isTokenNotValid(jsonData){
    if(jsonData.code && jsonData.code == "token_not_valid"){
        alert("Please Login Again! ")

        return false
    }
    return true
}

function getProductList(){
    const endpoint = `${baseEndpoint}/products/list/`;
    const options = getFetchOptions()

    fetch(endpoint, options)
    .then(response=>{
        return response.json()

    })
    .then(data=> {
        const validData= isTokenNotValid(data)
        if(validData){
            writeToContainer(data)
        }
    })
}
getProductList()