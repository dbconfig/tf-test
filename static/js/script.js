$.notify = function (text, type = 'info', duration = 10000, close = true) {
    switch (type) {
        case 'success':
            color = '#56ab2f' // green
            break
        case 'error':
            color = '#DA4453' // red
            break
    }
    Toastify({ text: text, duration: duration, close: close, backgroundColor: color }).showToast();
}
function ajaxResponse(r) {
    if (r.success) {
        if (r.action == 'register' || r.action == 'login') {
            location.reload()
        }
        else {
            if (r.message) {
                $.notify(r.message, 'success')
            }
        }
    } else {
        $.notify(r.message, 'error')
    }
}


function addSkill() {
    val = $('#skills-input').val()
    $('#skills').append('<div class="badge badge-secondary skill">' + val + ' <i class="bi bi-x cl" onclick="detachSkill(event)"></i></div> ')
    $('#skills-input').val('')
}

function detachSkill(e) {
    $(e.target).parent().detach()
}


function saveResume() {
    name = $('#name').val()
    hobbies = $('#hobbies').val()
    languages = []
    $('input:checked').each(function () {
        languages.push($(this).attr('data-lang'))
    })
    console.log(languages)
    skills = []
    $('.skill').each(function () {
        text = $(this).text()

        if (text && text != '')
            skills.push(text)
    })
    console.log(skills)

    $.ajax({
        url: '/api/resume/',
        type: 'PUT',
        headers: { "X-CSRFToken": $.cookie('csrftoken') },
        contentType: 'application/json',
        data: JSON.stringify({
            'name': name,
            'hobbies': hobbies,
            'languages': languages,
            'skills': skills,
        }),
        cache: false,
        async: false,
        success: function (r) {
            ajaxResponse(r)
        }, error: function (r) {
            ajaxResponse(JSON.parse(r.responseText))
        }
    })
}


window.onload = function () {

    $("form[ajax=true]").submit(function (e) {

        e.preventDefault()

        var form_data = $(this).serialize()
        var form_url = $(this).attr("action")
        var form_method = $(this).attr("method").toUpperCase()

        $.ajax({
            url: form_url,
            type: form_method,
            data: form_data,
            cache: false,
            async: false,
            success: function (r) {
                ajaxResponse(r)
            }, error: function (r) {
                console.log(JSON.parse(r.responseText))
                ajaxResponse(JSON.parse(r.responseText))
            }
        })
    })
}