use pyo3::exceptions::{PyException, PyOSError};
use pyo3::prelude::*;

#[pyclass(module = "indicatif._indicatif", extends = PyException)]
#[derive(Debug)]
pub(crate) struct TemplateError(indicatif::style::TemplateError);

impl std::fmt::Display for TemplateError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.0.fmt(f)
    }
}

impl std::error::Error for TemplateError {}

impl std::convert::From<TemplateError> for PyErr {
    fn from(err: TemplateError) -> PyErr {
        PyOSError::new_err(err.to_string())
    }
}

#[pyclass(module = "indicatif._indicatif")]
#[derive(Clone)]
pub(crate) struct ProgressStyle(pub indicatif::style::ProgressStyle);

#[pymethods]
impl ProgressStyle {
    #[new]
    #[pyo3(signature = (template = None, progress_chars = None, tick_chars = None))]
    fn new(
        template: Option<&str>,
        progress_chars: Option<&str>,
        tick_chars: Option<&str>,
    ) -> PyResult<Self> {
        let mut inner = indicatif::style::ProgressStyle::default_bar();

        if let Some(template) = template {
            inner = inner.template(template).map_err(TemplateError)?;
        }

        if let Some(progress_chars) = progress_chars {
            inner = inner.progress_chars(progress_chars);
        }
        if let Some(tick_chars) = tick_chars {
            inner = inner.tick_chars(tick_chars);
        }

        Ok(Self(inner))
    }

    #[staticmethod]
    fn default_bar() -> Self {
        Self(indicatif::style::ProgressStyle::default_bar())
    }

    #[staticmethod]
    fn default_spinner() -> Self {
        Self(indicatif::style::ProgressStyle::default_spinner())
    }

    #[staticmethod]
    fn with_template(template: &str) -> Result<Self, TemplateError> {
        indicatif::style::ProgressStyle::with_template(template)
            .map(Self)
            .map_err(TemplateError)
    }

    fn tick_chars(&self, s: &str) -> Self {
        Self(self.0.clone().tick_chars(s))
    }

    fn tick_strings(&self, s: Vec<String>) -> Self {
        let refs: Vec<&str> = s.iter().map(|s| s.as_str()).collect();
        Self(self.0.clone().tick_strings(&refs))
    }

    fn progress_chars(&self, s: &str) -> Self {
        Self(self.0.clone().progress_chars(s))
    }

    fn template(&self, s: &str) -> Result<Self, TemplateError> {
        self.0.clone().template(s).map(Self).map_err(TemplateError)
    }

    fn get_tick_str(&self, idx: u64) -> &str {
        self.0.get_tick_str(idx)
    }

    fn get_final_tick_str(&self) -> &str {
        self.0.get_final_tick_str()
    }
}
