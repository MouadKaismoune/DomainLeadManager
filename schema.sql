PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;


-- =====================================================
-- 1. DOMAINS
-- =====================================================

CREATE TABLE domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    domain_name TEXT NOT NULL,

    normalized_domain TEXT NOT NULL UNIQUE,

    extension TEXT,

    status TEXT NOT NULL DEFAULT 'active'
        CHECK (
            status IN (
                'active',
                'sold',
                'archived'
            )
        ),

    notes TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- 2. COMPANIES
-- =====================================================

CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_name TEXT NOT NULL,

    normalized_name TEXT NOT NULL,

    website TEXT,

    normalized_website TEXT,

    description TEXT,

    address TEXT,

    city TEXT,

    state TEXT,

    country TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- 3. DOMAIN LEADS
-- Relationship between domains and companies
-- =====================================================

CREATE TABLE domain_leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    domain_id INTEGER NOT NULL,

    company_id INTEGER NOT NULL,

    company_name TEXT,
    company_website TEXT,
    company_description TEXT,
    company_address TEXT,
    company_city TEXT,
    company_state TEXT,
    company_country TEXT,

    status TEXT NOT NULL DEFAULT 'new'
        CHECK (
            status IN (
                'new',
                'researching',
                'ready',
                'contacted',
                'interested',
                'not_interested',
                'archived'
            )
        ),

    priority TEXT NOT NULL DEFAULT 'normal'
        CHECK (
            priority IN (
                'low',
                'normal',
                'high'
            )
        ),

    notes TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (domain_id)
        REFERENCES domains(id)
        ON DELETE CASCADE,

    FOREIGN KEY (company_id)
        REFERENCES companies(id)
        ON DELETE CASCADE,

    UNIQUE (domain_id, company_id)
);


-- =====================================================
-- 4. COMPANY EMAILS
-- Emails belonging to the company
-- Example:
-- info@company.com
-- sales@company.com
-- =====================================================

CREATE TABLE company_emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    email TEXT NOT NULL,

    normalized_email TEXT NOT NULL UNIQUE,

    email_type TEXT NOT NULL DEFAULT 'general'
        CHECK (
            email_type IN (
                'general',
                'sales',
                'support',
                'info',
                'marketing',
                'other'
            )
        ),

    is_primary INTEGER NOT NULL DEFAULT 0
        CHECK (is_primary IN (0, 1)),

    source TEXT,

    notes TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (company_id)
        REFERENCES companies(id)
        ON DELETE CASCADE
);


-- =====================================================
-- 5. CONTACTS
-- People working at companies
-- =====================================================

CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    first_name TEXT,

    last_name TEXT,

    full_name TEXT NOT NULL,

    normalized_name TEXT NOT NULL,

    job_title TEXT,

    department TEXT,

    notes TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (company_id)
        REFERENCES companies(id)
        ON DELETE CASCADE
);


-- =====================================================
-- 6. CONTACT EMAILS
-- Each email belongs to ONE contact only
-- =====================================================

CREATE TABLE contact_emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    contact_id INTEGER NOT NULL,

    email TEXT NOT NULL,

    normalized_email TEXT NOT NULL UNIQUE,

    email_type TEXT NOT NULL DEFAULT 'work'
        CHECK (
            email_type IN (
                'work',
                'personal',
                'other'
            )
        ),

    is_primary INTEGER NOT NULL DEFAULT 0
        CHECK (is_primary IN (0, 1)),

    source TEXT,

    notes TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (contact_id)
        REFERENCES contacts(id)
        ON DELETE CASCADE
);


-- =====================================================
-- 7. COMPANY PHONES
-- =====================================================

CREATE TABLE company_phones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    phone TEXT NOT NULL,

    normalized_phone TEXT NOT NULL,

    phone_type TEXT NOT NULL DEFAULT 'business'
        CHECK (
            phone_type IN (
                'business',
                'mobile',
                'fax',
                'other'
            )
        ),

    is_primary INTEGER NOT NULL DEFAULT 0
        CHECK (is_primary IN (0, 1)),

    source TEXT,

    notes TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (company_id)
        REFERENCES companies(id)
        ON DELETE CASCADE
);


-- =====================================================
-- 8. CONTACT PHONES
-- =====================================================

CREATE TABLE contact_phones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    contact_id INTEGER NOT NULL,

    phone TEXT NOT NULL,

    normalized_phone TEXT NOT NULL,

    phone_type TEXT NOT NULL DEFAULT 'mobile'
        CHECK (
            phone_type IN (
                'mobile',
                'work',
                'home',
                'other'
            )
        ),

    is_primary INTEGER NOT NULL DEFAULT 0
        CHECK (is_primary IN (0, 1)),

    source TEXT,

    notes TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (contact_id)
        REFERENCES contacts(id)
        ON DELETE CASCADE
);


-- =====================================================
-- 9. COMPANY SOCIAL ACCOUNTS
-- =====================================================

CREATE TABLE company_socials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    platform TEXT NOT NULL,

    url TEXT NOT NULL,

    normalized_url TEXT NOT NULL,

    source TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (company_id)
        REFERENCES companies(id)
        ON DELETE CASCADE
);


-- =====================================================
-- 10. CONTACT SOCIAL ACCOUNTS
-- =====================================================

