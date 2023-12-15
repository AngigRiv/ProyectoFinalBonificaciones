document.addEventListener('DOMContentLoaded', function () {
    // Asignar evento de clic a todos los botones de eliminar
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.closest('tr').getAttribute('data-item-id');
            confirmDelete(itemId);
        });
    });

    // Asignar evento de clic al botón de agregar
    const addButton = document.getElementById('itemnotasventa-button');
    if (addButton) {
        addButton.addEventListener('click', function () {
            const formData = new FormData(document.getElementById('itemnotasventa-form'));

            // Enviar la solicitud para agregar un nuevo elemento
            fetch(itemsnotaventaCreateUrl, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: formData,
            })
                .then(response => {
                    if (!response.ok) {
                        // Si hay un error en la respuesta, lanzar una excepción
                        throw new Error('');
                    }
                    return response.json(); // Cambiado a json para manejar mensajes del servidor
                })
                .then(data => {
                    // Actualizar la tabla solo si el servidor indica que se registró correctamente
                    if (data.message && data.message.includes('correctamente')) {
                        updateItemsTable(data.newItem);
                        // Mostrar mensaje de éxito en el cuerpo de la página
                        showSuccessMessage('Artículo agregado correctamente. La página se actualizará en breve.');
                        // Recargar la página inmediatamente
                        window.location.reload(true);
                    } else {
                        // Si el mensaje no está presente, refrescar la página sin esperar
                        window.location.reload(true);
                    }
                })
                .catch(error => {
                    console.error(error);
                    // Después de mostrar el mensaje de error, recargar la página inmediatamente
                    window.location.reload(true);
                });
        });

        function showSuccessMessage(message) {
            // Agrega un elemento para mostrar el mensaje de éxito
            const successMessage = document.createElement('div');
            successMessage.className = 'alert alert-success';
            successMessage.innerHTML = message;

            // Agrega el mensaje al cuerpo de la página
            document.body.appendChild(successMessage);

            // Elimina el mensaje y recarga la página después de un breve tiempo
            setTimeout(() => {
                document.body.removeChild(successMessage);
                window.location.reload(true);
            }, 0); // Ajusta el tiempo según sea necesario
        }
    }

    // Inicializar Chart.js si la biblioteca está definida
    if (typeof Chart !== 'undefined' && Chart.defaults) {
        // Configuración global de Chart.js
        Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
        Chart.defaults.global.defaultFontColor = '#292b2c';
    } else {
        console.error('Chart.js no está definido o Chart.defaults no está disponible.');
    }
});

// Resto del código JavaScript existente...

// Función para confirmar la eliminación
function confirmDelete(itemnotaventaId) {
    const confirmation = confirm('¿Estás seguro de que deseas eliminar este artículo?');
    if (!confirmation) {
        return; // Usuario canceló la eliminación
    }

    const url = `/api/${itemnotaventaId}/eliminarItem/`;

    // Enviar la solicitud para eliminar el elemento
    fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
        .then(data => {
            // Actualizar la tabla solo si el servidor indica que se registró correctamente
            if (data.message.includes('correctamente')) {
                updateItemsTable(data.newItem);
                // Mostrar mensaje de éxito en el cuerpo de la página
                showSuccessMessage('Articulo agregado correctamente. La página se actualizará en breve.');
            }
        })
        .catch(error => {
            window.location.reload(true);
        })
        .finally(() => {
            // Elimina el mensaje y recarga la página después de un breve tiempo
            setTimeout(() => {
                window.location.reload(true);
            }, 0); // Ajusta el tiempo según sea necesario
        });
}

function handleDeleteSuccess(itemnotaventaId) {
    // Implementa acciones adicionales después de una eliminación exitosa si es necesario
    // Puedes dejar esta función vacía si no se requieren acciones adicionales
    // Esta función ahora se ejecutará antes de la alerta en el código anterior
    location.reload();
}

// Función para actualizar la tabla de elementos después de agregar uno nuevo
function updateItemsTable(newItem) {
    console.log('updateItemsTable called with:', newItem);

    const itemsTable = document.getElementById('datatablesItems').getElementsByTagName('tbody')[0];

    // Buscar si ya existe una fila para el elemento actual
    const existingRow = itemsTable.querySelector(`tr[data-item-id="${newItem.id}"]`);

    if (existingRow) {
        // Si existe, actualizar los valores de las celdas
        existingRow.cells[0].innerHTML = newItem.nota_venta_id.nro_pedido;
        existingRow.cells[1].innerHTML = newItem.nro_item;
        existingRow.cells[2].innerHTML = newItem.articulo_id;
        existingRow.cells[3].innerHTML = newItem.cantidad;
        existingRow.cells[4].innerHTML = newItem.es_bonificacion;
        // Actualiza las demás celdas según sea necesario
    } else {
        // Si no existe, crear una nueva fila y celdas
        const newRow = itemsTable.insertRow();
        newRow.setAttribute('data-item-id', newItem.id);

        const cell1 = newRow.insertCell(0);
        const cell2 = newRow.insertCell(1);
        const cell3 = newRow.insertCell(2);
        const cell4 = newRow.insertCell(3);
        const cell5 = newRow.insertCell(4);
        // ... (continúa con las celdas necesarias)

        // Asignar valores a las celdas
        cell1.innerHTML = newItem.nota_venta_id.nro_pedido;
        cell2.innerHTML = newItem.nro_item;
        cell3.innerHTML = newItem.articulo_id;
        cell4.innerHTML = newItem.cantidad;
        cell5.innerHTML = newItem.es_bonificacion;
        // ... (continúa asignando valores a las demás celdas)

        // Crear un botón de eliminación para la nueva fila
        const deleteButton = document.createElement('button');
        deleteButton.className = 'btn btn-danger btn-sm delete-btn';
        deleteButton.innerHTML = 'Eliminar';
        deleteButton.addEventListener('click', function () {
            const itemId = newRow.getAttribute('data-item-id');
            confirmDelete(itemId);
        });

        // Agregar el botón de eliminación a la nueva fila
        const deleteCell = newRow.insertCell();
        deleteCell.appendChild(deleteButton);
    }
}

// Función para eliminar una fila de la tabla correspondiente a un elemento eliminado
function removeItemFromTable(itemnotaventaId) {
    // Obtener la tabla de elementos
    const itemsTable = document.getElementById('datatablesItems').getElementsByTagName('tbody')[0];

    // Encontrar la fila correspondiente al elemento eliminado y eliminarla
    const rows = itemsTable.getElementsByTagName('tr');
    for (let i = 0; i < rows.length; i++) {
        if (rows[i].getAttribute('data-item-id') === itemnotaventaId) {
            itemsTable.deleteRow(i);
            break;
        }
    }
}

// Función para obtener el valor de la cookie CSRF
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}