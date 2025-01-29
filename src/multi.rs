use indicatif;
use pyo3::prelude::*;
use pyo3::types::PyAny;

use crate::{ProgressBar, ProgressDrawTarget};

#[pyclass(eq, eq_int, module = "indicatif._indicatif")]
#[derive(PartialEq, Debug, Clone)]
pub(crate) enum MultiProgressAlignment {
    Top,
    Bottom,
}

impl MultiProgressAlignment {
    pub fn native(&self) -> indicatif::MultiProgressAlignment {
        match self {
            Self::Top => indicatif::MultiProgressAlignment::Top,
            Self::Bottom => indicatif::MultiProgressAlignment::Bottom,
        }
    }
}

#[pyclass(module = "indicatif._indicatif")]
pub(crate) struct MultiProgress(indicatif::MultiProgress);

#[pymethods]
impl MultiProgress {
    #[new]
    fn new() -> Self {
        Self(indicatif::MultiProgress::new())
    }

    #[staticmethod]
    fn with_draw_target(draw_target: &ProgressDrawTarget) -> Self {
        Self(indicatif::MultiProgress::with_draw_target(
            draw_target.native(),
        ))
    }

    fn set_draw_target(&self, draw_target: &ProgressDrawTarget) {
        self.0.set_draw_target(draw_target.native());
    }

    fn set_move_cursor(&self, move_cursor: bool) {
        self.0.set_move_cursor(move_cursor)
    }

    fn set_alignment(&self, alignment: MultiProgressAlignment) {
        self.0.set_alignment(alignment.native());
    }

    fn add(&self, pb: ProgressBar) -> ProgressBar {
        self.0.add(pb.0.clone());

        pb
    }

    fn insert(&self, index: usize, pb: ProgressBar) -> ProgressBar {
        self.0.insert(index, pb.0.clone());

        pb
    }

    fn insert_from_back(&self, index: usize, pb: ProgressBar) -> ProgressBar {
        self.0.insert_from_back(index, pb.0.clone());

        pb
    }

    fn insert_before(&self, before: &ProgressBar, pb: ProgressBar) -> ProgressBar {
        self.0.insert_before(&before.0, pb.0.clone());

        pb
    }

    fn insert_after(&self, after: &ProgressBar, pb: ProgressBar) -> ProgressBar {
        self.0.insert_after(&after.0, pb.0.clone());

        pb
    }

    fn remove(&self, pb: &ProgressBar) {
        self.0.remove(&pb.0)
    }

    fn println(&self, msg: String) -> std::io::Result<()> {
        self.0.println(msg)
    }

    fn suspend(&self, f: PyObject) -> PyResult<Py<PyAny>> {
        self.0.suspend(|| Python::with_gil(|py| f.call0(py)))
    }

    fn clear(&self) -> std::io::Result<()> {
        self.0.clear()
    }

    fn is_hidden(&self) -> bool {
        self.0.is_hidden()
    }
}
