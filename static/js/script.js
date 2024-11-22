function enviarFormulario(tipo) {
    let formData = {};

    // Dependiendo del tipo de formulario (nuevo, modificar, eliminar), recoge los datos
    if (tipo === 'nuevo') {
        formData = {
            nombre: document.querySelector("input[name='nombre']").value,
            numero: document.querySelector("input[name='numero']").value,
            cantidad: document.querySelector("input[name='cantidad']").value
        };
    } else if (tipo === 'modificar') {
        formData = {
            id: document.querySelector("input[name='id']").value,
            nombre: document.querySelector("input[name='nombre']").value,
            cantidad: document.querySelector("input[name='cantidad']").value
        };
    } else if (tipo === 'eliminar') {
        formData = {
            id: document.querySelector("input[name='id']").value
        };
    }

    // Realizar la solicitud AJAX (usando Fetch API)
    let url = tipo === 'nuevo' ? '/nuevo' : tipo === 'modificar' ? '/modificar' : '/eliminar';
    let method = tipo === 'eliminar' ? 'DELETE' : 'POST';

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);  // Mostrar mensaje de éxito
        cargarProductos();    // Recargar la tabla de productos después de la acción
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function cargarProductos() {
    fetch('/productos', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(productos => {
        const tablaProductos = document.getElementById("tablaProductos").getElementsByTagName('tbody')[0];
        tablaProductos.innerHTML = '';  // Limpiar la tabla antes de agregar los nuevos productos

        productos.forEach(producto => {
            const fila = tablaProductos.insertRow();
            fila.innerHTML = `
                <td>${producto[0]}</td>
                <td>${producto[1]}</td>
                <td>${producto[2]}</td>
                <td>${producto[3]}</td>
            `;
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
function mostrarFormulario(tipo) {
    // Ocultar todos los formularios
    document.getElementById("formNuevo").style.display = "none";
    document.getElementById("formModificar").style.display = "none";
    document.getElementById("formEliminar").style.display = "none";

    // Mostrar el formulario correspondiente
    if (tipo === 'nuevo') {
        document.getElementById("formNuevo").style.display = "block";
    } else if (tipo === 'modificar') {
        document.getElementById("formModificar").style.display = "block";
    } else if (tipo === 'eliminar') {
        document.getElementById("formEliminar").style.display = "block";
    }
}

// Llamar a esta función cuando se cargue la página
document.addEventListener('DOMContentLoaded', cargarProductos);