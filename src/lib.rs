use pyo3::prelude::*;

mod console;
mod draw_target;
mod format;
mod in_memory;
mod multi;
mod progress_bar;
mod state;
mod style;

use crate::draw_target::ProgressDrawTarget;
use crate::format::{
    BinaryBytes, DecimalBytes, HumanBytes, HumanCount, HumanDuration, HumanFloatCount,
};
use crate::in_memory::InMemoryTerm;
use crate::multi::{MultiProgress, MultiProgressAlignment};
use crate::progress_bar::ProgressBar;
use crate::state::ProgressFinish;
use crate::style::{ProgressStyle, TemplateError};

/// A Python module implemented in Rust.
#[pymodule]
#[pyo3(name = "_indicatif")]
fn py_indicatif(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ProgressBar>()?;
    m.add_class::<ProgressStyle>()?;
    m.add_class::<InMemoryTerm>()?;
    m.add_class::<TemplateError>()?;
    m.add_class::<ProgressFinish>()?;
    m.add_class::<ProgressDrawTarget>()?;
    m.add_class::<MultiProgress>()?;
    m.add_class::<MultiProgressAlignment>()?;

    m.add_class::<BinaryBytes>()?;
    m.add_class::<DecimalBytes>()?;
    m.add_class::<HumanBytes>()?;
    m.add_class::<HumanCount>()?;
    m.add_class::<HumanDuration>()?;
    m.add_class::<HumanFloatCount>()?;

    // console
    m.add_class::<console::Color>()?;
    m.add_class::<console::Emoji>()?;
    m.add_class::<console::Style>()?;
    m.add_class::<console::StyledObject>()?;

    Ok(())
}
