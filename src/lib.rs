use multi::MultiProgress;
use pyo3::prelude::*;

mod console;
mod draw_target;
mod multi;
mod progress_bar;
mod style;

use crate::console::{Color, Style};
use crate::draw_target::ProgressDrawTarget;
use crate::progress_bar::ProgressBar;
use crate::style::{ProgressStyle, TemplateError};

/// A Python module implemented in Rust.
#[pymodule]
#[pyo3(name = "_indicatif")]
fn py_indicatif(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ProgressBar>()?;
    m.add_class::<ProgressStyle>()?;
    m.add_class::<TemplateError>()?;
    m.add_class::<ProgressDrawTarget>()?;
    m.add_class::<MultiProgress>()?;

    // console
    m.add_class::<Color>()?;
    m.add_class::<Style>()?;

    Ok(())
}
