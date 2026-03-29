// =============================================
// validacion.js
// Validaciones del formulario de registro
// usando jQuery Validation Plugin
// =============================================

$(function () {

  // ------------------------------------------
  // MÉTODOS PERSONALIZADOS
  // ------------------------------------------

  // Validación: contraseña fuerte
  // Reglas: 6-18 caracteres, al menos 1 mayúscula,
  // al menos 1 número, al menos 1 carácter especial
  $.validator.addMethod(
    'passFuerte',
    function (value) {
      const longitud  = value.length >= 6 && value.length <= 18;
      const mayuscula = /[A-ZÁÉÍÓÚÑ]/.test(value);
      const numero    = /\d/.test(value);
      const especial  = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(value);
      return longitud && mayuscula && numero && especial;
    },
    'La contraseña debe tener 6–18 caracteres e incluir al menos: 1 mayúscula, 1 número y 1 carácter especial (!@#$...).'
  );

  // Validación: edad mínima 13 años
  $.validator.addMethod(
    'mayor13',
    function (value) {
      if (!value) return false;
      const hoy  = new Date();
      const fecha = new Date(value + 'T00:00:00');
      if (isNaN(fecha)) return false;
      let edad = hoy.getFullYear() - fecha.getFullYear();
      const mes = hoy.getMonth() - fecha.getMonth();
      if (mes < 0 || (mes === 0 && hoy.getDate() < fecha.getDate())) edad--;
      return edad >= 13;
    },
    'Debes tener al menos 13 años para registrarte.'
  );

  // Validación: username sin espacios
  $.validator.addMethod(
    'sinEspacios',
    function (value) {
      return !/\s/.test(value);
    },
    'El nombre de usuario no puede contener espacios.'
  );

  // ------------------------------------------
  // INICIALIZACIÓN DEL VALIDADOR
  // ------------------------------------------
  $('#formRegistro').validate({

    // Apariencia integrada con Bootstrap
    errorClass:   'is-invalid',
    validClass:   'is-valid',
    errorElement: 'div',

    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');
      // Si el input está dentro de un input-group (ej: contraseña con botón)
      if (element.parent('.input-group').length) {
        error.insertAfter(element.parent());
      } else {
        error.insertAfter(element);
      }
    },

    highlight: function (element) {
      $(element).addClass('is-invalid').removeClass('is-valid');
    },

    unhighlight: function (element) {
      $(element).removeClass('is-invalid').addClass('is-valid');
    },

    // ------------------------------------------
    // REGLAS
    // ------------------------------------------
    rules: {
      nombreCompleto: {
        required:  true,
        minlength: 3
      },
      username: {
        required:   true,
        minlength:  3,
        maxlength:  20,
        sinEspacios: true
      },
      email: {
        required: true,
        email:    true
      },
      password: {
        required:   true,
        passFuerte: true
      },
      confirmPassword: {
        required: true,
        equalTo:  '#password'
      },
      fechaNacimiento: {
        required: true,
        mayor13:  true
      }
      // direccion: sin reglas (es opcional)
    },

    // ------------------------------------------
    // MENSAJES
    // ------------------------------------------
    messages: {
      nombreCompleto: {
        required:  'El nombre completo es obligatorio.',
        minlength: 'Debe tener al menos 3 caracteres.'
      },
      username: {
        required:  'El nombre de usuario es obligatorio.',
        minlength: 'Mínimo 3 caracteres.',
        maxlength: 'Máximo 20 caracteres.'
      },
      email: {
        required: 'El correo electrónico es obligatorio.',
        email:    'Ingresa un correo con formato válido (ej: usuario@correo.com).'
      },
      password: {
        required: 'La contraseña es obligatoria.'
      },
      confirmPassword: {
        required: 'Debes repetir la contraseña.',
        equalTo:  'Las contraseñas no coinciden.'
      },
      fechaNacimiento: {
        required: 'La fecha de nacimiento es obligatoria.'
      }
    },

    // ------------------------------------------
    // ENVÍO EXITOSO
    // ------------------------------------------
    submitHandler: function (form, event) {
      event.preventDefault();
      alert('✅ Registro completado correctamente.\n\nTodos los campos son válidos.');
      form.reset();
      // Limpia los estados visuales de Bootstrap
      $('.is-valid, .is-invalid').removeClass('is-valid is-invalid');
    }

  });

  // ------------------------------------------
  // UX: evitar pegar en "repetir contraseña"
  // ------------------------------------------
  $('#confirmPassword').on('paste', function (e) {
    e.preventDefault();
  });

});