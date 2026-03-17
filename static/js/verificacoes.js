// var nome = prompt("Como você chama?")
//
// if (nome == null) {
//     alert("Recarregue a página!")
// }
//
// else {
//     let correto = confirm("Você se chama " + nome + "?")
// }
//
// if (correto) {
//     alert( nome + " , bem vindo ao site de cursos!")
// }
//
// else {
//     alert("Recarregue a página!")
// }

function limpaInputsLogin() {
    const inputEmail = document.getElementById('input-email')
    const inputSenha = document.getElementById('input-senha')

    inputEmail.value = ''
    inputSenha.value = ''
}

function limpaInputsModal() {
    const inputNome = document.getElementById('input-nome')
    const inputNascimento = document.getElementById('input-nascimento')
    const inputCpf = document.getElementById('input-cpf')
    const inputEmail2 = document.getElementById('input-email2')
    const inputSenha2 = document.getElementById('input-senha2')
    const inputCargo = document.getElementById('input-cargo')
    const inputSalario = document.getElementById('input-salario')

    inputNome.value = ''
    inputNascimento.value = ''
    inputCpf.value = ''
    inputEmail2.value = ''
    inputSenha2.value = ''
    inputCargo.value = ''
    inputSalario.value = ''
}

document.addEventListener("DOMContentLoaded", function () {

    const formLogin = document.getElementById('form-login')
    formLogin.addEventListener("submit", function (event) {
        // Pegar os dois inputs do formulário
        const inputEmail = document.getElementById('input-email')
        const inputSenha = document.getElementById('input-senha')

        let temErro = false

        // Verificar se os inputs estão vazios
        if (inputEmail.value === '') {
            inputEmail.classList.add('is-invalid')
            temErro = true
        } else {
            inputEmail.classList.remove('is-invalid')
        }

        if (inputSenha.value === '') {
            inputSenha.classList.add('is-invalid')
            temErro = true
        } else {
            inputSenha.classList.remove('is-invalid')
        }

        if (temErro) {
            // Evita de enviar o form
            event.preventDefault()
            alert("Preencha todos os campos")
        }
    })

    const formModal = document.getElementById('form-modal')
    formModal.addEventListener("submit", function (event) {
        // Pegar os inputs do formulário
        const inputNome = document.getElementById('input-nome')
        const inputNascimento = document.getElementById('input-nascimento')
        const inputCpf = document.getElementById('input-cpf')
        const inputEmail2 = document.getElementById('input-email2')
        const inputSenha2 = document.getElementById('input-senha2')
        const inputCargo=document.getElementById('input-cargo')
        const inputSalario = document.getElementById('input-salario')

        let temErro = false

        // Verificar se os inputs estão vazios
        if (inputNome.value === '') {
            inputNome.classList.add('is-invalid')
            temErro = true
        } else {
            inputNome.classList.remove('is-invalid')
        }

        if (inputNascimento.value === '') {
            inputNascimento.classList.add('is-invalid')
            temErro = true
        } else {
            inputNascimento.classList.remove('is-invalid')
        }

        if (inputCpf.value === '') {
            inputCpf.classList.add('is-invalid')
            temErro = true
        } else {
            inputCpf.classList.remove('is-invalid')
        }

        if (inputEmail2.value === '') {
            inputEmail2.classList.add('is-invalid')
            temErro = true
        } else {
            inputEmail2.classList.remove('is-invalid')
        }

        if (inputSenha2.value === '') {
            inputSenha2.classList.add('is-invalid')
            temErro = true
        } else {
            inputSenha2.classList.remove('is-invalid')
        }

        if (inputCargo.value === '') {
            inputCargo.classList.add('is-invalid')
            temErro = true
        } else {
            inputCargo.classList.remove('is-invalid')
        }

        if (inputSalario.value === '') {
            inputSalario.classList.add('is-invalid')
            temErro = true
        } else {
            inputSalario.classList.remove('is-invalid')
        }
    })
})

