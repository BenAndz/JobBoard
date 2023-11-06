// Bouton qui affiche et cache les infos
function toggleDetails(buttonElement) {
    let detailsDiv = buttonElement.nextElementSibling;
    if (detailsDiv.style.display === "none" || detailsDiv.style.display === "") {
        detailsDiv.style.display = "block";
    } else {
        detailsDiv.style.display = "none";
    }
}

// Fonction pour se déconnecter 

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
    alert("Vous êtes bien déconnecté !")
}

// People : POST 

async function registerUser() {
    let form = document.getElementById('register-user');
    let formData = new FormData(form);
    let data = Object.fromEntries(formData);
    let password = document.getElementById('password').value;
    let passwordSecond = document.getElementById('password-second').value;

    if (password !== passwordSecond) {
        alert('Les mots de passe ne correspondent pas !');
        return;
    }

    try {
        let response = await fetch('http://127.0.0.1:8000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            let errorData = await response.json();
            alert(`Erreur: ${errorData.detail}`);
            return;
        }

        let result = await response.json();
        alert('Profil créé avec succès !');
        console.log(result);

        if (data.role === 'Candidat') {
            window.location.href = 'index-connexion.html';
        } else if (data.role === 'Recruteur') {
            window.location.href = 'index-connexion.html';
        }

    } catch (error) {
        alert(`Erreur: ${error}`);
    }
}

// People, connexion à un profil : POST

async function login() {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    const email = emailInput.value;
    const password = passwordInput.value;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${email}&password=${password}`,
        });

        if (!response.ok) {
            throw new Error('Invalid credentials');
        }

        const data = await response.json();
        console.log('Response data:', data);
        console.log('Token:', data.access_token); 
        alert('Connexion réussie !');

        const token = data.access_token;
        localStorage.setItem('token', token);

        // Si le recruteur a déjà un profil d'entreprise
        const companyProfileResponse = await fetch('http://127.0.0.1:8000/api/companies', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (companyProfileResponse.status === 404) {
            // Si le recruteur n'a pas de profil d'entreprise :
            window.location.href = 'index-créa-entreprise.html';
        } else {
            // Sinon, page d'accueil 
            window.location.href = 'index.html';
        }

    } catch (error) {
        alert('Login failed: ' + error.message);
    }
}


// People : GET

async function fetchPersonProfile() {
    try {
        let apiUrl = `http://127.0.0.1:8000/api/profile/`
        let token = localStorage.getItem("token");

        let response = await fetch(apiUrl, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error("Erreur lors de la récupération de votre profil")
        }

        let profile = await response.json();

        document.getElementById("candidate-first-name").innerText = profile.first_name;
        document.getElementById("candidate-last-name").innerText = profile.last_name;
        document.getElementById("candidate-email").innerText = profile.email;
        document.getElementById("candidate-phone").innerText = profile.phone;

        console.log("API URL:", apiUrl);
        console.log("API response :", response);
        console.log("Status Code:", response.status);
        console.log(profile)

    } catch (error) {
        console.error("Erreur:", error);
        alert("Une erreur s'est produite lors de la récupération du profil de l'entreprise.");
    }
}

// People, get user avec token :

async function getUserInfo() {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Pas de token trouvé');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/api/me', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Informations de l\'utilisateur:', data);
            
        } else {
            console.log('Erreur:', response.statusText);
            alert('Impossible d\'obtenir les informations de l\'utilisateur.');
        }
    } catch (error) {
        alert('Erreur lors de la récupération des informations de l\'utilisateur: ' + error.message);
    }
}

// People, put user avec token :