CREATE TABLE contact_socials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    contact_id INTEGER NOT NULL,

    platform TEXT NOT NULL,

    url TEXT NOT NULL,

    normalized_url TEXT NOT NULL,

    source TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (contact_id)
        REFERENCES contacts(id)
        ON DELETE CASCADE
);


-- =====================================================
-- INDEXES
-- =====================================================

-- Domains

CREATE INDEX idx_domains_normalized_domain
ON domains(normalized_domain);

CREATE INDEX idx_domains_status
ON domains(status);


-- Companies

CREATE INDEX idx_companies_normalized_name
ON companies(normalized_name);

CREATE INDEX idx_companies_normalized_website
ON companies(normalized_website);


-- Domain Leads

CREATE INDEX idx_domain_leads_domain_id
ON domain_leads(domain_id);

CREATE INDEX idx_domain_leads_company_id
ON domain_leads(company_id);

CREATE INDEX idx_domain_leads_status
ON domain_leads(status);

CREATE INDEX idx_domain_leads_priority
ON domain_leads(priority);


-- =====================================================
-- 3A. DOMAIN-SCOPED COMPANY DATA
-- Information entered for one domain opportunity only
-- =====================================================

CREATE TABLE IF NOT EXISTS domain_lead_company_emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_lead_id INTEGER NOT NULL,
    email TEXT NOT NULL,
    normalized_email TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_lead_id) REFERENCES domain_leads(id) ON DELETE CASCADE,
    UNIQUE (domain_lead_id, normalized_email)
);

CREATE TABLE IF NOT EXISTS domain_lead_company_phones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_lead_id INTEGER NOT NULL,
    phone TEXT NOT NULL,
    normalized_phone TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_lead_id) REFERENCES domain_leads(id) ON DELETE CASCADE,
    UNIQUE (domain_lead_id, normalized_phone)
);

CREATE TABLE IF NOT EXISTS domain_lead_company_socials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_lead_id INTEGER NOT NULL,
    platform TEXT NOT NULL,
    url TEXT NOT NULL,
    normalized_url TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_lead_id) REFERENCES domain_leads(id) ON DELETE CASCADE
);


-- =====================================================
-- 3B. DOMAIN-SCOPED CONTACTS
-- A contact entered for one opportunity must not leak into another
-- =====================================================

CREATE TABLE IF NOT EXISTS domain_lead_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_lead_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    job_title TEXT,
    department TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_lead_id) REFERENCES domain_leads(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS domain_lead_contact_emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_lead_contact_id INTEGER NOT NULL,
    email TEXT NOT NULL,
    normalized_email TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_lead_contact_id) REFERENCES domain_lead_contacts(id) ON DELETE CASCADE,
    UNIQUE (domain_lead_contact_id, normalized_email)
);

CREATE TABLE IF NOT EXISTS domain_lead_contact_phones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_lead_contact_id INTEGER NOT NULL,
    phone TEXT NOT NULL,
    normalized_phone TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_lead_contact_id) REFERENCES domain_lead_contacts(id) ON DELETE CASCADE,
    UNIQUE (domain_lead_contact_id, normalized_phone)
);

CREATE TABLE IF NOT EXISTS domain_lead_contact_socials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_lead_contact_id INTEGER NOT NULL,
    platform TEXT NOT NULL,
    url TEXT NOT NULL,
    normalized_url TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_lead_contact_id) REFERENCES domain_lead_contacts(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_domain_lead_company_emails_lead_id
ON domain_lead_company_emails(domain_lead_id);

CREATE INDEX IF NOT EXISTS idx_domain_lead_contacts_lead_id
ON domain_lead_contacts(domain_lead_id);

CREATE INDEX IF NOT EXISTS idx_domain_lead_contact_emails_contact_id
ON domain_lead_contact_emails(domain_lead_contact_id);


-- Company Emails

CREATE INDEX idx_company_emails_company_id
ON company_emails(company_id);

CREATE INDEX idx_company_emails_normalized_email
ON company_emails(normalized_email);


-- Contacts

CREATE INDEX idx_contacts_company_id
ON contacts(company_id);

CREATE INDEX idx_contacts_normalized_name
ON contacts(normalized_name);


-- Contact Emails

CREATE INDEX idx_contact_emails_contact_id
ON contact_emails(contact_id);

CREATE INDEX idx_contact_emails_normalized_email
ON contact_emails(normalized_email);


-- Company Phones

CREATE INDEX idx_company_phones_company_id
ON company_phones(company_id);

CREATE INDEX idx_company_phones_normalized_phone
ON company_phones(normalized_phone);


-- Contact Phones

CREATE INDEX idx_contact_phones_contact_id
ON contact_phones(contact_id);

CREATE INDEX idx_contact_phones_normalized_phone
ON contact_phones(normalized_phone);


-- Company Socials

CREATE INDEX idx_company_socials_company_id
ON company_socials(company_id);

CREATE INDEX idx_company_socials_normalized_url
ON company_socials(normalized_url);


-- Contact Socials

CREATE INDEX idx_contact_socials_contact_id
ON contact_socials(contact_id);

CREATE INDEX idx_contact_socials_normalized_url
ON contact_socials(normalized_url);


COMMIT;
