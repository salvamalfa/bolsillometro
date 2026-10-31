/* Interfaz de la entrevista: una pregunta por pantalla, el resultado en una sola cifra. */
(function () {
  "use strict";

  var B = window.Bolsillometro;
  var base = window.BOLSILLOMETRO_BASE;
  var datos = new B.Datos(base);
  var preguntas = datos.preguntas;
  var MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];

  var respuestas = {};
  var historial = [];
  var actual = -1;

  function $(id) {
    return document.getElementById(id);
  }

  function mostrar(id) {
    ["inicio", "pregunta", "resultado"].forEach(function (pantalla) {
      $(pantalla).hidden = pantalla !== id;
    });
    $("error").hidden = true;
    window.scrollTo(0, 0);
  }

  function error(mensaje) {
    $("error").textContent = mensaje;
    $("error").hidden = false;
  }

  function mes(periodo) {
    return MESES[Number(periodo.slice(5, 7)) - 1] + "-" + periodo.slice(0, 4);
  }

  function porcentaje(valor) {
    return valor.toLocaleString("es-MX", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + "%";
  }

  function resueltas() {
    return B.resolverRespuestas(datos, respuestas);
  }

  function siguienteIndice(desde) {
    var r = resueltas();
    for (var i = desde + 1; i < preguntas.length; i++) {
      if (B.aplica(preguntas[i], r)) return i;
    }
    return -1;
  }

  function cuantasFaltan(desde) {
    var r = resueltas();
    var n = 0;
    for (var i = desde + 1; i < preguntas.length; i++) if (B.aplica(preguntas[i], r)) n++;
    return n;
  }

  function responder(valor) {
    respuestas[preguntas[actual].id] = valor;
    // Si cambió una respuesta de la que dependen otras, las que ya no aplican no cuentan.
    avanzar();
  }

  function avanzar() {
    var siguiente = siguienteIndice(actual);
    if (siguiente < 0) {
      terminar();
      return;
    }
    if (actual >= 0) historial.push(actual);
    actual = siguiente;
    pintarPregunta();
  }

  function boton(texto, alElegir) {
    var b = document.createElement("button");
    b.type = "button";
    b.textContent = texto;
    b.addEventListener("click", alElegir);
    return b;
  }

  function pintarPregunta() {
    var p = preguntas[actual];
    var hechas = historial.length + 1;
    var total = hechas + cuantasFaltan(actual);
    $("barra").style.width = Math.round((100 * (hechas - 1)) / total) + "%";
    $("contador").textContent = "Pregunta " + hechas + " de " + total;
    $("texto").textContent = p.texto;
    var opciones = $("opciones");
    opciones.innerHTML = "";
    $("otro").hidden = true;

    if (p.tipo === "ciudad") {
      var lista = document.createElement("select");
      lista.setAttribute("aria-label", "Tu ciudad");
      var vacia = document.createElement("option");
      vacia.value = "";
      vacia.textContent = "Elige tu ciudad…";
      lista.appendChild(vacia);
      base.ciudades
        .slice()
        .sort(function (a, b) {
          return a.nombre.replace(/^la /, "").localeCompare(b.nombre.replace(/^la /, ""), "es");
        })
        .forEach(function (c) {
          var o = document.createElement("option");
          o.value = c.clave;
          o.textContent = c.nombre.replace(/^la /, "");
          lista.appendChild(o);
        });
      var nacional = document.createElement("option");
      nacional.value = "nacional";
      nacional.textContent = "Ninguna está cerca: usar precios nacionales";
      lista.appendChild(nacional);
      if (respuestas[p.id]) lista.value = respuestas[p.id];
      opciones.appendChild(lista);
      opciones.appendChild(
        boton("Siguiente", function () {
          if (!lista.value) return error("Elige una ciudad para seguir.");
          responder(lista.value);
        })
      );
    } else if (p.tipo === "opcion") {
      p.opciones.forEach(function (o) {
        opciones.appendChild(
          boton(o.texto, function () {
            responder(o.valor);
          })
        );
      });
    } else {
      base.cuestionario.escalas[p.escala].forEach(function (o) {
        opciones.appendChild(
          boton(o.texto, function () {
            responder(o.texto);
          })
        );
      });
      $("otro").hidden = false;
      $("etiqueta-monto").textContent = p.tipo === "porcentaje" ? "Otro porcentaje" : "Otro monto exacto";
      $("cada").textContent = p.tipo === "porcentaje" ? "% al año" : p.cada === "año" ? "al año" : "al mes";
      $("monto").value = typeof respuestas[p.id] === "number" ? respuestas[p.id] : "";
      // Un aumento puede ser negativo (la renta bajó); un monto no.
      $("monto").min = p.tipo === "porcentaje" ? "-99" : "0";
      $("monto").max = p.tipo === "porcentaje" ? "1000" : "";
    }
    $("atras").hidden = historial.length === 0;
    mostrar("pregunta");
  }

  function cargarCiudad(clave) {
    return new Promise(function (resolver, rechazar) {
      var ya = window.BOLSILLOMETRO_CIUDADES && window.BOLSILLOMETRO_CIUDADES[clave];
      if (ya) return resolver(ya);
      var script = document.createElement("script");
      script.src = "datos/ciudades/" + encodeURIComponent(clave) + ".js";
      script.onload = function () {
        resolver(window.BOLSILLOMETRO_CIUDADES[clave]);
      };
      script.onerror = function () {
        rechazar(new Error("No se pudieron cargar los precios de tu ciudad."));
      };
      document.head.appendChild(script);
    });
  }

  function terminar() {
    var clave = respuestas.ciudad || "nacional";
    var ciudad = clave === "nacional" ? Promise.resolve(null) : cargarCiudad(clave);
    ciudad
      .then(function (series) {
        // Si tu ciudad todavía no tiene el último mes, se usa el anterior.
        var presupuesto = B.presupuestoDesdeRespuestas(datos, respuestas, B.mesDelGasto(datos, series));
        var resultado = B.calcular(datos, presupuesto, series);
        pintarResultado(presupuesto, B.resumen(datos, resultado));
      })
      .catch(function (e) {
        error(e.message);
      });
  }

  function pintarResultado(presupuesto, r) {
    if (r.inflacion === null) return error("Todavía no hay 12 meses de datos para calcular tu inflación.");
    var lugar = "los precios nacionales";
    base.ciudades.forEach(function (c) {
      if (c.clave === presupuesto.ciudad) lugar = "los precios de " + c.nombre.replace(/\.$/, "");
    });
    $("cifra").textContent = porcentaje(r.inflacion);
    $("periodo").textContent = "de " + mes(r.desde) + " a " + mes(r.hasta) + ", con tu gasto y " + lugar + ".";

    var suben = $("suben");
    suben.innerHTML = "";
    if (r.suben.length) {
      var h = document.createElement("h3");
      h.textContent = "Lo que más la subió";
      suben.appendChild(h);
      var ul = document.createElement("ul");
      r.suben.forEach(function (s) {
        var li = document.createElement("li");
        li.innerHTML = "<span></span><span class='dato'></span>";
        li.children[0].textContent = s.rubro;
        li.children[1].textContent = "subió " + s.subio.toFixed(1) + "% · aporta " + s.puntos.toFixed(2);
        ul.appendChild(li);
      });
      if (r.baja) {
        var li = document.createElement("li");
        li.innerHTML = "<span></span><span class='dato'></span>";
        li.children[0].textContent = "Lo que más la bajó: " + r.baja.rubro;
        li.children[1].textContent =
          (r.baja.cambio < 0 ? "bajó " : "subió ") + Math.abs(r.baja.cambio).toFixed(1) + "% · resta " +
          Math.abs(r.baja.puntos).toFixed(2);
        ul.appendChild(li);
      }
      suben.appendChild(ul);
      var nota = document.createElement("p");
      nota.className = "nota";
      nota.textContent = "“Aporta” son puntos de tu " + porcentaje(r.inflacion) + ".";
      suben.appendChild(nota);
    }

    var cetes = $("cetes");
    cetes.innerHTML = "";
    if (r.cetes !== null) {
      var titulo = document.createElement("h3");
      titulo.textContent = "¿Tus ahorros le ganan?";
      var texto = document.createElement("p");
      var veredicto = r.real >= 0 ? "le ganó a tu inflación por " : "perdió contra tu inflación por ";
      texto.textContent =
        "En Cetes a 28 días, tu dinero ganó " + porcentaje(r.cetes) + ": " + veredicto + porcentaje(Math.abs(r.real)) + ".";
      cetes.appendChild(titulo);
      cetes.appendChild(texto);
      cetes.hidden = false;
    } else {
      cetes.hidden = true;
    }
    $("barra").style.width = "100%";
    mostrar("resultado");
  }

  function descargar() {
    var blob = new Blob([JSON.stringify(respuestas, null, 2) + "\n"], { type: "application/json" });
    var enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(blob);
    enlace.download = "mis-respuestas-bolsimetro.json";
    document.body.appendChild(enlace);
    enlace.click();
    enlace.remove();
  }

  $("fuente").textContent = base.fuente + " " + base.deslinde + " Datos hasta " + mes(datos.ultimo) + ".";
  $("empezar").addEventListener("click", function () {
    actual = -1;
    historial = [];
    avanzar();
  });
  $("atras").addEventListener("click", function () {
    if (!historial.length) return mostrar("inicio");
    actual = historial.pop();
    pintarPregunta();
  });
  $("otro").addEventListener("submit", function (evento) {
    evento.preventDefault();
    var valor = Number($("monto").value);
    var valido = $("monto").value !== "" && isFinite(valor);
    if (preguntas[actual].tipo === "porcentaje") {
      if (!valido || valor < -99 || valor > 1000) return error("Escribe un porcentaje entre -99 y 1000.");
    } else if (!valido || valor < 0) {
      return error("Escribe un número de 0 en adelante.");
    }
    responder(valor);
  });
  $("descargar").addEventListener("click", descargar);
  $("otra-vez").addEventListener("click", function () {
    respuestas = {};
    mostrar("inicio");
  });
})();