async function changeProfile() {
    let firstName = document.getElementById('first-name-change').value;
    let lastName = document.getElementById('last-name-change').value;
    let phone = document.getElementById('phone-change').value;

    let updatedProfile = {
        first_name: firstName,
        last_name: lastName,
        phone: phone,
    };

    try {
        let apiUrl = `http://127.0.0.1:8000/api/profile`
        let token = localStorage.getItem("token");

        let response = await fetch(apiUrl, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedProfile)
        });

        if (response.ok) {
            let result = await response.json();
            console.log("Le résultat est : ", result)

            alert("Votre profil a été modifié avec succès !")

            document.getElementById('first-name-change').innerText = result.first_name;
            document.getElementById('last-name-change').innerText = result.last_name;
            document.getElementById('phone-change').innerText = result.phone;

            window.location.reload();
            
        } else {
            console.error('Erreur lors de la mise à jour du profil', result);
            alert('Erreur lors de la mise à jour du profil');
        }

    } catch (error) {
        console.error('Erreur :', error);
        alert('Une erreur est survenue lors de la mise à jour du profil');
    }
}

// People, delete user avec token :

async function deleteUserProfile() {
    try {
        let apiUrl = `http://127.0.0.1:8000/api/profile`
        let token = localStorage.getItem("token");

        let response = await fetch(apiUrl, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            alert("Votre profil a été supprimé avec succès !");
            localStorage.removeItem("token");
            window.location.href = 'index.html'; 
        } else {
            console.error('Erreur lors de la suppression du profil');
            alert('Erreur lors de la suppression du profil');
        }

    } catch (error) {
        console.error('Erreur :', error);
        alert('Une erreur est survenue lors de la suppression du profil');
    }
}

// Companies : POST

async function postCompany() {
    let company_name = document.getElementById('company_name').value;
    let company_website = document.getElementById('company_website').value;
    let company_address = document.getElementById('company_address').value;
    let token = localStorage.getItem("token");

    let companyData = {
        company_name: company_name,
        company_website: company_website,
        company_address: company_address
    };

    try {
        let response = await fetch('http://127.0.0.1:8000/api/companies', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(companyData)
        });

        if (response.status === 403) {
            alert("Vous ne pouvez pas créer de profil entreprise.")
            window.location.href = "index.html";
            return;
        }

        let data = await response.json();

        console.log(data);
        alert(data.status);

    } catch (error) {
        console.error('Erreur:', error);
        alert("Une erreur s'est produite.");
    }   
}

// Company : GET

async function fetchCompanyProfile() {
    try {
        let apiUrl = `http://127.0.0.1:8000/api/companies`;
        let token = localStorage.getItem("token");

        let response = await fetch(apiUrl, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.status === 403) {
            window.location.href = "index.html";
            alert("Pas autorisé !")
            return;
        }
        
        if (!response.ok) {
            throw new Error("Erreur lors de la récupération de votre profil");
        }


        let profile = await response.json();

        document.getElementById("company-name").innerText = profile.company_name;
        document.getElementById("company-website").innerText = profile.company_website;
        document.getElementById("company-address").innerText = profile.company_address;

        console.log("API URL:", apiUrl);
        console.log("API response :", response);
        console.log("Status Code:", response.status);
        console.log(profile);

    } catch (error) {
        console.error("Erreur:", error);
        alert("Une erreur s'est produite lors de la récupération du profil de l'entreprise.");
    }
}


// Company PUT :

async function updateCompanyProfile() {
    let company_name_change = document.getElementById('company_name_change').value;
    let company_website_change = document.getElementById('company_website_change').value;
    let company_address_change = document.getElementById('company_address_change').value;
    let token = localStorage.getItem("token");

    let companyData = {
        company_name: company_name_change,
        company_website: company_website_change,
        company_address: company_address_change
    };

    try {
        let response = await fetch('http://127.0.0.1:8000/api/companies', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(companyData)
        });

        if (response.status === 403) {
            alert("Vous ne pouvez pas mettre à jour le profil de l'entreprise.")
            window.location.href = "index.html";
            return;
        }

        let data = await response.json();

        console.log(data);
        alert(data.status);

        window.location.reload();

    } catch (error) {
        console.error('Erreur:', error);
        alert("Une erreur s'est produite lors de la mise à jour du profil de l'entreprise.");
    }   
}

// Company : DELETE

