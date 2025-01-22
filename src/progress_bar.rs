use std::{borrow::Cow, time::Duration};

use pyo3::prelude::*;

use crate::{ProgressDrawTarget, ProgressStyle};

#[pyclass(module = "indicatif._indicatif")]
#[derive(Clone)]
pub(crate) struct ProgressBar(pub indicatif::ProgressBar);

#[pymethods]
impl ProgressBar {
    #[new]
    #[pyo3(signature = (length=None, message=None, prefix=None, style=None))]
    fn init(
        length: Option<u64>,
        message: Option<String>,
        prefix: Option<String>,
        style: Option<ProgressStyle>,
    ) -> Self {
        let mut inner = length.map_or_else(
            indicatif::ProgressBar::no_length,
            indicatif::ProgressBar::new,
        );

        if let Some(message) = message {
            inner = inner.with_message(message);
        }

        if let Some(prefix) = prefix {
            inner = inner.with_prefix(prefix);
        }

        if let Some(style) = style {
            inner = inner.with_style(style.0);
        }

        Self(inner)
    }

    #[staticmethod]
    fn new(len: u64) -> Self {
        Self(indicatif::ProgressBar::new(len))
    }

    #[staticmethod]
    fn no_length() -> Self {
        Self(indicatif::ProgressBar::no_length())
    }

    #[staticmethod]
    fn hidden() -> Self {
        Self(indicatif::ProgressBar::hidden())
    }

    #[staticmethod]
    fn new_spinner() -> Self {
        Self(indicatif::ProgressBar::new_spinner())
    }

    #[staticmethod]
    #[pyo3(signature = (len, draw_target))]
    fn with_draw_target(len: Option<u64>, draw_target: ProgressDrawTarget) -> Self {
        Self(indicatif::ProgressBar::with_draw_target(
            len,
            draw_target.native(),
        ))
    }

    //methods

    #[pyo3(signature = (msg=None))]
    fn abandon(&self, msg: Option<String>) {
        if let Some(msg) = msg {
            self.0.abandon_with_message(msg);
        } else {
            self.0.abandon();
        }
    }

    fn enable_steady_tick(&self, interval: Duration) {
        self.0.enable_steady_tick(interval);
    }

    fn disable_steady_tick(&self) {
        self.0.disable_steady_tick()
    }

    fn duration(&self) -> Duration {
        self.0.duration()
    }

    fn elapsed(&self) -> Duration {
        self.0.elapsed()
    }

    fn eta(&self) -> Duration {
        self.0.eta()
    }

    fn inc(&self, delta: u64) {
        self.0.inc(delta)
    }

    #[getter]
    fn message(&self) -> String {
        self.0.message()
    }

    #[setter]
    fn set_message(&self, title: String) {
        self.0.set_message(Cow::from(title))
    }

    #[getter]
    fn prefix(&self) -> String {
        self.0.prefix()
    }

    #[setter]
    fn set_prefix(&self, prefix: String) {
        self.0.set_prefix(prefix)
    }

    #[getter]
    fn style(&self) -> ProgressStyle {
        ProgressStyle(self.0.style())
    }

    #[setter]
    fn set_style(&self, style: ProgressStyle) {
        self.0.set_style(style.0.clone());
    }

    #[pyo3(signature = (msg=None))]
    fn finish(&self, msg: Option<String>) {
        if let Some(msg) = msg {
            self.0.finish_with_message(msg)
        } else {
            self.0.finish()
        }
    }

    fn tick(&self) {
        self.0.tick()
    }

    fn is_hidden(&self) -> bool {
        self.0.is_hidden()
    }

    fn is_finished(&self) -> bool {
        self.0.is_finished()
    }

    fn println(&self, msg: String) {
        self.0.println(msg)
    }

    #[getter]
    fn position(&self) -> u64 {
        self.0.position()
    }

    #[setter]
    fn set_position(&self, pos: u64) {
        self.0.set_position(pos)
    }

    #[getter]
    fn length(&self) -> Option<u64> {
        self.0.length()
    }

    #[setter]
    fn set_length(&self, len: Option<u64>) {
        if let Some(len) = len {
            self.0.set_length(len)
        } else {
            self.0.unset_length();
        }
    }

    fn unset_length(&self) {
        self.0.unset_length()
    }

    fn inc_length(&self, delta: u64) {
        self.0.inc_length(delta)
    }

    fn reset(&self) {
        self.0.reset()
    }

    fn finish_and_clear(&self) {
        self.0.finish_and_clear()
    }

    fn with_style(&self, style: ProgressStyle) -> Self {
        self.set_style(style);
        self.clone()
    }
}
