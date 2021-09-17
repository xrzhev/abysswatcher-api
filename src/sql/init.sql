BEGIN TRANSACTION;

CREATE TABLE "cert_state" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"state"	TEXT NOT NULL UNIQUE
);
INSERT INTO "cert_state" ("id","state") VALUES (1,'Fine');
INSERT INTO "cert_state" ("id","state") VALUES (2,'Warning');
INSERT INTO "cert_state" ("id","state") VALUES (3,'Danger');
INSERT INTO "cert_state" ("id","state") VALUES (4,'Expired');

CREATE TABLE "certs" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"port_id"	INTEGER NOT NULL UNIQUE,
	"begin_date"	TEXT,
	"expire_date"	TEXT,
	"begin_unixtime"	INTEGER,
	"expire_unixtime"	INTEGER,
	"issuer"	TEXT,
	"last_update"	TEXT,
	"cert_state"	INTEGER
);

CREATE TABLE "hosts" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"url"	TEXT NOT NULL UNIQUE
);

CREATE TABLE "ports" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"host_id"	INTEGER NOT NULL,
	"port"	INTEGER NOT NULL
);


CREATE INDEX "cert_state_index" ON "cert_state" (
	"id"	ASC,
	"state"	ASC
);

CREATE INDEX "certs_index" ON "certs" (
	"id"	ASC,
	"port_id"	ASC
);

CREATE INDEX "hosts_index" ON "hosts" (
	"id"	ASC,
	"url"	ASC
);

CREATE INDEX "ports_index" ON "ports" (
	"id"	ASC,
	"host_id"	ASC,
	"port"	ASC
);

COMMIT;
