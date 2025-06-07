CREATE TABLE IF NOT EXISTS login_nonces (
    id            SERIAL PRIMARY KEY,
    did             TEXT NOT NULL UNIQUE,
    nonce          TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS wallets (
    classic_address TEXT PRIMARY KEY,
    public_key    TEXT NOT NULL UNIQUE,
    seed         TEXT NOT NULL UNIQUE
);


-- 1. Create a table to persist registered DIDs (i.e. “users”)
CREATE TABLE IF NOT EXISTS users (
    id             SERIAL PRIMARY KEY,
    did            TEXT NOT NULL UNIQUE,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Create a table to store issued challenges for each DID
--    These should be cleaned up periodically once expired or consumed.
CREATE TABLE IF NOT EXISTS did_challenges (
    id             SERIAL PRIMARY KEY,
    did            TEXT NOT NULL,
    challenge      TEXT NOT NULL,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at     TIMESTAMPTZ NOT NULL,
    CONSTRAINT fk_challenge_user
        FOREIGN KEY(did)
        REFERENCES users(did)
        ON DELETE CASCADE
);

-- 3. Add an index to quickly look up unexpired challenges by DID
CREATE INDEX IF NOT EXISTS idx_did_challenges_did
    ON did_challenges(did);

-- 4. (Optional) A simple function to clean up expired challenges
CREATE OR REPLACE FUNCTION cleanup_expired_challenges()
RETURNS VOID AS $$
BEGIN
    DELETE FROM did_challenges
    WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;

-- 5. (Optional) Schedule that cleanup via pg_cron or your job scheduler:
--    SELECT cron.schedule('0 * * * *', 'SELECT cleanup_expired_challenges();');
