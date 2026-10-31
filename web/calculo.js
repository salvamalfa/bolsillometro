/*
 * Bolsímetro: el mismo cálculo que el CLI (cuestionario.py, personal.py, banxico.py),
 * en el navegador. Las pruebas de tests/test_web.py lo corren en Node y lo comparan contra
 * Python con los mismos datos.
 *
 * Todo pasa en tu navegador: no se manda nada a ningún servidor.
 */
(function (raiz) {
  "use strict";

  var MESES_POR = { mes: 1, bimestre: 2, trimestre: 3, semestre: 6, "año": 12 };
  var PLAZO_CETES = 28;
  var BASE_DIAS = 360;
  var HUECO_MAXIMO_CETES = 14;

  function ErrorPresupuesto(mensaje) {
    this.name = "ErrorPresupuesto";
    this.message = mensaje;
  }
  ErrorPresupuesto.prototype = Object.create(Error.prototype);

  // --- periodos "AAAA-MM" -----------------------------------------------------------------
  function desplazar(periodo, n) {
    var anio = Number(periodo.slice(0, 4));
    var mes = Number(periodo.slice(5, 7));
    var indice = anio * 12 + (mes - 1) + n;
    var a = Math.floor(indice / 12);
    var m = (indice % 12) + 1;
    return a + "-" + (m < 10 ? "0" : "") + m;
  }

  function finDeMes(periodo) {
    var anio = Number(periodo.slice(0, 4));
    var mes = Number(periodo.slice(5, 7));
    return new Date(Date.UTC(anio, mes, 0)); // día 0 del mes siguiente
  }

  function dias(a, b) {
    return Math.round((b - a) / 86400000);
  }

  // Redondeo a 2 decimales como Python (al par en empates exactos).
  function redondear2(valor) {
    var x = valor * 100;
    var r = Math.round(x);
    if (Math.abs(x % 1) === 0.5 && r % 2 !== 0) r -= 1;
    return r / 100;
  }

  // --- base --------------------------------------------------------------------------------
  function Datos(base) {
    this.base = base;
    this.periodos = base.periodos;
    this.posicion = {};
    for (var i = 0; i < base.periodos.length; i++) this.posicion[base.periodos[i]] = i;
    this.ultimo = null;
    var general = base.nacional.general;
    for (var j = general.length - 1; j >= 0; j--) {
      if (general[j] !== null) {
        this.ultimo = base.periodos[j];
        break;
      }
    }
    this.rubros = {};
    this.ordenRubros = [];
    for (var k = 0; k < base.rubros.length; k++) {
      var r = base.rubros[k];
      this.rubros[r.clave] = r;
      this.ordenRubros.push(r.clave);
    }
    this.preguntas = base.cuestionario.pregunta;
  }

  Datos.prototype.valor = function (serie, periodo) {
    var i = this.posicion[periodo];
    return i === undefined ? null : serie[i];
  };

  /** Gasto del hogar promedio por rubro a precios del mes ``e``: Σ w·I(e)/I(2Q jul-2024). */
  Datos.prototype.gastoOficialPorRubro = function (e) {
    var b = this.base;
    var resultado = {};
    for (var i = 0; i < this.ordenRubros.length; i++) {
      var rubro = this.rubros[this.ordenRubros[i]];
      var total = 0;
      for (var j = 0; j < rubro.genericos.length; j++) {
        var c = rubro.genericos[j];
        total += (b.ponderadores[c] * this.valor(b.nacional[c], e)) / b.base_oficial[c];
      }
      resultado[rubro.clave] = total;
    }
    return resultado;
  };

  // --- cuestionario → presupuesto ---------------------------------------------------------
  var OMITIDA = {};

  function resolver(datos, pregunta, valor) {
    if (typeof valor === "string" && pregunta.escala) {
      var opciones = datos.base.cuestionario.escalas[pregunta.escala];
      for (var i = 0; i < opciones.length; i++) {
        if (opciones[i].texto === valor) return opciones[i].omitir ? OMITIDA : opciones[i].valor;
      }
      throw new ErrorPresupuesto(pregunta.id + ": " + JSON.stringify(valor) + " no es una opción");
    }
    return valor;
  }

  function montoMensual(valor, cada) {
    if (valor !== null && typeof valor === "object") {
      cada = valor.cada || cada;
      valor = valor.monto;
    }
    if (typeof valor !== "number" || !isFinite(valor)) {
      throw new ErrorPresupuesto("monto inválido: " + JSON.stringify(valor));
    }
    if (valor < 0) throw new ErrorPresupuesto("monto negativo: " + valor);
    if (!(cada in MESES_POR)) throw new ErrorPresupuesto("frecuencia desconocida: " + cada);
    return valor / MESES_POR[cada];
  }

  function aplica(pregunta, respuestas) {
    if (!pregunta.si) return true;
    var otra = respuestas[pregunta.si.pregunta];
    if ("es" in pregunta.si) return otra === pregunta.si.es;
    if (otra === undefined || otra === null) return false;
    return montoMensual(otra, "mes") > pregunta.si.mayor_que;
  }

  /** El último mes con datos nacionales y, si hay ciudad, también de la ciudad. */
  function mesDelGasto(datos, seriesCiudad) {
    if (!seriesCiudad) return datos.ultimo;
    var local = ultimoConDato(datos, seriesCiudad.general);
    return local < datos.ultimo ? local : datos.ultimo;
  }

  /**
   * En orden, y solo las que aplican según las anteriores: una respuesta guardada para una
   * pregunta que ya no aplica (p. ej. gasolina tras decir que no hay auto) no se valida.
   */
  function resolverRespuestas(datos, respuestas) {
    var resueltas = {};
    datos.preguntas.forEach(function (p) {
      if (p.id in respuestas && aplica(p, resueltas)) {
        var v = resolver(datos, p, respuestas[p.id]);
        if (v !== OMITIDA) resueltas[p.id] = v;
      }
    });
    return resueltas;
  }

  /** Mismas reglas que cuestionario.presupuesto_desde_respuestas. */
  function presupuestoDesdeRespuestas(datos, respuestas, periodo) {
    var preguntas = datos.preguntas;
    var resueltas = resolverRespuestas(datos, respuestas);
    periodo = periodo || datos.ultimo;
    var oficial = datos.gastoOficialPorRubro(periodo);
    var ciudad = "nacional";
    var gasto = {};
    var ordenGasto = [];
    var aumento = {};
    var noCubierto = {};
    for (var j = 0; j < preguntas.length; j++) {
      var pregunta = preguntas[j];
      if (!(pregunta.id in resueltas) || !aplica(pregunta, resueltas)) continue;
      var valor = resueltas[pregunta.id];
      try {
        if (pregunta.tipo === "ciudad") {
          ciudad = String(valor);
        } else if (pregunta.tipo === "opcion") {
          var validas = pregunta.opciones.map(function (o) {
            return o.valor;
          });
          if (validas.indexOf(valor) < 0) throw new ErrorPresupuesto("debe ser una de: " + validas.join(", "));
        } else if (pregunta.tipo === "porcentaje") {
          if (valor === null) continue;
          if (typeof valor !== "number" || valor < -99 || valor > 1000) {
            throw new ErrorPresupuesto("debe ser un número entre -99 y 1000");
          }
          aumento[pregunta.aumento_propio] = valor;
        } else {
          var mensual = montoMensual(valor, pregunta.cada || "mes");
          if (pregunta.no_cubierto) {
            if (mensual) noCubierto[pregunta.no_cubierto] = mensual;
            continue;
          }
          var total = 0;
          for (var k = 0; k < pregunta.rubros.length; k++) total += oficial[pregunta.rubros[k]];
          for (var m = 0; m < pregunta.rubros.length; m++) {
            var r = pregunta.rubros[m];
            if (!(r in gasto)) {
              gasto[r] = 0;
              ordenGasto.push(r);
            }
            gasto[r] += (mensual * oficial[r]) / total;
          }
        }
      } catch (error) {
        if (error instanceof ErrorPresupuesto) throw new ErrorPresupuesto(pregunta.id + ": " + error.message);
        throw error;
      }
    }
    var gastoFinal = {};
    var orden = [];
    ordenGasto.forEach(function (r) {
      if (gasto[r] > 0) {
        gastoFinal[r] = redondear2(gasto[r]);
        orden.push(r);
      }
    });
    if (!orden.length) throw new ErrorPresupuesto("Las respuestas no traen ningún gasto mayor que cero");
    var aumentoFinal = {};
    Object.keys(aumento).forEach(function (r) {
      if (gastoFinal[r]) aumentoFinal[r] = aumento[r];
    });
    var noCubiertoFinal = {};
    Object.keys(noCubierto).forEach(function (c) {
      noCubiertoFinal[c] = redondear2(noCubierto[c]);
    });
    return {
      ciudad: ciudad,
      periodo_gasto: periodo,
      vivienda_propia: "gasto_efectivo",
      gasto: gastoFinal,
      orden: orden,
      aumento_propio: aumentoFinal,
      no_cubierto: noCubiertoFinal,
    };
  }

  // --- cálculo -----------------------------------------------------------------------------
  function ultimoConDato(datos, serie) {
    for (var i = serie.length - 1; i >= 0; i--) if (serie[i] !== null) return datos.periodos[i];
    return null;
  }

  /** Mismo cálculo que personal.calcular, con la ciudad ya cargada (o null). */
  function calcular(datos, presupuesto, seriesCiudad) {
    var b = datos.base;
    var e = presupuesto.periodo_gasto;
    var locales = null;
    var ultimoLocal = null;
    if (presupuesto.ciudad !== "nacional") {
      if (!seriesCiudad) throw new ErrorPresupuesto("ciudad desconocida: " + presupuesto.ciudad);
      locales = seriesCiudad;
      if (datos.valor(locales.general, e) === null) {
        throw new ErrorPresupuesto("Tu ciudad todavía no tiene datos de " + e);
      }
      ultimoLocal = ultimoConDato(datos, locales.general);
    }
    var pesos = {};
    var rubroDe = {};
    var fuente = {};
    var series = {};
    var orden = [];
    presupuesto.orden.forEach(function (clave) {
      if (clave === "vivienda_propia" && presupuesto.vivienda_propia !== "consumo") return;
      var monto = presupuesto.gasto[clave];
      if (!(monto > 0)) return;
      var rubro = datos.rubros[clave];
      if (clave in presupuesto.aumento_propio) {
        var codigo = "propio:" + clave;
        var mensual = Math.pow(1 + presupuesto.aumento_propio[clave] / 100, 1 / 12);
        series[codigo] = datos.periodos.map(function (p, i) {
          return 100 * Math.pow(mensual, i - datos.posicion[e]);
        });
        pesos[codigo] = monto;
        rubroDe[codigo] = clave;
        fuente[codigo] = "propio";
        orden.push(codigo);
        return;
      }
      var reparto = {};
      var total = 0;
      rubro.genericos.forEach(function (c) {
        reparto[c] = (b.ponderadores[c] * datos.valor(b.nacional[c], e)) / b.base_oficial[c];
        total += reparto[c];
      });
      rubro.genericos.forEach(function (c) {
        var local = locales ? locales[c] : null;
        var usaLocal =
          rubro.nacionales.indexOf(c) < 0 &&
          local &&
          datos.valor(local, e) !== null &&
          ultimoLocal !== null &&
          datos.valor(local, ultimoLocal) !== null;
        series[c] = usaLocal ? local : b.nacional[c];
        pesos[c] = (monto * reparto[c]) / total;
        rubroDe[c] = clave;
        fuente[c] = usaLocal ? "ciudad" : "nacional";
        orden.push(c);
      });
    });
    var suma = 0;
    orden.forEach(function (c) {
      suma += pesos[c];
    });
    orden.forEach(function (c) {
      pesos[c] = pesos[c] / suma;
    });
    var base = {};
    orden.forEach(function (c) {
      base[c] = datos.valor(series[c], e);
    });
    // P(t) = 100 Σ s_k I_k(t) / I_k(e), donde todas las series tienen dato.
    var indice = {};
    datos.periodos.forEach(function (p) {
      var total = 0;
      for (var i = 0; i < orden.length; i++) {
        var v = datos.valor(series[orden[i]], p);
        if (v === null) return;
        total += (pesos[orden[i]] * v) / base[orden[i]];
      }
      indice[p] = 100 * total;
    });
    return new Resultado(datos, presupuesto, indice, pesos, rubroDe, fuente, series, base, orden);
  }

  function Resultado(datos, presupuesto, indice, pesos, rubroDe, fuente, series, base, orden) {
    this.datos = datos;
    this.presupuesto = presupuesto;
    this.indice = indice;
    this.pesos = pesos;
    this.rubroDe = rubroDe;
    this.fuente = fuente;
    this.series = series;
    this.base = base;
    this.orden = orden;
    var periodos = Object.keys(indice).sort();
    this.ultimo = periodos[periodos.length - 1];
  }

  Resultado.prototype.inflacion = function (rezago) {
    var hasta = this.ultimo;
    var desde = desplazar(hasta, -rezago);
    if (!(desde in this.indice)) return null;
    return (this.indice[hasta] / this.indice[desde] - 1) * 100;
  };

  Resultado.prototype._relativo = function (codigo, periodo) {
    return this.datos.valor(this.series[codigo], periodo) / this.base[codigo];
  };

  /** Puntos que aporta cada rubro (incidencias), de mayor a menor en valor absoluto. */
  Resultado.prototype.incidenciasPorRubro = function (rezago) {
    var hasta = this.ultimo;
    var desde = desplazar(hasta, -rezago);
    var self = this;
    var denominador = 0;
    this.orden.forEach(function (c) {
      denominador += self.pesos[c] * self._relativo(c, desde);
    });
    var porRubro = {};
    this.orden.forEach(function (c) {
      var r = self.rubroDe[c];
      var aporte = (100 * self.pesos[c] * (self._relativo(c, hasta) - self._relativo(c, desde))) / denominador;
      porRubro[r] = (porRubro[r] || 0) + aporte;
    });
    return Object.keys(porRubro)
      .map(function (r) {
        return [r, porRubro[r]];
      })
      .sort(function (a, b) {
        return Math.abs(b[1]) - Math.abs(a[1]);
      });
  };

  /** Cuánto subieron, en %, los precios de cada rubro de tu canasta. */
  Resultado.prototype.variacionPorRubro = function (rezago) {
    var hasta = this.ultimo;
    var desde = desplazar(hasta, -rezago);
    var self = this;
    var antes = {};
    var despues = {};
    this.orden.forEach(function (c) {
      var r = self.rubroDe[c];
      antes[r] = (antes[r] || 0) + self.pesos[c] * self._relativo(c, desde);
      despues[r] = (despues[r] || 0) + self.pesos[c] * self._relativo(c, hasta);
    });
    var resultado = {};
    Object.keys(antes).forEach(function (r) {
      resultado[r] = (despues[r] / antes[r] - 1) * 100;
    });
    return resultado;
  };

  /** Igual que banxico.rendimiento_cetes: reinvertir cada 28 días de fin de mes a fin de mes. */
  function rendimientoCetes(cetes, desde, hasta) {
    if (!cetes || !cetes.length) return null;
    var subastas = cetes.map(function (par) {
      return [new Date(par[0] + "T00:00:00Z"), par[1]];
    });
    var inicio = finDeMes(desde);
    var fin = finDeMes(hasta);
    if (subastas[0][0] > inicio || dias(subastas[subastas.length - 1][0], fin) > HUECO_MAXIMO_CETES) {
      return null;
    }
    var factor = 1;
    var fecha = inicio;
    while (fecha < fin) {
      var tasa = null;
      for (var i = 0; i < subastas.length && subastas[i][0] <= fecha; i++) tasa = subastas[i][1];
      var tramo = Math.min(PLAZO_CETES, dias(fecha, fin));
      factor *= 1 + ((tasa / 100) * tramo) / BASE_DIAS;
      fecha = new Date(fecha.getTime() + tramo * 86400000);
    }
    return (factor - 1) * 100;
  }

  function rendimientoReal(nominal, inflacion) {
    return ((1 + nominal / 100) / (1 + inflacion / 100) - 1) * 100;
  }

  /** Lo que muestra la web: la cifra, lo que la subió y si los Cetes le ganaron. */
  function resumen(datos, resultado) {
    var anual = resultado.inflacion(12);
    var variaciones = resultado.variacionPorRubro(12);
    var incidencias = resultado.incidenciasPorRubro(12);
    var cetes = rendimientoCetes(datos.base.cetes, desplazar(resultado.ultimo, -12), resultado.ultimo);
    return {
      inflacion: anual,
      desde: desplazar(resultado.ultimo, -12),
      hasta: resultado.ultimo,
      suben: incidencias
        .filter(function (par) {
          return par[1] > 0;
        })
        .slice(0, 4)
        .map(function (par) {
          return { rubro: datos.rubros[par[0]].nombre, puntos: par[1], subio: variaciones[par[0]] };
        }),
      baja: incidencias
        .filter(function (par) {
          return par[1] < 0;
        })
        .sort(function (a, b) {
          return a[1] - b[1];
        })
        .slice(0, 1)
        .map(function (par) {
          return { rubro: datos.rubros[par[0]].nombre, puntos: par[1], cambio: variaciones[par[0]] };
        })[0] || null,
      cetes: cetes,
      real: cetes === null || anual === null ? null : rendimientoReal(cetes, anual),
    };
  }

  var api = {
    Datos: Datos,
    ErrorPresupuesto: ErrorPresupuesto,
    aplica: aplica,
    resolver: resolver,
    OMITIDA: OMITIDA,
    resolverRespuestas: resolverRespuestas,
    presupuestoDesdeRespuestas: presupuestoDesdeRespuestas,
    mesDelGasto: mesDelGasto,
    calcular: calcular,
    rendimientoCetes: rendimientoCetes,
    rendimientoReal: rendimientoReal,
    resumen: resumen,
    desplazar: desplazar,
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else raiz.Bolsillometro = api;
})(typeof window !== "undefined" ? window : this);
