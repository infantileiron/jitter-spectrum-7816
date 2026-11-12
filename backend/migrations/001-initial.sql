-- Initial demo schema comes from versioned SQLAlchemy metadata.
-- DOUBLE time/frequency parameters; JSON retains original points, no imputation.
-- Unique dataset/window/study names and report.run_id. Production requires reviewed ALTER migrations.
-- signal_datasets.version steps on each applied backfill; spectral_runs keeps dataset_version,
-- input_points snapshot and stale flag; backfill_batches records applied late-arrival batches.
CREATE INDEX IF NOT EXISTS ix_spectral_runs_status ON spectral_runs(status);
CREATE INDEX IF NOT EXISTS ix_backfill_batches_dataset ON backfill_batches(dataset_id);
