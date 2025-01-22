use console;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyclass(eq, module = "indicatif._indicatif")]
#[derive(PartialEq, Copy, Clone)]
pub(crate) enum Color {
    Black(),
    Red(),
    Green(),
    Yellow(),
    Blue(),
    Magenta(),
    Cyan(),
    White(),
    Color256(u8),
}

#[pymethods]
impl Color {
    #[new]
    fn new(color: &str) -> PyResult<Self> {
        match color.to_lowercase().as_str() {
            "black" => Ok(Self::Black()),
            "red" => Ok(Self::Red()),
            "green" => Ok(Self::Green()),
            "yellow" => Ok(Self::Yellow()),
            "blue" => Ok(Self::Blue()),
            "magenta" => Ok(Self::Black()),
            "cyan" => Ok(Self::Black()),
            "white" => Ok(Self::White()),
            _ => Err(PyValueError::new_err(format!("No color: {}", color))),
        }
    }
}

impl Color {
    fn unwrap(&self) -> console::Color {
        match self {
            Self::Black() => console::Color::Black,
            Self::Red() => console::Color::Red,
            Self::Green() => console::Color::Green,
            Self::Yellow() => console::Color::Yellow,
            Self::Blue() => console::Color::Blue,
            Self::Magenta() => console::Color::Magenta,
            Self::Cyan() => console::Color::Cyan,
            Self::White() => console::Color::White,
            Self::Color256(n) => console::Color::Color256(*n),
        }
    }
}

#[pyclass]
pub(crate) struct Style(console::Style);

#[pymethods]
impl Style {
    #[new]
    fn new() -> Self {
        Self(console::Style::new())
    }

    #[staticmethod]
    fn from_dotted_str(s: &str) -> Self {
        Self(console::Style::from_dotted_str(&s))
    }

    fn apply_to(&self, val: String) -> StyledObject {
        StyledObject(self.0.apply_to(val))
    }

    fn force_styling(&self, value: bool) -> Self {
        Self(self.0.clone().force_styling(value))
    }

    fn for_stderr(&self) -> Self {
        Self(self.0.clone().for_stderr())
    }

    fn for_stdout(&self) -> Self {
        Self(self.0.clone().for_stdout())
    }

    fn fg(&self, color: Color) -> Self {
        Self(self.0.clone().fg(color.unwrap()))
    }
    fn bg(&self, color: Color) -> Self {
        Self(self.0.clone().bg(color.unwrap()))
    }

    fn bold(&self) -> Self {
        Self(self.0.clone().bold())
    }

    fn dim(&self) -> Self {
        Self(self.0.clone().dim())
    }

    // colors
    fn black(&self) -> Self {
        Self(self.0.clone().black())
    }
    fn red(&self) -> Self {
        Self(self.0.clone().red())
    }
    fn green(&self) -> Self {
        Self(self.0.clone().green())
    }
    fn yellow(&self) -> Self {
        Self(self.0.clone().yellow())
    }
    fn blue(&self) -> Self {
        Self(self.0.clone().blue())
    }
    fn magenta(&self) -> Self {
        Self(self.0.clone().magenta())
    }
    fn cyan(&self) -> Self {
        Self(self.0.clone().cyan())
    }
    fn white(&self) -> Self {
        Self(self.0.clone().white())
    }

    fn color256(&self, color: u8) -> Self {
        Self(self.0.clone().color256(color))
    }
}

#[pyclass]
pub(crate) struct StyledObject(console::StyledObject<String>);

#[pymethods]
impl StyledObject {
    fn __str__(&self) -> String {
        format!("{}", self.0)
    }

    fn force_styling(&self, value: bool) -> Self {
        Self(self.0.clone().force_styling(value))
    }

    fn for_stderr(&self) -> Self {
        Self(self.0.clone().for_stderr())
    }

    fn for_stdout(&self) -> Self {
        Self(self.0.clone().for_stdout())
    }

    fn fg(&self, color: Color) -> Self {
        Self(self.0.clone().fg(color.unwrap()))
    }
    fn bg(&self, color: Color) -> Self {
        Self(self.0.clone().bg(color.unwrap()))
    }

    fn bold(&self) -> Self {
        Self(self.0.clone().bold())
    }

    fn dim(&self) -> Self {
        Self(self.0.clone().dim())
    }

    // colors
    fn black(&self) -> Self {
        Self(self.0.clone().black())
    }
    fn red(&self) -> Self {
        Self(self.0.clone().red())
    }
    fn green(&self) -> Self {
        Self(self.0.clone().green())
    }
    fn yellow(&self) -> Self {
        Self(self.0.clone().yellow())
    }
    fn blue(&self) -> Self {
        Self(self.0.clone().blue())
    }
    fn magenta(&self) -> Self {
        Self(self.0.clone().magenta())
    }
    fn cyan(&self) -> Self {
        Self(self.0.clone().cyan())
    }
    fn white(&self) -> Self {
        Self(self.0.clone().white())
    }

    fn color256(&self, color: u8) -> Self {
        Self(self.0.clone().color256(color))
    }
}

#[pyclass]
pub(crate) struct Emoji {
    emoji: String,
    fallback: String,
}

#[pymethods]
impl Emoji {
    #[new]
    fn new(emoji: String, fallback: String) -> Self {
        Self { emoji, fallback }
    }

    fn __str__(&self) -> String {
        format!("{}", self)
    }
}

impl std::fmt::Display for Emoji {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        console::Emoji(&self.emoji, &self.fallback).fmt(f)
    }
}
