use indicatif;
use pyo3::prelude::*;

use crate::{ProgressBar, ProgressDrawTarget};

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

    fn add(&self, pb: ProgressBar) -> ProgressBar {
        self.0.add(pb.0.clone());

        // pb.set_draw_target(pb.get);

        pb
    }

    fn insert_after(&self, after: &ProgressBar, pb: ProgressBar) -> ProgressBar {
        self.0.insert_after(&after.0, pb.0.clone());

        pb
    }

    fn println(&self, msg: String) -> std::io::Result<()> {
        self.0.println(msg)
    }

    // fn set_move_cursor(&self, move_cursor: bool) {
    //     self.0.set_
    // }

    // fn set_alignment(&self, alignment: MultiProgressAlignment) {}
}
