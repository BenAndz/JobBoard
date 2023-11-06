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
    application_id INT PRIMARY KEY AUTO_INCREMENT, 
    ad_id INT, 
    applicant_id INT, 
    date_applied DATE, 
    email_content TEXT,
    status ENUM('En attente', 'Acceptée', 'Refusée') DEFAULT 'En attente', 
    FOREIGN KEY (ad_id) REFERENCES advertisements(ad_id),
    FOREIGN KEY (applicant_id) REFERENCES people(person_id) 
)
