const userForm = document.getElementById('userForm');
userForm.addEventListener('submit', async e => {
    e.preventDefault()

    const username = userForm['username'].value
    const email = userForm['email'].value
    const password = userForm['password'].value

    const response = await fetch('api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username, 
            email, 
            password
        })
    })

    const newUser = await response.json()
    // console.log(newUser)

    userForm.reset()
})