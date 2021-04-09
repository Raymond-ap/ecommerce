const payment = document.querySelector('.payment')
async function contactAPI(url,body){
    const response=await fetch(url,{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken": csrftoken,
        },
        body:JSON.stringify(body)
    })

    return response.json()
}


payment.addEventListener('click', e => {
    product = 'gh'
    let url = '/payment/'

    data = {
        product
    }
    
    if (user) {
        contactAPI(url,data).then(res => {
            if (res['payment_url']) {
                window.location.href = res['payment_url']
            } else {
                console.log('Error')
            }
        }).catch(e => {
            console.log(e)
        })
    }
})