CREATE TABLE users
(
    uid VARCHAR(11),
    firstname VARCHAR,
    lastname VARCHAR,

    PRIMARY KEY (uid)
);

CREATE TABLE cabinets
(
    id VARCHAR,
    description VARCHAR,

    PRIMARY KEY (id)
);

CREATE TABLE categories
(
    id SERIAL,
    title VARCHAR NOT NULL,
    description VARCHAR,
    parent_id INTEGER DEFAULT NULL,

    PRIMARY KEY (id),
    UNIQUE (title),
    FOREIGN KEY (parent_id)
        REFERENCES categories (id)
        ON DELETE SET NULL
);

CREATE TABLE items
(
    id SERIAL,
    title VARCHAR NOT NULL,
    description VARCHAR,
    price FLOAT,
    link VARCHAR,
    category_id INTEGER,

    PRIMARY KEY (id),
    UNIQUE (title),
    FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE SET NULL
);

CREATE TABLE order_requests
(
    id SERIAL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    state INTEGER DEFAULT 0,
    item_id INTEGER,
    user_id VARCHAR,

    PRIMARY KEY (id),
    FOREIGN KEY (item_id)
        REFERENCES items(id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users (uid)
        ON DELETE CASCADE
);

CREATE TABLE storage_units
(
    id SERIAL,
    state INTEGER DEFAULT 0,
    verified BOOLEAN DEFAULT FALSE,
    item_id INTEGER,
    cabinet_id VARCHAR,

    FOREIGN KEY (item_id)
        REFERENCES items (id)
        ON DELETE SET NULL,
    FOREIGN KEY (cabinet_id)
        REFERENCES cabinets (id)
        ON DELETE SET NULL
);

CREATE TABLE cabinets_unlock_attempts
(
    id SERIAL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted BOOLEAN DEFAULT FALSE,
    user_id VARCHAR,
    cabinet_id VARCHAR,

    PRIMARY KEY (id),
    FOREIGN KEY (user_id)
        REFERENCES users (uid)
        ON DELETE CASCADE,
    FOREIGN KEY (cabinet_id)
        REFERENCES cabinets (id)
        ON DELETE CASCADE
);