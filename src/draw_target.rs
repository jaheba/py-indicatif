use indicatif;
use pyo3::prelude::*;

#[pyclass(module = "indicatif._indicatif")]
#[derive(Clone)]
pub(crate) enum ProgressDrawTarget {
    Stdout(Option<u8>),
    Stderr(Option<u8>),
    Hidden(),
}

#[pymethods]
impl ProgressDrawTarget {
    #[staticmethod]
    #[pyo3(signature = (refresh_rate=None))]
    fn stdout(refresh_rate: Option<u8>) -> Self {
        Self::Stdout(refresh_rate)
    }

    #[staticmethod]
    #[pyo3(signature = (refresh_rate=None))]
    fn stderr(refresh_rate: Option<u8>) -> Self {
        Self::Stderr(refresh_rate)
    }

    #[staticmethod]
    fn hidden() -> Self {
        Self::Hidden()
    }

    fn is_hidden(&self) -> bool {
        self.native().is_hidden()
    }
}

impl ProgressDrawTarget {
    pub(crate) fn native(&self) -> indicatif::ProgressDrawTarget {
        match self {
            Self::Stdout(refresh_rate) => refresh_rate.map_or_else(
                indicatif::ProgressDrawTarget::stdout,
                indicatif::ProgressDrawTarget::stdout_with_hz,
            ),
            Self::Stderr(refresh_rate) => refresh_rate.map_or_else(
                indicatif::ProgressDrawTarget::stderr,
                indicatif::ProgressDrawTarget::stderr_with_hz,
            ),

            Self::Hidden() => indicatif::ProgressDrawTarget::hidden(),
        }
    }
}
