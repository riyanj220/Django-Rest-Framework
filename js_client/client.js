const contentContainer = document.getElementById('content-container')

const loginform = document.getElementById('login-form');
const searchform = document.getElementById('search-form');

const baseEndpoint = "http://localhost:8000/api";

if (loginform) {
    loginform.addEventListener('submit', handleLogin);
}

if (searchform) {
    searchform.addEventListener('submit', handleSearch);
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

function handleSearch(event) {
    event.preventDefault();

    let formData = new FormData(searchform);
    let data = Object.fromEntries(formData);
    let searchParams = new URLSearchParams(data)

    const endpoint = `${baseEndpoint}/search/?${searchParams}`; // Fixed string interpolation

    const headers = {
        "Content-Type": "application/json", 
    }
    const authToken = localStorage.getItem('access')
    if(authToken){
        headers['Authorization'] = `Bearer ${authToken}`
    } 

    const options = {
        method: "GET",
        headers: headers,
    };

    fetch(endpoint, options)
        .then(response => response.json())  // Call .json() to parse the response
        .then(data=>{
            writeToContainer(data)
        })
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

const searchClient = algoliasearch('KZF6TKL69O', '3564646201b0dd359a76b31833a22553');

const search = instantsearch({
  indexName: 'cfe_Product',
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
  }),

  instantsearch.widgets.clearRefinements({
    container:"#clear-refinemets",
  }),

  instantsearch.widgets.refinementList({
    container:"#user-list",
    attribute: 'user'
  }),

  instantsearch.widgets.hits({
    container: '#hits',
    templates: {
        item: `<div>{{title}}<p>{{user}}</p><p>\${{price}}</p></div>`
    }
  })
]);

search.start();
