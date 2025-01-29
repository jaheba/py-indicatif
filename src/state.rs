use pyo3::prelude::*;

#[pyclass(module = "indicatif._indicatif")]
#[derive(Clone)]
pub(crate) enum ProgressFinish {
    AndLeave(),
    WithMessage(String),
    AndClear(),
    Abandon(),
    AbandonWithMessage(String),
}

impl ProgressFinish {
    pub fn native(&self) -> indicatif::ProgressFinish {
        match self {
            Self::AndLeave() => indicatif::ProgressFinish::AndLeave,
            Self::WithMessage(msg) => {
                indicatif::ProgressFinish::WithMessage(std::borrow::Cow::Owned(msg.clone()))
            }
            Self::AndClear() => indicatif::ProgressFinish::AndClear,
            Self::Abandon() => indicatif::ProgressFinish::Abandon,
            Self::AbandonWithMessage(msg) => {
                indicatif::ProgressFinish::AbandonWithMessage(std::borrow::Cow::Owned(msg.clone()))
            }
        }
    }
}
