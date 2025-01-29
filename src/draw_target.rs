use indicatif;
use pyo3::prelude::*;

use crate::in_memory::InMemoryTerm;

#[pyclass(module = "indicatif._indicatif")]
#[derive(Clone)]
pub(crate) enum ProgressDrawTarget {
    Stdout(Option<u8>),
    Stderr(Option<u8>),
    Hidden(),

    TermLike(InMemoryTerm),
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
    fn term_like(term_like: InMemoryTerm) -> Self {
        Self::TermLike(term_like)
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
            Self::TermLike(term_like) => {
                indicatif::ProgressDrawTarget::term_like(Box::new(term_like.0.clone()))
            }
        }
    }
}
