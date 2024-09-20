// const hamBurger = document.querySelector(".toggle-btn");

// hamBurger.addEventListener("click", function () {
//   document.querySelector("#sidebar").classList.toggle("expand");
// });


const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});

function sendRequest(serviceId) {
    var name = document.getElementById('name' + serviceId).value;
    var contactMethod = document.getElementById('contactMethod' + serviceId).value;
    var contactInfo = document.getElementById('contactInfo' + serviceId).value;
    var description = document.getElementById('description' + serviceId).value;
    var data = {
        'name': name,
        'contactMethod': contactMethod,
        'contactInfo': contactInfo,
        'description': description,
        'serviceId': serviceId
    };

    if (contactMethod === 'WhatsApp') {
        var phone = document.getElementById('phone' + serviceId).value;
        data['phone'] = phone;
    } else if (contactMethod === 'Email') {
        var email = document.getElementById('email' + serviceId).value;
        data['email'] = email;
    }

    // Envoyer les données à votre backend (Django) pour traitement
    // Vous pouvez utiliser AJAX pour cela
    fetch('{% url 'send_service_request' %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            // Traitement si la requête a réussi
            alert('Votre demande a été envoyée avec succès.');
            document.getElementById('exampleModal' + serviceId).modal('hide'); // Fermer la fenêtre modale
        } else {
            // Traitement en cas d'erreur de la requête
            alert('Une erreur s\'est produite lors de l\'envoi de votre demande. Veuillez réessayer.');
        }
    })
    .catch(error => {
        // Traitement en cas d'erreur lors de la requête
        console.error('Erreur lors de l\'envoi de la demande :', error);
        alert('Une erreur s\'est produite lors de l\'envoi de votre demande. Veuillez réessayer.');
    });
}

function showContactFields(serviceId) {
    var contactMethod = document.getElementById('contactMethod' + serviceId).value;
    if (contactMethod === 'WhatsApp') {
        document.getElementById('whatsappFields' + serviceId).style.display = 'block';
        document.getElementById('emailFields' + serviceId).style.display = 'none';
    } else if (contactMethod === 'Email') {
        document.getElementById('whatsappFields' + serviceId).style.display = 'none';
        document.getElementById('emailFields' + serviceId).style.display = 'block';
    }
}
