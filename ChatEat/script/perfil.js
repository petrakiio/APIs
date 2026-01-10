function deletar(){
    if(!confirm('Tem certeza que quer deletar sua conta?'))return
    fetch('/deletar',{
        method:'POST'
    }).then(res =>{
        if (res.ok){
            window.location.href='/'
        }else{
            alert('Erro ao deletar conta!')
        }
    })
}