async function deleteCompanyProfile() {
    let token = localStorage.getItem("token");

    try {
        let response = await fetch('http://127.0.0.1:8000/api/companies', {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.status === 403) {
            alert("Vous ne pouvez pas supprimer le profil de l'entreprise.")
            window.location.href = "index.html";
            return;
        }

        let data = await response.json();

        console.log(data);
        alert(data.status);

        window.location.href = "index.html";

    } catch (error) {
        console.error('Erreur:', error);
        alert("Une erreur s'est produite lors de la suppression du profil de l'entreprise.");
    }   
}

// Advertisements : POST

async function postAdvertisement() {
    let job_title = document.getElementById('job_title').value;
    let localisation = document.getElementById('localisation').value;
    let study_level = document.getElementById('study_level').value;
    let salary = document.getElementById('salary').value;
    let contract_type = document.getElementById('contract_type').value;
    let job_description = document.getElementById('job_description').value;
    let date_posted = document.getElementById('date_posted').value;
    let token = localStorage.getItem("token");

    let advertisementData = {
        job_title: job_title,
        localisation: localisation,
        study_level: study_level,
        salary: salary,
        contract_type: contract_type,
        job_description: job_description,
        date_posted: date_posted
    };

    try {
        let response = await fetch('http://127.0.0.1:8000/api/advertisements', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(advertisementData)
        });

        if (response.status === 403) {
            alert("Seuls les recruteurs peuvent poster une annonce.")
            window.location.href = "index.html";
            return;
        }

        let data = await response.json();

        console.log(data);
        alert(data.status);

    } catch (error) {
        console.error('Erreur:', error);
        alert("Une erreur s'est produite lors de la création de l'annonce.");
    }   
}

// Advertisement : GET

async function getLastAdvertisement() {
    let token = localStorage.getItem("token");

    try {
        let response = await fetch('http://127.0.0.1:8000/api/advertisements/last', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        let advertisement = await response.json();

        let adContainer = document.getElementById('ad-container');
        adContainer.innerHTML = `
            <h3>${advertisement.job_title}</h3>
            <p>Localisation: ${advertisement.localisation}</p>
            <p>Niveau d'étude: ${advertisement.study_level}</p>
            <p>Salaire: ${advertisement.salary}</p>
            <p>Type de contrat: ${advertisement.contract_type}</p>
            <p>Description: ${advertisement.job_description}</p>
            <p>Date de publication: ${advertisement.date_posted}</p>
        `;

    } catch (error) {
        console.error('Erreur:', error);
        alert("Une erreur s'est produite lors de la récupération de l'annonce.");
    }   
}

// Advertisement : PUT

async function modifyAdvertisement() {
    let job_title = document.getElementById('job_title_change').value;
    let localisation = document.getElementById('localisation_change').value;
    let study_level = document.getElementById('study_level_change').value;
    let salary = document.getElementById('salary_change').value;
    let contract_type = document.getElementById('contract_type_change').value;
    let job_description = document.getElementById('job_description_change').value;
    let date_posted = document.getElementById('date_posted_change').value;
    let token = localStorage.getItem("token");

    let advertisementData = {
        job_title: job_title,
        localisation: localisation,
        study_level: study_level,
        salary: salary,
        contract_type: contract_type,
        job_description: job_description,
        date_posted: date_posted
    };

    try {
        let response = await fetch('http://127.0.0.1:8000/api/advertisements', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(advertisementData)
        });

        if (response.status === 403) {
            alert("Seuls les recruteurs peuvent modifier une annonce.")
            window.location.href = "index.html";
            return;
        }

        let data = await response.json();

        console.log(data);
        alert(data.status);

    } catch (error) {
        console.error('Erreur:', error);
        alert("Une erreur s'est produite lors de la modification de l'annonce.");
    }   
}

// Advertisement : DELETE

async function deleteAdvertisement() {
    let token = localStorage.getItem("token");

    try {
        let response = await fetch('http://127.0.0.1:8000/api/advertisements', {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.status === 403) {
            alert("Seuls les recruteurs peuvent supprimer une annonce.")
            window.location.href = "index.html";
            return;
        }

        let data = await response.json();

        console.log(data);
        alert(data.status);

    } catch (error) {
        console.error('Erreur:', error);
        alert("Une erreur s'est produite lors de la suppression de l'annonce.");
    }   
}