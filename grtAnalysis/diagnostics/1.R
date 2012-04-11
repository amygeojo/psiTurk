# Example Data Diagnostics Script

# Check that all the test phases have 50 items
expect_that (all(daply(testtrials, .(subjid), nrow)==50), is_true())

