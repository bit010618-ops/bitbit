from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location


SOURCE = Path(__file__).with_name("make_dsp_batch_400_436_redraw.py").read_text(encoding="utf-8")


def load_generator_module():
    path = Path(__file__).with_name("make_dsp_batch_400_436_redraw.py")
    spec = spec_from_file_location("multirate_generator", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_multirate_generator_is_valid_python():
    compile(SOURCE.lstrip("\ufeff"), "make_dsp_batch_400_436_redraw.py", "exec")


def test_decimation_derivation_preserves_source_pages_406_to_408():
    assert "def decimation_full_derivation" in SOURCE
    assert r"X_d(e^{j\omega})=\frac{1}{M}\sum_{i=0}^{M-1}X(e^{j\frac{\omega-2\pi i}{M}})" in SOURCE
    assert r"X_d(e^{j\omega})=\frac{1}{2}\left[X(e^{j\frac{\omega}{2}})+X(e^{j(\frac{\omega}{2}-\pi)})\right]" in SOURCE


def test_interpolation_derivation_preserves_source_pages_417_to_420():
    assert "def interpolation_full_derivation" in SOURCE
    assert r"x_p(n)=\sum_{k=-\infty}^{\infty}x(k)\delta(n-kL)" in SOURCE
    assert r"X_p(e^{j\omega})=X(e^{j\omega L})" in SOURCE


def test_spectrum_vertical_axis_arrow_clears_the_highest_sample_dot():
    geometry = load_generator_module().spectrum_axis_geometry()
    assert geometry["vertical_arrow_headroom"] >= 10


def test_decimation_filter_uses_stacked_pi_over_m_fractions():
    body = SOURCE.split("def filter_cascade", 1)[1].split("\ndef ", 1)[0]
    assert r"\frac{\pi}{M}" in body
    assert r"\pi/M" not in body


def test_fractional_conversion_examples_preserve_source_pages_423_to_432():
    assert "def fractional_conversion_details" in SOURCE
    assert "先内插、再滤波、最后抽取" in SOURCE
    assert r"\frac{48000}{44100}=\frac{160}{147}" in SOURCE
    body = SOURCE.split("def fractional_conversion_details", 1)[1].split("\ndef ", 1)[0]
    assert r"\omega_c=\min\left(\frac{\pi}{L},\frac{\pi}{M}\right)" in body
    assert r"\min\left(\frac{\pi}{3},\frac{\pi}{2}\right)=\frac{\pi}{3}" in body
    assert "π/L" not in body
    assert "π/M" not in body
    assert "π/3" not in body
    assert "π/2" not in body


def test_multirate_subsections_do_not_force_sparse_new_pages():
    for name in (
        "decimation_full_derivation",
        "interpolation_full_derivation",
        "fractional_conversion_details",
    ):
        body = SOURCE.split(f"def {name}", 1)[1].split("\ndef ", 1)[0]
        assert "doc.new_page()" not in body


def test_source_pages_424_to_436_exercises_and_answers_are_retained():
    assert "def source_exercises_and_answers" in SOURCE
    assert "答案：先插值，再抽取" in SOURCE
    assert "答案：A、C" in SOURCE
    assert "截止频率为 π/2，增益为 1" in SOURCE
    assert r"y(m)=x(2m)" in SOURCE
    assert r"D=\frac{F_x}{F_y}=\frac{1000}{250}=4" in SOURCE
    body = SOURCE.split("def source_exercises_and_answers", 1)[1].split("\ndef ", 1)[0]
    assert "doc.new_page()" not in body
