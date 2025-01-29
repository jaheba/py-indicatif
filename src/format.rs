use std::time::Duration;

use indicatif;

use pyo3::prelude::*;

#[pyclass(module = "indicatif._indicatif")]
pub struct HumanBytes(pub u64);

#[pymethods]
impl HumanBytes {
    #[new]
    fn new(bytes: u64) -> Self {
        Self(bytes)
    }

    fn __str__(&self) -> String {
        format!("{}", indicatif::HumanBytes(self.0))
    }
}

#[pyclass(module = "indicatif._indicatif")]
pub struct DecimalBytes(pub u64);

#[pymethods]
impl DecimalBytes {
    #[new]
    fn new(bytes: u64) -> Self {
        Self(bytes)
    }

    fn __str__(&self) -> String {
        format!("{}", indicatif::DecimalBytes(self.0))
    }
}

#[pyclass(module = "indicatif._indicatif")]
pub struct BinaryBytes(pub u64);

#[pymethods]
impl BinaryBytes {
    #[new]
    fn new(bytes: u64) -> Self {
        Self(bytes)
    }

    fn __str__(&self) -> String {
        format!("{}", indicatif::BinaryBytes(self.0))
    }
}

#[pyclass(module = "indicatif._indicatif")]
pub struct HumanDuration(pub Duration);

#[pymethods]
impl HumanDuration {
    #[new]
    fn new(duration: Duration) -> Self {
        Self(duration)
    }

    fn __str__(&self) -> String {
        format!("{}", indicatif::HumanDuration(self.0))
    }
}

#[pyclass(module = "indicatif._indicatif")]
pub struct HumanCount(pub u64);

#[pymethods]
impl HumanCount {
    #[new]
    fn new(count: u64) -> Self {
        Self(count)
    }

    fn __str__(&self) -> String {
        format!("{}", indicatif::HumanCount(self.0))
    }
}

#[pyclass(module = "indicatif._indicatif")]
pub struct HumanFloatCount(pub f64);

#[pymethods]
impl HumanFloatCount {
    #[new]
    fn new(count: f64) -> Self {
        Self(count)
    }

    fn __str__(&self) -> String {
        format!("{}", indicatif::HumanFloatCount(self.0))
    }
}
