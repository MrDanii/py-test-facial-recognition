-- This script creates database table in our postgresql server

CREATE TABLE IF NOT EXISTS "AddressPersonImage" (
	"idAddressPersonImage" SERIAL,
	"idAddress" VARCHAR NULL,
	"personName" VARCHAR NULL,
	"embeddings" FLOAT[],
	"isActive" BOOLEAN DEFAULT TRUE,
	"createdBy" TIMESTAMP DEFAULT now()
)
