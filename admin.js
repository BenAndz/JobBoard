document.addEventListener('DOMContentLoaded', (event) => {
    getAllCompanies();
});

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('add-company').addEventListener('click', addCompany);
});

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('delete-company').addEventListener('click', enableDeleteMode);
});


let deleteMode = false;

function enableDeleteMode() {
    deleteMode = true;
}


async function getAllCompanies() {
    let apiUrl = `http://127.0.0.1:8000/api/companiesAll`;

    try {
        let response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error("Erreur lors de la récupération des entreprises");
        }
        let companies = await response.json();
        updateTable(companies);
        addCellEventListeners();
    } catch (error) {
        console.error(error);
    }
}

function updateTable(companies) {
    let table = document.getElementById('company-table');
    
    companies.forEach(company => {
        let row = table.insertRow();
        
        Object.keys(company).forEach(key => {
            let cell = row.insertCell();
            
            cell.textContent = company[key];
            
            cell.setAttribute('data-key', key);
        });
    });
}

let addMode = false;

function addCompany() {
    if (!addMode) {
        addMode = true;
        let table = document.getElementById('company-table');
        let row = table.insertRow(-1);  

        let keys = ['company_name', 'company_website', 'company_address', 'company_id', 'recruiter_id'];
        
        for (let i = 0; i < keys.length; i++) {
            let cell = row.insertCell(-1); 

            if (keys[i] !== 'company_id') {
                cell.contentEditable = "true"; 
            } else {
                cell.textContent = 'Automatique';
            }

            cell.setAttribute('data-key', keys[i]);
        }

        let saveButtonCell = row.insertCell(-1);
        let saveButton = document.createElement('button');
        saveButton.textContent = 'Sauvegarder';
        saveButton.addEventListener('click', () => saveCompany(row));
        saveButtonCell.appendChild(saveButton);

        document.getElementById('add-company').textContent = 'Annuler';
    } else {
        addMode = false;
        let table = document.getElementById('company-table');
        table.deleteRow(-1);
        document.getElementById('add-company').textContent = 'Ajouter une entreprise';
    }
}


async function saveCompany(row) {
    let companyData = {};
    for (let i = 0; i < 5; i++) {
        let cell = row.cells[i];
        companyData[cell.getAttribute('data-key')] = cell.textContent;
    }

    try {
        let response = await fetch('http://127.0.0.1:8000/api/companiesDB', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(companyData)
        });

        if (response.ok) {
            location.reload();
            alert('Entreprise sauvegardée avec succès !');
        } else {
            alert('Erreur lors de la sauvegarde de l\'entreprise');
        }
    } catch (error) {
        console.error('Erreur lors de l\'envoi de la requête:', error);
        alert('Erreur lors de la sauvegarde de l\'entreprise');
    }
}

async function addCellEventListeners() {
    let table = document.getElementById("company-table");
    for (let i = 1; i < table.rows.length; i++) {
        let row = table.rows[i];
        for (let j = 0; j < row.cells.length; j++) {
            let cell = row.cells[j];
            cell.addEventListener("click", function() {
                if (deleteMode && cell.getAttribute('data-key') === 'company_id') {
                    deleteCompany(cell.textContent);
                    deleteMode = false;  
                } else if (cell.getAttribute('data-key') !== 'company_id') {
                    editCell(cell);
                }
            });
        }
    }
}

async function editCell(cell) {
    let originalContent = cell.textContent;
    cell.contentEditable = "true";
    cell.focus();

    let row = cell.closest("tr");  
    let companyID = row.querySelector("[data-key='company_id']").textContent;  

    cell.addEventListener("blur", async function() {
        cell.contentEditable = "false";
        if (originalContent !== cell.textContent) {
            let companyData = {};
            for (let i = 0; i < row.cells.length; i++) {
                let cell = row.cells[i];
                companyData[cell.getAttribute('data-key')] = cell.textContent;
            }

            try {
                let response = await fetch(`http://127.0.0.1:8000/api/companiesChange/${companyID}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(companyData)
                });
                if (response.ok) {
                    location.reload();
                }
            } catch (error) {
                console.error('Erreur lors de l\'envoi de la requête:', error);
                alert('Erreur lors de la modification de l\'entreprise.');
            }
        }
    });
}

function enableDeleteMode() {
    let messageElement = document.getElementById('delete-message');

    if (!deleteMode) {
        deleteMode = true;
        messageElement.style.display = 'inline';
        document.getElementById('delete-company').textContent = 'Annuler';
    } else {
        deleteMode = false;
        messageElement.style.display = 'none';
        document.getElementById('delete-company').textContent = 'Supprimer une entreprise';
    }
}

async function deleteCompany(companyId) {
    try {
        let response = await fetch(`http://127.0.0.1:8000/api/deleteCompany/${companyId}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            alert('Entreprise supprimée avec succès !');
            location.reload();
        } else {
            alert('Erreur lors de la suppression de l\'entreprise.');
        }
    } catch (error) {
        console.error('Erreur lors de l\'envoi de la requête:', error);
        alert('Erreur lors de la suppression de l\'entreprise.');
    }
}
