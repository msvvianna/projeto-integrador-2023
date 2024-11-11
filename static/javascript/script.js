function navclick(focus) {
    const element = document.querySelectorAll(".nav-item")
    element.forEach(function (item) {
        let comparacao = item.getElementsByTagName("a")[0].href
        if (item.style.borderBottom !== "") {
            item.style.borderBottom = ""
        }
        if (comparacao === focus.getElementsByTagName("a")[0].href) {
            item.style.borderBottom = "3px solid orange"
        }
    })
}

function collapse() {
    const element = document.getElementById("mobile_menu")
    const icon = document.getElementById("mobile_btn")
    if (element.style.left === "-100vw" || element.style.left === "") {
        element.style.left = "0"
        icon.className = "fa-solid fa-xmark"
    } else {
        element.style.left = "-100vw"
        icon.className = "fa-solid fa-bars"
    }
}

function effect() {
    const scroll = window.scrollY
    const element = document.querySelectorAll(".nav-item")
    if (scroll > 92) {
        document.getElementsByTagName("header")[0].style.backgroundColor = "var(--color-primary-1)"
    } else {
        document.getElementsByTagName("header")[0].style.backgroundColor = "transparent"
    }
    element.forEach(function (item) {
        let focus = item.getElementsByTagName("a")[0].href
        let position = document.getElementById(focus.substring(focus.search(/#/) + 1))
        if (scroll >= position.getBoundingClientRect().top) {
            navclick(item)
        }
    })
}

function formulario(focus) {
    const element = document.getElementById(focus)
    const outhers = document.querySelectorAll(".page")
    const header = document.getElementsByTagName("header")[0]
    const body = document.getElementsByTagName("body")[0]
    const icons = document.querySelectorAll(".nav-buttons")[0].querySelectorAll(".fa-solid")

    const voltar = document.getElementById("voltar")
    outhers.forEach(function (item) {
        item.style.display = "none"
    })

    switch (focus) {
        case 'cadastro':
            voltar.onclick = function () {
                formulario('login')
            }
            break;
        case 'esqueci_senha':
            voltar.onclick = function () {
                formulario('login')
            }
            break;
        default:
            voltar.onclick = function () {
                formulario()
            }
    }

    if (focus == null || focus === "") {
        body.style.overflowY = ""
        if (window.innerWidth <= 1080) {
            icons.forEach(function (i) {
                i.style.display = "block"
                if (i.classList.contains("fa-arrow-right-from-bracket")) {
                    i.style.display = "none"
                }
            })
            voltar.style.display = "none"
            header.style.backgroundColor = "transparent"
        }
    } else {
        if (element.style.display === null || element.style.display === "none") {
            element.style.display = "flex"
            if (window.innerWidth <= 1080) {
                icons.forEach(function (i) {
                    i.style.display = "none"
                })
                voltar.style.display = "block"
                header.style.backgroundColor = "white"
            }
        }
        body.style.overflowY = "hidden"
    }

    document.querySelectorAll(".current").forEach(function (current) {
        current.style = "background: black !important; color: white !important; font-weight: 800; border: none"
    })
}

$(document).ready(function () {
    $.ajax({
        url: '/consulta_usuario',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            for (let i = 0; i < data.length; i++) {
                let row = "<tr>";
                row += "<td style='width: 200px'>" + data[i].nome + "</td>";
                row += "<td>" + data[i].email + "</td>";
                row += "<td>" + data[i].telefone + "</td>";
                row += "<td>" +
                    "<div style='width: auto; display: flex; flex-wrap: nowrap; gap: 8px; justify-content: center'>" +
                    "<button class='btn-default btn-deletar' style='width: 40px; background-color: red; color: white' data-id='" + data[i].email + "'><i class=\"fa-solid fa-trash\"></i></button>" +
                    "</div>" +
                    "</td>";
                row += "</tr>";
                $("#data-table tbody").append(row);
            }

            $("#data-table").DataTable({
                info: false
            });

            $('.btn-deletar').on('click', function () {
                const email = $(this).data('id');
                if (confirm('Tem certeza que deseja excluir este usuario?')) {
                    $.ajax({
                        url: '/delete_usuario/' + email,
                        type: 'POST',
                        success: function (response) {
                            if (response.success) {
                                location.reload();
                            } else {
                                alert('Erro ao excluir usuario.');
                            }
                        }
                    });
                }
            });
        },
        error: function () {
            alert('Erro ao buscar dados do usuario.');
        }
    });
});
let type = "user"
$(document).ready(function () {
    $.ajax({
        url: '/consulta_agendamento/' + type,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (type === "user") {
                for (let i = 0; i < data.length; i++) {
                    let row = "<tr>";
                    row += "<td>" + data[i].servico + "</td>";
                    row += "<td style='width: 200px'>" + data[i].data + "</td>";
                    row += "<td style='width: 100px'>" + data[i].preco + "</td>";
                    row +=
                        "<td>" +
                        "<div style='width: auto; display: flex; flex-wrap: nowrap; gap: 8px; justify-content: center'>" +
                        "<button class='btn-default btn-deletar-ag' style='width: 40px; background-color: red; color: white' data-id='" + data[i].id + "'><i class=\"fa-solid fa-trash\"></i></button>" +
                        "</div>" +
                        "</td>";

                    row += "</tr>";
                    $("#data-table-ag tbody").append(row);
                }
            } else {
                for (let i = 0; i < data.length; i++) {
                    let row = "<tr>";
                    row += "<td style='width: 200px'>" + data[i].nome + "</td>";
                    row += "<td>" + data[i].email + "</td>";
                    row += "<td>" + data[i].telefone + "</td>";
                    row += "<td>" + data[i].servico + "</td>";
                    row += "<td style='width: 200px'>" + data[i].data + "</td>";
                    row +=
                        "<td>" +
                        "<div style='width: auto; display: flex; flex-wrap: nowrap; gap: 8px; justify-content: center'>" +
                        "<button class='btn-default btn-deletar-ag' style='width: 40px; background-color: red; color: white' data-id='" + data[i].id + "'><i class=\"fa-solid fa-trash\"></i></button>" +
                        "</div>" +
                        "</td>";

                    row += "</tr>";
                    $("#data-table-ag tbody").append(row);
                }
            }


            $("#data-table-ag").DataTable({
                info: false
            });

            $('.btn-deletar-ag').on('click', function () {
                const id = $(this).data('id');
                if (confirm('Tem certeza que deseja excluir este agendamento?')) {
                    $.ajax({
                        url: '/delete_ag/' + id,
                        type: 'POST',
                        success: function (response) {
                            if (response.success) {
                                location.reload();
                            } else {
                                alert('Erro ao excluir o agendamento.');
                            }
                        }
                    });
                }
            });
        }
    });
});

$(document).ready(function () {
    $.ajax({
        url: '/consulta_servicos_precos',
        type: 'POST',
        dataType: 'json',
        success: function (produtos_list) {
            for (let i = 0; i < produtos_list.length; i++) {
                let row = "<tr>";
                row += "<td style='width: 250px'>" + produtos_list[i].produto + "</td>";
                row += "<td style='width: 110px'>" + produtos_list[i].preco + "</td>";
                row += "<td>" +
                    "<div style='width: auto; display: flex; flex-wrap: nowrap; gap: 8px; justify-content: center'>" +
                    "<button class='btn-default btn-deletar-ps' style='width: 40px; background-color: red; color: white' data-id='" + produtos_list[i].id + "'><i class=\"fa-solid fa-trash\"></i></button>" +
                    "</div>" +
                    "</td>";
                row += "</tr>";
                $("#data-table-ps tbody").append(row);
            }

            $("#data-table-ps").DataTable({
                info: false
            });

            $('.btn-deletar-ps').on('click', function () {
                const id = $(this).data('id');
                if (confirm('Tem certeza que deseja excluir este serviço?')) {
                    $.ajax({
                        url: '/delete_ps/' + id,
                        type: 'POST',
                        success: function (response) {
                            if (response.success) {
                                location.reload();
                            } else {
                                alert('Erro ao excluir esse serviço.');
                            }
                        }
                    });
                }
            });
        },
    });
});

$(document).ready(function () {
    $.ajax({
        url: '/consulta_datahora',
        type: 'POST',
        dataType: 'json',
        success: function (datahora_list) {
            for (let i = 0; i < datahora_list.length; i++) {
                let row = "<tr>";
                row += "<td style='width: 250px'>" + datahora_list[i].datahora + "</td>";
                row += "<td>" +
                    "<div style='width: auto; display: flex; flex-wrap: nowrap; gap: 8px; justify-content: center'>" +
                    "<button class='btn-default btn-deletar-dh' style='width: 40px; background-color: red; color: white' data-id='" + datahora_list[i].id + "'><i class=\"fa-solid fa-trash\"></i></button>" +
                    "</div>" +
                    "</td>";
                row += "</tr>";
                $("#data-table-dh tbody").append(row);
            }

            $("#data-table-dh").DataTable({
                info: false
            });

            $('.btn-deletar-dh').on('click', function () {
                const id = $(this).data('id');
                if (confirm('Tem certeza que deseja excluir esta data?')) {
                    $.ajax({
                        url: '/delete_dh/' + id,
                        type: 'POST',
                        success: function (response) {
                            if (response.success) {
                                location.reload();
                            } else {
                                alert('Erro ao excluir a data.');
                            }
                        }
                    });
                }
            });
        },
    });
});
