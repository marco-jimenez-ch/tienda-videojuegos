// =============================================
// validacion.js
// Validaciones centralizadas de todos los
// formularios usando jQuery Validation Plugin
// =============================================

$(function () {

  // ------------------------------------------
  // MÉTODOS PERSONALIZADOS (compartidos)
  // ------------------------------------------

  $.validator.addMethod('passFuerte', function (value) {
    const longitud  = value.length >= 6 && value.length <= 18;
    const mayuscula = /[A-ZÁÉÍÓÚÑ]/.test(value);
    const numero    = /\d/.test(value);
    const especial  = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(value);
    return longitud && mayuscula && numero && especial;
  }, 'La contraseña debe tener 6–18 caracteres e incluir al menos: 1 mayúscula, 1 número y 1 carácter especial (!@#$...).');

  $.validator.addMethod('mayor13', function (value) {
    if (!value) return false;
    const hoy   = new Date();
    const fecha = new Date(value + 'T00:00:00');
    if (isNaN(fecha)) return false;
    let edad = hoy.getFullYear() - fecha.getFullYear();
    const mes = hoy.getMonth() - fecha.getMonth();
    if (mes < 0 || (mes === 0 && hoy.getDate() < fecha.getDate())) edad--;
    return edad >= 13;
  }, 'Debes tener al menos 13 años para registrarte.');

  $.validator.addMethod('sinEspacios', function (value) {
    return !/\s/.test(value);
  }, 'El nombre de usuario no puede contener espacios.');

  // ------------------------------------------
  // FORMULARIO: REGISTRO
  // ------------------------------------------
  $('#formRegistro').validate({
    errorClass: 'is-invalid', validClass: 'is-valid', errorElement: 'div',
    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');
      if (element.parent('.input-group').length) { error.insertAfter(element.parent()); }
      else { error.insertAfter(element); }
    },
    highlight:   function (el) { $(el).addClass('is-invalid').removeClass('is-valid'); },
    unhighlight: function (el) { $(el).removeClass('is-invalid').addClass('is-valid'); },
    rules: {
      nombreCompleto:  { required: true, minlength: 3 },
      username:        { required: true, minlength: 3, maxlength: 20, sinEspacios: true },
      email:           { required: true, email: true },
      password:        { required: true, passFuerte: true },
      confirmPassword: { required: true, equalTo: '#password' },
      fechaNacimiento: { required: true, mayor13: true }
    },
    messages: {
      nombreCompleto:  { required: 'El nombre completo es obligatorio.', minlength: 'Debe tener al menos 3 caracteres.' },
      username:        { required: 'El nombre de usuario es obligatorio.', minlength: 'Mínimo 3 caracteres.', maxlength: 'Máximo 20 caracteres.' },
      email:           { required: 'El correo electrónico es obligatorio.', email: 'Ingresa un correo con formato válido.' },
      password:        { required: 'La contraseña es obligatoria.' },
      confirmPassword: { required: 'Debes repetir la contraseña.', equalTo: 'Las contraseñas no coinciden.' },
      fechaNacimiento: { required: 'La fecha de nacimiento es obligatoria.' }
    },
    submitHandler: function (form, event) {
      event.preventDefault();
      alert('Registro completado correctamente.');
      form.reset();
      $('.is-valid, .is-invalid').removeClass('is-valid is-invalid');
    }
  });
  $('#confirmPassword').on('paste', function (e) { e.preventDefault(); });

  // ------------------------------------------
  // FORMULARIO: LOGIN
  // ------------------------------------------
  $('#formLogin').validate({
    errorClass: 'is-invalid', validClass: 'is-valid', errorElement: 'div',
    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');
      if (element.parent('.input-group').length) { error.insertAfter(element.parent()); }
      else { error.insertAfter(element); }
    },
    highlight:   function (el) { $(el).addClass('is-invalid').removeClass('is-valid'); },
    unhighlight: function (el) { $(el).removeClass('is-invalid').addClass('is-valid'); },
    rules: {
      loginEmail:    { required: true, email: true },
      loginPassword: { required: true }
    },
    messages: {
      loginEmail:    { required: 'El correo es obligatorio.', email: 'Ingresa un correo válido.' },
      loginPassword: { required: 'La contraseña es obligatoria.' }
    },
    submitHandler: function (form, event) { event.preventDefault(); }
  });

  // ------------------------------------------
  // FORMULARIO: RECUPERAR CONTRASEÑA
  // ------------------------------------------
  $('#formRecuperar').validate({
    errorClass: 'is-invalid', validClass: 'is-valid', errorElement: 'div',
    errorPlacement: function (error, element) { error.addClass('invalid-feedback'); error.insertAfter(element); },
    highlight:   function (el) { $(el).addClass('is-invalid').removeClass('is-valid'); },
    unhighlight: function (el) { $(el).removeClass('is-invalid').addClass('is-valid'); },
    rules:    { emailRecuperar: { required: true, email: true } },
    messages: { emailRecuperar: { required: 'El correo es obligatorio.', email: 'Ingresa un correo con formato válido.' } },
    submitHandler: function (form, event) {
      event.preventDefault();
      const correo = $('#emailRecuperar').val();
      $('#mensajeConfirmacion').text('Hemos enviado las instrucciones a ' + correo + '.');
      $('#pasoEmail').hide();
      $('#pasoConfirmacion').show();
      setTimeout(function () { $('#pasoConfirmacion').hide(); $('#pasaNuevaPassword').show(); }, 3000);
    }
  });

  // ------------------------------------------
  // FORMULARIO: NUEVA CONTRASEÑA (recuperar)
  // ------------------------------------------
  $('#formNuevaPassword').validate({
    errorClass: 'is-invalid', validClass: 'is-valid', errorElement: 'div',
    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');
      if (element.parent('.input-group').length) { error.insertAfter(element.parent()); }
      else { error.insertAfter(element); }
    },
    highlight:   function (el) { $(el).addClass('is-invalid').removeClass('is-valid'); },
    unhighlight: function (el) { $(el).removeClass('is-invalid').addClass('is-valid'); },
    rules: {
      nuevaPassword:  { required: true, passFuerte: true },
      confirmarNueva: { required: true, equalTo: '#nuevaPassword' }
    },
    messages: {
      nuevaPassword:  { required: 'Ingresa tu nueva contraseña.' },
      confirmarNueva: { required: 'Repite la nueva contraseña.', equalTo: 'Las contraseñas no coinciden.' }
    },
    submitHandler: function (form, event) {
      event.preventDefault();
      $('#pasaNuevaPassword').html('<div class="form-card"><div class="card-body p-4 text-center"><div style="font-size:3rem;margin-bottom:12px">✅</div><h3>Contraseña actualizada</h3><p style="color:var(--muted)">Tu contraseña fue cambiada exitosamente.</p><div class="mt-4"><a href="../auth/login.html" class="btn btn-primary">Ir al login</a></div></div></div>');
    }
  });
  $('#toggleNueva').on('click', function () {
    const pwd = $('#nuevaPassword');
    const isPass = pwd.attr('type') === 'password';
    pwd.attr('type', isPass ? 'text' : 'password');
    $(this).text(isPass ? 'Ocultar' : 'Mostrar');
  });

  // ------------------------------------------
  // FORMULARIO: PERFIL - Datos personales
  // ------------------------------------------
  $('#formPerfil').validate({
    errorClass: 'is-invalid', validClass: 'is-valid', errorElement: 'div',
    errorPlacement: function (error, element) { error.addClass('invalid-feedback'); error.insertAfter(element); },
    highlight:   function (el) { $(el).addClass('is-invalid').removeClass('is-valid'); },
    unhighlight: function (el) { $(el).removeClass('is-invalid').addClass('is-valid'); },
    rules: {
      perfilNombre:   { required: true, minlength: 3 },
      perfilUsername: { required: true, minlength: 3, maxlength: 20, sinEspacios: true },
      perfilEmail:    { required: true, email: true },
      perfilFecha:    { required: true, mayor13: true }
    },
    messages: {
      perfilNombre:   { required: 'El nombre es obligatorio.', minlength: 'Mínimo 3 caracteres.' },
      perfilUsername: { required: 'El usuario es obligatorio.', minlength: 'Mínimo 3 caracteres.', maxlength: 'Máximo 20 caracteres.' },
      perfilEmail:    { required: 'El correo es obligatorio.', email: 'Formato de correo inválido.' },
      perfilFecha:    { required: 'La fecha es obligatoria.' }
    },
    submitHandler: function (form, event) { event.preventDefault(); alert('Perfil actualizado correctamente.'); }
  });

  // ------------------------------------------
  // FORMULARIO: PERFIL - Cambiar contraseña
  // ------------------------------------------
  $('#formCambiarPassword').validate({
    errorClass: 'is-invalid', validClass: 'is-valid', errorElement: 'div',
    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');
      if (element.parent('.input-group').length) { error.insertAfter(element.parent()); }
      else { error.insertAfter(element); }
    },
    highlight:   function (el) { $(el).addClass('is-invalid').removeClass('is-valid'); },
    unhighlight: function (el) { $(el).removeClass('is-invalid').addClass('is-valid'); },
    rules: {
      passwordActual:    { required: true },
      passwordNueva:     { required: true, passFuerte: true },
      passwordConfirmar: { required: true, equalTo: '#passwordNueva' }
    },
    messages: {
      passwordActual:    { required: 'Ingresa tu contraseña actual.' },
      passwordNueva:     { required: 'Ingresa tu nueva contraseña.' },
      passwordConfirmar: { required: 'Repite la nueva contraseña.', equalTo: 'Las contraseñas no coinciden.' }
    },
    submitHandler: function (form, event) {
      event.preventDefault();
      alert('Contraseña actualizada correctamente.');
      form.reset();
      $('.is-valid, .is-invalid').removeClass('is-valid is-invalid');
    }
  });
  $('#toggleActual').on('click', function () {
    const pwd = $('#passwordActual');
    const isPass = pwd.attr('type') === 'password';
    pwd.attr('type', isPass ? 'text' : 'password');
    $(this).text(isPass ? 'Ocultar' : 'Mostrar');
  });
  $('#toggleNuevaP').on('click', function () {
    const pwd = $('#passwordNueva');
    const isPass = pwd.attr('type') === 'password';
    pwd.attr('type', isPass ? 'text' : 'password');
    $(this).text(isPass ? 'Ocultar' : 'Mostrar');
  });
  $('#passwordConfirmar').on('paste', function (e) { e.preventDefault(); });

  // ------------------------------------------
  // FORMULARIO: CHECKOUT - Envío
  // ------------------------------------------
  $('#formEnvio').validate({
    errorClass: 'is-invalid', validClass: 'is-valid', errorElement: 'div',
    errorPlacement: function (error, element) { error.addClass('invalid-feedback'); error.insertAfter(element); },
    highlight:   function (el) { $(el).addClass('is-invalid').removeClass('is-valid'); },
    unhighlight: function (el) { $(el).removeClass('is-invalid').addClass('is-valid'); },
    rules: {
      nombreEnvio:    { required: true, minlength: 3 },
      emailEnvio:     { required: true, email: true },
      direccionEnvio: { required: true, minlength: 5 },
      ciudadEnvio:    { required: true },
      telefonoEnvio:  { required: true, minlength: 8 }
    },
    messages: {
      nombreEnvio:    { required: 'El nombre es obligatorio.' },
      emailEnvio:     { required: 'El correo es obligatorio.', email: 'Formato inválido.' },
      direccionEnvio: { required: 'La dirección es obligatoria.' },
      ciudadEnvio:    { required: 'La ciudad es obligatoria.' },
      telefonoEnvio:  { required: 'El teléfono es obligatorio.' }
    },
    submitHandler: function (form, event) {
      event.preventDefault();
      $('#pasoEnvio').hide();
      $('#pasoPago').show();
    }
  });

  // ------------------------------------------
  // FORMULARIO: CHECKOUT - Pago
  // ------------------------------------------
  $('#formPago').validate({
    errorClass: 'is-invalid', validClass: 'is-valid', errorElement: 'div',
    errorPlacement: function (error, element) { error.addClass('invalid-feedback'); error.insertAfter(element); },
    highlight:   function (el) { $(el).addClass('is-invalid').removeClass('is-valid'); },
    unhighlight: function (el) { $(el).removeClass('is-invalid').addClass('is-valid'); },
    rules: {
      nombreTarjeta: { required: true, minlength: 3 },
      numeroTarjeta: { required: true, minlength: 19 },
      vencimiento:   { required: true, minlength: 5 },
      cvv:           { required: true, minlength: 3 }
    },
    messages: {
      nombreTarjeta: { required: 'El nombre en la tarjeta es obligatorio.' },
      numeroTarjeta: { required: 'El número de tarjeta es obligatorio.', minlength: 'Ingresa los 16 dígitos.' },
      vencimiento:   { required: 'La fecha de vencimiento es obligatoria.' },
      cvv:           { required: 'El CVV es obligatorio.' }
    },
    submitHandler: function (form, event) {
      event.preventDefault();
      $('#pasoPago').hide();
      $('#pasoConfirmacion').show();
    }
  });

});
