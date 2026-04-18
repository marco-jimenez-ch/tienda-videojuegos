// =============================================
// validacion.js
// Validaciones centralizadas de todos los
// formularios usando jQuery Validation Plugin
// =============================================

$(function () {

  // ------------------------------------------
  // MÉTODOS PERSONALIZADOS (compartidos)
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
      const hoy   = new Date();
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
  // FORMULARIO: REGISTRO
  // ------------------------------------------
  $('#formRegistro').validate({

    errorClass:   'is-invalid',
    validClass:   'is-valid',
    errorElement: 'div',

    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');
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

    rules: {
      nombreCompleto: {
        required:  true,
        minlength: 3
      },
      username: {
        required:    true,
        minlength:   3,
        maxlength:   20,
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
    },

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

    submitHandler: function (form, event) {
      event.preventDefault();
      alert('✅ Registro completado correctamente.\n\nTodos los campos son válidos.');
      form.reset();
      $('.is-valid, .is-invalid').removeClass('is-valid is-invalid');
    }

  });

  // UX: evitar pegar en "repetir contraseña"
  $('#confirmPassword').on('paste', function (e) {
    e.preventDefault();
  });

  // ------------------------------------------
  // FORMULARIO: LOGIN
  // ------------------------------------------
  $('#formLogin').validate({

    errorClass:   'is-invalid',
    validClass:   'is-valid',
    errorElement: 'div',

    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');
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

    rules: {
      loginEmail:    { required: true, email: true },
      loginPassword: { required: true }
    },

    messages: {
      loginEmail: {
        required: 'El correo es obligatorio.',
        email:    'Ingresa un correo válido.'
      },
      loginPassword: {
        required: 'La contraseña es obligatoria.'
      }
    },

    submitHandler: function (form, event) {
      event.preventDefault();
      // La lógica real de login la manejará Django
    }

  });

  // ------------------------------------------
  // FORMULARIO: RECUPERAR CONTRASEÑA (paso 1)
  // ------------------------------------------
  $('#formRecuperar').validate({

    errorClass:   'is-invalid',
    validClass:   'is-valid',
    errorElement: 'div',

    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');
      error.insertAfter(element);
    },

    highlight: function (el) {
      $(el).addClass('is-invalid').removeClass('is-valid');
    },

    unhighlight: function (el) {
      $(el).removeClass('is-invalid').addClass('is-valid');
    },

    rules: {
      emailRecuperar: { required: true, email: true }
    },

    messages: {
      emailRecuperar: {
        required: 'El correo es obligatorio.',
        email:    'Ingresa un correo con formato válido.'
      }
    },

    submitHandler: function (form, event) {
      event.preventDefault();
      const correo = $('#emailRecuperar').val();
      $('#mensajeConfirmacion').text('Hemos enviado las instrucciones a ' + correo + '.');
      $('#pasoEmail').hide();
      $('#pasoConfirmacion').show();

      // Simula que tras 3 segundos aparece el formulario de nueva contraseña
      setTimeout(function () {
        $('#pasoConfirmacion').hide();
        $('#pasaNuevaPassword').show();
      }, 3000);
    }

  });

  // ------------------------------------------
  // FORMULARIO: NUEVA CONTRASEÑA (paso 3)
  // ------------------------------------------
  $('#formNuevaPassword').validate({

    errorClass:   'is-invalid',
    validClass:   'is-valid',
    errorElement: 'div',

    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');
      if (element.parent('.input-group').length) {
        error.insertAfter(element.parent());
      } else {
        error.insertAfter(element);
      }
    },

    highlight: function (el) {
      $(el).addClass('is-invalid').removeClass('is-valid');
    },

    unhighlight: function (el) {
      $(el).removeClass('is-invalid').addClass('is-valid');
    },

    rules: {
      nuevaPassword:  { required: true, passFuerte: true },
      confirmarNueva: { required: true, equalTo: '#nuevaPassword' }
    },

    messages: {
      nuevaPassword: {
        required: 'Ingresa tu nueva contraseña.'
      },
      confirmarNueva: {
        required: 'Repite la nueva contraseña.',
        equalTo:  'Las contraseñas no coinciden.'
      }
    },

    submitHandler: function (form, event) {
      event.preventDefault();
      $('#pasaNuevaPassword').html(`
        <div class="form-card">
          <div class="card-body p-4 text-center">
            <div style="font-size: 3rem; margin-bottom: 12px;">✅</div>
            <h3 style="margin-bottom: 8px;">Contraseña actualizada</h3>
            <p style="color: var(--muted);">Tu contraseña fue cambiada exitosamente.</p>
            <div class="mt-4">
              <a href="login.html" class="btn btn-primary">Ir al login</a>
            </div>
          </div>
        </div>
      `);
    }

  });

  // Toggle nueva contraseña en recuperar
  $('#toggleNueva').on('click', function () {
    const pwd = $('#nuevaPassword');
    const isPassword = pwd.attr('type') === 'password';
    pwd.attr('type', isPassword ? 'text' : 'password');
    $(this).text(isPassword ? 'Ocultar' : 'Mostrar');
  });

});
