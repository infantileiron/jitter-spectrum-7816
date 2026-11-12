-- Initial demo schema comes from versioned SQLAlchemy metadata.
-- DOUBLE time/frequency parameters; JSON retains original points, no imputation.
-- Unique dataset/window/study names and report.run_id. Production requires reviewed ALTER migrations.
CREATE INDEX IF NOT EXISTS ix_spectral_runs_status ON spectral_runs(status);
