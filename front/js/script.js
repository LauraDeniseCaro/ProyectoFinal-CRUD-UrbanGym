function validarFormulario() {
  var nombre = document.getElementById("nombre").value;
  var email = document.getElementById("email").value;
  var opcion = document.getElementById("opcion-select").value;
  var foto = document.getElementById("foto").value;
  var asunto = document.getElementById("asunto").value;
  var mensaje = document.getElementsByName("mensaje")[0].value;
  var acepto = document.getElementById("acepto").checked;
  var valido = true;

  // Verificar cada campo individualmente
  if (nombre === '') {
      mostrarError("nombre-error", "Por favor, ingresa tu nombre y apellido.");
      valido = false;
  } else {
      ocultarError("nombre-error");
  }

  if (!validarEmail(email)) {
      mostrarError("email-error", "Por favor, ingresa un correo electrónico válido.");
      valido = false;
  } else {
      ocultarError("email-error");
  }

  if (opcion === '') {
      mostrarError("opcion-error", "Por favor, selecciona tu horario de preferencia.");
      valido = false;
  } else {
      ocultarError("opcion-error");
  }

  if (foto === '') {
      mostrarError("foto-error", "Por favor, sube una foto de tu DNI.");
      valido = false;
  } else {
      ocultarError("foto-error");
  }

  if (asunto === '') {
      mostrarError("asunto-error", "Por favor, ingresa un asunto.");
      valido = false;
  } else {
      ocultarError("asunto-error");
  }

  if (mensaje === '') {
      mostrarError("mensaje-error", "Por favor, ingresa un mensaje.");
      valido = false;
  } else {
      ocultarError("mensaje-error");
  }

  if (!acepto) {
      mostrarError("acepto-error", "Por favor, acepta la política de privacidad.");
      valido = false;
  } else {
      ocultarError("acepto-error");
  }

  // Devolver si el formulario es válido o no
  return valido;
}


function enviarFormulario() {
  if (validarFormulario()) {
    Swal.fire({
        icon: 'success',
        title: '¡Formulario enviado!',
        text: 'El formulario se ha enviado correctamente.',
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById("form").submit();
        }
    });
  } else{
    alert("Por favor completa todos los campos antes de enviar el formulario.")
    return false
  }
}


function mostrarError(id, mensaje) {
  var errorElement = document.getElementById(id);
  errorElement.textContent = mensaje;
  errorElement.style.display = 'block';
}

function ocultarError(id) {
  var errorElement = document.getElementById(id);
  errorElement.textContent = '';
  errorElement.style.display = 'none';
}

function validarEmail(email) {
  // Expresión regular para validar un correo electrónico
  var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}