-- Companies table
CREATE TABLE companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(255) NOT NULL,
    company_website VARCHAR(255),
    company_address TEXT,
    recruiter_id INT,
    FOREIGN KEY (recruiter_id) REFERENCES people(person_id);
);

-- Advertisements table
CREATE TABLE advertisements (
    ad_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT NOT NULL,
    localisation VARCHAR(255) NOT NULL,
    study_level ENUM('CAP', 'BEP', 'Bac','Bac+2', 'Bac+3', 'Bac+5', 'Bac+8') NOT NULL,
    salary VARCHAR(255) NOT NULL,
    contract_type ENUM('CDI', 'CDD', 'Stage', 'Alternance') NOT NULL,
    job_description TEXT NOT NULL,
    date_posted DATE NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- People Table
CREATE TABLE people (
    person_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM("Candidat", "Recruteur") NOT NULL
);

-- Applications Table
CREATE TABLE applications (
    application_id INT PRIMARY KEY AUTO_INCREMENT, -- stocke un id unique pour chaque candidature dans la table ; INT = signifie que le type de données de cette colone est un entier ; Primary key = indique que cette colonne est la clé primaire de la table, ce qui signifie que chaque valeur doit être unique et qu'aucune valeur nulle n'est autorisée ; auto-increment = signifie que MySQL augmentera automatiquement la valeur de cette colonne de 1 à chaque nouvelle entrée, ce qui garantit que chaque candidature aura un identifiant unique
    ad_id INT, -- stocke l'identifiant de l'annonce à laquelle la candidature est soumise.
    applicant_id INT, -- stocke l'identifiant du candidat qui a soumis la candidature.
    date_applied DATE, -- type de données utilisé ici, ce qui permet de stocker une date sous la forme AAAA-MM-JJ.
    email_content TEXT, -- type de données, choisi ici car le contenu de l'email peut être assez long
    status ENUM('En attente', 'Acceptée', 'Refusée') DEFAULT 'En attente', -- 'status' indique le statut actuel de la candidature ; enum = énumération, signifie que le statut peut prendre l'une de ces trois valeurs ; default = définit la valeur par défaut de cette colonne à 'En attente', ce qui signifie que si aucune valeur n'est spécifiée lors de la création d'une nouvelle entrée, le statut sera automatiquement défini sur 'En attente'.
    FOREIGN KEY (ad_id) REFERENCES advertisements(ad_id),
    FOREIGN KEY (applicant_id) REFERENCES people(person_id) -- cette ligne crée une foreign-key sur la colonne applicant_id, la reliant à la colonne person_id dans la table people. Cela garantit que chaque applicant_id dans la table applications doit correspondre à un person_id existant dans la table people.
);

-- Primary key = colonne dans une table de base de données qui a un identifiant unique pour chaque ligne (chaque valeur est unique et non NULL) ; utilisée pour identifier de manière unique chaque enregistrement de la table.
-- Auto-increment = chaque nouvelle entrée dans la table aura la valeur automatiquement augmentée par rapport à l'entrée précédente (garantit l'unicité)
-- Foreign key = colonne qui crée une relation entre deux tables ; la foreign key fait référence à la primary key d'une autre table
-- REFERENCES = mot-clé utilisé pour définir à quelle clé primaire dans une autre table une clé étrangère fait référence.