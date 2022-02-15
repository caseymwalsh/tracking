# tracking
CREATE TABLE "tracking" (
    "id"    INTEGER,
    "trackingnumber"    TEXT NOT NULL UNIQUE,
    "status"    TEXT,
    "location"  TEXT,
    "shipper"   TEXT NOT NULL,
    "active"    INTEGER NOT NULL DEFAULT 1,
    "note"  TEXT,
    PRIMARY KEY("id" AUTOINCREMENT)
);
