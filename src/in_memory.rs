use indicatif::{self, TermLike};

use pyo3::prelude::*;

#[pyclass(module = "indicatif._indicatif")]
#[derive(Clone)]
pub struct InMemoryTerm(pub indicatif::InMemoryTerm);

#[pymethods]
impl InMemoryTerm {
    #[new]
    fn new(rows: u16, cols: u16) -> Self {
        Self(indicatif::InMemoryTerm::new(rows, cols))
    }

    fn reset(&self) {
        self.0.reset()
    }

    fn contents(&self) -> String {
        self.0.contents()
    }

    fn contents_formatted(&self) -> Vec<u8> {
        self.0.contents_formatted()
    }

    fn moves_since_last_check(&self) -> String {
        self.0.moves_since_last_check()
    }

    // impl TermLike for InMemoryTerm

    fn width(&self) -> u16 {
        self.0.width()
    }

    fn height(&self) -> u16 {
        self.0.height()
    }

    fn move_cursor_up(&self, n: usize) -> std::io::Result<()> {
        self.0.move_cursor_up(n)
    }

    fn move_cursor_down(&self, n: usize) -> std::io::Result<()> {
        self.0.move_cursor_down(n)
    }

    fn move_cursor_right(&self, n: usize) -> std::io::Result<()> {
        self.0.move_cursor_right(n)
    }

    fn move_cursor_left(&self, n: usize) -> std::io::Result<()> {
        self.0.move_cursor_left(n)
    }

    fn write_line(&self, s: &str) -> std::io::Result<()> {
        self.0.write_line(s)
    }

    fn write_str(&self, s: &str) -> std::io::Result<()> {
        self.0.write_str(s)
    }

    fn clear_line(&self) -> std::io::Result<()> {
        self.0.clear_line()
    }

    fn flush(&self) -> std::io::Result<()> {
        self.0.flush()
    }
}
